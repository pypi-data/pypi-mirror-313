# ruff: noqa: UP006
import typing
from datetime import datetime
from enum import IntEnum

from pydantic import BaseModel, Field

# TODO: The models from this file are generated from private protos
# Here we just duplicate the models, but we should migrate the private
# protos to this repository to make them public


###
#    learning_protos/config_p2p.py
###
class SimilarityFunction(IntEnum):
    DOT = 0
    COSINE = 1


class ResponseStatus(IntEnum):
    OK = 0
    ERROR = 1
    VALIDATION_ERROR = 2
    NOT_FOUND = 3


class ModelType(IntEnum):
    GENERATIVE = 0
    NER = 1
    RESOURCE_LABELER = 2
    CLASSIFIER = 3
    ANONYMIZER = 4
    VISUAL_LABELER = 5
    SUMMARY = 6
    DUMMY = 7
    PARAGRAPH_LABELER = 8
    EMBEDDINGS = 9
    RELATIONS = 10


class OpenAIKey(BaseModel):
    key: str = Field(default="")
    org: str = Field(default="")


class AzureOpenAIKey(BaseModel):
    key: str = Field(default="")
    url: str = Field(default="")
    deployment: str = Field(default="")
    model: str = Field(default="")


class HFLLMKey(BaseModel):
    class ModelType(IntEnum):
        LLAMA31 = 0
        QWEN25 = 1

    key: str = Field(default="")
    url: str = Field(default="")
    model: "HFLLMKey.ModelType" = Field(default=ModelType.LLAMA31)


class AzureMistralKey(BaseModel):
    key: str = Field(default="")
    url: str = Field(default="")


class PalmKey(BaseModel):
    credentials: str = Field(default="")
    location: str = Field(default="")


class MistralKey(BaseModel):
    key: str = Field(default="")


class AnthropicKey(BaseModel):
    key: str = Field(default="")


class TextGenerationKey(BaseModel):
    model: str = Field(default="")


class HFEmbeddingKey(BaseModel):
    url: str = Field(default="")
    key: str = Field(default="")
    matryoshka: typing.List[int] = Field(default_factory=list)
    similarity: str = Field(default="")
    size: int = Field(default=0)
    threshold: float = Field(default=0.0)
    passage_prompt: str = Field(default="")
    query_prompt: str = Field(default="")


class UserLearningKeys(BaseModel):
    openai: typing.Optional[OpenAIKey] = Field(default=None)
    azure_openai: typing.Optional[AzureOpenAIKey] = Field(default=None)
    palm: typing.Optional[PalmKey] = Field(default=None)
    anthropic: typing.Optional[AnthropicKey] = Field(default=None)
    claude3: typing.Optional[AnthropicKey] = Field(default=None)
    text_generation: typing.Optional[TextGenerationKey] = Field(default=None)
    mistral: typing.Optional[MistralKey] = Field(default=None)
    azure_mistral: typing.Optional[AzureMistralKey] = Field(default=None)
    hf_llm: typing.Optional[HFLLMKey] = Field(default=None)
    hf_embedding: typing.Optional[HFEmbeddingKey] = Field(default=None)


class OpenAIUserPrompt(BaseModel):
    system: str = Field(default="")
    prompt: str = Field(default="")


class AzureUserPrompt(BaseModel):
    system: str = Field(default="")
    prompt: str = Field(default="")


class HFUserPrompt(BaseModel):
    system: str = Field(default="")
    prompt: str = Field(default="")


class PalmUserPrompt(BaseModel):
    prompt: str = Field(default="")


class AnthropicUserPrompt(BaseModel):
    prompt: str = Field(default="")


class Claude3UserPrompt(BaseModel):
    system: str = Field(default="")
    prompt: str = Field(default="")


class TextGenerationUserPrompt(BaseModel):
    prompt: str = Field(default="")


class MistralUserPrompt(BaseModel):
    prompt: str = Field(default="")


class AzureMistralUserPrompt(BaseModel):
    prompt: str = Field(default="")


class SummaryPrompt(BaseModel):
    prompt: str = Field(default="")


class UserPrompts(BaseModel):
    openai: typing.Optional[OpenAIUserPrompt] = Field(default=None)
    azure_openai: typing.Optional[AzureUserPrompt] = Field(default=None)
    palm: typing.Optional[PalmUserPrompt] = Field(default=None)
    anthropic: typing.Optional[AnthropicUserPrompt] = Field(default=None)
    text_generation: typing.Optional[TextGenerationUserPrompt] = Field(default=None)
    mistral: typing.Optional[MistralUserPrompt] = Field(default=None)
    azure_mistral: typing.Optional[AzureMistralUserPrompt] = Field(default=None)
    claude3: typing.Optional[Claude3UserPrompt] = Field(default=None)


