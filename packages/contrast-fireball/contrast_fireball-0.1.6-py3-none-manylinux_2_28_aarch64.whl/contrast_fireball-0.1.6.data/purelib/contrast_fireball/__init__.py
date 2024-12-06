from ctypes import (
    c_int,
    cdll,
    POINTER,
    c_uint32,
    c_char,
    c_char_p,
    c_uint,
    byref,
    create_string_buffer,
)
from dataclasses import asdict, dataclass, field
import enum
import json
from os import path
from typing import (
    List,
    Dict,
    Optional,
    Type,
    TypeVar,
    Generic,
    TypedDict,
    Any,
)

T = TypeVar("T")

LIB_PATH = path.join(path.dirname(__file__), "cdylib", "libfireball_c")

API_VERSION = 1  # removed from fireball-core, but still in the C API
JSON_FORMAT = 1


# We'd like enum.StrEnum here, but it's only available in python 3.11. Inheriting from
# str allows us to easily serialize instances of this type using `json.dumps`.
class StrEnum(str, enum.Enum):
    pass


# integer values must align with fireball-core's BitAgentMessages enum
class AgentMessages(enum.Flag):
    NEW_CONFIG_AVAILABLE = 1 << 0
    NEW_APP_SETTINGS_AVAILABLE = 1 << 1
    NEW_SERVER_SETTINGS_AVAILABLE = 1 << 2


NO_MESSAGES = AgentMessages(0)


# string values must deserialize to values in fireball-core's AgentLanguage enum,
# according to the deserialization rules defined by `serde` for the enum.
class AgentLanguage(StrEnum):
    DOTNET = "DotNet"
    DOTNET_CORE = "DotNetCore"
    GO = "Go"
    NODE = "Node"
    JAVA = "Java"
    PYTHON = "Python"
    PHP = "Php"
    RUBY = "Ruby"


@dataclass(frozen=True)
class BindingApiSuccess(Generic[T]):
    messages: AgentMessages
    data: T


# we'd probably like `kw_only=True` for large dataclasses like this, but that feature
# was added in python 3.10
@dataclass(frozen=True)
class InitOptions:
    app_name: str
    app_path: str
    agent_language: AgentLanguage
    agent_version: str
    server_host_name: Optional[str]
    server_path: Optional[str]
    server_type: str
    config_paths: Optional[List[str]]
    overrides: Optional[Dict[str, str]]

    def _to_json_bytes(self) -> bytes:
        return json.dumps(asdict(self)).encode("utf-8")


libfireball_c = cdll.LoadLibrary(LIB_PATH)

libfireball_c.initialize_application.argtypes = [
    c_uint32,  # version
    c_uint32,  # format
    c_char_p,  # init_options_buf
    c_uint,  # init_options_buf_len
    POINTER(c_char_p),  # result
    POINTER(c_uint),  # result_size
    POINTER(c_uint),  # messages
]
libfireball_c.initialize_application.restype = c_int

libfireball_c.free_result.argtypes = [c_char_p]
libfireball_c.free_result.restype = c_int


class MustFreeBuffer(c_char_p):
    """
    Special subclass of c_char_p that guarantees fireball's `free_result` will be called
    when an instance is deleted by python's garbage collector. This is useful for cases
    where fireball allocates memory and leaves the caller responsible for freeing it.
    """

    def __del__(self) -> None:
        # If this fails, it'll at least be logged at the ERROR level.
        #
        # Translating the return code to an Exception in a __del__ could raise the
        # exception during GC, where the caller can't handle it.
        libfireball_c.free_result(self)


class InitAppSettings(TypedDict):
    """
    This class describes the basic structure of the dictionary we expect to receive
    from `initialize_application`. Ideally we'd use a more sophisticated data validation
    library to deserialize the data we receive back from Fireball. There are
    multiple potential solutions (libraries) for this and all are fairly complex - we
    don't want to spend time right now evaluating each of them. For now though, a
    TypedDict gives us basic type hints for top-level keys and values.
    """

    app_id: int
    common_config: Dict
    init_options: Dict
    teamserver_status: str
    teamserver_settings: Optional[Dict]
    archived_date: Optional[str]


