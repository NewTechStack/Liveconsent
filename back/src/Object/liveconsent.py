import requests
import uuid
import phonenumbers
from verify_email import verify_email

class liveconsent:
    def __init__(self):
        pass

    def sign(document_base64, recipients):
        request_id = str(uuid.uuid4())
        user_id = str(uuid.uuid4())
        if not isinstance(recipients, list):
            recipients = [recipients]
        if not all(isinstance(recipient, dict) for recipient in recipients):
            return [False, "Recipient invalid object type", 400]
        recipients_data = []
        for recipient in recipients:
            should_contain = ["email", "firstname", "lastname", "phone"]
            recipient_data = {
                "code_delivery": "email",
                "validation_method": "otvc",
                "signature_mode": "bulk",
                "signature_visual": "draw_it",
                "sms_request_delivery": True,
                "email": None,
                "firstname": None,
                "lastname": None,
                "phone": None
            }
            for data in should_contain:
                if not data in recipient:
                    return [False, f"Missing data: {data}", 400]
                if data == 'phone':
                    phone_number = recipient['phone']
                    phone = phonenumbers.parse(phone_number)
                    if phone_number[0] != '+' and not phonenumbers.is_possible_number(phone):
                        return [False, f"Invalid phone number {phone_number}", 400]
                if data == 'email':
                    email = recipient['phone']
                    if email is not verify_email(email):
                        return [False, f"Invalid email {email}", None]
                recipient_data[data] = recipient[data]
            recipients_data.append(recipient_data)
        url = "https://api.liveconsent.com/LCSWS/createrequest"
        payload = {
            "request": {
                "access_code_required": False,
                "request_create_draft": False,
                "signatures_order": False,
                "request_notify_signature": False,
                "request_validity_days": 30,
                "request_name": f"Request {request_id}",
                "unique_submit_id": f"user {user_id}"
            },
            "documents": [
                {
                    "document_content": "base64",
                    "document_filename": f"{document_base64}"
                }
            ],
            "recipients": recipients_data
        }
        headers = {
            "Accept": "application/json",
            "developer_key": "your developer_key",
            "authorization_token": "your authorization_token",
            "Content-Type": "application/json"
        }
        response = requests.request("POST", url, json=payload, headers=headers)
        print(response.text)
        return [True, {'request_id': request_id}, None]
