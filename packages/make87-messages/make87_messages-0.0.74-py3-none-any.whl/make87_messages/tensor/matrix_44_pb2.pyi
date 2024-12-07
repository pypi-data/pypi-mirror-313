from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Matrix44(_message.Message):
    __slots__ = ("timestamp", "m00", "m01", "m02", "m03", "m10", "m11", "m12", "m13", "m20", "m21", "m22", "m23", "m30", "m31", "m32", "m33")
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    M00_FIELD_NUMBER: _ClassVar[int]
    M01_FIELD_NUMBER: _ClassVar[int]
    M02_FIELD_NUMBER: _ClassVar[int]
    M03_FIELD_NUMBER: _ClassVar[int]
    M10_FIELD_NUMBER: _ClassVar[int]
    M11_FIELD_NUMBER: _ClassVar[int]
    M12_FIELD_NUMBER: _ClassVar[int]
    M13_FIELD_NUMBER: _ClassVar[int]
    M20_FIELD_NUMBER: _ClassVar[int]
    M21_FIELD_NUMBER: _ClassVar[int]
    M22_FIELD_NUMBER: _ClassVar[int]
    M23_FIELD_NUMBER: _ClassVar[int]
    M30_FIELD_NUMBER: _ClassVar[int]
    M31_FIELD_NUMBER: _ClassVar[int]
    M32_FIELD_NUMBER: _ClassVar[int]
    M33_FIELD_NUMBER: _ClassVar[int]
    timestamp: _timestamp_pb2.Timestamp
    m00: float
    m01: float
    m02: float
    m03: float
    m10: float
    m11: float
    m12: float
    m13: float
    m20: float
    m21: float
    m22: float
    m23: float
    m30: float
    m31: float
    m32: float
    m33: float
    def __init__(self, timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., m00: _Optional[float] = ..., m01: _Optional[float] = ..., m02: _Optional[float] = ..., m03: _Optional[float] = ..., m10: _Optional[float] = ..., m11: _Optional[float] = ..., m12: _Optional[float] = ..., m13: _Optional[float] = ..., m20: _Optional[float] = ..., m21: _Optional[float] = ..., m22: _Optional[float] = ..., m23: _Optional[float] = ..., m30: _Optional[float] = ..., m31: _Optional[float] = ..., m32: _Optional[float] = ..., m33: _Optional[float] = ...) -> None: ...
