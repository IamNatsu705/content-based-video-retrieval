from fastapi import FastAPI

app = FastAPI(title="Content-Based Video Retrieval API")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
