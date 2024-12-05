from __future__ import annotations
import httpx
import copy
from .resource_abc import Resource, Ref
from typing import Optional, Dict, List, Any, Sequence
from pydantic import BaseModel, field_serializer, model_validator, Field
from enum import Enum


class ActionId(BaseModel):
    """ActionId resource used with IdSelector

    Example
    -------
    >>> from fbnconfig.access import ActionId
    >>> ActionId(scope="myscope", activity="execute", entity="Feature")

    -------
    """
    scope: str
    activity: str
    entity: str


class MatchAllSelector(BaseModel):
    type_name: str = Field("matchAllSelectorDefinition", init=False, exclude=True)
    actions: List[ActionId]
    name: Optional[str] = None
    description: Optional[str] = None

class IdSelector(BaseModel):
    """IdSelector resource used with PolicyResource

    Example
    -------
    >>> from fbnconfig.access import IdSelector, ActionId
    >>> IdSelector(
            name="feature_id_selector",
            description="feature_id_selector",
            identifier={"scope": "myscope", "code": "mycode"},
            actions=[ActionId(scope="myscope", activity="execute", entity="Feature")])
    """
    type_name: str = Field("idSelectorDefinition", init=False, exclude=True)
    identifier: Dict[str, str]
    actions: List[ActionId]
    name: Optional[str] = None
    description: Optional[str] = None

class MetadataExpression(BaseModel):
    metadataKey: str
    operator: str
    textValue: str|None

class MetadataSelector(BaseModel):
    type_name: str = Field("metadataSelectorDefinition", init=False, exclude=True)
    actions: List[ActionId]
    name: str|None = None
    description: str|None = None
    expressions: List[MetadataExpression]

class PolicySelector(BaseModel):
    type_name: str = Field("policySelectorDefinition", init=False, exclude=True)
    actions: List[ActionId]
    name: str|None = None
    description: str|None = None
    identityRestriction: Dict[str, str]|None = None
    restrictionSelectors: Sequence[Selector]|None = None

    @field_serializer("restrictionSelectors", when_used="always")
    def serialize_selectors(self, selectors: Any):
        # convert array of selectors
        return [
            {selector.type_name: selector}
            for selector in selectors
        ]


Selector = IdSelector|MatchAllSelector|MetadataSelector|PolicySelector

class WhenSpec(BaseModel):
    """
    WhenSpec resource used with PolicyResource

    Example
    -------
    >>> from fbnconfig.access import WhenSpec
    >>>WhenSpec(activate="2024-08-31T18:00:00.0000000+00:00")

    Notes
    -------
    When deactivate is not supplied, the policy is valid from time in activate until end of time
    """
    activate: str
    deactivate: Optional[str] = None


class Grant(str, Enum):
    """Type of grant used with PolicyResource

    Available values are: Allow, Deny and Undefined
    """
    ALLOW = "Allow"
    DENY = "Deny"
    UNDEFINED = "Undefined"


class PolicyRef(BaseModel, Ref):
    id: str = Field(exclude=True, init=True)
    code: str
    scope: str = "default"

    def attach(self, client):
        try:
            client.request("get", f"/access/api/policies/{self.code}", params={"scope": self.scope})
        except httpx.HTTPStatusError as ex:
            if ex.response.status_code == 404:
                raise RuntimeError(f"Policy {self.scope}/{self.code} not found")
            else:
                raise ex


