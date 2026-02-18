from fastapi import APIRouter, HTTPException
import sqlite3
import os

router = APIRouter()


DB_PATH = "data/db/app.sqlite"
UPLOAD_DIR = "data/uploads"


@router.get("/health/live")
def liveness():
    """Simple liveness check to confirm the server is running"""
    return {"status": "alive"}

@router.get("/health/ready")
def readiness():
    """Readiness check to confirm the server is ready to handle requests"""
    checks = {}
    # SQLite check
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.execute("SELECT 1")
        conn.close()
        checks["database"] = "ok"
    except Exception as e:
        checks["database"] = f"error: {e}"

    # Filesystem check
    try:
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        test_path = os.path.join(UPLOAD_DIR, ".healthcheck")
        with open(test_path, "w") as f:
            f.write("ok")
        os.remove(test_path)
        checks["storage"] = "ok"
    except Exception as e:
        checks["storage"] = f"error: {e}"

    # Determine overall status
    if all(v == "ok" for v in checks.values()):
        return {"status": "ready", "checks": checks}

    raise HTTPException(status_code=503, detail={"status": "not_ready", "checks": checks})