from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Matrix22(_message.Message):
    __slots__ = ("timestamp", "m00", "m01", "m10", "m11")
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    M00_FIELD_NUMBER: _ClassVar[int]
    M01_FIELD_NUMBER: _ClassVar[int]
    M10_FIELD_NUMBER: _ClassVar[int]
    M11_FIELD_NUMBER: _ClassVar[int]
    timestamp: _timestamp_pb2.Timestamp
    m00: float
    m01: float
    m10: float
    m11: float
    def __init__(self, timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., m00: _Optional[float] = ..., m01: _Optional[float] = ..., m10: _Optional[float] = ..., m11: _Optional[float] = ...) -> None: ...
