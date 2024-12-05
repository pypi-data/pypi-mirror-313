from __future__ import annotations
import httpx
import copy
from .resource_abc import Resource, Ref
from pydantic import BaseModel, Field
from enum import Enum
from typing import Dict, Any, Optional, Union


class IdentityRoleRef(BaseModel, Ref):
    """Used to reference an existing identity role for role assignment
    Example
    -------
    >>> from fbnconfig.identity import IdentityRoleRef
    >>> admin = IdentityRoleRef(id="admin", name="lusid-administrator")
    """

    roleId: str | None = Field(None, exclude=True, init=False)
    name: str
    id: str = Field(exclude=True)

    def attach(self, client):
        search = client.request("get", "/identity/api/roles")
        try:
            match = next(role for role in search.json() if role["name"] == self.name)
        except StopIteration:
            raise (RuntimeError("No matching identity role with name", self.name))
        self.roleId = match["id"]


class IdentityRoleResource(BaseModel, Resource):
    """Manage a role

    Example
    -------
    >>> from fbnconfig.identity import IdentityRoleResource
    >>> operator =
    >>> IdentityRoleResource(id="export-role", description="scheduler-operators", name="export-admin")
    """
    id: str = Field(exclude=True)
    name: str
    description: str
    scope: str | None = Field(None, exclude=True, init=False)
    code: str | None = Field(None, exclude=True, init=False)
    roleId: str | None = Field(None, exclude=True, init=False)
    remote: Dict[str, Any] = Field(None, exclude=True, init=False)

    def read(self, client, old_state):
        get = client.request("get", f"/identity/api/roles/{old_state.roleId}")
        remote = get.json()
        remote.pop("id")
        remote.pop("name")
        remote.pop("roleId")
        remote.pop("source")
        remote.pop("samlName")
        self.remote = remote
        self.roleId = old_state.roleId

    def create(self, client: httpx.Client):
        desired = self.model_dump(mode="json", exclude_none=True)
        res = client.request("POST", "/identity/api/roles", json=desired)
        result = res.json()
        self.scope = result["roleId"]["scope"]
        self.code = result["roleId"]["code"]
        self.roleId = res.json()["id"]
        return {
            "id": self.id,
            "code": self.code,
            "scope": self.scope,
            "name": self.name,
            "roleId": self.roleId,
        }

    def update(self, client: httpx.Client, old_state):
        if self.name != old_state.name:
            raise (RuntimeError("Cannot change the name on a role"))
        self.read(client, old_state)
        remote = copy.deepcopy(self.remote)
        self.roleId = old_state.roleId
        desired = self.model_dump(mode="json", exclude_none=True, exclude={"name"})

        if desired == remote:
            return None
        client.request("put", f"/identity/api/roles/{old_state.roleId}", json=desired)

    @staticmethod
    def delete(client, old_state):
        client.request("DELETE", f"/identity/api/roles/{old_state.roleId}")

    def deps(self):
        return []


class UserType(str, Enum):
    """User type used with a UserResource"""
    PERSONAL = "Personal"
    SERVICE = "Service"


class UserRef(BaseModel, Ref):
    """Reference an existing user

    Example
    -------
    >>> from fbnconfig.identity import UserRef
    >>> user =  UserRef(id="export-user", login="exports@company.com")
    """
    id: str = Field(exclude=True)
    login: str
    userId: str | None = Field(None, exclude=True, init=False)

    def attach(self, client):
        user_list = client.request("get", "/identity/api/users")
        match = next((user for user in user_list.json() if user["login"] == self.login), None)
        if match is None:
            raise RuntimeError(f"No user with login {self.login} exists in the remote")
        self.userId = match["id"]


class UserResource(BaseModel, Resource):
    """Define a user"""
    id: str = Field(exclude=True)
    firstName: str
    lastName: str
    emailAddress: str
    secondEmailAddress: Optional[str] = None
    login: str
    type: UserType
    userId: str | None = Field(None, exclude=True, init=False)
    remote: Dict[str, Any] = Field({}, exclude=True, init=False)

    def read(self, client, old_state):
        get = client.request("get", f"/identity/api/users/{old_state.userId}")
        remote = get.json()
        remote.pop("status", None)
        remote.pop("external", None)
        remote.pop("id", None)
        remote.pop("roles", None)
        remote.pop("links", None)
        self.remote = remote
        self.userId = old_state.userId

    def create(self, client: httpx.Client) -> Dict[str, Any]:
        desired = self.model_dump(mode="json", exclude_none=True)
        res = client.request("POST", "/identity/api/users", json=desired)
        result = res.json()
        self.userId = result["id"]
        return {"id": self.id, "userId": self.userId}

    def update(self, client: httpx.Client, old_state):
        self.read(client, old_state)
        desired = self.model_dump(mode="json", exclude_none=True)
        if desired == self.remote:
            return None
        if self.login != self.remote["login"]:
            raise RuntimeError("Cannot change the login on an existing user")
        client.request("put", f"/identity/api/users/{old_state.userId}", json=desired)
        return {"id": self.id, "userId": self.userId}

    @staticmethod
    def delete(client, old_state):
        client.request("delete", f"/identity/api/users/{old_state.userId}")

    def deps(self):
        return []


class RoleAssignment(BaseModel, Resource):
    """Assign a role to a user"""
    id: str = Field(exclude=True)
    user: UserResource
    role: Union[IdentityRoleResource, IdentityRoleRef]
    roleId: str | None = Field(None, exclude=True, init=False)
    userId: str | None = Field(None, exclude=True, init=False)
    remote: Dict[str, Any] = Field(None, exclude=True, init=False)

    def read(self, client, old_state):
        self.roleId = old_state.roleId
        self.userId = old_state.user_id

    def create(self, client: httpx.Client) -> Dict[str, Any]:
        role_id = self.role.roleId
        user_id = self.user.userId
        client.request("put", f"/identity/api/roles/{role_id}/users/{user_id}")
        return {"id": self.id, "userId": user_id, "roleId": role_id}

    @staticmethod
    def delete(client: httpx.Client, old_state) -> None:
        role_id = old_state.roleId
        user_id = old_state.userId
        client.request("delete", f"/identity/api/roles/{role_id}/users/{user_id}")

    def update(self, client, old_state) -> Dict[str, Any] | None:
        if old_state.userId == self.user.userId and old_state.roleId == self.role.roleId:
            return None
        try:
            client.request(
                "delete",
                f"/identity/api/roles/{old_state.roleId}/users/{old_state.userId}",
            )
        except httpx.HTTPStatusError as e:
            # ignore 404 because if the old role or user are gone this won't exist
            if e.response.status_code != httpx.codes.NOT_FOUND:
                raise
            pass
        client.request(
            "put",
            f"/identity/api/roles/{self.role.roleId}/users/{self.user.userId}",
        )
        return {"id": self.id, "userId": self.user.userId, "roleId": self.role.roleId}

    def deps(self):
        return [self.user, self.role]
