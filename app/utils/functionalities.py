from __future__ import print_function
from ..schema.models import Message, db, User
from ..constants.http_status_codes import HTTP_200_OK
from ..services.chat_model import create_chat
import africastalking
from dotenv import load_dotenv
import os
from ..constants.http_status_codes import HTTP_200_OK

load_dotenv(override=True)

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

# responses to africas talking sms
class SMS:
    def __init__(self):
		# Set app credentials
        self.username = os.getenv("USERNAME")
        self.api_key = os.getenv('SANDBOX_API_KEY')

        # Initialize the SDK
        africastalking.initialize(self.username, self.api_key)

        # Get the SMS service
        self.sms = africastalking.SMS

    def send(self, phoneNumber, message, shortCode):
        try:
            formatted_phone_number = phoneNumber.strip().replace(" ", "")
            response = self.sms.send(message, [formatted_phone_number], shortCode)
            return response
        except Exception as e:
            return ('Error: %s' % str(e))

# A function to handle registration through USSD
def handle_ussd_registration(text):

  if text == '':
      # This is the first request.
      response  = "CON Welcome to EduSAI \n"
      response += "1 - Get started \n"
      response += "2 - Learn more \n"

  elif text == '1':
      response  = "END Thank you for your interest to start using EDuSAI. You will receive an SMS confirmation message shortly. \n"

  elif text == '2':
      response = "END EduSAI is an AI assistant to help you with your studies using SMS chats. \n"

  else :
      response = "END Invalid choice"

  # Send the response back to the API
  return response
