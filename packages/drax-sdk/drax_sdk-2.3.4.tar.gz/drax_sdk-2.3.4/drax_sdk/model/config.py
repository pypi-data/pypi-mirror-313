import os
from typing import Optional

from pydantic import BaseModel


class DraxConfigParams(BaseModel):
    project_id: Optional[str] = None
    api_key: str
    api_secret: str
    drax_core_url: str
    automation_url: str
    broker_port: int
    broker_host: str
    broker_vhost: str
    data_miner_url: str

    @classmethod
    def load_from_env(cls):
        return cls(
            project_id=os.getenv("DRAX_PROJECT_ID"),
            api_key=os.getenv("DRAX_PROJECT_API_KEY", "guest"),
            api_secret=os.getenv("DRAX_PROJECT__API_SECRET", "guest"),
            drax_core_url=os.getenv("DRAX_CORE_URL", "https://drax.network/core"),
            automation_url=os.getenv(
                "DRAX_AUTOMATION_URL", "https://drax.network/automation"
            ),
            broker_port=int(os.getenv("DRAX_BROKER_PORT", 5672)),
            broker_host=os.getenv("DRAX_BROKER_HOST", "35.205.187.28"),
            broker_vhost=os.getenv("DRAX_BROKER_VHOST", "/"),
            data_miner_url=os.getenv(
                "DRAX_DATA_MINER_URL", "https://drax.network/data-miner"
            ),
        )

    @classmethod
    def standard(cls, project_id: str, api_key: str, api_secret: str):
        return cls(
            project_id=project_id,
            api_key=api_key,
            api_secret=api_secret,
            drax_core_url="https://drax.network/core",
            automation_url="https://drax.network/automation",
            data_miner_url="https://drax.network/data-miner",
            broker_host="broker.drax.network",
            broker_port=5672,
            broker_vhost="/",
        )
