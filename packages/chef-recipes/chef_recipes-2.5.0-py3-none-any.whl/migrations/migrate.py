import os
from alembic.config import Config
from alembic import command

from loguru import logger

# alembic_config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "alembic.ini"))

migrations_dir = os.path.abspath(os.path.dirname(__file__))


def run():
    alembic_cfg = Config()
    alembic_cfg.file_config["alembic"]["script_location"] = migrations_dir
    logger.info(f"Creating ad-hoc alembic.ini, {migrations_dir=}")

    logger.info(f"running the migrations >> head")
    command.upgrade(alembic_cfg, "head")

    logger.info(f"migrations completed")


if __name__ == "__main__":
    run()
