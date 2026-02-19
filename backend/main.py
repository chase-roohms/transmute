from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from api import router
from core import get_settings
import uvicorn

def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(router, prefix="/api")
    web_dir = get_settings().web_dir
    if web_dir.exists():
        app.mount("/assets", StaticFiles(directory=web_dir / "assets"), name="assets")
        if (web_dir / "icons").exists():
            app.mount("/icons", StaticFiles(directory=web_dir / "icons"), name="icons")

        @app.get("/{full_path:path}")
        def serve_spa(full_path: str):
            return FileResponse(web_dir / "index.html")

    return app

if __name__ == "__main__":
    app = create_app()
    uvicorn.run(app, host="0.0.0.0", port=3313)
