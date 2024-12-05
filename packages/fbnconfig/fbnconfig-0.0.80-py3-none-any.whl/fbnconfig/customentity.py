from __future__ import annotations
import httpx
from .resource_abc import Resource
from typing import Dict, Any, List
from pydantic import BaseModel, Field
from enum import Enum
import copy

class CollectionType(str, Enum):
    Single = "Single"
    Array = "Array"

class LifeTime(str, Enum):
    Perpetual = "Perpetual"
    TimeVariant = "TimeVariant"

class FieldType(str, Enum):
    String = "String"
    Boolean = "Boolean"
    DateTime = "DateTime"
    Decimal =  "Decimal"

class FieldDefinition(BaseModel):
    name: str
    lifetime: LifeTime
    type: FieldType
    collectionType: CollectionType = CollectionType.Single
    required: bool
    description: str = ""

# These are optional in the API create and will be given default values. When read is called
# they will not be returned if they have the default value
DEFAULT_FIELD = {
    "collectionType": "Single",
    "description": ""
}

class EntityTypeResource(BaseModel, Resource):
    id: str = Field(exclude=True)
    entityTypeName: str
    displayName: str
    description: str
    fieldSchema: List[FieldDefinition]

    def read(self, client, old_state) -> Dict[str, Any]:
        entitytype = old_state.entitytype
        return client.request("get", f"/api/api/customentities/entitytypes/{entitytype}").json()

    def create(self, client: httpx.Client):
        desired = self.model_dump(mode="json", exclude_none=True)
        res = client.request("POST", "/api/api/customentities/entitytypes", json=desired).json()
        return {"entitytype": res["entityType"]}

    def update(self, client: httpx.Client, old_state):
        remote = self.read(client, old_state)
        # enrich remote fields with the default values if not present
        remote["fieldSchema"] = [rem | DEFAULT_FIELD for rem in remote["fieldSchema"]]
        desired = self.model_dump(mode="json", exclude_none=True)
        effective = remote | copy.deepcopy(desired)
        for i in range(0, len(self.fieldSchema)):
            if i < len(remote["fieldSchema"]):
                eff_field = remote["fieldSchema"][i] | desired["fieldSchema"][i]
                effective["fieldSchema"][i] = eff_field
        if effective == remote:
            return None
        res = client.request("PUT", f"/api/api/customentities/entitytypes/{old_state.entitytype}",
            json=desired).json()
        return {"entitytype": res["entityType"]}

    @staticmethod
    def delete(client, old_state):
        raise RuntimeError("Cannot delete a custom entity definition")

    def deps(self):
        return []
