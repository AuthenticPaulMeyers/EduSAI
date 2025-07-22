from __future__ import print_function
from ..schema.models import Message, db, User
from ..constants.http_status_codes import HTTP_200_OK
from ..services.chat_model import create_chat
import africastalking
from dotenv import load_dotenv
import os
from ..constants.http_status_codes import HTTP_400_BAD_REQUEST, HTTP_200_OK

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
# def sms_response(recipientPhoneNumber, message):
#     api_key = os.getenv('SANDBOX_API_KEY')
#     if not api_key:
#         return {'error': 'Invalid SANDBOX API_KEY'}, HTTP_400_BAD_REQUEST
#     response = requests.post(AT_URL,
#         headers={
#             "Accept": "application/json",
#             "apiKey": os.getenv('SANDBOX_API_KEY'),
#             "Content-Type": "application/json"
#         },
#         json={
#             "username": "sandbox",
#             "message": message,
#             "from": "3567",
#             "phoneNumbers": [recipientPhoneNumber]
#         }
#     )
#     print(os.getenv('SANDBOX_API_KEY'))
#     print(response.status_code)
#     print(response.text)
#     return response, HTTP_200_OK

class SMS:
    def __init__(self):
		# Set app credentials
        self.username = "sandbox"
        self.api_key = os.getenv('SANDBOX_API_KEY')

        # Initialize the SDK
        africastalking.initialize(self.username, self.api_key)

        # Get the SMS service
        self.sms = africastalking.SMS

    def send(self, phoneNumber, message, senderShortCode):
        try:
            response = self.sms.send(message, [phoneNumber], senderShortCode)
            print (response)
            return response
        except Exception as e:
            print ('Encountered an error while sending: %s' % str(e))
            return ('Encountered an error while sending: %s' % str(e))