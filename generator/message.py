from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import random
from typing import Any
from uuid import uuid4


SERVICES: dict[str, list[dict[str, Any]]] = {
    "nebula-pay": [
        {"method": "POST", "path": "/payments"},
        {"method": "GET", "path": "/payments/{id}"},
        {"method": "POST", "path": "/refunds"},
    ],
    "astro-cart": [
        {"method": "POST", "path": "/carts"},
        {"method": "PATCH", "path": "/carts/{id}"},
        {"method": "DELETE", "path": "/carts/{id}"},
    ],
    "galaxy-identity": [
        {"method": "POST", "path": "/users"},
        {"method": "POST", "path": "/sessions"},
        {"method": "DELETE", "path": "/sessions/{id}"},
    ],
    "orbit-delivery": [
        {"method": "POST", "path": "/shipments"},
        {"method": "GET", "path": "/shipments/{id}/status"},
        {"method": "PATCH", "path": "/shipments/{id}"},
    ],
}

STATUS_CODES = (200, 201, 202, 400, 401, 403, 404, 409, 422, 500, 503)


@dataclass(slots=True)
class ApiEvent:
    event_id: str
    created_at: str
    source_service: str
    endpoint: str
    method: str
    status_code: int
    latency_ms: int
    payload_size_bytes: int

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


def _render_path(path: str) -> str:
    if "{id}" in path:
        return path.replace("{id}", str(random.randint(1000, 9999)))
    return path


def generate_api_event() -> ApiEvent:
    service = random.choice(tuple(SERVICES.keys()))
    operation = random.choice(SERVICES[service])

    return ApiEvent(
        event_id=str(uuid4()),
        created_at=datetime.now(timezone.utc).isoformat(),
        source_service=service,
        endpoint=_render_path(operation["path"]),
        method=operation["method"],
        status_code=random.choice(STATUS_CODES),
        latency_ms=random.randint(15, 1800),
        payload_size_bytes=random.randint(120, 80_000),
    )
