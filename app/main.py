from fastapi import FastAPI
from app.embeddings import load_data, build_index
from app.rag_engine import find_similar
from app.risk_engine import assess_risk
from app.fallback_engine import get_best_practices

app = FastAPI(title="AI Bug Busters API")

data = load_data()
embeddings = build_index(data)

MIN_CONFIDENCE = 0.6
LOW_CONFIDENCE = 0.4
VALIDATION_THRESHOLD = 0.3


# ✅ ✅ Enhanced Explanation (WITH RISK)
def generate_explanation(issue, matched_issue, fix, confidence, risk):
    return f"""
This recommendation is based on semantic similarity between your input and historical incidents.

🔹 Input: {issue}
🔹 Matched Incident: {matched_issue}

✅ Why this fix is suggested:
- Similar patterns detected in previous incidents
- The fix '{fix}' has successfully resolved similar issues

📊 Confidence Score: {round(confidence*100, 2)}%
Represents how closely your issue matches known cases.

⚠ Risk Level: {risk.upper()}
- Low → Safe to apply
- Medium → Validate before applying
- High → Requires careful analysis
""".strip()


@app.get("/")
def home():
    return {"message": "AI Bug Busters is running 🚀"}


@app.get("/analyze")
def analyze(issue: str):
    try:
        if not issue or len(issue.strip()) < 3:
            return {
                "message": "Please provide a more detailed incident description."
            }

        results, scores = find_similar(embeddings, data, issue)

        if not results:
            return {
                "message": "No similar incidents found.",
                "best_practices": get_best_practices(issue),
                "explanation": "No matching incident found. Providing general troubleshooting guidance."
            }

        best = results[0]
        best_score = scores[0]
        risk = best.get("risk", "low")  # ✅ already exists in your data

        # ✅ Validation
        if best_score < VALIDATION_THRESHOLD:
            return {
                "input_issue": issue,
                "message": "Input is too generic or unrelated.",
                "confidence": float(best_score),
                "best_practices": get_best_practices(issue),
                "explanation": "The input does not closely match known incidents."
            }

        # ✅ HIGH CONFIDENCE
        if best_score >= MIN_CONFIDENCE:
            confidence, _ = assess_risk(best_score, risk)

            return {
                "input_issue": issue,
                "matched_issue": best["incident"],
                "root_cause": best.get("root_cause"),
                "suggested_fix": best.get("fix"),
                "confidence": float(confidence),
                "risk": risk,  # ✅ added
                "level": "HIGH_CONFIDENCE",
                "explanation": generate_explanation(
                    issue, best["incident"], best["fix"], confidence, risk
                )
            }

        # ✅ MEDIUM CONFIDENCE
        elif best_score >= LOW_CONFIDENCE:

            return {
                "input_issue": issue,
                "message": "No exact match found. Showing closest relevant solution.",
                "matched_issue": best["incident"],
                "root_cause": best.get("root_cause"),
                "suggested_fix": best.get("fix"),
                "confidence": float(best_score),
                "risk": risk,
                "level": "MEDIUM_CONFIDENCE",
                "explanation": generate_explanation(
                    issue, best["incident"], best["fix"], best_score, risk
                )
            }

        # ✅ LOW CONFIDENCE
        else:
            return {
                "input_issue": issue,
                "message": "No relevant incident found. Showing general best practices.",
                "confidence": float(best_score),
                "best_practices": get_best_practices(issue),
                "level": "LOW_CONFIDENCE",
                "explanation": "Low similarity. Providing general troubleshooting guidance."
            }

    except Exception as e:
        return {"error": str(e)}