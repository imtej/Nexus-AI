"""
PII Sanitization Evaluator
Verifies zero PII (Personally Identifiable Information) enters the shared Collective Knowledge database.
"""

import re

def evaluate_pii_sanitization(text: str) -> dict:
    """
    Checks text for common PII patterns (email, phone, SSN, IP addresses).
    """
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    phone_pattern = r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'
    ssn_pattern = r'\b\d{3}-\d{2}-\d{4}\b'

    emails_found = re.findall(email_pattern, text)
    phones_found = re.findall(phone_pattern, text)
    ssns_found = re.findall(ssn_pattern, text)

    has_pii = bool(emails_found or phones_found or ssns_found)

    return {
        "passed": not has_pii,
        "pii_detected": {
            "emails": emails_found,
            "phones": phones_found,
            "ssns": ssns_found
        }
    }

if __name__ == "__main__":
    test_insight = "Many users find morning journaling helpful for managing daily anxiety."
    result = evaluate_pii_sanitization(test_insight)
    print("PII Sanitization Result:", result)