def initialize_application(
    init_options: InitOptions,
) -> BindingApiSuccess[InitAppSettings]:
    """
    This should be the first call from an application to Fireball to populate all of the
    agent-provided parameters required for teamserver communication.

    The app_id in the returned dictionary should be used for all other reporting calls.
    It will be used to differentiate between different applications in the same process.

    Calling init on an already initialized application will simply return the currently
    known agent settings.

    Calling init on an application which has already been shut down will start the
    application again on teamserver and return its settings. A new app_id will be
    generated for the restarted application.
    """
    init_options_bytes = init_options._to_json_bytes()
    result = MustFreeBuffer()
    result_size = c_uint()
    messages = c_uint()
    return_status: int = libfireball_c.initialize_application(
        API_VERSION,
        JSON_FORMAT,
        init_options_bytes,
        len(init_options_bytes),
        byref(result),
        byref(result_size),
        byref(messages),
    )
    assert_ok(return_status)
    result_dict: InitAppSettings = (
        json.loads(result.value[: result_size.value])
        if result.value is not None
        else {}
    )

    return BindingApiSuccess(messages=AgentMessages(messages.value), data=result_dict)


class InstanceInfo(TypedDict):
    """
    InstanceInfo describes static information about the loaded Fireball library.
    """

    reporting_instance_id: str
    """
    Reporting instance ID of the current process. This a new UUID created during
    the process. It will be reported as the X-Contrast-Reporting-Instance header
    to all TeamServer calls.
    """

    crate_version: str
    """
    Version of the fireball crate used for this build.
    """

    git_tag: str
    """
    git tag of this fireball release.
    """

    current_dir: str
    """
    Current directory of the process.  This will be used as the default `server_path`
    if not specified in the InitOptions sent to `initialize_application`.
    """

    host_name: str
    """
    Hostname of the machine.  This will be used as the default `server_host_name` if not
    specified in the InitOptions sent to `initialize_application`.
    """


def get_info() -> InstanceInfo:
    """
    Get static fireball api information. This api is safe to call anytime, even
    without initializing any applications.
    """

    result = MustFreeBuffer()
    result_size = c_uint()

    return_status: int = libfireball_c.get_info(
        API_VERSION,
        JSON_FORMAT,
        byref(result),
        byref(result_size),
    )
    assert_ok(return_status)
    result_dict: InstanceInfo = (
        json.loads(result.value[: result_size.value])
        if result.value is not None
        else {}
    )

    return result_dict


libfireball_c.get_info.argtypes = [
    c_uint32,  # version
    c_uint32,  # format
    POINTER(c_char_p),  # result
    POINTER(c_uint),  # result_size
]
libfireball_c.get_info.restype = c_int


class AssessEventType(StrEnum):
    METHOD = "METHOD"
    PROPAGATION = "PROPAGATION"
    TAG = "TAG"


