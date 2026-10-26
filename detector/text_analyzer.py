import re

# Each rule has a stable ID, a category, a weight, and a user-friendly explanation.
# These are heuristic demo rules, not statistically validated fraud indicators.
TEXT_RULES = [
    {
        "id": "upfront_fee",
        "title": "Possible upfront payment request",
        "points": 30,
        "pattern": r"\b(pay|payment|deposit|registration fee|processing fee|security fee|training fee)\b.{0,70}\b(to secure|to confirm|for selection|mandatory|before joining|to get|for internship|refundable fee)\b|\b(pay|send|transfer)\b.{0,50}\b(fee|money|deposit)\b",
        "explanation": "The advertisement may be asking the applicant to pay money to obtain or secure the opportunity.",
        "recommendation": "Do not pay to secure an opportunity until you have independently verified the organization and the reason for any charge."
    },
    {
        "id": "guaranteed_selection",
        "title": "Guaranteed selection or placement claim",
        "points": 15,
        "pattern": r"\b(guaranteed (job|selection|placement|internship)|100% (job|placement|selection) guarantee|sure shot selection)\b",
        "explanation": "Absolute guarantees can be used to pressure applicants and should be checked carefully.",
        "recommendation": "Ask for written selection criteria and verify the opportunity through the organization's official channels."
    },
    {
        "id": "unrealistic_income",
        "title": "Potentially unrealistic earnings claim",
        "points": 10,
        "pattern": r"\b(earn|income|salary|stipend)\b.{0,35}\b(huge|unlimited|guaranteed|instant|lakhs in days|easy money)\b|\b(get rich quick|earn money without work|no work required)\b",
        "explanation": "The wording promotes unusually easy or guaranteed earnings without enough context.",
        "recommendation": "Compare the compensation with the duties and ask for clear written terms."
    },
    {
        "id": "urgency",
        "title": "Pressure or urgency language",
        "points": 10,
        "pattern": r"\b(only today|act now|limited seats|immediate payment|last chance|pay within \d+ hours|hurry up)\b",
        "explanation": "Artificial urgency can discourage applicants from checking the offer carefully.",
        "recommendation": "Take time to verify the offer. Do not let a deadline prevent reasonable checks."
    },
    {
        "id": "sensitive_documents",
        "title": "Sensitive information request",
        "points": 15,
        "pattern": r"\b(send|submit|upload|share)\b.{0,50}\b(password|otp|one.time password|bank pin|card cvv|net banking credentials)\b|\b(pay to release|pay to receive)\b.{0,35}\b(certificate|offer letter|internship certificate)\b",
        "explanation": "The text appears to request credentials or payment tied to receiving a document.",
        "recommendation": "Never share passwords, OTPs, banking PINs, or card security codes with a recruiter."
    },
    {
        "id": "vague_work",
        "title": "Vague or missing work details",
        "points": 5,
        "pattern": None,
        "explanation": "The advertisement provides little detail about the work, responsibilities, or expected skills.",
        "recommendation": "Ask for specific responsibilities, supervisor details, duration, and written internship terms."
    }
]

NEGATION_RE = re.compile(
    r"\b(no|not|never|without|zero)\b.{0,30}\b(registration fee|processing fee|security fee|upfront fee|payment required|fee)\b",
    re.IGNORECASE
)


def analyze_text(description: str) -> list[dict]:
    """Return one finding per matching rule, with simple negation handling."""
    text = re.sub(r"\s+", " ", description).strip()
    lower = text.lower()
    findings = []

    for rule in TEXT_RULES:
        pattern = rule["pattern"]
        if not pattern:
            continue

        match = re.search(pattern, lower, flags=re.IGNORECASE)
        if not match:
            continue

        # Avoid flagging common reassuring statements such as "no registration fee".
        matched_text = match.group(0)
        if rule["id"] == "upfront_fee" and NEGATION_RE.search(lower):
            continue

        findings.append({
            "id": rule["id"],
            "title": rule["title"],
            "points": rule["points"],
            "explanation": rule["explanation"],
            "evidence": matched_text[:180],
            "source": "advertisement text"
        })

    meaningful_words = re.findall(r"\b[a-zA-Z]{3,}\b", text)
    responsibility_terms = [
        "responsibilit", "develop", "design", "analy", "assist", "build",
        "research", "test", "project", "task", "work", "skill", "python",
        "marketing", "software", "data", "content"
    ]
    has_work_details = any(term in lower for term in responsibility_terms)
    if len(meaningful_words) >= 8 and not has_work_details:
        findings.append({
            "id": "vague_work",
            "title": "Vague or missing work details",
            "points": 5,
            "explanation": TEXT_RULES[-1]["explanation"],
            "evidence": "Few recognizable responsibility or skill terms were found.",
            "source": "advertisement text"
        })

    return findings
