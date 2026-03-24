import smtplib
from email.message import EmailMessage
from datetime import datetime
import os


# =========================
# EMAIL CONFIGURATION
# =========================
SENDER_EMAIL = "s34256374@gmail.com"
APP_PASSWORD = "laathyohsscrkskc"   # ❗ No spaces
RECEIVER_EMAIL = "golaganisrikanth123@gmail.com"


# =========================
# SEND SCAM ALERT FUNCTION
# =========================
def send_scam_alert(phone_number,
                    audio_file_path,
                    scam_probability,
                    found_keywords,
                    found_sensitive,
                    decision):

    try:
        msg = EmailMessage()
        msg["Subject"] = "🚨 Vishing Scam Alert Detected"
        msg["From"] = SENDER_EMAIL
        msg["To"] = RECEIVER_EMAIL

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Format keywords
        keywords_text = ", ".join(found_keywords) if found_keywords else "None"

        # Format sensitive info
        if found_sensitive:
            sensitive_text = "\n".join(
                [f"{k}: {v}" for k, v in found_sensitive.items()]
            )
        else:
            sensitive_text = "None"

        # Email Body
        body = f"""
🚨 VISHING SCAM DETECTION ALERT 🚨

Time Detected: {timestamp}
Caller Phone Number: {phone_number}

ML Scam Probability: {scam_probability:.2f}%

Detected Keywords:
{keywords_text}

Sensitive Information Detected:
{sensitive_text}

Final Decision:
{decision}

The suspicious audio file is attached for further investigation.
"""

        msg.set_content(body)

        # Attach audio file
        if os.path.exists(audio_file_path):
            with open(audio_file_path, "rb") as f:
                file_data = f.read()
                file_name = os.path.basename(audio_file_path)

            msg.add_attachment(
                file_data,
                maintype="audio",
                subtype="wav",
                filename=file_name
            )

        # Send email
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(SENDER_EMAIL, APP_PASSWORD)
            smtp.send_message(msg)

        print("✅ Scam report email sent successfully!")

    except Exception as e:
        print("❌ Failed to send email.")
        print("Error:", e)