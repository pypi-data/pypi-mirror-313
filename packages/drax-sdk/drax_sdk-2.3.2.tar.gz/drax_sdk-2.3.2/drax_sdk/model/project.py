from typing import Optional

from pydantic import BaseModel, Field


class Project(BaseModel):
    id: Optional[str] = Field(default=None)
    name: str
    api_key: Optional[str] = Field(alias="apiKey", default=None)
    api_secret: Optional[str] = Field(alias="apiSecret", default=None)

    def get_state_request_topic(self):
        return f"{self.id}/requests/states"

    def get_configuration_request_topic(self):
        return f"{self.id}/requests/configurations"

    class Config:
        populate_by_name = True
