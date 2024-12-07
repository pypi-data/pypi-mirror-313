class EnvModel:
    API_KEY: str


class GlobalConfigModel:
    DEBUG: bool
    ENV: str
    DEV_APPS: str
    PRODUCT: str
    TENANT_ID: str


class ConfigModel:
    GLOBAL_CONFIG: GlobalConfigModel
    DEV: EnvModel
    BETA: EnvModel
    PROD: EnvModel