class AssessTaintRangeTag(StrEnum):
    BASE32_ENCODED = "BASE32_ENCODED"
    BASE64_DECODED = "BASE64_DECODED"
    BASE64_ENCODED = "BASE64_ENCODED"
    COMPARED = "COMPARED"
    CONSTANT = "CONSTANT"
    CROSS_SITE = "CROSS_SITE"
    CSS_DECODED = "CSS_DECODED"
    CSS_ENCODED = "CSS_ENCODED"
    CSV_DECODED = "CSV_DECODED"
    CSV_ENCODED = "CSV_ENCODED"
    CUSTOM_ENCODED_CMD_INJECTION = "CUSTOM_ENCODED_CMD_INJECTION"
    CUSTOM_ENCODED_EXPRESSION_LANGUAGE_INJECTION = (
        "CUSTOM_ENCODED_EXPRESSION_LANGUAGE_INJECTION"
    )
    CUSTOM_ENCODED_HEADER_INJECTION = "CUSTOM_ENCODED_HEADER_INJECTION"
    CUSTOM_ENCODED_HQL_INJECTION = "CUSTOM_ENCODED_HQL_INJECTION"
    CUSTOM_ENCODED_LDAP_INJECTION = "CUSTOM_ENCODED_LDAP_INJECTION"
    CUSTOM_ENCODED_LOG_INJECTION = "CUSTOM_ENCODED_LOG_INJECTION"
    CUSTOM_ENCODED_NOSQL_INJECTION = "CUSTOM_ENCODED_NOSQL_INJECTION"
    CUSTOM_ENCODED_PATH_TRAVERSAL = "CUSTOM_ENCODED_PATH_TRAVERSAL"
    CUSTOM_ENCODED_REDOS = "CUSTOM_ENCODED_REDOS"
    CUSTOM_ENCODED_REFLECTED_XSS = "CUSTOM_ENCODED_REFLECTED_XSS"
    CUSTOM_ENCODED_REFLECTION_INJECTION = "CUSTOM_ENCODED_REFLECTION_INJECTION"
    CUSTOM_ENCODED_SMTP_INJECTION = "CUSTOM_ENCODED_SMTP_INJECTION"
    CUSTOM_ENCODED_SQL_INJECTION = "CUSTOM_ENCODED_SQL_INJECTION"
    CUSTOM_ENCODED_SSRF = "CUSTOM_ENCODED_SSRF"
    CUSTOM_ENCODED_STORED_XSS = "CUSTOM_ENCODED_STORED_XSS"
    CUSTOM_ENCODED_TRUST_BOUNDARY_VIOLATION = "CUSTOM_ENCODED_TRUST_BOUNDARY_VIOLATION"
    CUSTOM_ENCODED_UNSAFE_CODE_EXECUTION = "CUSTOM_ENCODED_UNSAFE_CODE_EXECUTION"
    CUSTOM_ENCODED_UNSAFE_READLINE = "CUSTOM_ENCODED_UNSAFE_READLINE"
    CUSTOM_ENCODED_UNSAFE_XML_DECODE = "CUSTOM_ENCODED_UNSAFE_XML_DECODE"
    CUSTOM_ENCODED_UNTRUSTED_DESERIALIZATION = (
        "CUSTOM_ENCODED_UNTRUSTED_DESERIALIZATION"
    )
    CUSTOM_ENCODED_UNVALIDATED_FORWARD = "CUSTOM_ENCODED_UNVALIDATED_FORWARD"
    CUSTOM_ENCODED_UNVALIDATED_REDIRECT = "CUSTOM_ENCODED_UNVALIDATED_REDIRECT"
    CUSTOM_ENCODED_XPATH_INJECTION = "CUSTOM_ENCODED_XPATH_INJECTION"
    CUSTOM_ENCODED_XXE = "CUSTOM_ENCODED_XXE"
    CUSTOM_ENCODED = "CUSTOM_ENCODED"
    CUSTOM_SECURITY_CONTROL_APPLIED = "CUSTOM_SECURITY_CONTROL_APPLIED"
    CUSTOM_VALIDATED_CMD_INJECTION = "CUSTOM_VALIDATED_CMD_INJECTION"
    CUSTOM_VALIDATED_EXPRESSION_LANGUAGE_INJECTION = (
        "CUSTOM_VALIDATED_EXPRESSION_LANGUAGE_INJECTION"
    )
    CUSTOM_VALIDATED_HEADER_INJECTION = "CUSTOM_VALIDATED_HEADER_INJECTION"
    CUSTOM_VALIDATED_HQL_INJECTION = "CUSTOM_VALIDATED_HQL_INJECTION"
    CUSTOM_VALIDATED_LDAP_INJECTION = "CUSTOM_VALIDATED_LDAP_INJECTION"
    CUSTOM_VALIDATED_LOG_INJECTION = "CUSTOM_VALIDATED_LOG_INJECTION"
    CUSTOM_VALIDATED_NOSQL_INJECTION = "CUSTOM_VALIDATED_NOSQL_INJECTION"
    CUSTOM_VALIDATED_PATH_TRAVERSAL = "CUSTOM_VALIDATED_PATH_TRAVERSAL"
    CUSTOM_VALIDATED_REDOS = "CUSTOM_VALIDATED_REDOS"
    CUSTOM_VALIDATED_REFLECTED_XSS = "CUSTOM_VALIDATED_REFLECTED_XSS"
    CUSTOM_VALIDATED_REFLECTION_INJECTION = "CUSTOM_VALIDATED_REFLECTION_INJECTION"
    CUSTOM_VALIDATED_SMTP_INJECTION = "CUSTOM_VALIDATED_SMTP_INJECTION"
    CUSTOM_VALIDATED_SQL_INJECTION = "CUSTOM_VALIDATED_SQL_INJECTION"
    CUSTOM_VALIDATED_SSRF = "CUSTOM_VALIDATED_SSRF"
    CUSTOM_VALIDATED_STORED_XSS = "CUSTOM_VALIDATED_STORED_XSS"
    CUSTOM_VALIDATED_TRUST_BOUNDARY_VIOLATION = (
        "CUSTOM_VALIDATED_TRUST_BOUNDARY_VIOLATION"
    )
    CUSTOM_VALIDATED_UNSAFE_CODE_EXECUTION = "CUSTOM_VALIDATED_UNSAFE_CODE_EXECUTION"
    CUSTOM_VALIDATED_UNSAFE_READLINE = "CUSTOM_VALIDATED_UNSAFE_READLINE"
    CUSTOM_VALIDATED_UNSAFE_XML_DECODE = "CUSTOM_VALIDATED_UNSAFE_XML_DECODE"
    CUSTOM_VALIDATED_UNTRUSTED_DESERIALIZATION = (
        "CUSTOM_VALIDATED_UNTRUSTED_DESERIALIZATION"
    )
    CUSTOM_VALIDATED_UNVALIDATED_FORWARD = "CUSTOM_VALIDATED_UNVALIDATED_FORWARD"
    CUSTOM_VALIDATED_UNVALIDATED_REDIRECT = "CUSTOM_VALIDATED_UNVALIDATED_REDIRECT"
    CUSTOM_VALIDATED_XPATH_INJECTION = "CUSTOM_VALIDATED_XPATH_INJECTION"
    CUSTOM_VALIDATED_XXE = "CUSTOM_VALIDATED_XXE"
    CUSTOM_VALIDATED = "CUSTOM_VALIDATED"
    CUSTOM = "CUSTOM"
    DATABASE_WRITE = "DATABASE_WRITE"
    HTML_DECODED = "HTML_DECODED"
    HTML_ENCODED = "HTML_ENCODED"
    JAVA_DECODED = "JAVA_DECODED"
    JAVA_ENCODED = "JAVA_ENCODED"
    JAVASCRIPT_DECODED = "JAVASCRIPT_DECODED"
    JAVASCRIPT_ENCODED = "JAVASCRIPT_ENCODED"
    LDAP_DECODED = "LDAP_DECODED"
    LDAP_ENCODED = "LDAP_ENCODED"
    LIMITED_CHARS = "LIMITED_CHARS"
    NO_CONTROL_CHARS = "NO_CONTROL_CHARS"
    NO_NEWLINES = "NO_NEWLINES"
    OS_DECODED = "OS_DECODED"
    OS_ENCODED = "OS_ENCODED"
    POTENTIAL_SANITIZED = "POTENTIAL_SANITIZED"
    POTENTIAL_VALIDATED = "POTENTIAL_VALIDATED"
    SAFE_REDIRECT = "SAFE_REDIRECT"
    SQL_DECODED = "SQL_DECODED"
    SQL_ENCODED = "SQL_ENCODED"
    UNTRUSTED = "UNTRUSTED"
    URL_DECODED = "URL_DECODED"
    URL_ENCODED = "URL_ENCODED"
    VALIDATED = "VALIDATED"
    VBSCRIPT_DECODED = "VBSCRIPT_DECODED"
    VBSCRIPT_ENCODED = "VBSCRIPT_ENCODED"
    XML_DECODED = "XML_DECODED"
    XML_ENCODED = "XML_ENCODED"
    XMLIF_VALIDATED_XXE = "XMLIF_VALIDATED_XXE"
    XPATH_DECODED = "XPATH_DECODED"
    XPATH_ENCODED = "XPATH_ENCODED"
    XSS_ENCODED = "XSS_ENCODED"


