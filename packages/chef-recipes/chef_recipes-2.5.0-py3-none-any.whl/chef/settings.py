import os.path
from enum import StrEnum
from pathlib import Path
from typing import Union, Optional
from distutils.sysconfig import get_python_lib
from loguru import logger

from pydantic import Field
from pydantic_settings import BaseSettings


HOME_DIR = Path.home() / '.chef'


class StorageType(StrEnum):
    LOCAL = 'LOCAL'


class ImageFormat(StrEnum):
    AVIF = 'AVIF'


def get_bundled_frontend_path():
    site_packages = get_python_lib()
    frontend_root = os.path.join(site_packages, "src", "js", "chef", "dist")
    logger.info(frontend_root)
    if os.path.isdir(frontend_root):
        return frontend_root


def get_locally_build_frontend_path():
    return "./src/js/chef/dist" if os.path.isdir("./src/js/chef/dist") else None


def get_default_frontend_path() -> str:
    return get_bundled_frontend_path() or get_locally_build_frontend_path()


class Settings(BaseSettings):
    """Default config will store all user data in ~/.chef"""
    serve_frontend_path: Union[str, None] = Field(default_factory=get_default_frontend_path)
    serve_frontend: bool = True
    serve_static: bool = True
    database_uri: str = "sqlite:///" + os.path.join(HOME_DIR,  "chef.db")
    log_file: Union[str, None] = None
    log_level: str = "DEBUG"
    log_sql: bool = False

    storage_backend: StorageType = StorageType.LOCAL
    images_folder: str = os.path.join(HOME_DIR,  "images")

    uvicorn_host: str = "0.0.0.0"
    uvicorn_port: int = 8000

    public_url: str = "http://localhost:8000"
    gpt_enpoint_url: str = "http://localhost:8001"

    sentry_dsn: Optional[str] = None


settings = Settings(_env_file=".env")
