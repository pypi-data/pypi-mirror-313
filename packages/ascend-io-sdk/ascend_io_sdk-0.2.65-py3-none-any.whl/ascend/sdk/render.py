"""Utility functions to download Ascend resource definitions."""

import base64
import collections
import os
import pathlib
from typing import List, Optional, Tuple

import glog
import jinja2
from google.protobuf import descriptor
from google.protobuf.internal.containers import RepeatedCompositeFieldContainer
from google.protobuf.message import Message as ProtoMessage

from ascend.protos.ascend import ascend_pb2
from ascend.protos.schema import schema_pb2
from ascend.sdk.builder import dataflow_from_proto, data_service_from_proto
from ascend.sdk.client import Client
from ascend.sdk.common import components_ordered_by_dependency, dataflows_ordered_by_dependency
from ascend.sdk.connection_value import Union as UnionValue
from ascend.sdk.connection_value import value_from_proto
from ascend.sdk.definitions import Dataflow, DataService, Definition, ReadConnector, Transform, WriteConnector, Connection

# A bit funky of an approach to support multiple versions of protobuf that use different internal container classes
REPEATED_CONTAINERS = [RepeatedCompositeFieldContainer]
try:
  from google.protobuf.pyext._message import RepeatedCompositeContainer

  REPEATED_CONTAINERS.append(RepeatedCompositeContainer)
except:
  pass

TEMPLATES_V1 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates", "v1")  # deprecated
TEMPLATES_V2 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates", "v2")
TEMPLATES_V3 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates", "v3")


class InlineCodeReader:
  def __init__(self, code: str):
    self.code = code

  def __repr__(self) -> str:
    return self.code


class InlineCode:
  """ Represents the result of extraction of inline code from a component - such as
  a sql statement or PySpark code. Contains all of the metadata needed to render
  a component definition, with the inline code written to a separate file, and a reference
  to this code stored in the component.
  """
  def __init__(self, code: str, attribute_path: Tuple[str, ...], resource_path: str, base_path: str, base64_encoded: bool = False):
    """
    Parameters:
    - code: inline code
    - attribute_path: path of the attribute in the component definition that contains
    the inline code, represented as a tuple of path components. For instance, the
    path for sql code in a Transform is ("operator", "sql_query", "sql")
    - resource_path: file path to which inline code is written
    - base_path: base path of dataflow or data service resource definition
    - base64_encoded: if set to `True`, inline code is base64 encoded
    """
    self.code = code
    self.resource_path = resource_path
    self.attribute_path = attribute_path
    self._rel_path = os.path.relpath(os.path.realpath(resource_path), os.path.realpath(base_path))
    self.base64_encoded = base64_encoded

  def loader(self) -> str:
    rel_path_components = ", ".join(map(lambda x: f'"{x}"', pathlib.Path(self._rel_path).parts))
    path_code = f'''pathlib.Path(os.path.join(os.path.dirname(os.path.realpath(__file__)), {rel_path_components})).read_bytes().decode("utf-8")'''
    if self.base64_encoded:
      return f'''base64.b64decode({path_code}).decode("utf-8")'''
    return path_code


def extract_inline_code(component: Definition, resource_path: str, base_path: str):
  icl = _inline_code_list_for(component, resource_path, base_path)
  for ic in icl:
    pathlib.Path(os.path.dirname(ic.resource_path)).mkdir(parents=True, exist_ok=True)
    with open(ic.resource_path, "wb") as f:
      f.write(ic.code.encode("utf-8"))
  inline = {ic.attribute_path: InlineCodeReader(ic.loader()) for ic in icl}
  glog.debug(f'inline code for {component}: {inline}')
  return inline


