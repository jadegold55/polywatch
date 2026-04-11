from fastapi import FastAPI

app = FastAPI()


@app.get("/")  # type: ignore[misc]
def read_root() -> dict[str, str]:
    return {"Hello": "World"}


@app.get("/health")  # type: ignore[misc]
def read_health() -> dict[str, str]:
    return {"status": "healthy"}
