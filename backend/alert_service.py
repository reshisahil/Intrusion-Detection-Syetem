
from database import get_connection


def get_all_alerts():
    conn = get_connection()

    cursor = conn.execute(
        "SELECT * FROM alerts ORDER BY id DESC"
    )

    alerts = [dict(row) for row in cursor.fetchall()]

    conn.close()
    return alerts


def get_alert_by_id(alert_id):
    conn = get_connection()

    cursor = conn.execute(
        "SELECT * FROM alerts WHERE id = ?",
        (alert_id,)
    )

    row = cursor.fetchone()
    conn.close()

    return dict(row) if row else None


def update_alert_status(alert_id, status):
    conn = get_connection()

    cursor = conn.execute(
        "UPDATE alerts SET status = ? WHERE id = ?",
        (status, alert_id)
    )

    conn.commit()
    updated = cursor.rowcount > 0
    conn.close()

    return updated