def download_component(client: Client, data_service_id: str, dataflow_id: str, component_id: str, resource_base_path: str = ".", template_dir: str = None):
  """
  Downloads a Component and writes its definition to a file named `{component_id}.py` under
  `resource_base_path`. Inline code for PySpark and SQL Transforms are written as separate
  files in the same folder with the file names derived from the id of the component to
  which the code belongs. Creates `resource_base_path` if `resource_base_path` does not exist.

  Parameters:
  - client: SDK client
  - data_service_id: DataService id
  - dataflow_id: Dataflow id
  - component_id: Component id
  - resource_base_path: path to which Component definition will be written are written
  - template_dir: directory that contains templates for rendering. Defaults to v1 template directory.
  """
  if os.path.exists(resource_base_path) and not os.path.isdir(resource_base_path):
    raise ValueError(f"Specified resource path ({resource_base_path}) must be a directory")
  pathlib.Path(resource_base_path).mkdir(parents=True, exist_ok=True)

  # find our component and write it
  dataflow = get_dataflow(client, data_service_id, dataflow_id)
  for component in dataflow.components:
    if component.id == component_id:
      component_path = os.path.join(resource_base_path, f"{component_id}_apply.py")
      glog.info(f"Writing component definition to ({component_path}) and component resource files to ({resource_base_path})")
      with open(component_path, "w", encoding="utf-8") as f:
        f.write(
            _jinja_render(template_dir,
                          'component.jinja',
                          data_service_id=data_service_id,
                          dataflow_id=dataflow_id,
                          component=component,
                          base_path=resource_base_path,
                          hostname=client.hostname))
        return

  raise KeyError(f"Component with id of {component_id} not found in dataflow {data_service_id}.{dataflow_id}")


def _rewrite_ds_connection_ids(client: Client, data_service: DataService):
  ds_connections = client.list_connections(data_service.id).data
  connections = {c.id.value: c.entity_metadata.id for c in ds_connections}
  for c in data_service.connections:
    c.id = connections.get(c.id)

  connections = {c.id.value: c.entity_metadata.id for c in ds_connections}
  dp_proto = getattr(data_service.data_plane_config, data_service.data_service_type, None)
  if dp_proto:
    dp_proto.connection_id = connections.get(dp_proto.connection_id)


def _rewrite_connection_ids_to_friendly_ids(connections: dict, dataflow: Dataflow):
  cids_map = {x.id.value: x.entity_metadata.id for x in connections.data}
  glog.debug(f'Connection ID Map {cids_map}')
  for c in dataflow.components:
    glog.debug(f'Connection {c} Rewriting IDs')
    # for transform, there is no container.
    cid = c.container.record_connection.connection_id.value if hasattr(c, 'container') else None
    # backward compatible change, if using the new sdk against old env, we may get into a case that
    # uuid to friendly map get an empty mapping value.
    friendly_id = cids_map.get(cid) if cid else None
    glog.debug(f'Connection {cid} -> {friendly_id}')
    if friendly_id:
      c.container.record_connection.connection_id.value = friendly_id


def _rewrite_credential_ids_to_friendly_ids(credentials: dict, dataflow: Dataflow):
  cids_map = {x.credential.id.value: x.credential_id for x in credentials.data}
  for c in dataflow.components:
    cid = c.operator.spark_function.credentials_configuration.id.value if hasattr(c, 'operator') and hasattr(c.operator, 'spark_function') else None
    friendly_id = cids_map.get(cid) if cid else None
    if friendly_id:
      c.operator.spark_function.credentials_configuration.id.value = friendly_id


def download_dataflow(client: Client, data_service_id: str, dataflow_id: str, resource_base_path: str = ".", template_dir: str = None):
  """
  Downloads a Dataflow and writes its definition to a file named `{dataflow_id}.py` under
  `resource_base_path`. Inline code for Transforms and ReadConnectors are written as separate
  files to a sub-folder - `resource_base_path`/`components`/ with the file names derived
  from the id of the component to which the code belongs. Creates `resource_base_path` if
  `resource_base_path` does not exist.

  Parameters:
  - client: SDK client
  - data_service_id: DataService id
  - dataflow_id: Dataflow id
  - resource_base_path: path to which Dataflow definition and resource files are written
  - template_dir: directory that contains templates for rendering. Defaults to v1 template directory.
  """
  write_dataflow(client.hostname, data_service_id, get_dataflow(client, data_service_id, dataflow_id), resource_base_path, template_dir)


def get_dataflow(client: Client, data_service_id: str, dataflow_id: str) -> Dataflow:
  df_proto = client.get_dataflow(data_service_id=data_service_id, dataflow_id=dataflow_id).data
  dataflow = dataflow_from_proto(client, data_service_id, df_proto)

  # translate connection id to friendly id
  connections = client.list_connections(data_service_id)
  _rewrite_connection_ids_to_friendly_ids(connections, dataflow)

  # translate credential id to friendly id
  credentials = client.list_data_service_credentials(data_service_id)
  _rewrite_credential_ids_to_friendly_ids(credentials, dataflow)

  return dataflow


