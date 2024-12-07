from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ImageRGBA(_message.Message):
    __slots__ = ("timestamp", "width", "height", "pixels")
    class Pixel(_message.Message):
        __slots__ = ("red", "green", "blue", "alpha")
        RED_FIELD_NUMBER: _ClassVar[int]
        GREEN_FIELD_NUMBER: _ClassVar[int]
        BLUE_FIELD_NUMBER: _ClassVar[int]
        ALPHA_FIELD_NUMBER: _ClassVar[int]
        red: int
        green: int
        blue: int
        alpha: int
        def __init__(self, red: _Optional[int] = ..., green: _Optional[int] = ..., blue: _Optional[int] = ..., alpha: _Optional[int] = ...) -> None: ...
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    WIDTH_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    PIXELS_FIELD_NUMBER: _ClassVar[int]
    timestamp: _timestamp_pb2.Timestamp
    width: int
    height: int
    pixels: _containers.RepeatedCompositeFieldContainer[ImageRGBA.Pixel]
    def __init__(self, timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., width: _Optional[int] = ..., height: _Optional[int] = ..., pixels: _Optional[_Iterable[_Union[ImageRGBA.Pixel, _Mapping]]] = ...) -> None: ...
