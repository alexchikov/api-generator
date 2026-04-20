from __future__ import annotations

from fastapi import FastAPI


app = FastAPI(title="Synthetic API Generator", version="2.0.0")


@app.get("/")
def root() -> dict[str, str]:
    return {
        "message": "Synthetic API generator is running. Events are published to Kafka.",
    }


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
