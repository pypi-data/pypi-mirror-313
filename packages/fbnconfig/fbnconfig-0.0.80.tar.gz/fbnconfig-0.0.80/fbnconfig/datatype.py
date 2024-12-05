from __future__ import annotations
import httpx
from .resource_abc import Resource, Ref
import typing
from typing import Dict, Any
from pydantic import BaseModel, Field
from enum import Enum
import copy

class TypeValueRange(str, Enum):
    Open = "Open"
    Closed = "Closed"


class ValueType(str, Enum):
    Boolean              = "Boolean"
    Code                 = "Code"
    Currency             = "Currency"
    CurrencyAndAmount    = "CurrencyAndAmount"
    CutLocalTime         = "CutLocalTime"
    DateOrCutLabel       = "DateOrCutLabel"
    DateTime             = "DateTime"
    Decimal              = "Decimal"
    Id                   = "Id"
    Int                  = "Int"
    List                 = "List"
    Map                  = "Map"
    MetricValue          = "MetricValue"
    Percentage           = "Percentage"
    PropertyArray        = "PropertyArray"
    ResourceId           = "ResourceId"
    ResultValue          = "ResultValue"
    String               = "String"
    TradePrice           = "TradePrice"
    UnindexedText        = "UnindexedText"
    Uri                  = "Uri"

class Unit(BaseModel):
    code: str
    displayName: str
    description: str
    details: Any|None = None

class UnitSchema(str, Enum):
    NoUnits = "NoUnits"
    Basic = "Basic"
    Iso4217Currency = "Iso4217Currency"

class FieldDefinition(BaseModel):
    key: str
    isRequired: bool
    isUnique: bool

class FieldValue(BaseModel):
    value: str
    fields: Dict[str, str]  # limit to strings because get returns strings

class ReferenceData(BaseModel):
    fieldDefinitions: typing.List[FieldDefinition]
    values: typing.List[FieldValue]

class DataTypeRef(BaseModel, Ref):
    id: str = Field(exclude=True)
    scope: str
    code: str

    def attach(self, client):
        scope, code = self.scope, self.code
        try:
            client.get(f"/api/api/datatypes/{scope}/{code}", params={"includeSystem": True})
        except httpx.HTTPStatusError as ex:
            if ex.response.status_code == 404:
                raise RuntimeError(f"Datatype {scope}/{code} not found")
            else:
                raise ex

class DataTypeResource(BaseModel, Resource):
    id: str = Field(exclude=True)
    scope: str
    code: str
    typeValueRange: TypeValueRange
    displayName: str
    description: str
    valueType: ValueType
    acceptableValues: typing.List[str]|None = None
    unitSchema: UnitSchema = UnitSchema.NoUnits
    acceptableUnits: typing.List[Unit]|None = None
    referenceData: ReferenceData|None = None

    def read(self, client, old_state) -> Dict[str, Any]:
        return client.request("get", f"/api/api/datatypes/{old_state.scope}/{old_state.code}").json()

    def create(self, client: httpx.Client):
        desired = self.model_dump(mode="json", exclude_none=True)
        client.request("POST", "/api/api/datatypes", json=desired).json()
        return {"scope": self.scope, "code": self.code}

    def update(self, client: httpx.Client, old_state):
        if [self.scope, self.code] != [old_state.scope, old_state.code]:
            raise RuntimeError("Cannot change scope/code on datatype")
        remote = self.read(client, old_state)
        remote.pop("href")
        remote.pop("id")
        remote.pop("links")
        remote.pop("version")
        desired = self.model_dump(mode="json", exclude_none=True, exclude={"scope", "code"})
        effective = remote | copy.deepcopy(desired)
        if "referenceData" in remote and "referenceData" in effective:
            # sort the fields since the api changes the order they come back
            remote["referenceData"]["fieldDefinitions"].sort(key=lambda field: field["key"])
            effective["referenceData"]["fieldDefinitions"].sort(key=lambda field: field["key"])
            # sort the values since the api changes the order they come back
            remote["referenceData"]["values"].sort(key=lambda field: field["value"])
            effective["referenceData"]["values"].sort(key=lambda field: field["value"])
        if "acceptableValues" in remote and "acceptableValues" in effective:
            # sort the acceptableValues since the api changes the order they come back
            remote["acceptableValues"].sort()
            effective["acceptableValues"].sort()
        if effective == remote:
            return None
        # check for illegal modifications
        readonly_fields = ["typeValueRange", "unitSchema", "valueType"]
        modified = [field for field in readonly_fields if effective[field] != remote[field]]
        if len(modified) > 0:
            raise RuntimeError(f"Cannot change readonly fields {modified} on datatype")
        if effective["referenceData"]["fieldDefinitions"] != remote["referenceData"]["fieldDefinitions"]:
            raise RuntimeError(
                "Cannot change readonly fields referenceData.fieldDefinitions on datatype"
            )
        # update reference data values if required
        if effective["referenceData"]["values"] != remote["referenceData"]["values"]:
            client.request("PUT", f"/api/api/datatypes/{self.scope}/{self.code}/referencedatavalues",
                json=effective["referenceData"]["values"]
            )
        # update core data if required
        effective.pop("referenceData")
        remote.pop("referenceData")
        if effective != remote:
            client.request("PUT", f"/api/api/datatypes/{self.scope}/{self.code}", json=desired)
        return {"scope": self.scope, "code": self.code}

    @staticmethod
    def delete(client, old_state):
        raise RuntimeError("Cannot delete a datatype definition")

    def deps(self):
        return []
