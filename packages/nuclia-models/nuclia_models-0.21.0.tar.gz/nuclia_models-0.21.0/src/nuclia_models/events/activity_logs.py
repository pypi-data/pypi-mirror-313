import re
from datetime import datetime
from enum import Enum
from typing import Annotated, Any, Generic, Literal, Optional, TypeVar

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator, model_validator
from pydantic.main import create_model

from nuclia_models.common.client import ClientType
from nuclia_models.common.pagination import Pagination
from nuclia_models.common.user import UserType
from nuclia_models.common.utils import CaseInsensitiveEnum

T = TypeVar("T")


class EventType(CaseInsensitiveEnum):
    # Nucliadb
    VISITED = "visited"
    MODIFIED = "modified"
    DELETED = "deleted"
    NEW = "new"
    SEARCH = "search"
    SUGGEST = "suggest"
    INDEXED = "indexed"
    CHAT = "chat"
    # Tasks
    STARTED = "started"
    STOPPED = "stopped"
    # Processor
    PROCESSED = "processed"


class BaseConfigModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class GenericFilter(BaseConfigModel, Generic[T]):
    eq: Optional[T] = None
    gt: Optional[T] = None
    ge: Optional[T] = None
    lt: Optional[T] = None
    le: Optional[T] = None
    ne: Optional[T] = None
    isnull: Optional[bool] = None


class StringFilter(GenericFilter[str]):
    like: Optional[str] = None
    ilike: Optional[str] = None


class AuditMetadata(StringFilter):
    key: str


class QueryFiltersCommon(BaseConfigModel):
    id: Optional[GenericFilter[int]] = None
    date: Optional[BaseConfigModel] = Field(None, serialization_alias="event_date")
    user_id: Optional[GenericFilter[str]] = None
    user_type: Optional[GenericFilter[UserType]] = None
    client_type: Optional[GenericFilter[ClientType]] = None
    total_duration: Optional[GenericFilter[float]] = None
    audit_metadata: Optional[list[AuditMetadata]] = Field(
        None, serialization_alias="data.user_request.audit_metadata"
    )
    resource_id: Optional[BaseConfigModel] = None


class QueryFiltersSearch(QueryFiltersCommon):
    question: Optional[StringFilter] = Field(None, serialization_alias="data.user_request.query")
    resources_count: Optional[StringFilter] = Field(
        None, serialization_alias="data.resources_count", json_schema_extra={"cast_to": "int"}
    )
    filter: Optional[BaseConfigModel] = Field(None, serialization_alias="data.request.filter")
    learning_id: Optional[BaseConfigModel] = Field(None, serialization_alias="data.request.learning_id")


class QueryFiltersChat(QueryFiltersSearch):
    rephrased_question: Optional[StringFilter] = Field(
        None, serialization_alias="data.request.rephrased_question"
    )
    answer: Optional[StringFilter] = Field(None, serialization_alias="data.request.answer")
    retrieved_context: Optional[BaseConfigModel] = Field(None, serialization_alias="data.request.context")
    chat_history: Optional[BaseConfigModel] = Field(None, serialization_alias="data.request.chat_context")
    feedback_good: Optional[GenericFilter[bool]] = Field(
        None,
        serialization_alias="data.feedback.good",
        json_schema_extra={"cast_to": "bool"},
        description="True if the feedback provided for the main question is positive.",
    )
    feedback_comment: Optional[StringFilter] = Field(
        None,
        serialization_alias="data.feedback.feedback",
        description="User-provided comment on the feedback for the question.",
    )
    feedback_good_all: Optional[GenericFilter[bool]] = Field(
        None,
        serialization_alias="data.feedback.all",
        json_schema_extra={"cast_to": "bool"},
        description=(
            "True if all feedback, including that on the main question"
            " and each related text block, is positive."
        ),
    )
    feedback_good_any: Optional[GenericFilter[bool]] = Field(
        None,
        serialization_alias="data.feedback.any",
        json_schema_extra={"cast_to": "bool"},
        description=(
            "True if there is any positive feedback" " on the question itself or any related text block."
        ),
    )
    feedback: Optional[BaseConfigModel] = Field(
        None,
        serialization_alias="data.feedback",
        description=(
            "Raw feedback data associated with the question or generative answer,"
            " including feedback on related text blocks."
        ),
    )
    model: Optional[StringFilter] = Field(None, serialization_alias="data.request.model")
    rag_strategies_names: Optional[BaseConfigModel] = Field(None, serialization_alias="data.rag_strategies")
    rag_strategies: Optional[BaseConfigModel] = Field(
        None, serialization_alias="data.user_request.rag_strategies"
    )
    status: Optional[GenericFilter[int]] = Field(
        None,
        serialization_alias="data.request.status_code",
        json_schema_extra={"cast_to": "int"},
    )
    time_to_first_char: Optional[BaseConfigModel] = Field(
        None,
        serialization_alias="data.generative_answer_first_chunk_time",
        json_schema_extra={"cast_to": "int"},
    )


