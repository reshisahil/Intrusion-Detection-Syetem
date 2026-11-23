from risk_scoring import calculate_risk


def test_high_risk_score():
    result = calculate_risk(rule_score=80, ml_score=90)

    assert result["risk_score"] == 86
    assert result["severity"] == "High"


def test_low_risk_score():
    result = calculate_risk(rule_score=20)

    assert result["risk_score"] == 20
    assert result["severity"] == "Low"


def test_medium_risk_score():
    result = calculate_risk(rule_score=50)

    assert result["severity"] == "Medium"
