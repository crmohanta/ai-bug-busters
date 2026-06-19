def assess_risk(similarity, risk_level):
    confidence = 1 / (1 + similarity)

    if risk_level == "low" and confidence > 0.7:
        return confidence, "AUTO_EXECUTE"
    elif confidence > 0.5:
        return confidence, "APPROVAL_REQUIRED"
    else:
        return confidence, "SUGGEST_ONLY"