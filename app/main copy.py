from fastapi import FastAPI
from app.embeddings import load_data, build_index
from app.rag_engine import find_similar
from app.risk_engine import assess_risk
from app.automation import execute_fix

app = FastAPI()

data = load_data()
index, _ = build_index(data)

@app.get("/analyze")
def analyze(issue: str):
    results, scores = find_similar(index, data, issue)
    
    best = results[0]
    confidence, action = assess_risk(scores[0], best["risk"])

    execution_result = None
    if action == "AUTO_EXECUTE":
        execution_result = execute_fix(best["fix"])

    return {
        "matched_issue": best["incident"],
        "suggested_fix": best["fix"],
        "confidence": confidence,
        "action": action,
        "execution": execution_result
    }