from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Definimos los tipos de datos
    DATABASE_URL: str
    SECRET_KEY: str
    ODOO_URL: str
    ODOO_DB: str
    ODOO_USER: str
    ODOO_PASS: str

    # Le indicamos que lea el archivo .env
    model_config = SettingsConfigDict(env_file=".env")

# Instanciamos para usar en todo el proyecto
settings = Settings()