def write_dataflow(hostname: str, data_service_id: str, dataflow: Dataflow, resource_base_path: str = ".", template_dir: str = None):
  if os.path.exists(resource_base_path) and not os.path.isdir(resource_base_path):
    raise ValueError(f"Specified resource path ({resource_base_path}) must be a directory")

  dataflow_path = os.path.join(resource_base_path, f"{dataflow.id}.py")
  glog.info(f"Writing dataflow definition to {dataflow_path}")
  pathlib.Path(resource_base_path).mkdir(parents=True, exist_ok=True)

  with open(dataflow_path, "w", encoding="utf-8") as f:
    f.write(_jinja_render(template_dir, 'dataflow.jinja', data_service_id=data_service_id, dataflow=dataflow, hostname=hostname, base_path=resource_base_path))


def download_data_service(client: Client, data_service_id: str, resource_base_path: str = ".", template_dir: str = None):
  """
  Downloads a DataService and writes its definition to a file named `{data_service_id}.py`
  under `resource_base_path`. Inline code for Transforms and ReadConnectors are written as separate
  files to sub-folders - `resource_base_path`/`{dataflow_id}`/`components`/ with the file name derived from
  the id of the component to which the code belongs. Creates `resource_base_path` if
  `resource_base_path` does not exist.

  Parameters:
  - client: SDK client
  - data_service_id: DataService id
  - resource_base_path: base path to which DataService definition and resource files are written
  - template_dir: directory that contains templates for rendering. Defaults to v1 template directory.
  """
  ds_proto = client.get_data_service(data_service_id=data_service_id).data
  data_service = data_service_from_proto(client, ds_proto)
  _rewrite_ds_connection_ids(client, data_service)
  data_service.dataflows = [get_dataflow(client, data_service_id, df.id) for df in data_service.dataflows]
  write_data_service(client.hostname, data_service, resource_base_path, template_dir)


def write_data_service(hostname: str, data_service: DataService, resource_base_path: str = ".", template_dir: str = None):
  if os.path.exists(resource_base_path) and not os.path.isdir(resource_base_path):
    raise ValueError(f"Specified resource path ({resource_base_path}) must be a directory")

  data_service_path = os.path.join(resource_base_path, f"{data_service.id}.py")
  glog.info(f"Writing data service definition to {data_service_path}")
  pathlib.Path(resource_base_path).mkdir(parents=True, exist_ok=True)

  with open(data_service_path, "w", encoding="utf-8") as f:
    f.write(_jinja_render(template_dir, 'data_service.jinja', data_service=data_service, hostname=hostname, base_path=resource_base_path))


_proto_mods = [
    "ascend", "component", "connection", "content_encoding", "core", "environment", "expression", "format", "function", "io", "operator", "pattern", "schema",
    "text"
]

_gmod_classes = [("google.protobuf.wrappers_pb2", "DoubleValue"), ("google.protobuf.wrappers_pb2", "BoolValue"), ("google.protobuf.wrappers_pb2", "Int64Value"),
                 ("google.protobuf.wrappers_pb2", "UInt64Value"), ("google.protobuf.wrappers_pb2", "Int32Value"),
                 ("google.protobuf.wrappers_pb2", "UInt32Value"), ("google.protobuf.duration_pb2", "Duration"), ("google.protobuf.timestamp_pb2", "Timestamp"),
                 ("google.protobuf.struct_pb2", "NullValue"), ("google.protobuf.empty_pb2", "Empty")]


def _classname_map() -> dict:
  classname_map: dict = {}

  for defclass in [
      'DataService', 'Credential', 'Connection', 'Dataflow', 'ReadConnector', 'WriteConnector', 'Transform', 'ComponentGroup', 'DataFeed', 'DataFeedConnector',
      'DataShare', 'DataShareConnector'
  ]:
    classname_map[defclass] = f"definitions.{defclass}"

  for _, cls in _gmod_classes:
    classname_map[f"google.protobuf.{cls}"] = cls

  return classname_map


