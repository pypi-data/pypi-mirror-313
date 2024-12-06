from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class GetPodStackTraceDumpRequest(_message.Message):
    __slots__ = ("namespace", "pod_name", "container_name", "process_id", "process_name", "auto_detect_process")
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    POD_NAME_FIELD_NUMBER: _ClassVar[int]
    CONTAINER_NAME_FIELD_NUMBER: _ClassVar[int]
    PROCESS_ID_FIELD_NUMBER: _ClassVar[int]
    PROCESS_NAME_FIELD_NUMBER: _ClassVar[int]
    AUTO_DETECT_PROCESS_FIELD_NUMBER: _ClassVar[int]
    namespace: str
    pod_name: str
    container_name: str
    process_id: int
    process_name: str
    auto_detect_process: bool
    def __init__(
        self,
        namespace: _Optional[str] = ...,
        pod_name: _Optional[str] = ...,
        container_name: _Optional[str] = ...,
        process_id: _Optional[int] = ...,
        process_name: _Optional[str] = ...,
        auto_detect_process: bool = ...,
    ) -> None: ...

class GetPodStackTraceDumpResponse(_message.Message):
    __slots__ = ("stack_trace",)
    STACK_TRACE_FIELD_NUMBER: _ClassVar[int]
    stack_trace: str
    def __init__(self, stack_trace: _Optional[str] = ...) -> None: ...
