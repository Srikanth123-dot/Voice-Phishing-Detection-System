def detect_vishing(text):
    text = text.lower()
    score = 0

    # English
    bill = ["pending bill","due payment","electricity bill","loan due"]
    urgency = ["pay immediately","today only","last chance","within 2 hours"]
    threat = ["service disconnected","account blocked","legal action"]
    payment = ["upi","otp","wallet","link","whatsapp"]

    # Telugu
    telugu_bill = ["పెండింగ్","బిల్","బాకీ","విద్యుత్"]
    telugu_urgency = ["వెంటనే","ఈరోజే","చివరి అవకాశం"]
    telugu_threat = ["కట్ చేస్తారు","బ్లాక్ చేస్తారు","లీగల్ యాక్షన్"]
    telugu_payment = ["upi","otp","లింక్","whatsapp"]

    for w in bill:
        if w in text: score += 2
    for w in urgency:
        if w in text: score += 3
    for w in threat:
        if w in text: score += 4
    for w in payment:
        if w in text: score += 5

    for w in telugu_bill:
        if w in text: score += 2
    for w in telugu_urgency:
        if w in text: score += 3
    for w in telugu_threat:
        if w in text: score += 4
    for w in telugu_payment:
        if w in text: score += 5

    return "⚠️ SCAM CALL" if score >= 7 else "✅ LIKELY SAFE"
