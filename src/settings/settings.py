from decouple import config
from pydantic import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Shopping Cart"
    DATABASE_URI: str = config("DATABASE_URI")
    PORT: int = config("PORT")

settings = Settings()
