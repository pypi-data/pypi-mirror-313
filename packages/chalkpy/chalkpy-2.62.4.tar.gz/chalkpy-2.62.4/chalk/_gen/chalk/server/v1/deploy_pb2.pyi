from chalk._gen.chalk.auth.v1 import audit_pb2 as _audit_pb2
from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from chalk._gen.chalk.server.v1 import deployment_pb2 as _deployment_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import (
    ClassVar as _ClassVar,
    Iterable as _Iterable,
    Mapping as _Mapping,
    Optional as _Optional,
    Union as _Union,
)

DESCRIPTOR: _descriptor.FileDescriptor

class DeployBranchRequest(_message.Message):
    __slots__ = ("branch_name", "reset_branch", "archive", "is_hot_deploy")
    BRANCH_NAME_FIELD_NUMBER: _ClassVar[int]
    RESET_BRANCH_FIELD_NUMBER: _ClassVar[int]
    ARCHIVE_FIELD_NUMBER: _ClassVar[int]
    IS_HOT_DEPLOY_FIELD_NUMBER: _ClassVar[int]
    branch_name: str
    reset_branch: bool
    archive: bytes
    is_hot_deploy: bool
    def __init__(
        self,
        branch_name: _Optional[str] = ...,
        reset_branch: bool = ...,
        archive: _Optional[bytes] = ...,
        is_hot_deploy: bool = ...,
    ) -> None: ...

class DeployBranchResponse(_message.Message):
    __slots__ = ("deployment_id",)
    DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    deployment_id: str
    def __init__(self, deployment_id: _Optional[str] = ...) -> None: ...

class GetDeploymentRequest(_message.Message):
    __slots__ = ("deployment_id",)
    DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    deployment_id: str
    def __init__(self, deployment_id: _Optional[str] = ...) -> None: ...

class GetDeploymentResponse(_message.Message):
    __slots__ = ("deployment",)
    DEPLOYMENT_FIELD_NUMBER: _ClassVar[int]
    deployment: _deployment_pb2.Deployment
    def __init__(self, deployment: _Optional[_Union[_deployment_pb2.Deployment, _Mapping]] = ...) -> None: ...

class ListDeploymentsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListDeploymentsResponse(_message.Message):
    __slots__ = ("deployments",)
    DEPLOYMENTS_FIELD_NUMBER: _ClassVar[int]
    deployments: _containers.RepeatedCompositeFieldContainer[_deployment_pb2.Deployment]
    def __init__(
        self, deployments: _Optional[_Iterable[_Union[_deployment_pb2.Deployment, _Mapping]]] = ...
    ) -> None: ...

class SuspendDeploymentRequest(_message.Message):
    __slots__ = ("deployment_id",)
    DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    deployment_id: str
    def __init__(self, deployment_id: _Optional[str] = ...) -> None: ...

class SuspendDeploymentResponse(_message.Message):
    __slots__ = ("deployment",)
    DEPLOYMENT_FIELD_NUMBER: _ClassVar[int]
    deployment: _deployment_pb2.Deployment
    def __init__(self, deployment: _Optional[_Union[_deployment_pb2.Deployment, _Mapping]] = ...) -> None: ...

class ScaleDeploymentRequest(_message.Message):
    __slots__ = ("deployment_id", "sizing")
    DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    SIZING_FIELD_NUMBER: _ClassVar[int]
    deployment_id: str
    sizing: _deployment_pb2.InstanceSizing
    def __init__(
        self,
        deployment_id: _Optional[str] = ...,
        sizing: _Optional[_Union[_deployment_pb2.InstanceSizing, _Mapping]] = ...,
    ) -> None: ...

class ScaleDeploymentResponse(_message.Message):
    __slots__ = ("deployment",)
    DEPLOYMENT_FIELD_NUMBER: _ClassVar[int]
    deployment: _deployment_pb2.Deployment
    def __init__(self, deployment: _Optional[_Union[_deployment_pb2.Deployment, _Mapping]] = ...) -> None: ...

class TagDeploymentRequest(_message.Message):
    __slots__ = ("deployment_id", "tag")
    DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    TAG_FIELD_NUMBER: _ClassVar[int]
    deployment_id: str
    tag: str
    def __init__(self, deployment_id: _Optional[str] = ..., tag: _Optional[str] = ...) -> None: ...

class TagDeploymentResponse(_message.Message):
    __slots__ = ("deployment", "untagged_deployment_id")
    DEPLOYMENT_FIELD_NUMBER: _ClassVar[int]
    UNTAGGED_DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    deployment: _deployment_pb2.Deployment
    untagged_deployment_id: str
    def __init__(
        self,
        deployment: _Optional[_Union[_deployment_pb2.Deployment, _Mapping]] = ...,
        untagged_deployment_id: _Optional[str] = ...,
    ) -> None: ...

class GetActiveDeploymentsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetActiveDeploymentsResponse(_message.Message):
    __slots__ = ("deployments",)
    DEPLOYMENTS_FIELD_NUMBER: _ClassVar[int]
    deployments: _containers.RepeatedCompositeFieldContainer[_deployment_pb2.Deployment]
    def __init__(
        self, deployments: _Optional[_Iterable[_Union[_deployment_pb2.Deployment, _Mapping]]] = ...
    ) -> None: ...
