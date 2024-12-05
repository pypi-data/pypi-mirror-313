import json
from types import SimpleNamespace
from typing import NamedTuple, List, Union

import httpx

from . import http_client
from . import log
from .access import PolicyResource, RoleResource, PolicyCollectionResource  # noqa: F401
from .configuration import SetResource, ItemResource, SystemConfigResource  # noqa: F401
from .customentity import EntityTypeResource  # noqa: F401
from .datatype import DataTypeResource  # noqa: F401

# import all resources here, so they are available in globals()
from .drive import FolderResource, FileResource  # noqa: F401
from .identity import IdentityRoleResource, UserResource, RoleAssignment  # noqa: F401
from .lumi import ViewResource  # noqa: F401
from .property import DefinitionResource  # noqa: F401
from .resource_abc import Resource, Ref
from .scheduler import ImageResource, JobResource, ScheduleResource  # noqa: F401
from .sequence import SequenceResource  # noqa: F401
from .side_definition import SideResource  # noqa: F401
from .transaction_type import TransactionTypeResource  # noqa: F401

Deployment = NamedTuple("Deployment", [("id", str), ("resources", List[Union[Resource, Ref]])])
deployments = []

Action = NamedTuple("Action", [("id", str), ("type", str), ("change", str)])


def deployment(id, resources):
    d = Deployment(id, resources)
    deployments.append(d)


def recurse_resources(resources):
    seen = dict()
    ordered = []

    def helper(items):
        for res in items:
            deps = res.deps()
            if len(deps) > 0:
                helper(deps)
            if seen.get(res.id, None) is None:
                seen[res.id] = id(res)
                ordered.append(res)
            elif id(res) != seen[res.id]:
                raise RuntimeError(
                    f"Resource ID: {res.id} has been used on more than one resource"
                )

    helper(resources)
    return ordered


def sort_deployed(entries):
    seen = set()
    ordered = []

    def helper(items):
        for e in items:
            dep_ids = e.dependencies
            if len(dep_ids) > 0:
                deps = [e for e in entries if e.resource_id in dep_ids]
                helper(deps)
            if e.resource_id not in seen:
                seen.add(e.resource_id)
                ordered.append(e)

    helper(entries)
    return ordered


def run(client: httpx.Client, deployment) -> List[Action]:
    actions = []
    resources = deployment.resources
    all_resources = recurse_resources(resources)
    deploy_state = log.list_resources_for_deployment(client, deployment.id)
    for resource in all_resources:
        if isinstance(resource, Ref):
            resource.attach(client)
            actions.append(Action(id=resource.id, type=type(resource).__name__, change="attach"))
            print("attach", type(resource).__name__)
            continue
        match = [e for e in deploy_state if e.resource_id == resource.id]
        if len(match) == 0:
            print("deploy: create", type(resource).__name__, resource.id)
            state = resource.create(client)
            log.record(client, deployment.id, resource, state)
            actions.append(Action(id=resource.id, type=type(resource).__name__, change="create"))
        else:
            print("deploy: update", type(resource).__name__, resource.id)
            state = resource.update(client, match[0].state)
            if state is not None:
                log.record(client, deployment.id, resource, state)
                actions.append(Action(id=resource.id, type=type(resource).__name__, change="update"))
            else:
                print("deploy: nochange", type(resource).__name__, resource.id)
                actions.append(Action(id=resource.id, type=type(resource).__name__, change="nochange"))
    for deployed in reversed(sort_deployed(deploy_state)):
        matching_resource = [e for e in all_resources if e.id == deployed.resource_id]
        if len(matching_resource) == 0:
            klas = globals()[deployed.resource_type]
            print("deploy: remove", deployed.resource_type, deployed.resource_id)
            klas.delete(client, deployed.state)
            log.remove(client, deployment.id, deployed.resource_id)
            actions.append(Action(id=deployed.resource_id, type=deployed.resource_type, change="remove"))
    return actions


# called as a library
def deploy(deployment: Deployment, lusid_url: str, access_token: str) -> List[Action]:
    client = http_client.create_client(lusid_url, access_token)
    return run(client, deployment)


def load_vars(vars_file):
    if vars_file:
        host_vars = SimpleNamespace(**json.load(vars_file))
    else:
        host_vars = SimpleNamespace()
    return host_vars