@dataclass(frozen=True)
class AssessTaintRange:
    range: str
    tag: AssessTaintRangeTag


@dataclass(frozen=True)
class AssessStackFrame:
    line_number: int
    eval: Optional[str] = None
    file: Optional[str] = None
    method: Optional[str] = None
    signature: Optional[str] = None
    type: Optional[str] = None


class SignatureExpressionType(StrEnum):
    MEMBER_EXPRESSION = "MEMBER_EXPRESSION"
    CALL_EXPRESSION = "CALL_EXPRESSION"
    BINARY_EXPRESSION = "BINARY_EXPRESSION"
    ASSIGNMENT_EXPRESSION = "ASSIGNMENT_EXPRESSION"


@dataclass(frozen=True)
class AssessSignature:
    arg_types: List[str]
    class_name: str
    constructor: bool
    flags: int
    method_name: str
    return_type: str
    void_method: bool
    signature: Optional[str] = None
    expression_type: Optional[SignatureExpressionType] = None
    operator: Optional[str] = None


@dataclass(frozen=True)
class AssessEventProperty:
    key: str
    value: str


class SourceType(StrEnum):
    """
    The type of the source of the data.
    """

    BODY = "BODY"
    BROKER_MESSAGE = "BROKER_MESSAGE"
    CANARY_DATABASE = "CANARY_DATABASE"
    COOKIE = "COOKIE"
    COOKIE_KEY = "COOKIE_KEY"
    HEADER = "HEADER"
    HEADER_KEY = "HEADER_KEY"
    HEADER_MAP = "HEADER_MAP"
    JMS_MESSAGE = "JMS_MESSAGE"
    JWS_MESSAGE = "JWS_MESSAGE"
    MATRIX_PARAMETER = "MATRIX_PARAMETER"
    MULTIPART = "MULTIPART"
    MULTIPART_CONTENT_DATA = "MULTIPART_CONTENT_DATA"
    MULTIPART_FILE_NAME = "MULTIPART_FILE_NAME"
    MULTIPART_FORM_DATA = "MULTIPART_FORM_DATA"
    MULTIPART_HEADER = "MULTIPART_HEADER"
    MULTIPART_HEADER_KEY = "MULTIPART_HEADER_KEY"
    MULTIPART_PARAMETER = "MULTIPART_PARAMETER"
    MULTIPART_PARAMETER_KEY = "MULTIPART_PARAMETER_KEY"
    MULTIPART_PART_NAME = "MULTIPART_PART_NAME"
    OTHER = "OTHER"
    PARAMETER = "PARAMETER"
    PARAMETER_KEY = "PARAMETER_KEY"
    PATH_PARAMETER = "PATH_PARAMETER"
    QUERYSTRING = "QUERYSTRING"
    RABBITMQ_MESSAGE = "RABBITMQ_MESSAGE"
    RMI_MESSAGE = "RMI_MESSAGE"
    RPC_MESSAGE = "RPC_MESSAGE"
    SERVER_VARIABLE = "SERVER_VARIABLE"
    SESSION_ID = "SESSION_ID"
    SOCKET = "SOCKET"
    TAINTED_DATABASE = "TAINTED_DATABASE"
    URI = "URI"
    WEBSERVICE_BODY = "WEBSERVICE_BODY"
    WEBSERVICE_HEADER = "WEBSERVICE_HEADER"
    WEBSOCKET = "WEBSOCKET"