def _inline_code_list_for(component: Definition, resource_path_prefix: str, base_path: str) -> Optional[List[InlineCode]]:
  glog.debug(f'Extracting code from component {component} of type {type(component)} into {resource_path_prefix} of {base_path}')
  if isinstance(component, Transform) and component.operator:
    if component.operator.HasField("spark_function") and component.operator.spark_function.executable.code.source.HasField("inline"):
      language = component.operator.spark_function.executable.code.language.WhichOneof("language")
      if language in ("sql", "snowflake_sql", "databricks_sql", "bigquery_sql"):
        resource_name = f"{component.id}.sql"
      elif language in ("python", "snowpark"):
        resource_name = f"{component.id}.py"
      else:
        raise ValueError(f"code download for language type \"{language}\" is unsupported")
      return [
          InlineCode(code=component.operator.spark_function.executable.code.source.inline,
                     resource_path=os.path.join(resource_path_prefix, resource_name),
                     base_path=base_path,
                     attribute_path=("operator", "spark_function", "executable", "code", "source", "inline"))
      ]
    elif component.operator.HasField("sql_query"):
      return [
          InlineCode(code=component.operator.sql_query.sql,
                     resource_path=os.path.join(resource_path_prefix, f"{component.id}.sql"),
                     base_path=base_path,
                     attribute_path=("operator", "sql_query", "sql"))
      ]
    else:
      return []
  # for custom blob write
  elif isinstance(component, WriteConnector):
    icl = []
    if component.container:
      details = component.container.record_connection.details
      if details.get('write_strategy'):
        write_strategy_value = value_from_proto(details.get('write_strategy'))
        custom_function = write_strategy_value.get('custom_function')
        if custom_function:
          custom_code = custom_function.get('code_interface', {}).get('write_all', {}).get("code_fingerprint_strategy",
                                                                                           UnionValue()).get("content_based_fingerprint", {}).get("code")
          if custom_code:
            icl.append(
                InlineCode(
                    code=custom_code,
                    resource_path=os.path.join(resource_path_prefix, f"{component.id}_custom_code.py"),  # noqa: E126
                    base_path=base_path,
                    attribute_path=('container', 'record_connection', 'details', 'write_strategy', 'custom_function', 'code_interface', 'write_all',
                                    'code_fingerprint_strategy', 'content_based_fingerprint', 'code'),
                    base64_encoded=False))
    return icl
  # TODO(xiaoxi): refactor to make this shorter by traverse down by following the attribute path after extracting the value_from_proto
  elif isinstance(component, ReadConnector):
    icl = []
    if component.container:
      if component.container.HasField("byte_function") and component.container.byte_function.container.executable.code.source.HasField("inline"):
        icl.append(
            InlineCode(
                code=base64.b64decode(component.container.byte_function.container.executable.code.source.inline).decode(),
                resource_path=os.path.join(resource_path_prefix, f"custom_read_connector_{component.id}.py"),  # noqa: E126
                base_path=base_path,
                attribute_path=("container", "byte_function", "container", "executable", "code", "source", "inline"),
                base64_encoded=True))
      elif component.container.HasField("record_connection"):
        details = component.container.record_connection.details
        code_interface = details.get("code_interface", {})
        # new custom python RC
        if code_interface:
          code_interface_value = value_from_proto(code_interface)
          for interface_type in ['bytes', 'pandas_dataframe', 'spark_dataframe']:
            code = code_interface_value.get(interface_type, dict()).get("code_fingerprint_strategy", UnionValue()).get("content_based_fingerprint",
                                                                                                                       {}).get("code")
            if code:
              icl.append(
                  InlineCode(
                      code=code,
                      resource_path=os.path.join(resource_path_prefix, f"{component.id}_custom_code.py"),  # noqa: E126
                      base_path=base_path,
                      attribute_path=('container', 'record_connection', 'details', 'code_interface', interface_type, 'code_fingerprint_strategy',
                                      'content_based_fingerprint', 'code'),
                      base64_encoded=False))

          parser_type = code_interface_value.get("bytes", dict()).get("parser_type", UnionValue())
          if parser_type.get("user_parser", {}):
            parser_code = parser_type.get("user_parser", {}).get("code_interface",
                                                                 {}).get("byte_stream", {}).get("code_fingerprint_strategy",
                                                                                                UnionValue()).get("content_based_fingerprint", {}).get("code")
            if parser_code:
              icl.append(
                  InlineCode(
                      code=parser_code,
                      resource_path=os.path.join(resource_path_prefix, f"{component.id}_custom_parser.py"),  # noqa: E126
                      base_path=base_path,
                      attribute_path=("container", "record_connection", "details", "code_interface", "bytes", "parser_type", "user_parser", "code_interface",
                                      "byte_stream", "code_fingerprint_strategy", "content_based_fingerprint", "code"),
                      base64_encoded=False))
        # for user parser in blob rc
        parser = details.get('parser_type')
        if parser:
          parser_value = value_from_proto(parser)
          parser_code = parser_value.get('user_parser', {}).get('code_interface', {}).get('byte_stream', {}).get('code_fingerprint_strategy',
                                                                                                                 {}).get('content_based_fingerprint',
                                                                                                                         {}).get('code')
          if parser_code:
            icl.append(
                InlineCode(
                    code=parser_code,
                    resource_path=os.path.join(resource_path_prefix, f"{component.id}_custom_parser.py"),  # noqa: E126
                    base_path=base_path,
                    attribute_path=("container", "record_connection", "details", "parser_type", "user_parser", "code_interface", "byte_stream",
                                    "code_fingerprint_strategy", "content_based_fingerprint", "code"),
                    base64_encoded=False))

    if component.bytes and component.bytes.parser.HasField("lambda_parser") and component.bytes.parser.lambda_parser.HasField(
        "code") and component.bytes.parser.lambda_parser.code.HasField("inline"):
      icl.append(
          InlineCode(
              code=base64.b64decode(component.bytes.parser.lambda_parser.code.inline).decode(),
              resource_path=os.path.join(resource_path_prefix, f"custom_parser_{component.id}.py"),  # noqa: E126
              base_path=base_path,
              attribute_path=("bytes", "parser", "lambda_parser", "code", "inline"),
              base64_encoded=True))
    return icl
  elif isinstance(component, Connection):
    glog.debug(f'Looking for custom code in Connection {component}')
    if component.details.get("shared_lib", None):
      code_string = value_from_proto(component.details['shared_lib'])
      if code_string:
        return [
            InlineCode(code=code_string,
                       resource_path=os.path.join(resource_path_prefix, f"{component.id}_shared.py"),
                       base_path=base_path,
                       attribute_path=('details', 'shared_lib'))
        ]
  return []


