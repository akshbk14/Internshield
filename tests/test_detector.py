from detector.text_analyzer import analyze_text
from detector.risk_scorer import calculate_risk
from detector.company_checks import check_company_details


def test_payment_language_is_flagged():
    findings = analyze_text(
        "Pay a registration fee to secure your internship. "
        "The software intern will develop and test Python features for eight weeks."
    )
    assert any(item["id"] == "upfront_fee" for item in findings)


def test_no_fee_statement_is_not_flagged_as_payment_request():
    findings = analyze_text(
        "There is no registration fee. Interns will develop Python features, "
        "test software, review code, and document project tasks."
    )
    assert not any(item["id"] == "upfront_fee" for item in findings)


def test_score_is_capped_at_100():
    findings = [
        {"id": "a", "points": 80, "title": "A", "explanation": "A"},
        {"id": "b", "points": 50, "title": "B", "explanation": "B"}
    ]
    result = calculate_risk(findings, "x" * 100)
    assert result["score"] == 100


def test_domain_mismatch_is_flagged():
    findings = check_company_details(
        company_name="Example",
        website="https://company.example",
        recruiter_email="hr@different.example"
    )
    assert any(item["id"] == "domain_mismatch" for item in findings)