class PolicyResource(BaseModel, Resource):
    """Manage a policy

    Attributes
    -------
    id: str
        Resource identifier
    """
    id: str = Field(exclude=True)
    code: str
    scope: str = Field("default", init=False, exclude=True)
    description: str
    applications: List[str]
    grant: Grant
    # dict of idselector is the old form for backward compatability
    # new form is array of Selector
    selectors: Sequence[Selector|Dict[str, IdSelector]]
    when: WhenSpec

    @field_serializer("selectors", when_used="always")
    def serialize_selectors(self, selectors: Any):
        # backward compatability when the user passes in their own
        # dict
        if all([isinstance(selector, dict) for selector in selectors]):
            return selectors
        # new version: convert list of selectors to list of dicts
        # where the key in each dict is the type of selector
        return [
            {selector.type_name: selector}
            for selector in selectors
        ]

    def read(self, client, old_state):
        remote = client.request("get", f"/access/api/policies/{self.code}",
                params={"scope": self.scope}).json()
        remote.pop("id")
        remote.pop("links")
        return remote

    def create(self, client: httpx.Client):
        desired = self.model_dump(mode="json", exclude_none=True)
        client.request("POST", "/access/api/policies", json=desired)
        return {"id": self.id, "code": self.code}

    def update(self, client: httpx.Client, old_state):
        if old_state.code != self.code:
            raise (RuntimeError("Cannot change the code on a policy"))
        get = self.read(client, old_state)
        remote = copy.deepcopy(get)
        desired = self.model_dump(mode="json", exclude_none=True, exclude={"scope", "code"})
        if (
            desired["when"].get("deactivate", None) is None
        ):  # deactivate is defaulted on the server so not a difference unless we set it
            remote["when"].pop("deactivate")
        if desired == remote:
            return None
        client.request("put", f"/access/api/policies/{self.code}", json=desired)
        return {"id": self.id, "code": self.code}

    @staticmethod
    def delete(client, old_state):
        client.request("DELETE", f"/access/api/policies/{old_state.code}")

    def deps(self):
        return []


class PolicyCollectionRef(BaseModel, Ref):
    id: str = Field(exclude=True, init=True)
    code: str
    scope: str = "default"

    def attach(self, client):
        try:
            client.get(f"/access/api/policycollections/{self.code}", params={"scope": self.scope})
        except httpx.HTTPStatusError as ex:
            if ex.response.status_code == 404:
                raise RuntimeError(f"PolicyCollection {self.scope}/{self.code} not found")
            else:
                raise ex


class PolicyCollectionResource(BaseModel, Resource):
    id: str = Field(exclude=True)
    # collections can be referenced by scope, but it can't be specified
    scope: str = Field("default", init=False, exclude=True)
    code: str
    description: str|None = None
    policies: Sequence[PolicyResource|PolicyRef] = []
    policyCollections: Sequence[PolicyCollectionResource|PolicyCollectionRef]|None = []
    metadata: Dict[str, List[str]]|None = None

    @field_serializer("policies", when_used="json")
    def serialize_policies(self, policies: Any):
        return [{"code": p.code, "scope": p.scope} for p in policies]

    @field_serializer("policyCollections", when_used="json")
    def serialize_collections(self, collections: Any):
        return [{"code": p.code, "scope": p.scope} for p in collections]

    def read(self, client, old_state) -> Dict[str, Any]:
        scope = old_state.scope
        code = old_state.code
        params = {"scope": scope} if scope is not None else None
        remote = client.get(f"/access/api/policycollections/{code}", params=params).json()
        remote.pop("links")
        remote.pop("id")
        return remote

    def create(self, client) -> Dict[str, Any]:
        desired = self.model_dump(mode="json", exclude_none=True)
        res = client.request("POST", "/access/api/policycollections", json=desired)
        return res.json()["id"]

    def update(self, client, old_state) -> Dict[str, Any]|None:
        if old_state.code != self.code:
            self.delete(client, old_state)
            return self.create(client)
        remote = self.read(client, old_state)
        desired = self.model_dump(mode="json", exclude_none=True, exclude={"code"})
        if desired == remote:
            return None
        client.request("put", f"/access/api/policycollections/{self.code}", json=desired)
        return {"code": self.code, "scope": old_state.scope}

    @staticmethod
    def delete(client, old_state):
        client.request("DELETE", f"/access/api/policycollections/{old_state.code}")

    def deps(self) -> List[Resource|Ref]:
        deps: List[Resource|Ref] = []
        for pol in self.policies:
            deps.append(pol)
        if self.policyCollections:
            for col in self.policyCollections:
                deps.append(col)
        return deps


