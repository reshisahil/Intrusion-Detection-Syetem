def detect_threats(data):

    threats = []

    # Rule 1: Port Scan Detection
    if data.get("unique_ports", 0) >= 15 and data.get("time_window_seconds", 999) <= 10:
        threats.append({
            "attack_type": "Port Scan",
            "severity": "High",
            "score": 70,
            "reason": "Multiple ports accessed within a short time"
        })

    # Rule 2: Excessive Connections
    if data.get("connection_attempts", 0) >= 50:
        threats.append({
            "attack_type": "Excessive Connections",
            "severity": "Medium",
            "score": 50,
            "reason": "Too many connection attempts detected"
        })

    # Rule 3: High Connection Failure Rate
    attempts = data.get("connection_attempts", 0)
    failures = data.get("failed_connections", 0)

    if attempts > 0:
        failure_rate = (failures / attempts) * 100

        if failure_rate >= 70:
            threats.append({
                "attack_type": "High Failure Rate",
                "severity": "High",
                "score": 75,
                "reason": f"Connection failure rate is {failure_rate:.1f}%"
            })

    # Rule 4: Traffic Anomaly
    if data.get("bytes_sent", 0) >= 10_000_000:
        threats.append({
            "attack_type": "High Traffic",
            "severity": "Medium",
            "score": 50,
            "reason": "Unusually high traffic volume detected"
        })

    return threats
