from fastapi import FastAPI, Request, HTTPException, logger
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from typing import AsyncContextManager
import logging
import atexit
from fastapi.openapi.docs import get_swagger_ui_html
import uvicorn

from src.app.snippets import router_snippets
from src.app.auth import router_auth
from src.logger import LOGGING_CONFIG
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

app = FastAPI(docs_url=None)

app.include_router(router_auth)
app.include_router(router_snippets)


@app.middleware("http")
async def error_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except HTTPException as exc:
        return JSONResponse(
            status_code=exc.status_code,
            content={"message": exc.detail}
        )
    except Exception as e:
        logger.error(f"{request.url} | Error in application: {e}")
        return JSONResponse(
            status_code=500,
            content={"message": "Internal server error"}
        )


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncContextManager[None]:
    logging.config.dictConfig(LOGGING_CONFIG)
    queue_handler = logging.getHandlerByName("queue_handler")
    try:
        if queue_handler is not None:
            queue_handler.listener.start()
            atexit.register(queue_handler.listener.stop)
        yield
    finally:
        if queue_handler is not None:
            queue_handler.listener.stop()


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css",
    )


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