@dataclass(frozen=True)
class AssessEventSource:
    source_name: str
    source_type: SourceType


class AssessEventAction(StrEnum):
    CREATION = "CREATION"
    A2O = "A2O"
    A2P = "A2P"
    A2A = "A2A"
    A2R = "A2R"
    O2A = "O2A"
    O2O = "O2O"
    O2P = "O2P"
    O2R = "O2R"
    P2A = "P2A"
    P2O = "P2O"
    P2P = "P2P"
    P2R = "P2R"
    TAG = "TAG"
    TRIGGER = "TRIGGER"


@dataclass(frozen=True)
class AssessParentObject:
    id: int


@dataclass(frozen=True)
class AssessObject:
    tracked: bool
    value: str
    hash: int = 0


@dataclass(frozen=True)
class AssessEvent:
    action: AssessEventAction
    args: List[AssessObject]
    event_sources: List[AssessEventSource]
    object: AssessObject
    parent_object_ids: List[AssessParentObject]
    ret: AssessObject
    signature: AssessSignature
    stack: List[AssessStackFrame]
    taint_ranges: List[AssessTaintRange]
    type: AssessEventType
    # properties is a required field in the Rust struct but in the
    # python agent we don't use it
    properties: List[AssessEventProperty] = field(default_factory=list)
    code: Optional[str] = None
    context: Optional[str] = None
    field_name: Optional[str] = None
    object_id: Optional[int] = None
    source: Optional[str] = None
    summary: Optional[bool] = None
    tags: Optional[str] = None
    target: Optional[str] = None
    thread: Optional[str] = None
    time: Optional[int] = None