class SemanticConfig(BaseModel):
    similarity: SimilarityFunction = Field(default=SimilarityFunction.DOT)
    size: int = Field(default=0)
    threshold: float = Field(default=0.0)
    max_tokens: int = Field(default=0)
    matryoshka_dims: typing.List[int] = Field(default_factory=list)
    external: bool = Field(default=False)


class LearningConfiguration(BaseModel):
    semantic_model: str = Field(default="")
    anonymization_model: str = Field(default="")
    ner_model: str = Field(default="")
    visual_labeling: str = Field(default="")
    relation_model: str = Field(default="")
    summary: str = Field(default="")
    summary_model: str = Field(default="")
    summary_provider: str = Field(default="")
    summary_prompt_id: str = Field(default="")
    summary_prompt: SummaryPrompt = Field()
    user_keys: UserLearningKeys = Field()
    user_prompts: UserPrompts = Field()
    prefer_markdown_generative_response: bool = Field(default=False)
    semantic_models: typing.List[str] = Field(default_factory=list)
    semantic_model_configs: typing.Dict[str, SemanticConfig] = Field(default_factory=dict)
    default_semantic_model: str = Field(default="")
    generative_model: str = Field(default="")
    generative_provider: str = Field(default="")
    generative_prompt_id: str = Field(default="")


class AddKBConfigRequest(BaseModel):
    kbid: str = Field(default="")
    account: str = Field(default="")
    config: LearningConfiguration = Field()


class UpdateKBConfigRequest(BaseModel):
    kbid: str = Field(default="")
    config: LearningConfiguration = Field()


class UpdateKBConfigResponse(BaseModel):
    status: ResponseStatus = Field(default=ResponseStatus.OK)


class DeleteKBConfigRequest(BaseModel):
    kbid: str = Field(default="")


class DeleteKBConfigResponse(BaseModel):
    status: ResponseStatus = Field(default=ResponseStatus.OK)


class GetKBConfigRequest(BaseModel):
    kbid: str = Field(default="")


class GetExternalKBConfigRequest(BaseModel):
    account: str = Field(default="")
    kbid: str = Field(default="")


class GetKBConfigResponse(BaseModel):
    status: ResponseStatus = Field(default=ResponseStatus.OK)
    config: LearningConfiguration = Field()
    semantic_vector_similarity: str = Field(default="")
    semantic_vector_size: int = Field(default=0)
    semantic_threshold: float = Field(default=0.0)
    errors: typing.List[str] = Field(default_factory=list)
    semantic_matryoshka_dimensions: typing.List[int] = Field(default_factory=list)


class AddModelRequest(BaseModel):
    model_type: ModelType = Field(default=ModelType.GENERATIVE)
    trained_date: datetime = Field(default_factory=datetime.now)
    location: str = Field(default="")
    log: str = Field(default="")
    loss: float = Field(default=0.0)
    accuracy: float = Field(default=0.0)
    account: str = Field(default="")
    trained_kbid: str = Field(default="")
    model_uuid: str = Field(default="")
    trained_dataset: str = Field(default="")
    title: str = Field(default="")


class AddModelResponse(BaseModel):
    uuid: str = Field(default="")


class DeleteModelRequest(BaseModel):
    model_id: str = Field(default="")
    account_id: str = Field(default="")


class DeleteModelResponse(BaseModel):
    pass


class GetModelsRequest(BaseModel):
    kbid: str = Field(default="")


class GetExternalModelsRequest(BaseModel):
    kbid: str = Field(default="")
    account: str = Field(default="")


class Model(BaseModel):
    model_type: ModelType = Field(default=ModelType.GENERATIVE)
    trained_date: datetime = Field(default_factory=datetime.now)
    model_id: str = Field(default="")
    account: str = Field(default="")
    trained_kbid: str = Field(default="")
    trained_dataset: str = Field(default="")
    title: str = Field(default="")
    provider: str = Field(default="")
    prompt_id: str = Field(default="")
    kbids: typing.List[str] = Field(default_factory=list)


class GetModelsResponse(BaseModel):
    models: typing.List[Model] = Field(default_factory=list)


class SetAvailableModelsRequest(BaseModel):
    kbid: str = Field(default="")
    models: typing.List[str] = Field(default_factory=list)


class SetAvailableModelsResponse(BaseModel):
    pass


class GetModelRequest(BaseModel):
    model_id: str = Field(default="")


class GetAccountModelsRequest(BaseModel):
    account: str = Field(default="")
    client_id: str = Field(default="")