def create_dynamic_model(name: str, base_model: type[QueryFiltersChat]) -> type[BaseModel]:
    field_definitions = {}
    field_type_map = {
        "id": int,
        "user_type": Optional[UserType],
        "client_type": Optional[ClientType],
        "total_duration": Optional[float],
        "time_to_first_char": Optional[float],
        "resources_count": Optional[int],
        "feedback_good": Optional[bool],
        "feedback": Optional[dict],
        "status": Optional[int],
        "rag_strategies": Optional[list],
        "rag_strategies_names": Optional[list],
        "chat_history": Optional[list],
        "retrieved_context": Optional[list],
    }
    for field_name in base_model.model_fields:
        field_type = field_type_map.get(field_name, Optional[str])

        field_definitions[field_name] = (field_type, Field(default=None))

    return create_model(name, **field_definitions)  # type: ignore


ActivityLogsQueryResponse = create_dynamic_model(
    name="ActivityLogsQueryResponse", base_model=QueryFiltersChat
)


class ActivityLogsQueryCommon(BaseConfigModel):
    year_month: str

    @field_validator("year_month")
    @classmethod
    def validate_year_month(cls, value: str) -> str:
        if not re.match(r"^\d{4}-(0[1-9]|1[0-2])$", value):
            msg = "year_month must be in the format YYYY-MM"
            raise ValueError(msg)
        return value

    @staticmethod
    def _validate_show(show: set[str], model: type[QueryFiltersCommon]) -> set[str]:
        allowed_fields = list(model.model_fields.keys())
        for field in show:
            if field.startswith("audit_metadata."):
                continue
            if field not in allowed_fields:
                msg = f"{field} is not a field. List of fields: {allowed_fields}"
                raise ValueError(msg)
        return show


SHOW_LITERAL = Literal[tuple(QueryFiltersCommon.model_fields.keys())]  # type: ignore
SHOW_SEARCH_LITERAL = Literal[tuple(QueryFiltersSearch.model_fields.keys())]  # type: ignore
SHOW_CHAT_LITERAL = Literal[tuple(QueryFiltersChat.model_fields.keys())]  # type: ignore
DEFAULT_SHOW_VALUES = {"id", "date"}
DEFAULT_SHOW_SEARCH_VALUES = DEFAULT_SHOW_VALUES | {"question", "resources_count"}
DEFAULT_SHOW_CHAT_VALUES = DEFAULT_SHOW_SEARCH_VALUES | {
    "rephrased_question",
    "answer",
    "rag_strategies_names",
}


class ActivityLogs(ActivityLogsQueryCommon):
    show: set[SHOW_LITERAL] = DEFAULT_SHOW_VALUES  # type: ignore
    filters: QueryFiltersCommon

    @field_validator("show")
    @classmethod
    def validate_show(cls, show: set[str]) -> set[str]:
        return cls._validate_show(show=show, model=QueryFiltersCommon)


class ActivityLogsSearch(ActivityLogsQueryCommon):
    show: set[SHOW_SEARCH_LITERAL] = DEFAULT_SHOW_SEARCH_VALUES  # type: ignore
    filters: QueryFiltersSearch

    @field_validator("show")
    @classmethod
    def validate_show(cls, show: set[str]) -> set[str]:
        return cls._validate_show(show=show, model=QueryFiltersSearch)


class ActivityLogsChat(ActivityLogsQueryCommon):
    show: set[SHOW_CHAT_LITERAL] = DEFAULT_SHOW_CHAT_VALUES  # type: ignore
    filters: QueryFiltersChat

    @field_validator("show")
    @classmethod
    def validate_show(cls, show: set[str]) -> set[str]:
        return cls._validate_show(show=show, model=QueryFiltersChat)


class PaginationMixin(BaseModel):
    pagination: Pagination = Pagination()

    @model_validator(mode="after")
    @classmethod
    def validate_pagination_and_filters(cls, values):  # type: ignore
        if values.pagination and values.filters and values.filters.id is not None:
            raise ValueError("Payload cannot have both 'pagination' and an 'id' in 'filters'.")  # noqa: TRY003, EM101
        return values


class ActivityLogsSearchQuery(ActivityLogsSearch, PaginationMixin):
    pass


class ActivityLogsChatQuery(ActivityLogsChat, PaginationMixin):
    pass


class ActivityLogsQuery(ActivityLogs, PaginationMixin):
    pass


class DownloadRequestType(str, Enum):
    QUERY = "query"


class DownloadFormat(str, Enum):
    NDJSON = "ndjson"
    CSV = "csv"


class DownloadRequest(BaseModel):
    id: Annotated[int, Field(exclude=True)]
    request_id: str
    download_type: DownloadRequestType
    download_format: DownloadFormat
    event_type: EventType
    requested_at: datetime
    user_id: Annotated[str, Field(exclude=True)]
    kb_id: str
    query: Annotated[dict[Any, Any], Field(exclude=True)]
    download_url: Optional[str]

    # Configuration for Pydantic v2 to handle ORM mapping
    class Config:
        from_attributes = True


class DownloadActivityLogsQueryMixin(BaseModel):
    email_address: Optional[EmailStr] = Field(default=None)
    notify_via_email: bool = Field(default=False)


class DownloadActivityLogsSearchQuery(DownloadActivityLogsQueryMixin, ActivityLogsSearch):
    pass


class DownloadActivityLogsChatQuery(DownloadActivityLogsQueryMixin, ActivityLogsChat):
    pass


class DownloadActivityLogsQuery(DownloadActivityLogsQueryMixin, ActivityLogs):
    pass