class HttpVersion(StrEnum):
    Http0_9 = "0.9"
    Http1_0 = "1.0"
    Http1_1 = "1.1"
    Http2_0 = "2.0"
    Http3_0 = "3.0"


@dataclass(frozen=True)
class AssessRequest:
    headers: Dict[str, List[str]]
    method: str
    parameters: Dict[str, List[str]]
    uri: str
    body: Optional[str] = None
    port: Optional[int] = None
    protocol: Optional[str] = None
    query_string: Optional[str] = None
    standard_normalized_uri: Optional[str] = None
    version: Optional[HttpVersion] = None
    context_path: Optional[str] = None
    server_version_info: Optional[str] = None


@dataclass(frozen=True)
class AssessRouteObservation:
    verb: str
    url: str


@dataclass(frozen=True)
class AssessRoute:
    signature: str
    observations: List[AssessRouteObservation]
    count: int


@dataclass(frozen=True, repr=False)
class AssessFinding:
    version: int
    events: List[AssessEvent]
    rule_id: str
    routes: List[AssessRoute]
    hash: int
    properties: Optional[Dict[str, str]] = None
    request: Optional[AssessRequest] = None
    evidence: Optional[str] = None
    tags: Optional[str] = None
    created: Optional[int] = None

    def _to_json_bytes(self) -> bytes:
        return json.dumps(asdict(self)).encode("utf-8")


def new_finding(app_id: int, finding: AssessFinding) -> BindingApiSuccess[None]:
    """
    This function reports a new Assess finding/trace. Findings with duplicate hashes
    will be ignored between sends to TeamServer. Duplicate findings that do
    not pass TeamServer Preflight check will also be dropped.
    Sensitive data in the finding will be masked according to your configuration
    and set feature flags.
    """
    finding_bytes = finding._to_json_bytes()
    messages = c_uint()

    ret = libfireball_c.new_finding(
        API_VERSION,
        JSON_FORMAT,
        app_id,
        finding_bytes,
        len(finding_bytes),
        byref(messages),
    )

    assert_ok(ret)

    return BindingApiSuccess(messages=AgentMessages(messages.value), data=None)


libfireball_c.new_finding.argtypes = [
    c_uint32,  # version
    c_uint32,  # format
    c_uint,  # app_id
    c_char_p,  # finding_buf
    c_uint,  # finding_buf_len
    POINTER(c_uint),  # messages
]
libfireball_c.new_finding.restype = c_int


@dataclass(frozen=True)
class DiscoveredRoute:
    """
    Describes a route handler registered by the application.

    This is similar to an ObservedRoute, but adds a field for
    reporting the application framework (since route discovery
    requires framework support) and makes the URL optional
    (since there isn't a concrete request being observed and
    the route may be registered for a general URL pattern).
    """

    framework: str
    """
    The application framework that registered the route handler.
    """

    signature: str
    """
    The signature of the route handler.
    """

    url: Optional[str]
    """
    The concrete, normalized URL of the request that matches
    this route.
    """

    verb: Optional[str]
    """
    The HTTP verb used by the route handler.

    If None, the route handler is assumed to handle all verbs.
    """


def new_discovered_routes(
    app_id: int, routes: List[DiscoveredRoute]
) -> BindingApiSuccess[None]:
    """
    Report discovered routes.

    If an exception is raised, then no routes are reported.
    """
    discovered_routes_bytes = json.dumps([asdict(route) for route in routes]).encode(
        "utf-8"
    )
    messages = c_uint()

    return_status: int = libfireball_c.new_discovered_routes(
        API_VERSION,
        JSON_FORMAT,
        app_id,
        discovered_routes_bytes,
        len(discovered_routes_bytes),
        byref(messages),
    )

    assert_ok(return_status)
    return BindingApiSuccess(messages=AgentMessages(messages.value), data=None)


