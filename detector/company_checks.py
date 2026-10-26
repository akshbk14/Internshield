import re
from urllib.parse import urlparse


def _domain_from_url(value: str) -> str:
    value = value.strip()
    if not value:
        return ""
    if "://" not in value:
        value = "https://" + value
    try:
        host = urlparse(value).hostname or ""
        host = host.lower().strip(".")
        return host[4:] if host.startswith("www.") else host
    except ValueError:
        return ""


def _email_domain(value: str) -> str:
    value = value.strip().lower()
    if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", value):
        return ""
    return value.rsplit("@", 1)[1]


def check_company_details(company_name="", website="", recruiter_email="", stipend="", payment_requested=False):
    findings = []

    if payment_requested:
        findings.append({
            "id": "upfront_fee",
            "title": "Applicant reports an upfront payment request",
            "points": 30,
            "explanation": "You indicated that the opportunity asks you to pay a fee. This deserves careful independent verification.",
            "evidence": "Payment requested: Yes",
            "source": "user-provided form"
        })

    site_domain = _domain_from_url(website)
    email_domain = _email_domain(recruiter_email)

    if website and not site_domain:
        findings.append({
            "id": "invalid_website",
            "title": "Website address could not be parsed",
            "points": 5,
            "explanation": "The website value does not look like a valid web address.",
            "evidence": website[:180],
            "source": "user-provided form"
        })

    if recruiter_email and not email_domain:
        findings.append({
            "id": "invalid_email",
            "title": "Recruiter email format looks invalid",
            "points": 5,
            "explanation": "The recruiter email does not match a basic email format.",
            "evidence": recruiter_email[:180],
            "source": "user-provided form"
        })

    if site_domain and email_domain and site_domain != email_domain:
        # This is only a literal domain mismatch check; it does not understand corporate groups,
        # recruitment agencies, subdomains, or legitimate third-party hiring platforms.
        site_root = site_domain.removeprefix("www.")
        email_root = email_domain.removeprefix("www.")
        if site_root != email_root:
            findings.append({
                "id": "domain_mismatch",
                "title": "Recruiter email and website domains differ",
                "points": 10,
                "explanation": "The email domain differs from the website domain supplied. Legitimate recruiters may use separate hiring platforms, so verify independently.",
                "evidence": f"Website domain: {site_domain}; email domain: {email_domain}",
                "source": "user-provided form"
            })

    if not company_name and not website:
        findings.append({
            "id": "missing_company_details",
            "title": "Company details were not provided",
            "points": 5,
            "explanation": "Without a company name or website, there is less information available for this assessment.",
            "evidence": "Company name and website are both empty.",
            "source": "user-provided form"
        })

    if stipend:
        digits = re.sub(r"[^\d]", "", stipend)
        if digits and int(digits) >= 1000000:
            findings.append({
                "id": "extreme_stipend_entry",
                "title": "Stipend value needs clarification",
                "points": 5,
                "explanation": "The stipend entered is unusually large as a numeric value; confirm the amount and time period.",
                "evidence": f"Stipend entered: {stipend[:80]}",
                "source": "user-provided form"
            })

    return findings
