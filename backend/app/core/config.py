from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')

    app_name: str = 'EraRide API'
    environment: str = 'development'
    api_v1_prefix: str = '/api/v1'

    secret_key: str = 'change-me'
    access_token_expire_minutes: int = 60 * 24 * 7

    allowed_email_domains: str = 'gehu.ac.in,geu.ac.in'

    database_url: str = 'postgresql+asyncpg://eraride:eraride@localhost:5432/eraride'
    redis_url: str = 'redis://localhost:6379/0'

    stripe_secret_key: str = ''
    stripe_webhook_secret: str = ''

    otp_ttl_seconds: int = 300
    ride_cache_ttl_seconds: int = 60
    rate_limit_per_minute: int = 120

    @property
    def email_domains(self) -> set[str]:
        return {d.strip().lower() for d in self.allowed_email_domains.split(',') if d.strip()}


@lru_cache
def get_settings() -> Settings:
    return Settings()
