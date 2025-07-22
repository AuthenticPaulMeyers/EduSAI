from flask import jsonify
from ..schema.models import Message, db, User
from ..constants.http_status_codes import HTTP_200_OK
from ..services.chat_model import create_chat
import requests
from dotenv import load_dotenv
import os

load_dotenv(override=True)

AT_URL = 'https://api.africastalking.com/version1/messaging/bulk'

# A function to handle sms chat logic
def handle_ai_chat(language, user_id, user_message):

    messages = [
        {
            "role": "system", 
            "content": f"""You are an assistant who teaches secondary school students from Malawi using the Malawi National Examination Board syllabus and The Ministry of education syllabus in Malawi. You teach in {language}. You answer questions precisely whilst maintaning child safety and educational ethics. Your responses are not outside of educational curricullum. Your responses are short not more than 170 characters. Answer these questions:"""
        }
    ]

    try:

        db.session.add(Message(user_id=user_id, content=user_message, role='user'))
        db.session.commit()

        history = Message.query.filter_by(user_id=user_id).order_by(Message.created_at).all()
        messages += [msg.to_dict() for msg in history]

        reply = create_chat(user_message, messages)

        db.session.add(Message(user_id=user_id, content=reply, role='assistant'))
        db.session.commit()

        conversation_history = Message.query.filter_by(user_id=user_id).order_by(Message.created_at).all()

        conversation_history_dicts = [msg.to_dict() for msg in conversation_history]

        return conversation_history_dicts, HTTP_200_OK
    except Exception as e:
        print(f'Error: {e}')
        return f"Error: {e}"


def handle_ussd_registration(fullname, phoneNumber):

    try: 
        db.session.add(User(fullname, phoneNumber))
        db.session.commit()
    except Exception as e:
        print(f"Error: {e}")
        return (f"Error: {e}")

# responses to africas talking sms

def sms_response(recipientPhoneNumber, message):
    requests.post(AT_URL,
        headers={
            "Accept": "application/json",
            "apiKey": os.getenv('SANDBOX_API_KEY'),
            "Content-Type": "application/json"
        },
        data={
            "username": "sandbox",
            "message": message,
            "from": "3567",
            "to": recipientPhoneNumber
        }
    )





# curl -X POST \
#     https://api.africastalking.com/version1/messaging/bulk \
#     -H 'Accept: application/json' \
#     -H 'Content-Type: application/json' \
#     -H 'apiKey: MyAppApiKey' \
#     -d '{
#     "username": "username",
#     "message": "This is a sample message.",
#     "senderId": "ABC",
#     "phoneNumbers": [
#         "+254711XXXYYY",
#         "+254711YYYZZZ"
#     ]
# }'
