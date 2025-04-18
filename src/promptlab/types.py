from dataclasses import dataclass
from typing import List, Optional

from pydantic import BaseModel, field_validator

from promptlab.enums import TracerType
from promptlab.evaluator.evaluator import Evaluator
from promptlab.model.model import EmbeddingModel, Model
from promptlab.utils import Utils

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

    model_config = {
        "arbitrary_types_allowed": True
    }
    
class AssetConfig(BaseModel):

    name: str
    version: int

class ExperimentConfig(BaseModel):

    inference_model: Model
    embedding_model: EmbeddingModel
    prompt_template: PromptTemplate
    dataset: Dataset
    evaluation: List[EvaluationConfig]

    model_config = {
        "arbitrary_types_allowed": True
    }
    
class TracerConfig(BaseModel):

    type: TracerType  
    db_file: str

    @field_validator('db_file')
    def validate_db_server(cls, value):             
        return Utils.sanitize_path(value)
    
    class Config:
        use_enum_values = True 