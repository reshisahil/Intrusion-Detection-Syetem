from detection_service import analyze_record


def test_detection_pipeline(test_db):
    sample_record = {
        "unique_ports": 25,
        "time_window_seconds": 10,
        "connection_attempts": 80,
        "failed_connections": 70,
        "bytes_sent": 15000000
    }

    result = analyze_record(sample_record, record_index=1)

    assert result["record_index"] == 1
    assert result["detections_found"] > 0
    assert len(result["alerts"]) > 0

    for alert in result["alerts"]:
        assert alert["alert_id"] > 0
