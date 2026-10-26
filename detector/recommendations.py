def build_recommendations(findings: list[dict]) -> list[str]:
    recommendations = []
    for item in findings:
        if item["id"] == "upfront_fee" or item["id"] == "payment_checkbox":
            recommendations.append("Do not pay a fee to secure an internship before independently verifying the organization and the charge.")
        elif item["id"] == "sensitive_documents":
            recommendations.append("Never share passwords, OTPs, banking PINs, or card security codes with a recruiter.")
        elif item["id"] == "domain_mismatch":
            recommendations.append("Contact the company using contact information found independently on its official website.")
        elif item["id"] in ("invalid_email", "invalid_website"):
            recommendations.append("Recheck the contact details and use an independently located official company channel.")
        elif item["id"] in ("guaranteed_selection", "urgency", "unrealistic_income"):
            recommendations.append("Take time to review the written terms and verify the claims; do not let pressure tactics rush your decision.")
        elif item["id"] in ("vague_work", "missing_company_details"):
            recommendations.append("Ask for the company identity, supervisor, responsibilities, duration, and written internship terms.")
        elif item["id"] == "extreme_stipend_entry":
            recommendations.append("Confirm the stipend amount, currency, and payment period in writing.")
    if not recommendations:
        recommendations.append("Verify the company, recruiter, internship duties, duration, and written terms using independent sources.")
    # Preserve order while removing duplicate recommendations.
    return list(dict.fromkeys(recommendations))[:6]