def _validate_template_dir(template_dir) -> str:
  glog.debug(f'Using template {template_dir}')
  if not template_dir:
    glog.info('Defaulting rendering to TEMPLATES_V3')
    return str(TEMPLATES_V2)
  if TEMPLATES_V1 == template_dir:
    glog.warning('TEMPLATES_V1 is deprecated and will be removed from the next release.')

  return str(template_dir)


def _jinja_render(template_dir, filename, **kwargs) -> str:
  template_dir = _validate_template_dir(template_dir)
  env = jinja2.Environment(extensions=['jinja2.ext.do'], loader=jinja2.FileSystemLoader(template_dir), trim_blocks=True, lstrip_blocks=True)
  return env.get_template(filename).render(classname_map=_classname_map(),
                                           extract_inline_code=extract_inline_code,
                                           gmod_classes=_gmod_classes,
                                           ordered_components=components_ordered_by_dependency,
                                           ordered_dataflows=dataflows_ordered_by_dependency,
                                           os=os,
                                           proto_mods=_proto_mods,
                                           renderer=_render_definition,
                                           template_dir=template_dir,
                                           write_dataflow=write_dataflow,
                                           **kwargs)


def _load_template(template_dir: str, file_name: str) -> jinja2.Template:
  env = jinja2.Environment(extensions=['jinja2.ext.do'], loader=jinja2.FileSystemLoader(template_dir), trim_blocks=True, lstrip_blocks=True)
  return env.get_template(file_name)


def _render_definition(val: Definition,
                       attribute_path: Tuple[str, ...] = (),
                       indent=0,
                       classname_map: dict = {},
                       attribute_overrides: dict = {},
                       template_dir: str = None):
  defcls = val.__class__.__name__
  cls = classname_map.get(defcls, defcls)
  if template_dir:
    tmpl = _load_template(template_dir, 'render_definition.jinja')
  else:
    tmpl = jinja2.Template('''{{cls}}(
{% for k, v in vars(val).items() %}\
{% if attribute_overrides.get(_append(attribute_path, k)) %}\
{{_spaces_for(indent+2)}}{{k}}=\
{{attribute_overrides.get(_append(attribute_path, k))}},\n\
{% else %}\
{{_spaces_for(indent+2)}}{{k}}=\
{{_render_value(v, _append(attribute_path, k), indent+2, classname_map, attribute_overrides)}},\n\
{% endif %}\
{% endfor %}\
{{_spaces_for(indent)}})''')
  return tmpl.render(val=val,
                     vars=vars,
                     _render_value=_render_value,
                     _spaces_for=_spaces_for,
                     _append=_append,
                     indent=indent,
                     classname_map=classname_map,
                     attribute_path=attribute_path,
                     attribute_overrides=attribute_overrides,
                     cls=cls,
                     template_dir=template_dir)


