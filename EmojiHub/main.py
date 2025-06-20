import uvicorn
from src.app import get_app


app = get_app()

if __name__ == "__main__":
    host = "0.0.0.0"
    port = 8000
    reload = False
    uvicorn.run("main:app", host=host, port=port, log_level="info", reload=reload)