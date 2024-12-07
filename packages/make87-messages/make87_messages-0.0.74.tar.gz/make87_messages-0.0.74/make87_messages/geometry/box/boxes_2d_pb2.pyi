from make87_messages.geometry.box import box_2d_pb2 as _box_2d_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Boxes2D(_message.Message):
    __slots__ = ("timestamp", "boxes")
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    BOXES_FIELD_NUMBER: _ClassVar[int]
    timestamp: _timestamp_pb2.Timestamp
    boxes: _containers.RepeatedCompositeFieldContainer[_box_2d_pb2.Box2D]
    def __init__(self, timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., boxes: _Optional[_Iterable[_Union[_box_2d_pb2.Box2D, _Mapping]]] = ...) -> None: ...

class Boxes2DAxisAligned(_message.Message):
    __slots__ = ("timestamp", "boxes")
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    BOXES_FIELD_NUMBER: _ClassVar[int]
    timestamp: _timestamp_pb2.Timestamp
    boxes: _containers.RepeatedCompositeFieldContainer[_box_2d_pb2.Box2DAxisAligned]
    def __init__(self, timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., boxes: _Optional[_Iterable[_Union[_box_2d_pb2.Box2DAxisAligned, _Mapping]]] = ...) -> None: ...
