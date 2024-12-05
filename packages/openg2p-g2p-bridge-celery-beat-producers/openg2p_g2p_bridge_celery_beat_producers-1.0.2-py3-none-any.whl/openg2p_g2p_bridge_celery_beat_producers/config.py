from openg2p_fastapi_common.config import Settings as BaseSettings
from pydantic_settings import SettingsConfigDict

from . import __version__


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="g2p_bridge_celery_beat_", env_file=".env", extra="allow"
    )
    openapi_title: str = "OpenG2P G2P Bridge Celery Tasks"
    openapi_description: str = """
        Celery tasks for OpenG2P G2P Bridge API
        ***********************************
        Further details goes here
        ***********************************
        """
    openapi_version: str = __version__

    db_dbname: str = "openg2p_g2p_bridge_db"
    db_driver: str = "postgresql"

    celery_broker_url: str = "redis://localhost:6379/0"
    celery_backend_url: str = "redis://localhost:6379/0"

    mapper_resolve_attempts: int = 3
    funds_available_check_attempts: int = 3
    funds_blocked_attempts: int = 3
    funds_disbursement_attempts: int = 3
    statement_process_attempts: int = 3

    mapper_resolve_frequency: int = 3600
    funds_available_check_frequency: int = 3600
    funds_blocked_frequency: int = 3600
    funds_disbursement_frequency: int = 3600
    mt940_processor_frequency: int = 3600

    process_future_disbursement_schedules: bool = False
