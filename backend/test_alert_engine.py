from alert_engine import save_alert


def test_save_alert(test_db):
    detection = {
        "attack_type": "DDoS",
        "severity": "High",
        "score": 85,
        "reason": "Test alert"
    }

    alert_id = save_alert(detection, record_index=1)

    assert alert_id > 0
