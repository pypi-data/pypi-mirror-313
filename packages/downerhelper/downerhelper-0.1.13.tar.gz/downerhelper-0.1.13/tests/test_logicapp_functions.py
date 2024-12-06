import pytest
from downerhelper.logicapp import send_email
from downerhelper.secrets import get_key_url
import os
import base64
import logging

file_name = "temp.txt"

def test_send_email(keyvault_url):
    key_url = get_key_url(os.getenv('SEND_EMAIL_SECRET'), keyvault_url, None)
    recipients = ["marcus.oates@downergroup.com"] * 2
    subject = "Pytest Email"
    body = "This is a test email sent from a pytest"

    assert send_email(key_url, recipients, subject, body)

    with pytest.raises(Exception):
        send_email(None, recipients, subject, body)

    with pytest.raises(Exception):
        send_email(key_url, "", subject, body)

    attachments = []
    with open(file_name, 'rb') as file:
        attachments.append({
            "Name": file_name,
            "ContentBytes": base64.b64encode(file.read()).decode('utf-8')
        })
    with open(file_name, 'rb') as file:
        attachments.append({
            "Name": file_name,
            "ContentBytes": file.read()
        })

    assert send_email(key_url, recipients, subject, body, attachments=attachments)
    
    cc=bcc=recipients

    assert send_email(key_url, recipients, subject, body, cc=cc, bcc=bcc)

    recipients=cc=bcc=";".join(recipients)

    assert send_email(key_url, recipients, subject, body, cc=cc, bcc=bcc)

    for importance in ["Normal", "Low", "High"]:
        assert send_email(key_url, recipients, subject, body, importance=importance)