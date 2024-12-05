import os.path

import typer
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.models import Response
from loguru import logger
from starlette.staticfiles import StaticFiles

from chef.api import api_router
from chef.models import ensure_tables
from chef.scripts.migrate_images import run as migrate_images_fn
from chef.settings import settings, Settings
from migrations.migrate import run as migrate_db_fn

cli_app = typer.Typer()

if settings.sentry_dsn:
    import sentry_sdk
    from sentry_sdk.integrations.fastapi import FastApiIntegration
    from sentry_sdk.integrations.starlette import StarletteIntegration
    sentry_sdk.init(
        dsn=settings.sentry_dsn,
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        traces_sample_rate=1.0,
        # Set profiles_sample_rate to 1.0 to profile 100%
        # of sampled transactions.
        # We recommend adjusting this value in production.
        profiles_sample_rate=1.0,
        integrations=[
            StarletteIntegration(
                transaction_style="endpoint",
                failed_request_status_codes=[403, range(500, 599)],
            ),
            FastApiIntegration(
                transaction_style="endpoint",
                failed_request_status_codes=[403, range(500, 599)],
            ),
        ],
    )


app = FastAPI(
    title="Chef",
    summary="Personal recipe management app.",
    version="2.5.0"
)
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:8080",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def print_banner(settings_in: Settings):
    options = "\n".join([f"{k.upper()}: '{v}'" for k, v in settings_in])
    logger.info(f"""

        ███████╗██╗  ██╗███████╗███████╗
        ██╔════╝██║  ██║██╔════╝██╔════╝
        ██║     ███████║█████╗  █████╗  
        ██║     ██╔══██║██╔══╝  ██╔══╝  
        ║██████ ██║  ██║███████╗██║     
        ╚═════════╝  ╚═╝╚══════╝╚═╝

        ...starting with following settings:

    {options}
    """)


@cli_app.command()
def migrate_images():
    print_banner(settings)
    should_it_continue = input("continue? [y/n]")
    if should_it_continue not in ("n", "N", "no", "No", "NO"):
        migrate_images_fn()


@cli_app.command()
def migrate_db():
    migrate_db_fn()


class StaticFilesCache(StaticFiles):
    def __init__(
            self,
            *args,
            cachecontrol="public, max-age=31536000, s-maxage=31536000, immutable",
            **kwargs
    ):
        self.cachecontrol = cachecontrol
        super().__init__(*args, **kwargs)

    def file_response(self, *args, **kwargs) -> Response:
        resp: Response = super().file_response(*args, **kwargs)
        resp.headers.setdefault("Cache-Control", self.cachecontrol)
        return resp


@cli_app.command()
def serve(hostname: str = settings.uvicorn_host, port: int = settings.uvicorn_port):
    settings.uvicorn_port = port
    settings.uvicorn_host = hostname
    print_banner(settings)

    if not os.path.isdir(settings.images_folder):
        logger.info(f"Creating images folder: {settings.images_folder}")
        os.makedirs(settings.images_folder, exist_ok=True)

    ensure_tables()

    if settings.log_file:
        logger.add(settings.log_file, level=settings.log_level)

    if settings.serve_frontend:
        if not settings.serve_frontend_path or not os.path.isdir(settings.serve_frontend_path):
            logger.error(
                f"Frontend files '{settings.serve_frontend_path}' not found, "
                f"frontend can't be served."
            )
            return
        app.mount("/images", StaticFilesCache(directory=settings.images_folder))
        app.mount("/", StaticFiles(directory=settings.serve_frontend_path, html=True))

    uvicorn.run(app, host=hostname, port=port)


def app_entrypoint():
    cli_app()


if __name__ == '__main__':
    app_entrypoint()
