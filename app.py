import json
from flask import Flask, render_template, request, jsonify
from detector.text_analyzer import analyze_text
from detector.company_checks import check_company_details
from detector.risk_scorer import calculate_risk
from detector.recommendations import build_recommendations

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 1 * 1024 * 1024  # 1 MB request limit


@app.get("/")
def home():
    return render_template("index.html")


@app.post("/api/analyze")
def analyze():
    data = request.get_json(silent=True) or {}

    description = str(data.get("description", "")).strip()
    company_name = str(data.get("company_name", "")).strip()
    company_website = str(data.get("company_website", "")).strip()
    recruiter_email = str(data.get("recruiter_email", "")).strip()
    stipend = str(data.get("stipend", "")).strip()
    payment_requested = bool(data.get("payment_requested", False))

    if len(description) < 30:
        return jsonify({
            "error": "Please enter at least 30 characters of internship description."
        }), 400

    if len(description) > 12000:
        return jsonify({"error": "Description is too long. Keep it under 12,000 characters."}), 400

    findings = analyze_text(description)
    findings.extend(check_company_details(
        company_name=company_name,
        website=company_website,
        recruiter_email=recruiter_email,
        stipend=stipend,
        payment_requested=payment_requested
    ))

    result = calculate_risk(findings, description)
    result["recommendations"] = build_recommendations(result["findings"])
    result["company_name"] = company_name or "Not provided"
    result["disclaimer"] = (
        "This is an automated, rule-based risk assessment, not proof that an offer is "
        "fraudulent or genuine. Verify important details independently."
    )
    return jsonify(result)


@app.get("/api/samples")
def samples():
    with open("data/sample_offers.json", "r", encoding="utf-8") as f:
        return jsonify(json.load(f))


@app.errorhandler(413)
def too_large(_error):
    return jsonify({"error": "Request is too large. Please shorten the advertisement."}), 413


if __name__ == "__main__":
    # Debug is useful locally. Do not use debug=True for public deployment.
    app.run(host="127.0.0.1", port=5000, debug=True)
