from generator.message import STATUS_CODES, SERVICES, generate_api_event


def test_generate_api_event_has_valid_shape() -> None:
    event = generate_api_event().as_dict()

    assert event["source_service"] in SERVICES
    assert event["method"] in {"GET", "POST", "PATCH", "DELETE"}
    assert isinstance(event["endpoint"], str) and event["endpoint"].startswith("/")
    assert event["status_code"] in STATUS_CODES
    assert 15 <= event["latency_ms"] <= 1800
    assert 120 <= event["payload_size_bytes"] <= 80_000
    assert event["event_id"]
    assert event["created_at"].endswith("+00:00")
