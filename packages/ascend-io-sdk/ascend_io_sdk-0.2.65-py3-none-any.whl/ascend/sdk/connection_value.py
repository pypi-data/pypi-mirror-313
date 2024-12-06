from __future__ import annotations
import math

from builtins import staticmethod
from datetime import datetime, date
from google.protobuf import timestamp_pb2
from typing import Any, Dict, Optional
from ascend.protos.ascend import ascend_pb2


def timestamp_to_proto(ts: float) -> timestamp_pb2.Timestamp:
  seconds = math.floor(ts)
  nanos = math.floor((ts - seconds) * 10**9)
  return timestamp_pb2.Timestamp(seconds=seconds, nanos=nanos)


def values_dict_from_proto(d: Dict[str, ascend_pb2.Value]) -> Dict[str, Any]:
  return {key: value_from_proto(value) for key, value in d.items() if value is not None}


def struct_value_from_proto(proto: ascend_pb2.Struct) -> Dict[str, Any]:
  return values_dict_from_proto(proto.fields)


def struct_value_to_proto(value: Dict[str, Any]) -> ascend_pb2.Struct:
  return ascend_pb2.Struct(fields={key: value_to_proto(val) for key, val in value.items()})


def maybe_value_from_proto(proto: ascend_pb2.Value) -> Optional[Any]:
  if proto.WhichOneof('kind') is None:
    return None
  return value_from_proto(proto)


def value_from_proto(proto: ascend_pb2.Value) -> Any:
  kind = proto.WhichOneof("kind")
  if kind in ("number_value", "string_value", "bool_value", "int_value", "long_value", "decimal_value"):
    return getattr(proto, kind)
  elif kind == "struct_value":
    return struct_value_from_proto(proto.struct_value)
  elif kind == "timestamp_value":
    ts = proto.timestamp_value
    return datetime.utcfromtimestamp(ts.seconds + ts.nanos * 1e-9)
  elif kind == "date_value":
    ts = proto.date_value
    return datetime.utcfromtimestamp(ts.seconds).date()
  elif kind == "union_value":
    u = proto.union_value
    return Union(**{u.tag: value_from_proto(u.value)}) if u.tag else Union.empty()
  else:
    raise NotImplementedError(f"Unknown value format '{kind}'")


# N.B.: This method may not resolve exact type to convert to. Prefer using `ascend.connection.ctype.field.Field.any_to_value(v)` or
# `ascend.connection.ctype.configuration_shape.ConfigurationShape.values_to_proto`
def value_to_proto(v: Any) -> ascend_pb2.Value:
  if isinstance(v, int):
    return ascend_pb2.Value(long_value=v)
  elif isinstance(v, str):
    return ascend_pb2.Value(string_value=v)
  elif isinstance(v, bool):
    return ascend_pb2.Value(bool_value=v)
  elif isinstance(v, float):
    return ascend_pb2.Value(number_value=v)
  elif isinstance(v, dict):
    return ascend_pb2.Value(struct_value=ascend_pb2.Struct(fields=[value_to_proto(val) for key, val in v.items()]))
  elif isinstance(v, date):
    dt = datetime(year=v.year, month=v.month, day=v.day)
    return ascend_pb2.Value(date_value=timestamp_to_proto(dt.timestamp()))
  elif isinstance(v, datetime):
    return ascend_pb2.Value(timestamp_value=timestamp_to_proto(v.timestamp()))
  else:
    raise NotImplementedError(f"Unknown value type '{type(v)}' value={v}")


class Union(object):
  __unset = object()

  @staticmethod
  def empty() -> Union:
    return Union()

  def __init__(self, **kwargs):
    if len(kwargs) > 1:
      raise ValueError(f"ambiguous union value: {kwargs.keys()}")
    self._maybe_case: Optional[(str, Any)] = next(iter(kwargs.items()), None)
    assert self._maybe_case is None or self._maybe_case[0], "Union tag cannot be empty"

  def is_empty(self):
    return self._maybe_case is None

  def non_empty(self):
    return self._maybe_case is not None

  def tag(self, *, default: str = __unset) -> str:
    if self.is_empty():
      if default is Union.__unset:
        raise ValueError("undefined union")
      else:
        return default
    return self._tag()

  def tag_or_none(self) -> Optional[str]:
    if self.is_empty():
      return None
    else:
      return self._tag()

  def _tag(self) -> str:
    return self._maybe_case[0]

  def value(self) -> Any:
    if self.is_empty():
      raise ValueError("undefined union")
    return self._value()

  def value_or_none(self) -> Optional[Any]:
    if self.is_empty():
      return None
    else:
      return self._value()

  def _value(self) -> str:
    return self._maybe_case[1]

  def get(self, item: str, default: Optional[Any] = None) -> Optional[Any]:
    if item in self:
      return self._value()
    else:
      return default

  def __getitem__(self, item):
    if not self.is_empty() and item == self._tag():
      return self._value()
    else:
      raise KeyError(item)

  def __contains__(self, item):
    return not self.is_empty() and item == self._tag()

  def __str__(self) -> str:
    return f"Union({'' if (self.is_empty()) else f'{self._tag()}={self._value()}'})"
