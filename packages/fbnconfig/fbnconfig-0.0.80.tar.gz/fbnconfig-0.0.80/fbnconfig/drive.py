from __future__ import annotations
from pathlib import PurePosixPath, PurePath
import hashlib
import httpx
from .resource_abc import Resource, Ref
from typing import Union, Optional
from pydantic import BaseModel, Field

class FolderRef(BaseModel, Ref):
    """Reference to a drive directory. """
    id: str = Field(exclude=True, init=True)
    driveId: str = Field("/", exclude=True, init=False)
    folderPath: str

    def attach(self, client):
        if self.folderPath == "/":
            self.driveId = "/"
            return
        p = PurePosixPath(self.folderPath)
        search = client.post("/drive/api/search/", json={"withPath": str(p.parent), "name": str(p.name)})
        values = search.json()["values"]
        if len(values) != 1:
            raise RuntimeError("Expected to find exactly one match path for PathRef but found " \
                + str(len(values)))
        self.driveId = values[0]["id"]

    def path(self):
        return PurePosixPath(self.folderPath)


root = FolderRef(id = "drive_root", folderPath="/")

class FolderResource(BaseModel, Resource):
    """Resource describing a Drive folder

    Creates if it doesn't exist and updates if it has changed:
        - When name is changed, the reference for the folder will be maintained
        - When parent is changed, the folder will be moved under new parent

    Example
    -------
        >>> from fbnconfig import drive, Deployment
        >>> f1 = drive.FolderResource(id="base_folder", name="first_level", parent=drive.root)
        >>> f2 = drive.FolderResource(id="base_folder", name="second_level", parent=f1)
        >>> Deployment("myDeployment", [f1,f2])

    Notes
    -----
    If the folder is the parent of another resource, all dependents need to be deleted before this one

    Attributes
    ----------
    id : str
        resource identifier; this will be used in the log to reference the folder resource

    name : str
        folder name that will be displayed in Drive UI

    parent:  Union[FolderResource, RootFolder]
        Folder reference to the parent folder; if it is in root, use 'drive.root'
    """
    id: str = Field(exclude=True)
    driveId: str | None = Field(None, exclude=True, init=False)
    name: str
    parent: Union[FolderResource, FolderRef]

    def read(self, client, old_state):
        pass

    def create(self, client: httpx.Client):
        body = {"path": str(self.parent.path()), "name": self.name}
        res = client.request("POST", "/drive/api/folders", json=body)
        self.driveId = res.json()["id"]
        return {
            "id": self.id,
            "driveId": self.driveId,
            "name": self.name,
            "parentId": self.parent.driveId,
        }

    def update(self, client: httpx.Client, old_state):
        self.driveId = old_state.driveId
        if self.name != old_state.name or self.parent.driveId != old_state.parentId:
            body = {"path": str(self.parent.path()), "name": self.name}
            client.request("PUT", "/drive/api/folders/" + old_state.driveId, json=body)
            return {
                "id": self.id,
                "driveId": self.driveId,
                "name": self.name,
                "parentId": self.parent.driveId,
            }
        return None

    @staticmethod
    def delete(client, old_state):
        client.request("DELETE", "/drive/api/folders/" + old_state.driveId)

    def deps(self):
        return [self.parent] if self.parent else []

    def path(self):
        return self.parent.path() / PurePosixPath(self.name)


class FileResource(BaseModel, Resource):
    """Resource describing a Drive file.

    Creates if it doesn't exist and updates if content changes.

    Example
    -------
        >>> from fbnconfig import drive, Deployment
        >>> import pathlib
        >>> f1 = drive.FolderResource(id="base_folder", name="first_level", parent=drive.root)
        >>> content_path = pathlib.Path(__file__).parent.resolve() / pathlib.Path("myfile1.txt")
        >>> ff_with_path =
        >>> drive.FileResource(id="file1", folder=f1, name="myfile1.txt", content_path=content_path)
        >>> ff_with_content =
        >>> drive.FileResource(id="file2", folder=f1, name="myfile2.txt", content="Content of my file")
        >>> Deployment("myDeployment", [f1, ff_with_path, ff_with_content])

    Notes
    -----
    Can only supply a path to content or the content itself, but not both

    Attributes
    ----------
    id : str
      resource identifier; this will be used in the log to reference the file resource
    name : str
      file name that will be displayed in Drive UI
    content: Optional[Union[str, bytes]]
        file content
    content_path: Optional[PurePath]
        Path to the content of the file
    folder: FolderResource
      Folder reference to the parent folder; if it is in root, use 'drive.root'
      """
    id: str = Field(exclude=True)
    driveId: str | None = Field(None, exclude=True, init=False)
    name: str
    content: Optional[Union[str, bytes]] = None
    content_path: Optional[PurePath] = None
    folder: FolderResource
    content_hash: str | None = Field(None, exclude=True, init=False)

    def read(self, client, old_state) -> None:
        pass

    def __init__(self, **options):
        super().__init__(**options)
        if self.content_path is not None:
            if self.content is not None:
                raise RuntimeError(
                    "Only one of content and content_path should be specified in FileResource"
                )
            if not self.content_path.is_absolute():
                raise RuntimeError("content_path should be an absolute path")
            with open(self.content_path, "rb") as ff:
                self.content = ff.read()
            self.content_hash = hashlib.sha256(self.content).hexdigest()
        elif self.content is not None:
            encoded = self.content.encode() if isinstance(self.content, str) else self.content
            self.content_hash = hashlib.sha256(encoded).hexdigest()

        else:
            raise RuntimeError("Either content or content_path should be specified in FileResource")

    def create(self, client):
        path = str(self.folder.path())
        res = client.request(
            "POST",
            "/drive/api/files",
            headers={
                "x-lusid-drive-filename": self.name,
                "x-lusid-drive-path": path,
                "content-type": "application/octet-stream",
            },
            content=self.content,
        )
        self.driveId = res.json()["id"]
        return {
            "id": self.id,
            "driveId": self.driveId,
            "name": self.name,
            "parentId": self.folder.driveId,
            "content_hash": self.content_hash,
        }

    def update(self, client, old_state):
        self.driveId = old_state.driveId
        if (
            self.name == old_state.name
            and self.folder.driveId == old_state.parentId
            and self.content_hash == old_state.content_hash
        ):
            return None

        if self.content_hash != old_state.content_hash:
            assert self.driveId is not None
            client.request(
                "put",
                "/drive/api/files/" + self.driveId + "/contents",
                headers={"content-type": "application/octet-stream"},
                content=self.content,
            )
        if self.name != old_state.name or self.folder.driveId != old_state.parentId:
            json = {"path": str(self.folder.path()), "name": self.name}
            client.request("PUT", "/drive/api/files/" + old_state.driveId, json=json)
        return {
            "id": self.id,
            "driveId": self.driveId,
            "name": self.name,
            "parentId": self.folder.driveId,
            "content_hash": self.content_hash,
        }

    @staticmethod
    def delete(client, old_state):
        client.request("DELETE", "/drive/api/files/" + old_state.driveId)

    def deps(self):
        return [self.folder]

    def path(self):
        return self.folder.path() / PurePosixPath(self.name)
