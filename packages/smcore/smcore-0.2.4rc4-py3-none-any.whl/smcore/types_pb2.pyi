from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Ping(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class Hello(_message.Message):
    __slots__ = ("spec",)
    SPEC_FIELD_NUMBER: _ClassVar[int]
    spec: AgentSpec
    def __init__(self, spec: _Optional[_Union[AgentSpec, _Mapping]] = ...) -> None: ...

class Goodbye(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CoreData(_message.Message):
    __slots__ = ("data", "link")
    DATA_FIELD_NUMBER: _ClassVar[int]
    LINK_FIELD_NUMBER: _ClassVar[int]
    data: bytes
    link: str
    def __init__(self, data: _Optional[bytes] = ..., link: _Optional[str] = ...) -> None: ...

class Post(_message.Message):
    __slots__ = ("tags", "metadata", "data")
    TAGS_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    tags: _containers.RepeatedScalarFieldContainer[str]
    metadata: CoreData
    data: CoreData
    def __init__(self, tags: _Optional[_Iterable[str]] = ..., metadata: _Optional[_Union[CoreData, _Mapping]] = ..., data: _Optional[_Union[CoreData, _Mapping]] = ...) -> None: ...

class Log(_message.Message):
    __slots__ = ("severity", "message")
    class Severity(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        Debug: _ClassVar[Log.Severity]
        Info: _ClassVar[Log.Severity]
        Warning: _ClassVar[Log.Severity]
        Error: _ClassVar[Log.Severity]
        Critical: _ClassVar[Log.Severity]
    Debug: Log.Severity
    Info: Log.Severity
    Warning: Log.Severity
    Error: Log.Severity
    Critical: Log.Severity
    SEVERITY_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    severity: Log.Severity
    message: str
    def __init__(self, severity: _Optional[_Union[Log.Severity, str]] = ..., message: _Optional[str] = ...) -> None: ...

class Halt(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class HaltAndCatchFire(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class Message(_message.Message):
    __slots__ = ("id", "index", "source", "timeSent", "timeRecv", "ping", "hello", "goodbye", "log", "halt", "haltAndCatchFire", "createAgent", "post", "replyingTo")
    ID_FIELD_NUMBER: _ClassVar[int]
    INDEX_FIELD_NUMBER: _ClassVar[int]
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    TIMESENT_FIELD_NUMBER: _ClassVar[int]
    TIMERECV_FIELD_NUMBER: _ClassVar[int]
    PING_FIELD_NUMBER: _ClassVar[int]
    HELLO_FIELD_NUMBER: _ClassVar[int]
    GOODBYE_FIELD_NUMBER: _ClassVar[int]
    LOG_FIELD_NUMBER: _ClassVar[int]
    HALT_FIELD_NUMBER: _ClassVar[int]
    HALTANDCATCHFIRE_FIELD_NUMBER: _ClassVar[int]
    CREATEAGENT_FIELD_NUMBER: _ClassVar[int]
    POST_FIELD_NUMBER: _ClassVar[int]
    REPLYINGTO_FIELD_NUMBER: _ClassVar[int]
    id: int
    index: int
    source: str
    timeSent: _timestamp_pb2.Timestamp
    timeRecv: _timestamp_pb2.Timestamp
    ping: Ping
    hello: Hello
    goodbye: Goodbye
    log: Log
    halt: Halt
    haltAndCatchFire: HaltAndCatchFire
    createAgent: CreateAgent
    post: Post
    replyingTo: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, id: _Optional[int] = ..., index: _Optional[int] = ..., source: _Optional[str] = ..., timeSent: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., timeRecv: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., ping: _Optional[_Union[Ping, _Mapping]] = ..., hello: _Optional[_Union[Hello, _Mapping]] = ..., goodbye: _Optional[_Union[Goodbye, _Mapping]] = ..., log: _Optional[_Union[Log, _Mapping]] = ..., halt: _Optional[_Union[Halt, _Mapping]] = ..., haltAndCatchFire: _Optional[_Union[HaltAndCatchFire, _Mapping]] = ..., createAgent: _Optional[_Union[CreateAgent, _Mapping]] = ..., post: _Optional[_Union[Post, _Mapping]] = ..., replyingTo: _Optional[_Iterable[int]] = ...) -> None: ...

class AgentSpec(_message.Message):
    __slots__ = ("name", "entrypoint", "attributes", "context")
    NAME_FIELD_NUMBER: _ClassVar[int]
    ENTRYPOINT_FIELD_NUMBER: _ClassVar[int]
    ATTRIBUTES_FIELD_NUMBER: _ClassVar[int]
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    name: str
    entrypoint: str
    attributes: bytes
    context: bytes
    def __init__(self, name: _Optional[str] = ..., entrypoint: _Optional[str] = ..., attributes: _Optional[bytes] = ..., context: _Optional[bytes] = ...) -> None: ...

class CreateAgent(_message.Message):
    __slots__ = ("spec", "runner")
    SPEC_FIELD_NUMBER: _ClassVar[int]
    RUNNER_FIELD_NUMBER: _ClassVar[int]
    spec: AgentSpec
    runner: str
    def __init__(self, spec: _Optional[_Union[AgentSpec, _Mapping]] = ..., runner: _Optional[str] = ...) -> None: ...

class AgentBundle(_message.Message):
    __slots__ = ("agents",)
    AGENTS_FIELD_NUMBER: _ClassVar[int]
    agents: _containers.RepeatedCompositeFieldContainer[CreateAgent]
    def __init__(self, agents: _Optional[_Iterable[_Union[CreateAgent, _Mapping]]] = ...) -> None: ...

class GetMessagesRequest(_message.Message):
    __slots__ = ("startingAt", "filterPings")
    STARTINGAT_FIELD_NUMBER: _ClassVar[int]
    FILTERPINGS_FIELD_NUMBER: _ClassVar[int]
    startingAt: int
    filterPings: bool
    def __init__(self, startingAt: _Optional[int] = ..., filterPings: bool = ...) -> None: ...

class MessageStack(_message.Message):
    __slots__ = ("messages",)
    MESSAGES_FIELD_NUMBER: _ClassVar[int]
    messages: _containers.RepeatedCompositeFieldContainer[Message]
    def __init__(self, messages: _Optional[_Iterable[_Union[Message, _Mapping]]] = ...) -> None: ...

class Ack(_message.Message):
    __slots__ = ("status", "message")
    class Status(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        OK: _ClassVar[Ack.Status]
    OK: Ack.Status
    STATUS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    status: Ack.Status
    message: str
    def __init__(self, status: _Optional[_Union[Ack.Status, str]] = ..., message: _Optional[str] = ...) -> None: ...
