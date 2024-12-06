from enum import Enum
from pydantic import BaseModel


class ComponentType(Enum):
    MODULE = "Module"
    PROJECT = "Project"


class ApiType(Enum):
    REST = "REST"
    GRAPHQL = "GraphQL"


class BaseGeneratorServiceOptions(BaseModel):
    component_type: ComponentType
    api_type: ApiType
    name: str   
    
    
class ProjectGeneratorServiceOptions(BaseModel):
    generate_venv: bool
    

class ModuleGeneratorServiceOptions(BaseModel):
    pass


class GeneratorServiceOptions(BaseModel):
    base: BaseGeneratorServiceOptions
    project: ProjectGeneratorServiceOptions | None = None
    module: ModuleGeneratorServiceOptions | None = None
    