from pydantic import BaseSettings
from pymongo import MongoClient


class Settings(BaseSettings):
    mongo_host: str = "127.0.0.1"
    mongo_port: str = "27017"
    mongo_username: str = ""
    mongo_password: str = ""
    mongo_db_name: str = "pyrchitecture"
    mongo_server_selection_timeout_ms: int = 20000
    mongo_connect_timeout_ms: int = 20000

    @property
    def mongo_address(self) -> str:
        return f"mongodb://{self.mongo_username}:{self.mongo_password}@{self.mongo_host}:{self.mongo_port}"


settings = Settings()


db = MongoClient(
    host=settings.mongo_host,
    port=int(settings.mongo_port),
    username=settings.mongo_username,
    password=settings.mongo_password,
    serverSelectionTimeoutMS=settings.mongo_server_selection_timeout_ms,
    connectTimeoutMS=settings.mongo_connect_timeout_ms,
)[settings.mongo_db_name]