class PolicyIdRoleResource(BaseModel):
    """Used to refer to a policy resource in a role resource
    """

    policies: Sequence[PolicyResource|PolicyRef]|None = []
    policyCollections: List[PolicyCollectionResource]|None = []

    @field_serializer("policies", when_used="json")
    def serialize_policy_identifiers(self, policies: List[PolicyResource|PolicyRef]):
        # this takes a policy resource as a dep, but it only needs to send the identifiers
        return [{"code": p.code, "scope": p.scope} for p in policies]

    @field_serializer("policyCollections", when_used="json")
    def serialize_collection_identifiers(self, policies: Any):
        # this takes a policy resource as a dep, but it only needs to send the identifiers
        return [{"code": p.code, "scope": p.scope} for p in policies]

class Permission(str, Enum):
    """Permission type used on a role resource
    """
    READ = "Read"
    WRITE = "Write"
    EXECUTE = "Execute"

class NonTransitiveSupervisorRoleResource(BaseModel):
    roles: Sequence[RoleResource|RoleRef]

    @field_serializer("roles", when_used="always")
    def serialize_role_identifiers(self, roles: List[RoleResource|RoleRef]):
        return [{"code": r.code, "scope": r.scope} for r in roles]

class RoleResourceRequest(BaseModel):
    nonTransitiveSupervisorRoleResource: NonTransitiveSupervisorRoleResource|None = None
    policyIdRoleResource: PolicyIdRoleResource|None = None


class RoleRef(BaseModel, Ref):
    """Reference an existing Role
    """
    id: str = Field(exclude=True, init=True)
    scope: str = "default"
    code: str

    def attach(self, client):
        try:
            params = {"scope": self.scope}
            client.request("get", f"/access/api/roles/{self.code}", params=params)
        except httpx.HTTPStatusError as ex:
            if ex.response.status_code == 404:
                raise RuntimeError(f"Role {self.scope}/{self.code} not found")
            else:
                raise ex


class RoleResource(BaseModel, Resource):
    """Define a role resource
    """
    id: str = Field(exclude=True)
    scope: str = Field("default", exclude=True, init=False)
    code: str
    description: str|None = None
    policy_resource: PolicyIdRoleResource|None = None
    resource: None|RoleResourceRequest = None
    when: WhenSpec
    permission: Permission
    roleHierarchyIndex: Optional[int] = None
    remote: Dict[str, Any] = Field(None, exclude=True, init=False)

    @model_validator(mode="before")
    @classmethod
    def extract_policy_ids(cls, options: Dict[str, Any]) -> Dict[str, Any]:
        if not isinstance(options, dict):
            return options
        # if new style policies use the resource directly
        if options.get("policy_resource", None) is None:
            return options
        # if an old format policy_resource is passed, build the resource from it
        options["resource"] = RoleResourceRequest(policyIdRoleResource=options["policy_resource"])
        return options


    def read(self, client, old_state):
        get = client.request("get", f"/access/api/roles/{self.code}")
        self.remote = get.json()
        self.remote.pop("id")
        self.remote.pop("links")

    def create(self, client):
        body = self.model_dump(mode="json", exclude={"policy_resource"}, exclude_none=True)
        client.request("POST", "/access/api/roles", json=body)
        return {"id": self.id, "code": self.code}

    def update(self, client: httpx.Client, old_state):
        if old_state.code != self.code:
            raise (RuntimeError("Cannot change the code on a role"))
        self.read(client, old_state)
        remote = copy.deepcopy(self.remote)
        desired = self.model_dump(mode="json", exclude={"code", "policy_resource"}, exclude_none=True)
        remote["when"].pop(
            "deactivate"
        )  # deactivate is defaulted on the server so not a difference unless we set it
        remote.pop("roleHierarchyIndex")  # set by the server
        if desired == remote:
            return None
        client.request("put", f"/access/api/roles/{self.code}", json=desired)
        return {"id": self.id, "code": self.code}

    @staticmethod
    def delete(client, old_state):
        client.request("DELETE", f"/access/api/roles/{old_state.code}")

    def deps(self):
        if self.resource is None or self.resource.policyIdRoleResource is None:
            return []
        res = self.resource.policyIdRoleResource
        pol_deps = [v for v in res.policies] if res.policies is not None else []
        col_deps = [v for v in res.policyCollections] if res.policyCollections is not None else []
        return pol_deps + col_deps
