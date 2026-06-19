from fastapi import FastAPI
from app.embeddings import load_data, build_index
from app.rag_engine import find_similar
from app.risk_engine import assess_risk
from app.automation import execute_fix
from app.fallback_engine import get_best_practices

app = FastAPI(title="AI Bug Busters API")

# ✅ Load data and embeddings at startup
data = load_data()
embeddings = build_index(data)

# ✅ Thresholds
MIN_CONFIDENCE = 0.6
LOW_CONFIDENCE = 0.4
VALIDATION_THRESHOLD = 0.3   # ✅ Generic AI-based validation


@app.get("/")
def home():
    return {"message": "AI Bug Busters is running 🚀"}


@app.get("/analyze")
def analyze(issue: str):
    try:
        # ✅ -------------------------------
        # ✅ BASIC INPUT VALIDATION
        # ✅ -------------------------------
        if not issue or len(issue.strip()) < 3:
            return {
                "message": "Please provide a more detailed incident description."
            }

        # ✅ -------------------------------
        # ✅ AI MATCHING (CORE ENGINE)
        # ✅ -------------------------------
        results, scores = find_similar(embeddings, data, issue)

        if not results:
            return {
                "message": "No similar incidents found.",
                "best_practices": get_best_practices(issue)
            }

        best = results[0]
        best_score = scores[0]

        # ✅ -------------------------------
        # ✅ GENERIC AI-BASED VALIDATION (NEW ✅)
        # ✅ -------------------------------
        if best_score < VALIDATION_THRESHOLD:
            return {
                "input_issue": issue,
                "message": "Input is too generic or unrelated. Showing general best practices.",
                "confidence": float(best_score),
                "best_practices": get_best_practices(issue),
                "validation_failed": True
            }

        # ✅ -------------------------------
        # ✅ CASE 1: STRONG MATCH
        # ✅ -------------------------------
        if best_score >= MIN_CONFIDENCE:
            confidence, action = assess_risk(best_score, best["risk"])

            execution_result = None
            if action == "AUTO_EXECUTE":
                execution_result = execute_fix(best["fix"])

            return {
                "input_issue": issue,
                "matched_issue": best["incident"],
                "root_cause": best.get("root_cause"),
                "suggested_fix": best.get("fix"),
                "confidence": float(confidence),
                "action": action,
                "execution_result": execution_result
            }

        # ✅ -------------------------------
        # ✅ CASE 2: MEDIUM MATCH (SMART FALLBACK)
        # ✅ -------------------------------
        elif best_score >= LOW_CONFIDENCE:
            return {
                "input_issue": issue,
                "message": "No exact match found. Showing closest relevant solution.",
                "matched_issue": best["incident"],
                "root_cause": best.get("root_cause"),
                "suggested_fix": best.get("fix"),
                "confidence": float(best_score),
                "action": "SUGGEST_ONLY",
                "fallback_used": True
            }

        # ✅ -------------------------------
        # ✅ CASE 3: LOW MATCH → BEST PRACTICES
        # ✅ -------------------------------
        else:
            return {
                "input_issue": issue,
                "message": "No relevant incident found. Showing general best practices.",
                "confidence": float(best_score),
                "best_practices": get_best_practices(issue),
                "fallback_used": True
            }

    except Exception as e:
        return {
            "error": str(e),
            "message": "Something went wrong in analysis"
        }