from openg2p_fastapi_common.config import Settings as BaseSettings
from pydantic_settings import SettingsConfigDict

from . import __version__


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="g2p_bridge_", env_file=".env", extra="allow"
    )

    openapi_title: str = "OpenG2P G2P Bridge API"
    openapi_description: str = """
        This module enables cash transfers from PBMS
        ***********************************
        Further details goes here
        ***********************************
        """
    openapi_version: str = __version__

    db_dbname: str = "openg2p_g2p_bridge_db"
