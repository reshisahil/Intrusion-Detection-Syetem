from detection_rules import detect_threats


def test_port_scan_detection():
    data = {
        "unique_ports": 25,
        "time_window_seconds": 10
    }

    results = detect_threats(data)

    assert any(
        threat["attack_type"] == "Port Scan"
        for threat in results
    )


def test_excessive_connections():
    data = {"connection_attempts": 80}

    results = detect_threats(data)

    assert any(
        threat["attack_type"] == "Excessive Connections"
        for threat in results
    )


def test_no_threat_for_empty_record():
    assert detect_threats({}) == []
