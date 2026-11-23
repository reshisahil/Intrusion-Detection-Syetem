from alert_engine import save_alert
from alert_service import (
    get_all_alerts,
    get_alert_by_id,
    update_alert_status
)


def test_alert_service(test_db):
    detection = {
        "attack_type": "DDoS",
        "severity": "High",
        "score": 85,
        "reason": "Test alert"
    }

    alert_id = save_alert(detection, record_index=1)

    alerts = get_all_alerts()
    assert len(alerts) == 1

    alert = get_alert_by_id(alert_id)
    assert alert["attack_type"] == "DDoS"

    updated = update_alert_status(alert_id, "Resolved")
    assert updated is True

    alert = get_alert_by_id(alert_id)
    assert alert["status"] == "Resolved"


def test_nonexistent_alert(test_db):
    assert get_alert_by_id(999) is None
