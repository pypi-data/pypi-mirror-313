import time
import textwrap
import json
import sys
from typing import Dict, Any, List
from pydantic import BaseModel, Field
from .resource_abc import Resource, Ref
from enum import Enum

def background_query(client, sql):
    res = client.put("/honeycomb/api/SqlBackground", content=sql, headers={"Content-type": "text/plain"})
    return res.json()

def get_progress(client, execution_id, progress_url):
    return client.get("/honeycomb" + progress_url).json()

def wait_for_background(client, execution):
    execution_id = execution["executionId"]
    progress_url = execution["progress"]["href"]
    progress = get_progress(client, execution_id, progress_url)
    status = progress["status"]
    match status:
      case "Faulted" | "Cancelled":
          raise RuntimeError("Query was " + status + progress["progress"])
      case "Created" | "WaitingForActivation" | "WaitingToRun" | "WaitingForChildrenToComplete":
          return None
      case "Running":
          return None
      case "RanToCompletion":
          return progress
      case _:
          raise RuntimeError("Unknown status:" + status)

def fetch(client, execution, progress):
    res = client.get("/honeycomb" + execution["fetchJsonProper"]["href"])
    return res.json()

def query(client, sql):
    execution = background_query(client, sql)
    progress = None
    while True:
        if progress is None:
            time.sleep(1)
            progress = wait_for_background(client, execution)
        else:
            return fetch(client, execution, progress)

def put_query(client, sql):
    res = client.put(
        "/honeycomb/api/Sql/json",
        content=sql,
        params={"jsonProper": True},
        headers={"Content-type": "text/plain"}
    )
    return res.json()

class ParameterType(str, Enum):
    BigInt   =  "BigInt"
    Boolean  =  "Boolean"
    Date     =  "Date"
    DateTime =  "DateTime"
    Decimal  =  "Decimal"
    Double   =  "Double"
    Int      =  "Int"
    Table    =  "Table"
    Text     =  "Text"

class VariableType(str, Enum):
    Scalar = "@@"
    Table = "@"


class Variable(BaseModel):
    name: str
    type: VariableType
    sql: str

    def init_str(self):
        #  eg @scalar = select 2 + 2
        return f"{self.type.value}{self.name} = {self.sql}"

    def with_str(self):
        return f"{self.type.value}{self.name}"

class Parameter(BaseModel):
    name: str
    type: ParameterType
    value: Any
    setAsDefaultValue: bool = True
    isMandatory: bool = True
    tooltip: str

    # return in the same format thst sys.file stores it in
    def metadata(self):
        base: Dict[str, Any] = {
            "Name": self.name,
            "Type": self.type.value,
            "Description": self.tooltip,
        }
        if self.setAsDefaultValue and self.type != ParameterType.Table:
            base["DefaultValue"] = self.value
        if self.type == ParameterType.Table:
            if self.isMandatory:
                base["ConditionUsage"] = 2
            else:
                base["ConditionUsage"] = 0
        return base

def lumi_fmt(value):
    if isinstance(value, Variable):
        return f"{value.type.value}{value.name}"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    return '"' + value.replace('"', '""') + '"'


class ViewRef(BaseModel, Ref):
    """ Reference an existing view


    Example
    ----------
    >>> from fbnconfig import lumi
    >>> lumi.ViewResource(
    ...  id="lumi-example-ref",
    ...  provider="Views.fbnconfig.existing_view")


    Attributes
    ----------
    id : str
         Resource identifier.
    provider : str
        Name of the view referenced. This is assumed to exist
    """
    id: str = Field(exclude=True)
    provider: str

    def attach(self, client):
        path = self.provider.replace(".", "/")
        res = put_query(
            client,
            f"select 1 from sys.file where path = 'databaseproviders/{path}.sql'"
        )
        if len(res) != 1:
            raise RuntimeError(f"Failed to attach ref to {self.provider}. No rows returned")


