from google.protobuf import timestamp_pb2 as _timestamp_pb2
from make87_messages.spatial.rotation import quaternion_pb2 as _quaternion_pb2
from make87_messages.spatial.translation import translation_3d_pb2 as _translation_3d_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Pose3D(_message.Message):
    __slots__ = ("timestamp", "translation", "rotation")
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    TRANSLATION_FIELD_NUMBER: _ClassVar[int]
    ROTATION_FIELD_NUMBER: _ClassVar[int]
    timestamp: _timestamp_pb2.Timestamp
    translation: _translation_3d_pb2.Translation3D
    rotation: _quaternion_pb2.Quaternion
    def __init__(self, timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., translation: _Optional[_Union[_translation_3d_pb2.Translation3D, _Mapping]] = ..., rotation: _Optional[_Union[_quaternion_pb2.Quaternion, _Mapping]] = ...) -> None: ...
