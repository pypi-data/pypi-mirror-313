import logging
import logging.config
import secrets
import time
from http import HTTPStatus

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from starlette_csrf import CSRFMiddleware

import app.settings as settings
from app.api import (
    alert,
    auth,
    basic_auth_user,
    channel,
    event,
    healthy,
    integration,
    management,
    report,
    silence,
    user_notification_settings,
)
from app.exception import AlertBackendException
from app.model.result_model import Result
from app.scheduler.wakeup_alert import start_scheduler
from app.schema.response_model import ResponseModel

logging.config.fileConfig(settings.LOGGER_CONFIG, disable_existing_loggers=False)
log = logging.getLogger("appLogger")
log.setLevel(settings.APP_DEBUG_MODE)

server = [
    {"url": "https://api.ags.cloudzcp.net", "description": "Staging Server"},
    {"url": "https://api.dev.cloudzcp.net", "description": "Dev Server"},
    {"url": "http://localhost:9150", "description": "Local Server"},
]

app = FastAPI(
    # root_path=f"{settings.APP_ROOT}",
    title=f"{settings.APP_TITLE}",
    description=f"{settings.APP_DESCRIPTION}",
    version=f"{settings.APP_VERSION}",
    docs_url=f"{settings.DOCS_URL}",
    openapi_url=f"{settings.OPENAPI_URL}",
    redoc_url=f"{settings.REDOC_URL}",
    default_response_class=JSONResponse,
    debug=True,
    # servers=server,
    root_path_in_servers=True,
)

app.mount(
    f"{settings.APP_ROOT}/html", StaticFiles(directory="public/html"), name="html"
)


# downgrading the openapi version to 3.0.0
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
        openapi_version="3.0.0",
        servers=app.servers,
    )
    app.openapi_schema = openapi_schema

    return app.openapi_schema


app.openapi = custom_openapi

app.include_router(alert.router, tags=["alert"], prefix=settings.APP_ROOT)
app.include_router(event.router, tags=["event"], prefix=settings.APP_ROOT)
app.include_router(channel.router, tags=["channel"], prefix=settings.APP_ROOT)
app.include_router(integration.router, tags=["integration"], prefix=settings.APP_ROOT)
app.include_router(silence.router, tags=["silence"], prefix=settings.APP_ROOT)
app.include_router(report.router, tags=["report"], prefix=settings.APP_ROOT)
app.include_router(
    user_notification_settings.router,
    tags=["notification setttings"],
    prefix=settings.APP_ROOT,
)
app.include_router(management.router, tags=["management"], prefix=settings.APP_ROOT)
app.include_router(
    basic_auth_user.router, tags=["basic auth user"], prefix=settings.APP_ROOT
)
app.include_router(healthy.router, tags=["healthy"])
# app.include_router(k8s.router, tags=["kubernetes"])

if settings.AUTH_API_ENABLED:
    app.include_router(auth.router, tags=["test auth"], prefix=settings.APP_ROOT)

app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

__csrf_secret_key = secrets.token_urlsafe(16)
log.info(f"CRSF Secret Key: {__csrf_secret_key}")
# references
# https://pypi.org/project/starlette-csrf/3.0.0/
# https://dev-in-seoul.tistory.com/44#CORS%20%EC%84%A4%EC%A0%95%EA%B3%BC%20CSRF%20%EA%B3%B5%EA%B2%A9%EC%9D%84%20%EB%A7%89%EA%B8%B0-1
app.add_middleware(
    CSRFMiddleware,
    secret=__csrf_secret_key,
    cookie_domain="localhost",
    cookie_name="csrftoken",
    cookie_path="/",
    cookie_secure=False,
    cookie_httponly=True,
    cookie_samesite="lax",
    header_name="x-csrf-token",
    safe_methods={"GET", "HEAD", "OPTIONS", "TRACE", "POST", "PUT", "DELETE", "PATCH"},
)

__session_secret_key = secrets.token_urlsafe(32)
log.info(f"Session Secret Key: {__session_secret_key}")

app.add_middleware(
    SessionMiddleware,
    secret_key=__session_secret_key,
    session_cookie="session_id",
    max_age=1800,
    same_site="lax",
    https_only=True,
)


@app.middleware("http")
async def http_middleware(request: Request, call_next):
    """
    HTTP Middleware to add custom headers to the response
    1. Display request information
    2. Put process time information into Header: X-Process-Time
    3. Display response information
    """
    await __display_request_info(request)

    start_time = time.time()

    response = await call_next(request)

    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = f"{process_time:.5f}"

    log.info(
        f"Process time:{process_time:.5f} - URL: {request.url} - Proceeded successfully!"
    )

    # await __display_response_info(response)

    return response


@app.exception_handler(AlertBackendException)
async def exception_handler(request: Request, e: AlertBackendException):
    return JSONResponse(
        status_code=e.status_code,
        content=ResponseModel(
            result=Result.FAILED, code=e.code, message=e.detail
        ).model_dump(exclude_none=True),
    )


# Start the scheduler for awake the alerts snoozed time over
start_scheduler()
log.info(
    f"Scheduler started with interval {settings.WAKEUP_SCHEDULER_INTERVAL} minutes"
)
log.info(f"The application({settings.APP_NAME}) has been started")


async def __display_request_info(request: Request):
    """
    Display request information
    """
    request_info = "\n"
    request_info += (
        "===================== REQUEST Started ============================\n"
    )
    request_info += f"# Headers: {dict(request.headers)}\n"

    request_info += f"# Path: {request.url.path}\n"
    request_info += f"# Method: {request.method}\n"

    body = await request.body()
    request_info += f"# Body: {body.decode()}\n"

    request_info += f"# Query Params: {dict(request.query_params)}\n"
    request_info += (
        "===================== REQUEST Finished ===========================\n"
    )

    log.info(request_info)


async def __display_response_info(response: StreamingResponse):
    """
    Display response information
    """

    response_info = "\n"
    response_info += (
        "===================== RESPONSE Started ===========================\n"
    )
    response_info += f"# Headers: { dict(response.headers)}\n"
    response_info += f"# Status Code: {response.status_code}\n"

    if isinstance(response, StreamingResponse):
        original_iterator = response.body_iterator

        async def __log_and_stream_response(buffer: str):
            response_body = b""
            async for chunk in original_iterator:
                response_body += chunk
                yield chunk
            buffer += f"# Body: {response_body.decode('utf-8')}\n"
            buffer += (
                "===================== RESPONSE Finished ==========================\n"
            )
            if response.status_code >= HTTPStatus.BAD_REQUEST:
                log.error(buffer)
            else:
                log.info(buffer)

        response.body_iterator = __log_and_stream_response(response_info)
    else:
        response_info += f"# Body: {response.body}\n"
        response_info += (
            "===================== RESPONSE Finished ==========================\n"
        )
        log.info(response_info)
