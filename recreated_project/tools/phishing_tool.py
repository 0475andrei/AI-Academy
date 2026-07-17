import re

def analyze_phishing_email(email: str) -> dict:
    """
    Performs a simple phishing analysis on an email.
    Returns a structured report.
    """
    
    score = 0
    indicators = []
    
    suspicious_words = [
        'urgent', 
        'immediate action',
        'verify your account',
        'click here',
        'password',
        'login',
        'bank',
        'account',
        'suspend',
        'update'
]
    
    for word in suspicious_words:
        if word.lower() in email.lower():
            score += 1
            indicators.append(f"Contains suspicious word: {word}")
    
    urls= re.findall(r'(https?://[^\s]+)', email)
    
    if urls:
        score += 1
        indicators.append(f"Contains {len(urls)} suspicious URL(s)")
    if "@" not in email:
        score += 1
        indicators.append("No sender email detected")
    
    if score >= 5:
        risk = "High"
    elif score >= 3:
        risk = "Medium"
    else:
        risk = "Low"
        
    return {
        "risk": risk,
        "score": score,
        "indicators": indicators,}


class PhishingAnalysisTool:
    def __init__(self):
        self.name = "analyze_phishing_email"
        self.description = "Analyzes an email subject and body to determine if it is a phishing attempt."
        
        self.parameters = {
            "type": "object",
            "properties": {
                "subject": {"type": "string", "description": "The subject line of the email"},
                "body": {"type": "string", "description": "The main text of the email"}
            },
            "required": ["subject", "body"]
        }

    def callback(self, subject, body):
        subject_lower = subject.lower()
        if "urgent" in subject_lower or "password reset" in subject_lower:
            return "CRITICAL: High probability of phishing detected based on urgency indicators."
        
        return "Analysis complete: Proceed with standard caution."