
from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html
import uvicorn

from src.app.snippets import router_snippets
from src.app.auth import router_auth
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

app = FastAPI(docs_url=None)

app.include_router(router_auth)
app.include_router(router_snippets)


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