def _render_value(val, attribute_path: Tuple[str, ...], indent=0, classname_map: dict = {}, attribute_overrides: dict = {}, template_dir: str = None):
  """ Renders values in Python definition form. Support is limited to
  resource definitions, proto messages, and native types.
  """
  glog.debug(f'_render_value at path: {attribute_path} type: {type(val)} for overrides: {attribute_overrides}')
  if isinstance(val, list) or type(val) in REPEATED_CONTAINERS:
    return _render_array(val, attribute_path, indent, classname_map, attribute_overrides, template_dir=template_dir)
  elif isinstance(val, collections.abc.MutableMapping):
    return _render_map(val, attribute_path, indent, classname_map, attribute_overrides, template_dir=template_dir)
  elif isinstance(val, schema_pb2.Field):
    return _render_proto_field(val, attribute_path, indent, classname_map, attribute_overrides, template_dir=template_dir)
  elif isinstance(val, ascend_pb2.Value):
    return _render_proto_value(val, attribute_path, indent, classname_map, attribute_overrides, template_dir=template_dir)
  elif isinstance(val, ProtoMessage):
    return _render_message(val, attribute_path, indent, classname_map, attribute_overrides, template_dir=template_dir)
  elif isinstance(val, Definition):
    return _render_definition(val, attribute_path, indent, classname_map, attribute_overrides, template_dir=template_dir)
  elif isinstance(val, InlineCodeReader):
    glog.debug(f'val is an InlineCodeReader {val}')
    return _render_code_reader(val)
  elif isinstance(val, str):
    return repr(val)
  else:
    return val


def _render_code_reader(val):
  return f"value.String({val})"


def _render_array(arr, attribute_path: Tuple[str, ...], indent=0, classname_map: dict = {}, attribute_overrides: dict = {}, template_dir: str = None):
  if template_dir:
    tmpl = _load_template(template_dir, 'render_array.jinja')
  else:
    tmpl = jinja2.Template('''[
{% for v in arr %}\
{{_spaces_for(indent+2)}}{{ _render_value(v, attribute_path, indent+2, classname_map, attribute_overrides) }},\n\
{% endfor %}\
{{_spaces_for(indent)}}]''')
  return tmpl.render(
      arr=arr,
      _render_value=_render_value,
      _spaces_for=_spaces_for,
      indent=indent,
      classname_map=classname_map,
      attribute_path=attribute_path,
      attribute_overrides=attribute_overrides,
      template_dir=template_dir,
  )


def _render_map(mp, attribute_path: Tuple[str, ...], indent=0, classname_map: dict = {}, attribute_overrides: dict = {}, template_dir: str = None):
  if template_dir:
    tmpl = _load_template(template_dir, 'render_map.jinja')
  else:
    tmpl = jinja2.Template('''{
{% for k in sorted(mp.keys()) %}\
{{_spaces_for(indent+2)}}{{_render_value(k, attribute_path, indent+2, classname_map, attribute_overrides)}}: \
{{ _render_value(mp[k], _append(attribute_path, k), indent+2, classname_map, attribute_overrides) }},\n\
{% endfor %}\
{{_spaces_for(indent)}}}''')
  return tmpl.render(
      mp=mp,
      sorted=sorted,
      _render_value=_render_value,
      _spaces_for=_spaces_for,
      _append=_append,
      indent=indent,
      classname_map=classname_map,
      attribute_path=attribute_path,
      attribute_overrides=attribute_overrides,
      template_dir=template_dir,
  )


