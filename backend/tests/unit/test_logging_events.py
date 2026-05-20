from __future__ import annotations

import logging

from app.services.logging import get_logger, log_event


def test_log_event_emits_structured_fields(caplog) -> None:
    logger = get_logger("faq_assistant.test")

    with caplog.at_level(logging.INFO, logger="faq_assistant.test"):
        log_event(
            logger,
            "authorization_failed",
            request_id="req-1",
            user_role="end_user",
            route="/admin/analytics/summary",
        )

    assert caplog.records
    record = caplog.records[0]
    assert record.event == "authorization_failed"
    assert record.request_id == "req-1"
    assert record.user_role == "end_user"
    assert record.route == "/admin/analytics/summary"
