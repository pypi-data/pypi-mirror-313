import requests
import base64

def send_email(key_url, recipients, subject, body, attachments=[], cc=[], bcc=[], importance="Normal"):
    emails = {
        "recipients": recipients,
        "cc": cc,
        "bcc": bcc
    }
    for key, value in emails.items():
        if isinstance(value, str): continue
        emails[key] = ";".join(value)

    if importance not in ["Normal", "Low", "High"]: importance = "Normal"

    content_key = "ContentBytes"
    for data in attachments:
        if isinstance(data[content_key], str): continue
        data[content_key] = base64.b64encode(data[content_key]).decode("utf-8")
    
    response = requests.post(key_url[1],
        json={
            "recipients": emails['recipients'],
            "subject": subject,
            "body": body,
            "key": key_url[0],
            "attachments": attachments,
            "cc": emails['cc'],
            "bcc": emails['bcc'],
            "importance": importance
        })
    
    if response.ok: return True
    raise Exception(f"Error in logic app: {response.text}")