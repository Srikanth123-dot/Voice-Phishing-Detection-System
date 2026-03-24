def detect_keywords(text):
    scam_keywords = {
        # English
        "otp": ["otp"],
        "upi": ["upi"],
        "account": ["account"],
        "blocked": ["blocked", "suspend"],
        "customer id": ["customer id"],
        "bank": ["bank"],
        "payment": ["payment", "pay"],
        "amazon": ["amazon"],
        "electricity bill": ["electricity", "bill"],

        # Telugu (spoken words that appear after STT)
        "ఖాతా (account)": ["ఖాతా"],
        "బ్లాక్ (blocked)": ["బ్లాక్"],
        "కస్టమర్ ఐడి (customer id)": ["ఐడి", "కస్టమర్"],
        "బ్యాంక్ (bank)": ["బ్యాంక్"],
        "చెల్లింపు (payment)": ["చెల్లింపు"],
        "బిల్ (bill)": ["బిల్"],
        "అమెజాన్ (amazon)": ["అమెజాన్"]
    }

    text_lower = text.lower()
    detected = []

    for label, variants in scam_keywords.items():
        for word in variants:
            if word.lower() in text_lower:
                detected.append(label)
                break

    return detected
