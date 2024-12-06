from app_paths import get_paths, AppPaths
from typing import Tuple, Type
from pathlib import Path
from pydantic import BaseModel, SecretBytes, SecretStr, field_validator

from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    TomlConfigSettingsSource,
)

from pathlib import Path

paths = get_paths("tubescience_cli", "TubeScience")
paths.env_paths = (Path.cwd() / ".env",)
paths.secrets_paths = (Path("/var/run"), Path("/run/secrets"))
paths.settings_paths = (
    paths.site_config_path / "settings.toml",
    paths.user_config_path / "settings.toml",
)


class LoggingSettings(BaseSettings):
    log_level: str = "INFO"
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    log_date_format: str = "%Y-%m-%d %H:%M:%S"


class TemporalSettings(BaseModel):
    host: str = "localhost:7233"
    task_queue: str = "ts-ad-classification"
    namespace: str = "default"
    mtls_tls_cert: SecretBytes = SecretBytes(b"")
    mtls_tls_key: SecretBytes = SecretBytes(b"")

    @field_validator("mtls_tls_cert", "mtls_tls_key", mode="before")
    def validate_mtls_tls(cls, v):
        if not v:
            return v
        if isinstance(v, (str, bytes)):
            if str(v).startswith("-----BEGIN"):
                return v
            elif Path(v).exists():
                v = Path(v).read_bytes()
        return v


class RetoolRPCSettings(BaseModel):
    token: SecretStr = SecretStr("")
    resource_id: str = ""
    host: str = "https://ts.app"
    environment_name: str = "production"
    polling_interval_ms: int = 1000
    log_level: str = "info"


class SnowflakeSettings(BaseModel):
    account: str = "ov02505.us-east-2.aws"
    warehouse: str = "ANALYTICS_WH"
    database: str = "RETOOL_DEV_DB"
    schema: str = "DAPPER"
    user: str = "RETOOL_USER"
    password: SecretStr = SecretStr("")


class Settings(BaseSettings):

    model_config = SettingsConfigDict(
        env_prefix="TS_",
        case_sensitive=False,
        env_nested_delimiter="__",
        env_file=(str(p) for p in paths.env_paths if p.exists()),
        secrets_dir=(str(p) for p in paths.secrets_paths if p.exists()),
        toml_file=(str(p) for p in paths.settings_paths if p.exists()),
        extra="allow",
    )

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        return (
            init_settings,
            env_settings,
            dotenv_settings,
            file_secret_settings,
            TomlConfigSettingsSource(settings_cls),
        )

    paths: AppPaths = paths
    debug: bool = False
    testing: bool = False
    logging: LoggingSettings = LoggingSettings()
    snowflake: SnowflakeSettings = SnowflakeSettings()
    temporal: TemporalSettings = TemporalSettings()
    retool_rpc: RetoolRPCSettings = RetoolRPCSettings()

settings = Settings()
