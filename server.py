import base64  # noqa: F401
import hashlib
import os  # noqa: F401
from pathlib import Path

import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel, ConfigDict

INDEX_PATH = Path(__file__).with_name("index.html")
app = FastAPI()


# Request model for text submitted to the generate endpoint.
class Text(BaseModel):
    model_config = ConfigDict(extra="forbid")

    text: str


@app.get("/", response_class=FileResponse)
@app.get("/index.html", response_class=FileResponse)
def index() -> FileResponse:
    return FileResponse(INDEX_PATH)


@app.post("/generate")
def generate(payload: Text) -> dict[str, str]:
    checksum = hashlib.sha256(payload.text.encode("utf-8")).hexdigest()
    return {"checksum": checksum}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)