libfireball_c.new_discovered_routes.argtypes = [
    c_uint32,  # version
    c_uint32,  # format
    c_uint,  # app_id
    c_char_p,  # routes_buf
    c_uint,  # routes_buf_len
    POINTER(c_uint),  # messages
]
libfireball_c.new_discovered_routes.restype = c_int


@dataclass(frozen=True)
class RouteSource:
    """
    A dataflow source event observed within a route handler.
    """

    type: SourceType
    name: Optional[str] = None


@dataclass(frozen=True)
class ObservedRoute:
    signature: str
    """
    The signature of the route that handled the current request.
    """

    verb: Optional[str]
    """
    The HTTP verb of the current request.
    """

    url: str
    """
    The concrete, normalized URL of the current request.
    """

    sources: List[RouteSource]
    """
    The Assess sources retrieved while processing the current request.
    """

    def _to_json_bytes(self) -> bytes:
        return json.dumps(asdict(self)).encode("utf-8")


def new_observed_route(app_id: int, route: ObservedRoute) -> BindingApiSuccess[None]:
    """
    Record an observed route.

    Routes are reported periodically in batches. This endpoint can be called multiple
    times for the same route, but Fireball will only report duplicate routes at a rate
    of once per minute to avoid overloading TeamServer. The caller can implement this
    same throttling on its side to improve performance and avoid sending duplicate
    routes to Fireball.
    """
    observed_route_bytes = route._to_json_bytes()
    messages = c_uint()

    return_status: int = libfireball_c.new_observed_route(
        API_VERSION,
        JSON_FORMAT,
        app_id,
        observed_route_bytes,
        len(observed_route_bytes),
        byref(messages),
    )

    assert_ok(return_status)
    return BindingApiSuccess(messages=AgentMessages(messages.value), data=None)


libfireball_c.new_observed_route.argtypes = [
    c_uint32,  # version
    c_uint32,  # format
    c_uint,  # app_id
    c_char_p,  # observed_route_buf
    c_uint,  # observed_route_buf_len
    POINTER(c_uint),  # messages
]
libfireball_c.new_observed_route.restype = c_int


class InventoryComponent:
    """
    Base class for components to send in `new_inventory_components`. There should be no
    need to instantiate this directly.

    This class and its subclass heirarchy is an attempt to python-ify fireball's
    `InventoryComponent` enum. This enum is slightly more complicated than others
    because its variants are a variety of types. It looks more like a Union, but to
    capture common serialization behavior we've decided to use inheritance instead.
    """

    def _to_c_api_dict(self) -> dict:
        """
        Create a dictionary representation of this inventory component that conforms
        to fireball's C bindings API.
        """
        return {"c": self._as_json_serializable(), "type": self.__class__.__name__}

    def _as_json_serializable(self) -> Any:
        """
        Create a python representation of this inventory component's data that can be
        serialized with json.dumps(). By default does not perform any conversion;
        override this method in child classes for custom behavior.
        """
        return self


class AppActivityComponentType(StrEnum):
    DB = "db"
    LDAP = "ldap"
    WS = "ws"


@dataclass(frozen=True)
class ArchitectureComponent(InventoryComponent):
    type: AppActivityComponentType
    url: str
    vendor: Optional[str] = None
    remote_host: Optional[str] = None
    remote_port: Optional[str] = None

    def _as_json_serializable(self) -> Any:
        """
        Overrides this function on the base class; dataclasses are not directly json-
        serializable, so we use `dataclasses.asdict` here.
        """
        return asdict(self)


class Browser(InventoryComponent, str):
    pass


class Technology(InventoryComponent, str):
    pass


class Url(InventoryComponent, str):
    pass


class UrlCount(InventoryComponent, int):
    pass


class HttpCallCount(InventoryComponent, int):
    pass


class QueryCount(InventoryComponent, int):
    pass