class ViewResource(BaseModel, Resource):
    """Create and manage a Luminesce view

    Example
    ----------
    >>> from fbnconfig import lumi
    >>> lumi.ViewResource(
    ...  id="lumi-example-view",
    ...  provider="Views.fbnconfig.example",
    ...  description="My resource test view",
    ...  documentationLink="http://example.com/query",
    ...  variableShape=False,
    ...  useDryRun=True,
    ...  allowExecuteIndirectly=False,
    ...  distinct=True,
    ...  sql='select 2+#PARAMETERVALUE(p1)   as   twelve',
    ...  parameters=[
    ...      lumi.Parameter(
    ...          name="p1",
    ...          value=10,
    ...          setAsDefaultValue=True,
    ...          tooltip="a number",
    ...          type=lumi.ParameterType.Int
    ...      )

    Attributes
    ----------
    id : str
         Resource identifier.
    provider : str
        Name of the view managed by this resource
    description : str
        View description
    sql: str
        The query string for the view
    parameters : list of `Parameter`, optional
        List of parameters for the view
    dependencies : list of dependencies, optional
        This can be another view or any other resource
    documentationLink: str, optional
        Displays one or more hyperlinks in the summary dialog for the view
    variableShape: bool, optional
        This is useful if data returned is likely to vary in shape between queries. Defaults to false.
    allowExecuteIndirectly : bool, optional
        Allows end users to query providers within the view even if they are not entitled to use those
        providers directly.
        Defaults to false.
    limit: int, optional
        Test option when developing view, does not have an effect on a published view. Defaults to None
    groupBy: str, optional
        Test option when developing view, does not have an effect on a published view. Defaults to None
    filter: str, optional
        Test option when developing view, does not have an effect on a published view. Defaults to None
    offset: int, optional
        Test option when developing view, does not have an effect on a published view. Defaults to None
    distinct: bool, optional
        Test option when developing view, does not have an effect on a published view. Defaults to None
    useDryRun: bool, optional
        Intended for automatic deployment of views. See docs for more details. Defaults to false
    variables: List of `Variable`, optional
        A table variable that can be passed into the view by an end user or in code

    See Also
    --------
    `https://support.lusid.com/knowledgebase/article/KA-01767/en-us`__
    """
    id: str = Field(exclude=True)
    provider: str = Field(serialization_alias="Provider")
    description: str = Field(serialization_alias="Description")
    sql: str
    parameters: List[Parameter] = []
    dependencies: List | None = None
    documentationLink: str|None = None
    variableShape: bool|None = None
    allowExecuteIndirectly: bool|None = None
    limit: int|None = None
    groupBy: str|None = None
    filter: str|None = None
    offset: int|None = None
    distinct: bool|None = None
    useDryRun: bool|None = None
    variables: List[Variable] = []

    class Registration:
        tries = 10
        wait_time = 1

    _saved_options = { # maps from sys.file metadata to view option names
        "Description": "description",
        "DocumentationLink": "documentationLink",
        "IsWithinDirectProviderView": "variableShape",
        "IsWithinViewAllowingIndirectExecute": "allowExecuteIndirectly",
    }
    _test_options = [
        "distinct",
        "filter",
        "groupby",
        "limit",
        "offset",
        "preamble",
        "useDryRun",
    ]

    def read(self, client, old_state) -> Dict[str, Any]:
        path = old_state.provider.replace(".", "/")
        res = put_query(
            client,
            textwrap.dedent(f"""\
                select f.Content, r.Version from sys.file as f
                join sys.registration as r on r.Name = '{old_state.provider}'
                where path = 'databaseproviders/{path}.sql'
                order by r.Version asc
                limit 1
            """)
        )
        assert len(res) == 1

        def strip_column_description(kv: Dict) -> Dict:
            if kv["Type"] == "Table":
                kv["Description"] = kv["Description"].split("\nAvailable columns")[0]

            return kv

        parts = res[0]["Content"].split("--- MetaData ---")
        sql = parts[0]
        metadata = json.loads(parts[1])

        parameters =  [strip_column_description(p) for p in metadata["Parameters"]]
        props = {
            v: metadata[k]
            for k, v in self._saved_options.items()
            if metadata.get(k, None) is not None
        }
        return {"sql": sql, "version": res[0]["Version"], "parameters": parameters} | props

    @staticmethod
    def registration_version(client, view_name) -> int | None:
        rows = put_query(client, textwrap.dedent(f"""\
            select Version from sys.registration where Name='{view_name}'
            order by Version asc
            limit 1
        """))
        return int(rows[0]["Version"]) if len(rows) > 0 else None

    def format_option(self, option, value):
        if isinstance(value, bool) and value:
            return f"--{option}"
        if isinstance(value, (int, float)):
            return f"--{option}={value}"
        return f"--{option}={lumi_fmt(value)}"

    def get_variables(self):
        param_variables = [
            param.value for param in self.parameters
            if isinstance(param.value, Variable)
        ]
        seen = set()
        return [
            value for value in self.variables + param_variables
            if value.name not in seen and not seen.add(value.name)
        ]

    def template(self, desired):
        options = [
            self.format_option(option, desired[option])
            for option in ["provider"] + self._test_options + list(self._saved_options.values())
            if desired.get(option) is not None
        ]
        tpl = textwrap.dedent("""\
            {preamble}@x = use Sys.Admin.SetupView{with_clause}
            {options}{params}
            ----
            {sql}
            enduse;
            select * from @x;
        """)
        params = [
            # can't quote the tooltip as causes an error from lumi HC-3322
            f"{p.name},{p.type.value},{lumi_fmt(p.value)},{lumi_fmt(p.isMandatory)},{p.tooltip}"
            if p.type == ParameterType.Table else
            f"{p.name},{p.type.value},{lumi_fmt(p.value)},{lumi_fmt(p.setAsDefaultValue)},{p.tooltip}"
            for p in self.parameters
        ]
        param_clause = "\n--parameters\n{0}".format("\n".join(params)) \
            if len(params) > 0 else ""
        variables = self.get_variables()
        preamble = ";\n".join([v.init_str() for v in variables]) + ";\n" \
            if len(variables) > 0 else ""
        with_clause = " with " + ", ".join([v.with_str() for v in variables]) \
            if len(variables) > 0 else ""
        sql = tpl.format(
            options="\n".join(options),
            params=param_clause,
            sql=desired["sql"],
            with_clause=with_clause,
            preamble=preamble
        )
        return sql

    def create(self, client) -> Dict[str, Any]:
        desired = self.model_dump(exclude_none=True)
        sql = self.template(desired)
        put_query(client, sql)
        for i in range(0, self.Registration.tries):
            if self.registration_version(client, self.provider) is not None:
                break
            else:
                if i == self.Registration.tries - 1:
                    sys.stderr.write(
                        f"warning: no view registration after {i} tries for {self.provider}"
                    )
                else:
                    time.sleep(self.Registration.wait_time)
        return {"provider": self.provider}

    def update(self, client, old_state):
        if self.provider != old_state.provider:
            self.delete(client, old_state)
            self.create(client)
            return
        desired = self.model_dump(exclude_none=True, by_alias=False, exclude=set(self._test_options))
        raw_remote = self.read(client, old_state)
        remote_props = {
            k.lower(): v
            for k, v in raw_remote.items()
            if k in self._saved_options.values() and v is not None
        }
        desired_props = {
            k.lower(): v
            for k, v in desired.items()
            if k in self._saved_options.values() and v is not None
        }
        remote_params = raw_remote["parameters"]
        desired_params = [p.metadata() for p in self.parameters]
        effective_params = [
            (remote_params[i] | desired_params[i])
            if i < len(remote_params) and remote_params[i]["Name"] == desired_params[i]["Name"]
            else desired_params[i]
            for i, des in enumerate(desired_params)
        ]
        remote_sql = textwrap.dedent(raw_remote["sql"].rstrip())
        remote_version = raw_remote["version"]
        desired_sql = textwrap.dedent(self.sql.rstrip())
        if (desired_sql == remote_sql and remote_props | desired_props == remote_props
                and effective_params == remote_params):
            return None
        sql = self.template(desired)
        put_query(client, sql)
        for i in range(0, self.Registration.tries):
            version: int | None = self.registration_version(client, self.provider)
            if version is not None and remote_version < version:
                break
            else:
                if i == self.Registration.tries - 1:
                    sys.stderr.write(
                        f"warning: no view registration after {i} tries for {self.provider}"
                    )
                else:
                    time.sleep(self.Registration.wait_time)
        return {"provider": self.provider}

    def deps(self):
        return self.dependencies if self.dependencies else []

    @staticmethod
    def delete(client, old_state):
        sql = textwrap.dedent(f"""\
        @x = use Sys.Admin.SetupView
        --provider={old_state.provider}
        --deleteProvider
        ----
        select 1 as deleting
        enduse;
        select * from @x;
        """)
        put_query(client, textwrap.dedent(sql))
        for i in range(0, ViewResource.Registration.tries):
            if ViewResource.registration_version(client, old_state.provider) is None:
                break
            else:
                if i == ViewResource.Registration.tries - 1:
                    sys.stderr.write(
                        f"warning: no view deregistration after {i} tries for {old_state.provider}"
                    )
                else:
                    time.sleep(ViewResource.Registration.wait_time)