def _render_proto_field(field: schema_pb2.Field,
                        attribute_path: Tuple[str, ...],
                        indent=0,
                        classname_map: dict = {},
                        attribute_overrides: dict = {},
                        template_dir: str = None):
  kind = field.schema.WhichOneof('details')
  args = ''
  if kind == 'array':
    args += f', {_render_value(field.schema.array.element_schema, attribute_path, indent, classname_map, attribute_overrides, template_dir=template_dir)}'
  elif kind == 'decimal':
    precision = field.schema.decimal.precision or 10
    scale = field.schema.decimal.scale or 0
    args += f', {precision}, {scale}'
  elif kind == 'dictionary':
    # We wrap these in Field objects as adding in more wrappers (this time for Schema types)
    # seems like overkill.
    key_schema = _render_value(schema_pb2.Field(name=None, schema=field.schema.dictionary.key_schema),
                               attribute_path,
                               indent,
                               classname_map,
                               attribute_overrides,
                               template_dir=template_dir)
    value_schema = _render_value(schema_pb2.Field(name=None, schema=field.schema.dictionary.value_schema),
                                 attribute_path,
                                 indent,
                                 classname_map,
                                 attribute_overrides,
                                 template_dir=template_dir)
    args = f", key_type={key_schema}, value_type={value_schema}"
  elif kind == 'map':
    args += f', {_render_value(field.schema.map.field, attribute_path, indent, classname_map, attribute_overrides, template_dir=template_dir)}'
  return f"field.{kind.capitalize()}('{field.name}'{args})"


def _render_proto_value(val: ascend_pb2.Value,
                        attribute_path: Tuple[str, ...],
                        indent=0,
                        classname_map: dict = {},
                        attribute_overrides: dict = {},
                        template_dir: str = None):
  kind = val.WhichOneof('kind')
  if kind == 'struct_value':
    args = _render_value(val.struct_value.fields, attribute_path, indent, classname_map, attribute_overrides, template_dir=template_dir)
  elif kind == 'union_value':
    fields = '{}'
    if val.union_value.value.struct_value.fields:
      fields = _render_value(val.union_value.value.struct_value.fields,
                             _append(attribute_path, val.union_value.tag),
                             indent,
                             classname_map,
                             attribute_overrides,
                             template_dir=template_dir)
    args = f"{val.union_value.tag}={fields}"
  else:
    if attribute_overrides.get(attribute_path) and attribute_path[-1] == 'code':
      tmpl = jinja2.Template('''{{attribute_overrides.get(attribute_path)}}''')
      t = ''.join(w.capitalize() for w in kind.split('_')[:-1])
      return f"value.{t}({tmpl.render(attribute_overrides=attribute_overrides, attribute_path=attribute_path, template_dir=template_dir)})"
    else:
      args = _render_value(getattr(val, kind), attribute_path, indent, classname_map, attribute_overrides, template_dir=template_dir)
  t = ''.join(w.capitalize() for w in kind.split('_')[:-1])
  return f"value.{t}({args})"


def _render_message(message: ProtoMessage,
                    attribute_path: Tuple[str, ...],
                    indent=0,
                    classname_map: dict = {},
                    attribute_overrides: dict = {},
                    template_dir: str = None):
  def render_message_field(field_descriptor, val, attribute_path, indent, template_dir: str = None):
    if field_descriptor.label == descriptor.FieldDescriptor.LABEL_REPEATED:
      if hasattr(val, 'items'):
        return _render_map(val, attribute_path, indent, classname_map, attribute_overrides, template_dir)
      else:
        return _render_array(val, attribute_path, indent, classname_map, attribute_overrides, template_dir)
    elif field_descriptor.type == descriptor.FieldDescriptor.TYPE_MESSAGE:
      return _render_message(val, attribute_path, indent, classname_map, attribute_overrides, template_dir)
    elif field_descriptor.type == descriptor.FieldDescriptor.TYPE_STRING:
      return repr(val)
    else:
      return val

  cls = message.DESCRIPTOR.full_name
  cls = classname_map.get(cls, cls)
  if template_dir:
    tmpl = _load_template(template_dir, 'render_message.jinja')
  else:
    tmpl = jinja2.Template('''{{cls}}(
{% for field in message.ListFields() %}\
{{ _spaces_for(indent+2) }}{{ field[0].name }}=\
{{ attribute_overrides.get(_append(attribute_path, field[0].name),\
render_message_field(field[0], field[1], _append(attribute_path, field[0].name), indent+2)) }},\n\
{% endfor %}\
{{_spaces_for(indent)}})''')
  return tmpl.render(
      message=message,
      cls=cls,
      render_message_field=render_message_field,
      _spaces_for=_spaces_for,
      _append=_append,
      indent=indent,
      attribute_path=attribute_path,
      attribute_overrides=attribute_overrides,
      template_dir=template_dir,
  )


def _append(tpl: Tuple[str, ...], val: str):
  return tpl + (val, )


def _spaces_for(indent):
  return " " * indent
