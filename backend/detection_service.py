
from detection_rules import detect_threats
from risk_scoring import calculate_risk
from alert_engine import save_alert


def analyze_record(record, record_index=None):

    detections = detect_threats(record)

    generated_alerts = []

    for detection in detections:

        risk = calculate_risk(
            rule_score=detection["score"]
        )

        alert_data = {
            "attack_type": detection["attack_type"],
            "severity": risk["severity"],
            "score": risk["risk_score"],
            "reason": detection["reason"]
        }

        alert_id = save_alert(
            alert_data,
            record_index
        )

        generated_alerts.append({
            "alert_id": alert_id,
            **alert_data
        })

    return {
        "record_index": record_index,
        "detections_found": len(detections),
        "alerts": generated_alerts
    }
