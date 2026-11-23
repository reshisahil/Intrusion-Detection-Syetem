
from datetime import datetime, timezone
from database import get_connection


def save_alert(detection, record_index=None):

    timestamp = datetime.now(timezone.utc).isoformat()

    conn = get_connection()

    cursor = conn.execute("""
        INSERT INTO alerts (
            timestamp,
            attack_type,
            severity,
            risk_score,
            reason,
            record_index
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        timestamp,
        detection["attack_type"],
        detection["severity"],
        int(detection["score"]),
        detection["reason"],
        record_index
    ))

    alert_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return alert_id
