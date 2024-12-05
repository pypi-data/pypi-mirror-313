"""
Encapsulates properties an agent tool
"""
from typing import Optional
from pydantic import BaseModel, Field

class AgentTool(BaseModel):
    """
    Encapsulates properties for an agent tool.
    """
    name: str = Field(..., description="The name of the agent tool.")
    description: str = Field(..., description="The description of the agent tool.")
    package_name: str = Field(..., description="The package name of the agent tool. For internal tools, this value will be FoundationaLLM. For external tools, this value will be the name of the package.")
    ai_model_object_ids: Optional[dict] = Field(default=[], description="A dictionary object identifiers of the AIModel objects for the agent tool.")
    api_endpoint_configuration_object_ids: Optional[dict] = Field(default=[], description="A dictionary object identifiers of the APIEndpointConfiguration objects for the agent tool.")
    properties: Optional[dict] = Field(default=[], description="A dictionary of properties for the agent tool.")
