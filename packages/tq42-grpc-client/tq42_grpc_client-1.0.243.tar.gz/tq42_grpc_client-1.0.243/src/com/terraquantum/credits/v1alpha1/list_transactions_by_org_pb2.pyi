from com.terraquantum.credits.v1alpha1 import credits_event_pb2 as _credits_event_pb2
from com.terraquantum.plan.v1.plan import plan_pb2 as _plan_pb2
from buf.validate import validate_pb2 as _validate_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ListTransactionsByOrgRequest(_message.Message):
    __slots__ = ("organization_id",)
    ORGANIZATION_ID_FIELD_NUMBER: _ClassVar[int]
    organization_id: str
    def __init__(self, organization_id: _Optional[str] = ...) -> None: ...

class ListTransactionsByOrgResponse(_message.Message):
    __slots__ = ("transactions",)
    TRANSACTIONS_FIELD_NUMBER: _ClassVar[int]
    transactions: _containers.RepeatedCompositeFieldContainer[Transaction]
    def __init__(self, transactions: _Optional[_Iterable[_Union[Transaction, _Mapping]]] = ...) -> None: ...

class Transaction(_message.Message):
    __slots__ = ("type", "amount", "created_at", "consumption_event", "initial_allocation_event")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    AMOUNT_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    CONSUMPTION_EVENT_FIELD_NUMBER: _ClassVar[int]
    INITIAL_ALLOCATION_EVENT_FIELD_NUMBER: _ClassVar[int]
    type: _credits_event_pb2.TransactionType
    amount: int
    created_at: _timestamp_pb2.Timestamp
    consumption_event: ConsumptionEvent
    initial_allocation_event: InitialAllocationEvent
    def __init__(self, type: _Optional[_Union[_credits_event_pb2.TransactionType, str]] = ..., amount: _Optional[int] = ..., created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., consumption_event: _Optional[_Union[ConsumptionEvent, _Mapping]] = ..., initial_allocation_event: _Optional[_Union[InitialAllocationEvent, _Mapping]] = ...) -> None: ...

class ConsumptionEvent(_message.Message):
    __slots__ = ("experiment_run_id", "project_id", "experiment_id")
    EXPERIMENT_RUN_ID_FIELD_NUMBER: _ClassVar[int]
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    EXPERIMENT_ID_FIELD_NUMBER: _ClassVar[int]
    experiment_run_id: str
    project_id: str
    experiment_id: str
    def __init__(self, experiment_run_id: _Optional[str] = ..., project_id: _Optional[str] = ..., experiment_id: _Optional[str] = ...) -> None: ...

class InitialAllocationEvent(_message.Message):
    __slots__ = ("plan_type",)
    PLAN_TYPE_FIELD_NUMBER: _ClassVar[int]
    plan_type: _plan_pb2.PlanTypeProto
    def __init__(self, plan_type: _Optional[_Union[_plan_pb2.PlanTypeProto, str]] = ...) -> None: ...
