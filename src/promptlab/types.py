from dataclasses import dataclass
from typing import List, Optional, Any, Protocol, runtime_checkable

from pydantic import BaseModel, field_validator

from promptlab.enums import TracerType
from promptlab.evaluator.evaluator import Evaluator
from promptlab.utils import Utils


@dataclass
class InferenceResult:
    inference: str
    prompt_tokens: int
    completion_tokens: int
    latency_ms: int


@dataclass
class ModelConfig:
    type: str
    api_key: Optional[str] = None
    api_version: Optional[str] = None
    endpoint: Optional[str] = None
    inference_model_deployment: Optional[str] = None
    embedding_model_deployment: Optional[str] = None
    max_concurrent_tasks: int = 5


@dataclass
class InferenceModelConfig:
    type: str
    inference_model_deployment: str
    api_key: Optional[str] = None
    api_version: Optional[str] = None
    endpoint: Optional[str] = None


@dataclass
class EmbeddingModelConfig:
    type: str
    embedding_model_deployment: str
    api_key: Optional[str] = None
    api_version: Optional[str] = None
    endpoint: Optional[str] = None


@runtime_checkable
class Model(Protocol):
    def invoke(self, system_prompt: str, user_prompt: str) -> InferenceResult: ...

    async def ainvoke(
        self, system_prompt: str, user_prompt: str
    ) -> InferenceResult: ...


@runtime_checkable
class EmbeddingModel(Protocol):
    def __call__(self, text: str) -> Any: ...


@dataclass
class Dataset:
    name: str
    description: str
    file_path: str
    version: int = 0


@dataclass
class PromptTemplate:
    name: str = None
    description: str = None
    system_prompt: str = None
    user_prompt: str = None
    version: int = 0


class EvaluationConfig(BaseModel):
    metric: str
    column_mapping: dict
    evaluator: Optional[Evaluator] = None

    model_config = {"arbitrary_types_allowed": True}


class AssetConfig(BaseModel):
    name: str
    version: int


class ExperimentConfig(BaseModel):
    inference_model: Model
    embedding_model: EmbeddingModel
    prompt_template: PromptTemplate
    dataset: Dataset
    evaluation: List[EvaluationConfig]

    model_config = {"arbitrary_types_allowed": True}


class TracerConfig(BaseModel):
    type: TracerType
    db_file: str

    @field_validator("db_file")
    def validate_db_server(cls, value):
        return Utils.sanitize_path(value)

    class Config:
        use_enum_values = True
