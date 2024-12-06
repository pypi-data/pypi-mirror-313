from chalk._gen.chalk.aggregate.v1 import backfill_pb2 as _backfill_pb2
from chalk._gen.chalk.aggregate.v1 import timeseries_pb2 as _timeseries_pb2
from chalk._gen.chalk.auth.v1 import audit_pb2 as _audit_pb2
from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
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

class PlanAggregateBackfillRequest(_message.Message):
    __slots__ = ("params",)
    PARAMS_FIELD_NUMBER: _ClassVar[int]
    params: _backfill_pb2.AggregateBackfillUserParams
    def __init__(
        self, params: _Optional[_Union[_backfill_pb2.AggregateBackfillUserParams, _Mapping]] = ...
    ) -> None: ...

class PlanAggregateBackfillResponse(_message.Message):
    __slots__ = ("estimate", "errors", "backfills", "aggregate_backfill_id")
    ESTIMATE_FIELD_NUMBER: _ClassVar[int]
    ERRORS_FIELD_NUMBER: _ClassVar[int]
    BACKFILLS_FIELD_NUMBER: _ClassVar[int]
    AGGREGATE_BACKFILL_ID_FIELD_NUMBER: _ClassVar[int]
    estimate: _backfill_pb2.AggregateBackfillCostEstimate
    errors: _containers.RepeatedScalarFieldContainer[str]
    backfills: _containers.RepeatedCompositeFieldContainer[_backfill_pb2.AggregateBackfillWithCostEstimate]
    aggregate_backfill_id: str
    def __init__(
        self,
        estimate: _Optional[_Union[_backfill_pb2.AggregateBackfillCostEstimate, _Mapping]] = ...,
        errors: _Optional[_Iterable[str]] = ...,
        backfills: _Optional[_Iterable[_Union[_backfill_pb2.AggregateBackfillWithCostEstimate, _Mapping]]] = ...,
        aggregate_backfill_id: _Optional[str] = ...,
    ) -> None: ...

class GetAggregatesRequest(_message.Message):
    __slots__ = ("for_features",)
    FOR_FEATURES_FIELD_NUMBER: _ClassVar[int]
    for_features: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, for_features: _Optional[_Iterable[str]] = ...) -> None: ...

class GetAggregatesResponse(_message.Message):
    __slots__ = ("series", "errors")
    SERIES_FIELD_NUMBER: _ClassVar[int]
    ERRORS_FIELD_NUMBER: _ClassVar[int]
    series: _containers.RepeatedCompositeFieldContainer[_timeseries_pb2.AggregateTimeSeries]
    errors: _containers.RepeatedScalarFieldContainer[str]
    def __init__(
        self,
        series: _Optional[_Iterable[_Union[_timeseries_pb2.AggregateTimeSeries, _Mapping]]] = ...,
        errors: _Optional[_Iterable[str]] = ...,
    ) -> None: ...

class GetAggregateBackfillJobsRequest(_message.Message):
    __slots__ = ("limit", "cursor")
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    CURSOR_FIELD_NUMBER: _ClassVar[int]
    limit: int
    cursor: str
    def __init__(self, limit: _Optional[int] = ..., cursor: _Optional[str] = ...) -> None: ...

class GetAggregateBackfillJobsResponse(_message.Message):
    __slots__ = ("jobs", "cursor")
    JOBS_FIELD_NUMBER: _ClassVar[int]
    CURSOR_FIELD_NUMBER: _ClassVar[int]
    jobs: _containers.RepeatedCompositeFieldContainer[_backfill_pb2.AggregateBackfillJob]
    cursor: str
    def __init__(
        self,
        jobs: _Optional[_Iterable[_Union[_backfill_pb2.AggregateBackfillJob, _Mapping]]] = ...,
        cursor: _Optional[str] = ...,
    ) -> None: ...

class GetAggregateBackfillJobRequest(_message.Message):
    __slots__ = ("aggregate_backfill_id",)
    AGGREGATE_BACKFILL_ID_FIELD_NUMBER: _ClassVar[int]
    aggregate_backfill_id: str
    def __init__(self, aggregate_backfill_id: _Optional[str] = ...) -> None: ...

class GetAggregateBackfillJobResponse(_message.Message):
    __slots__ = ("job",)
    JOB_FIELD_NUMBER: _ClassVar[int]
    job: _backfill_pb2.AggregateBackfillJob
    def __init__(self, job: _Optional[_Union[_backfill_pb2.AggregateBackfillJob, _Mapping]] = ...) -> None: ...
