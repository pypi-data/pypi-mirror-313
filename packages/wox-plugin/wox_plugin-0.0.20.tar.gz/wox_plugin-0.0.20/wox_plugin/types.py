from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional, Protocol, Union, Callable, Any, TypedDict, Literal
import uuid

# Basic types
MapString = Dict[str, str]
Platform = Literal["windows", "darwin", "linux"]

# Context
class Context(TypedDict):
    Values: Dict[str, str]

    # get traceId from context
    def get_trace_id(self) -> str:
        return self["Values"]["traceId"]

def new_context() -> Context:
    return {"Values": {"traceId": str(uuid.uuid4())}}

def new_context_with_value(key: str, value: str) -> Context:
    ctx = new_context()
    ctx["Values"][key] = value
    return ctx

# Selection
class SelectionType(str, Enum):
    TEXT = "text"
    FILE = "file"

@dataclass
class Selection:
    Type: SelectionType
    Text: Optional[str] = None
    FilePaths: Optional[List[str]] = None

# Query Environment
@dataclass
class QueryEnv:
    """
    Active window title when user query
    """
    ActiveWindowTitle: str
    
    """
    Active window pid when user query, 0 if not available
    """
    ActiveWindowPid: int

    """
    active browser url when user query
    Only available when active window is browser and https://github.com/Wox-launcher/Wox.Chrome.Extension is installed
    """
    ActiveBrowserUrl: str

# Query
class QueryType(str, Enum):
    INPUT = "input"
    SELECTION = "selection"

@dataclass
class Query:
    Type: QueryType
    RawQuery: str
    TriggerKeyword: Optional[str]
    Command: Optional[str]
    Search: str
    Selection: Selection
    Env: QueryEnv

    def is_global_query(self) -> bool:
        return self.Type == QueryType.INPUT and not self.TriggerKeyword

# Result
class WoxImageType(str, Enum):
    ABSOLUTE = "absolute"
    RELATIVE = "relative"
    BASE64 = "base64"
    SVG = "svg"
    URL = "url"
    EMOJI = "emoji"
    LOTTIE = "lottie"

@dataclass
class WoxImage:
    ImageType: WoxImageType
    ImageData: str

def new_base64_wox_image(image_data: str) -> WoxImage:
    return WoxImage(ImageType=WoxImageType.BASE64, ImageData=image_data)

class WoxPreviewType(str, Enum):
    MARKDOWN = "markdown"
    TEXT = "text"
    IMAGE = "image"
    URL = "url"
    FILE = "file"

@dataclass
class WoxPreview:
    PreviewType: WoxPreviewType
    PreviewData: str
    PreviewProperties: Dict[str, str]

class ResultTailType(str, Enum):
    TEXT = "text"
    IMAGE = "image"

@dataclass
class ResultTail:
    Type: ResultTailType
    Text: Optional[str] = None
    Image: Optional[WoxImage] = None

@dataclass
class ActionContext:
    ContextData: str

@dataclass
class ResultAction:
    Id: Optional[str] = None
    Name: str
    Icon: Optional[WoxImage] = None
    IsDefault: Optional[bool] = None
    PreventHideAfterAction: Optional[bool] = None
    Action: Callable[[ActionContext], None]
    Hotkey: Optional[str] = None

@dataclass
class Result:
    Title: str
    Icon: WoxImage
    Id: Optional[str] = None
    SubTitle: Optional[str] = None
    Preview: Optional[WoxPreview] = None
    Score: Optional[float] = None
    Group: Optional[str] = None
    GroupScore: Optional[float] = None
    Tails: Optional[List[ResultTail]] = None
    ContextData: Optional[str] = None
    Actions: Optional[List[ResultAction]] = None
    RefreshInterval: Optional[int] = None
    OnRefresh: Optional[Callable[["RefreshableResult"], "RefreshableResult"]] = None

@dataclass
class RefreshableResult:
    Title: str
    SubTitle: str
    Icon: WoxImage
    Preview: WoxPreview
    Tails: List[ResultTail]
    ContextData: str
    RefreshInterval: int
    Actions: List[ResultAction]

# Plugin API
@dataclass
class ChangeQueryParam:
    QueryType: QueryType
    QueryText: Optional[str] = None
    QuerySelection: Optional[Selection] = None

# AI
class ConversationRole(str, Enum):
    USER = "user"
    SYSTEM = "system"

class ChatStreamDataType(str, Enum):
    STREAMING = "streaming"
    FINISHED = "finished"
    ERROR = "error"

@dataclass
class Conversation:
    Role: ConversationRole
    Text: str
    Timestamp: int

ChatStreamFunc = Callable[[ChatStreamDataType, str], None]

# Settings
class PluginSettingDefinitionType(str, Enum):
    HEAD = "head"
    TEXTBOX = "textbox"
    CHECKBOX = "checkbox"
    SELECT = "select"
    LABEL = "label"
    NEWLINE = "newline"
    TABLE = "table"
    DYNAMIC = "dynamic"

@dataclass
class PluginSettingValueStyle:
    PaddingLeft: int
    PaddingTop: int
    PaddingRight: int
    PaddingBottom: int
    Width: int
    LabelWidth: int

@dataclass
class PluginSettingDefinitionValue:
    def get_key(self) -> str:
        raise NotImplementedError

    def get_default_value(self) -> str:
        raise NotImplementedError

    def translate(self, translator: Callable[[Context, str], str]) -> None:
        raise NotImplementedError

@dataclass
class PluginSettingDefinitionItem:
    Type: PluginSettingDefinitionType
    Value: PluginSettingDefinitionValue
    DisabledInPlatforms: List[Platform]
    IsPlatformSpecific: bool

@dataclass
class MetadataCommand:
    Command: str
    Description: str

# Plugin Interface
class Plugin(Protocol):
    async def init(self, ctx: Context, init_params: "PluginInitParams") -> None:
        ...

    async def query(self, ctx: Context, query: Query) -> List[Result]:
        ...

# Public API Interface
class PublicAPI(Protocol):
    async def change_query(self, ctx: Context, query: ChangeQueryParam) -> None:
        ...

    async def hide_app(self, ctx: Context) -> None:
        ...

    async def show_app(self, ctx: Context) -> None:
        ...

    async def notify(self, ctx: Context, message: str) -> None:
        ...

    async def log(self, ctx: Context, level: str, msg: str) -> None:
        ...

    async def get_translation(self, ctx: Context, key: str) -> str:
        ...

    async def get_setting(self, ctx: Context, key: str) -> str:
        ...

    async def save_setting(self, ctx: Context, key: str, value: str, is_platform_specific: bool) -> None:
        ...

    async def on_setting_changed(self, ctx: Context, callback: Callable[[str, str], None]) -> None:
        ...

    async def on_get_dynamic_setting(self, ctx: Context, callback: Callable[[str], PluginSettingDefinitionItem]) -> None:
        ...

    async def on_deep_link(self, ctx: Context, callback: Callable[[MapString], None]) -> None:
        ...

    async def on_unload(self, ctx: Context, callback: Callable[[], None]) -> None:
        ...

    async def register_query_commands(self, ctx: Context, commands: List[MetadataCommand]) -> None:
        ...

    async def llm_stream(self, ctx: Context, conversations: List[Conversation], callback: ChatStreamFunc) -> None:
        ...

@dataclass
class PluginInitParams:
    API: PublicAPI
    PluginDirectory: str 