class GetModelResponse(BaseModel):
    model_type: ModelType = Field(default=ModelType.GENERATIVE)
    trained_date: datetime = Field(default_factory=datetime.now)
    location: str = Field(default="")
    log: str = Field(default="")
    loss: float = Field(default=0.0)
    accuracy: float = Field(default=0.0)
    account: str = Field(default="")
    trained_kbid: str = Field(default="")
    model_id: str = Field(default="")
    kbids: typing.List[str] = Field(default_factory=list)


class DeleteTrainedModelsOfAccountRequest(BaseModel):
    account: str = Field(default="")


class DeleteTrainedModelsOfAccountResponse(BaseModel):
    class Status(IntEnum):
        OK = 0
        ERROR = 1

    status: "DeleteTrainedModelsOfAccountResponse.Status" = Field(default=Status.OK)


###
#    learning_protos/data_augmentation_p2p.py
###
class ApplyTo(IntEnum):
    TEXT_BLOCK = 0
    FIELD = 1


class KBConfiguration(BaseModel):
    account: str = Field(default="")
    kbid: str = Field(default="")
    onprem: bool = Field(default=False)


class EntityDefinition(BaseModel):
    label: str = Field(default="")
    description: typing.Optional[str] = Field(default="")


class EntityExample(BaseModel):
    name: str = Field(default="")
    label: str = Field(default="")
    example: str = Field(default="")


class RelationExample(BaseModel):
    source: str = Field(default="")
    target: str = Field(default="")
    label: str = Field(default="")
    example: str = Field(default="")


class GraphOperation(BaseModel):
    entity_defs: typing.List[EntityDefinition] = Field(default_factory=list)
    entity_examples: typing.List[EntityExample] = Field(default_factory=list)
    relation_examples: typing.List[RelationExample] = Field(default_factory=list)
    ident: str = Field(default="")


class Label(BaseModel):
    label: str = Field(default="")
    description: str = Field(default="")
    examples: typing.List[str] = Field(default_factory=list)


class LabelOperation(BaseModel):
    labels: typing.List[Label] = Field(default_factory=list)
    ident: str = Field(default="")
    description: str = Field(default="")
    multiple: bool = Field(default=False)


class GuardOperation(BaseModel):
    enabled: bool = Field(default=False)


class AskOperation(BaseModel):
    question: str = Field(default="")
    destination: str = Field(default="")
    json: bool = Field(default=False)  # type: ignore


class QAOperation(BaseModel):
    question_generator_prompt: str = Field(default="")
    system_question_generator_prompt: str = Field(default="")
    summary_prompt: str = Field(default="")
    generate_answers_prompt: str = Field(default="")


class ExtractOperation(BaseModel):
    class Model(IntEnum):
        TABLES = 0

    model: "ExtractOperation.Model" = Field(default=Model.TABLES)


class Operation(BaseModel):
    graph: typing.Optional[GraphOperation] = Field(default=None)
    label: typing.Optional[LabelOperation] = Field(default=None)
    ask: typing.Optional[AskOperation] = Field(default=None)
    qa: typing.Optional[QAOperation] = Field(default=None)
    extract: typing.Optional[ExtractOperation] = Field(default=None)
    prompt_guard: typing.Optional[GuardOperation] = Field(default=None)
    llama_guard: typing.Optional[GuardOperation] = Field(default=None)


class Filter(BaseModel):
    contains: typing.List[str] = Field(default_factory=list)
    resource_type: typing.List[str] = Field(default_factory=list)
    field_types: typing.List[str] = Field(default_factory=list)
    not_field_types: typing.List[str] = Field(default_factory=list)
    rids: typing.List[str] = Field(default_factory=list)
    fields: typing.List[str] = Field(default_factory=list)
    splits: typing.List[str] = Field(default_factory=list)


class LLMConfig(BaseModel):
    model: str = Field(default="")
    provider: str = Field(default="")
    keys: typing.Optional[UserLearningKeys] = Field(default=None)
    prompts: typing.Optional[UserPrompts] = Field(default=None)


class DataAugmentation(BaseModel):
    name: str = Field(default="")
    on: ApplyTo = Field(default=ApplyTo.TEXT_BLOCK)
    filter: Filter = Field()
    operations: typing.List[Operation] = Field(default_factory=list)
    llm: LLMConfig = Field()


class DataAugmentations(BaseModel):
    class Status(IntEnum):
        FOUND = 0
        NOT_FOUND = 1

    data_augmentations: typing.List[DataAugmentation] = Field(default_factory=list)
    status: "DataAugmentations.Status" = Field(default=Status.FOUND)
