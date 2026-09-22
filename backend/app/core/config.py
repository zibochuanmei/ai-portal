from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "ai-portal"
    app_version: str = "0.1.0"
    app_env: str = "development"
    api_prefix: str = "/api/v1"
    cors_origins: str = "http://localhost:5173"
    deployment_mode: str = "local-compose"
    compose_project_name: str = "ai-portal"
    data_root: str = "../.data"
    default_company_code: str = "HZ"
    default_region_code: str = "TW"
    default_factory_code: str = "TAIPEI"
    default_timezone: str = "Asia/Taipei"
    default_locale: str = "zh-CN"
    supported_region_codes: str = "TW"
    supported_factory_codes: str = "TAIPEI"
    auth_mode: str = "demo"
    jwt_secret: str = "change-this-in-infra-env"
    access_token_expire_minutes: int = 60
    sso_issuer_url: str = ""
    sso_client_id: str = ""
    sso_client_secret: str = ""

    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_db: str = "ai_portal"
    postgres_user: str = "ai_portal"
    postgres_password: str = "change-me"
    database_url: str = "postgresql+asyncpg://ai_portal:change-me@localhost:5432/ai_portal"
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_url: str = "redis://localhost:6379/0"
    minio_host: str = "localhost"
    minio_endpoint: str = "localhost:9000"
    minio_secure: bool = False
    minio_root_user: str = "minioadmin"
    minio_root_password: str = "change-me-too"
    minio_business_bucket: str = "ai-portal-business-dev"
    minio_vector_bucket: str = "ai-portal-milvus-dev"
    etcd_endpoints: str = "localhost:2379"
    milvus_host: str = "localhost"
    milvus_port: int = 19530
    milvus_uri: str = "http://localhost:19530"
    milvus_collection_prefix: str = "ai_portal_dev"

    file_max_size_mb: int = 50
    allowed_file_extensions: str = "pdf,doc,docx,xls,xlsx,txt,jpg,jpeg,png"
    file_scan_required: bool = False
    document_default_classification: str = "internal"
    document_default_domain: str = "production"
    document_default_factory_code: str = "TAIPEI"
    storage_raw_prefix: str = "raw"
    storage_processed_prefix: str = "processed"

    log_level: str = "INFO"
    log_dir: str = "logs/backend"
    log_file_name: str = "ai-portal.jsonl"
    log_rotation_mb: int = 20
    log_backup_count: int = 5
    trace_header: str = "X-Request-ID"

    model_gateway_default_provider: str = "mock"
    model_gateway_timeout_seconds: int = 60
    model_gateway_max_retries: int = 2
    external_model_enabled: bool = False
    zhipu_api_base_url: str = "https://open.bigmodel.cn/api/paas/v4"
    zhipu_api_key: str = ""
    zhipu_model: str = ""
    qwen_api_base_url: str = "https://dashscope.aliyuncs.com/compatible-mode/v1"
    qwen_api_key: str = ""
    qwen_model: str = ""
    local_model_enabled: bool = False
    local_model_dir: str = "/models"
    local_intent_model: str = ""
    local_embedding_model: str = ""
    local_reranker_model: str = ""
    gpu_enabled: bool = False
    gpu_device: int = 0

    model_config = SettingsConfigDict(
        env_file=(".env", "../infra/.env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def cors_origin_list(self) -> list[str]:
        return [item.strip() for item in self.cors_origins.split(",") if item.strip()]

    @property
    def allowed_file_extension_list(self) -> list[str]:
        return [item.strip().lower().lstrip(".") for item in self.allowed_file_extensions.split(",") if item.strip()]

    @property
    def supported_factory_code_list(self) -> list[str]:
        return [item.strip() for item in self.supported_factory_codes.split(",") if item.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