def new_inventory_components(
    app_id: int, components: List[InventoryComponent]
) -> BindingApiSuccess[None]:
    """
    Record a new inventory component observed by the application.

    Components include:
    * Browser (user agent)
    * Technology (such as platform, framework or runtime)
    * Web service component
    * Database component
    * Ldap component
    * Request count (this will be additive)

    These components will be batched and sent to TeamServer at the app_activity
    interval. Duplicate items between sends will be ignored. The agent may call this api
    at the end of every request, or do some local batching itself and report it at the
    app_activity interval.
    """
    components_bytes = json.dumps(
        [component._to_c_api_dict() for component in components]
    ).encode("utf-8")
    messages = c_uint()

    return_status: int = libfireball_c.new_inventory_components(
        API_VERSION,
        JSON_FORMAT,
        app_id,
        components_bytes,
        len(components_bytes),
        byref(messages),
    )

    assert_ok(return_status)
    return BindingApiSuccess(messages=AgentMessages(messages.value), data=None)


libfireball_c.new_inventory_components.argtypes = [
    c_uint32,  # version
    c_uint32,  # format
    c_uint,  # app_id
    c_char_p,  # components_buf
    c_uint,  # components_buf_len
    POINTER(c_uint),  # messages
]
libfireball_c.new_inventory_components.restype = c_int


def assert_ok(return_status: int) -> None:
    """
    Assert that a call to a fireball C API function was successful, and raise
    an Error if it was not.

    Errors are translated into different exception types based on the return code.

    The Error will contain the error message and stack trace from the last error
    that occurred in the fireball C API.
    """
    if return_status == 0:
        return

    Exc = RETURN_CODES_TO_EXCEPTIONS.get(return_status, UnexpectedError)

    error_message_length = libfireball_c.last_error_message_length()
    error_message = create_string_buffer(error_message_length)

    error_stack_length = libfireball_c.last_error_stack_length()
    error_stack = create_string_buffer(error_stack_length)

    last_error_message_return_status = libfireball_c.last_error_message(
        error_message, error_message_length, error_stack, error_stack_length
    )
    # Make sure not to recursively call assert_ok because it could
    # cause infinite recursion.
    if last_error_message_return_status < 0:
        raise UnexpectedError(
            "An error occurred, but the error message could not be retrieved. "
            "See the reporter logs for more information.",
            stack="",
        )

    raise Exc(error_message.value.decode(), error_stack.value.decode())


@dataclass
class Error(Exception):
    """
    An error that occurred in the fireball C API.
    """

    message: str
    stack: str


class Panic(Error):
    """
    There was an unhandled panic in the fireball code.

    This should never happen and should be considered a bug.
    """

    ...


class ArgumentValidationError(Error):
    """
    Indicates invalid arguments were passed to the api call.

    This could be improper formatting, non-existen app_id, bad serialization,
    or missing required fields.  This error indicates an agent bug.
    """

    ...


class AppArchivedError(Error):
    """
    Indicates that the application has been archived on TeamServer.

    The agent should stop reporting data for this application, or re-initialize
    it if it thinks it has been unarchived.
    """

    ...


class AuthenticationError(Error):
    """
    The TeamServer authentication credentials are wrong or expired.

    The agent shoulds stop reporting data until the credentials are updated.
    """

    ...


class TeamServerError(Error):
    """
    An unhandled error from TeamServer.

    It should not normally occur. This error indicate a broken connection to
    the server and some other invalid state. Read the details for more information.
    """

    ...


class ConfigurationError(Error):
    """
    Indicates a configuration error in the Contrast agent.

    This could be a missing configuration file, a bad configuration file,
    or a configuration file that is not readable.
    """

    ...


class UnexpectedError(Error):
    """
    Any other unexpected error in the Fireball client, such as when parsing responses
    or configuration.

    This should never happen and may indicate a bug.
    """

    ...


RETURN_CODES_TO_EXCEPTIONS: Dict[int, Type[Error]] = {
    1: Panic,
    2: ArgumentValidationError,
    3: AppArchivedError,
    4: AuthenticationError,
    5: TeamServerError,
    6: ConfigurationError,
    7: UnexpectedError,
}

libfireball_c.last_error_message.argtypes = [
    POINTER(c_char),  # message_buffer
    c_int,  # message_length
    POINTER(c_char),  # stack_buffer
    c_int,  # stack_length
]
libfireball_c.last_error_message.restype = c_int

libfireball_c.last_error_message_length.argtypes = []
libfireball_c.last_error_message_length.restype = c_int

libfireball_c.last_error_stack_length.argtypes = []
libfireball_c.last_error_stack_length.restype = c_int
