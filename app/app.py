from fastapi import FastAPI
from starlette.responses import RedirectResponse

from routers.types import router as types_router

app = FastAPI(title="Bofire Types API", version="0.1.0", root_path="/")


@app.get("/", include_in_schema=False)
async def redirect():
    return RedirectResponse(url="/docs")


app.include_router(types_router)
