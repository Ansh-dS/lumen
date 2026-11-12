import uvicorn

from backend.api.server import app

# __all__: special variable, expose only app from this file to the outer world.
# rest things are invisible. 
__all__ = ["app"]

if __name__ == "__main__":
    uvicorn.run("backend.api.server:app", host="0.0.0.0", port=8000, reload=True)
