
def calculate_risk(rule_score=0, ml_score=None):

    rule_score = max(0, min(100, float(rule_score)))

    if ml_score is None:
        final_score = rule_score
    else:
        ml_score = max(0, min(100, float(ml_score)))

        # Combine rule-based and ML scores
        final_score = (rule_score * 0.4) + (ml_score * 0.6)

    final_score = round(final_score)

    if final_score >= 75:
        severity = "High"
    elif final_score >= 40:
        severity = "Medium"
    else:
        severity = "Low"

    return {
        "risk_score": final_score,
        "severity": severity
    }
