from flask import request, jsonify, Blueprint, Response
from ..constants.http_status_codes import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_200_OK, HTTP_201_CREATED
from ..utils.functionalities import handle_ai_chat
from app import limiter, get_remote_address
import os
from ..schema.models import User
from dotenv import load_dotenv
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse

load_dotenv(override=True)

sms_bp = Blueprint('sms', __name__, url_prefix='/v1.0')

LANGUAGES = ['Chichewa', 'English']

# setup twilio
account_sid = os.environ["TWILIO_ACCOUNT_SID"]
auth_token = os.environ["TWILIO_AUTH_TOKEN"]
client = Client(account_sid, auth_token)

@sms_bp.route('/edusai', methods=['POST'])
@limiter.limit("50 per hour", key_func=get_remote_address)
def sms_and_ussd():

    # Get the phone number of the user from the request
    user_phone = request.form.get('From')
    # fetch user_id from the database using the phone number 
    user = User.query.filter_by(phonenumber=user_phone).first()
    user_id = user.id if user else None

    # Placeholder
    language = 'English'

    if language not in LANGUAGES:
        return jsonify({'error': 'Invalid language.'}), HTTP_400_BAD_REQUEST

    user_message = request.form.get('Body')
    resp = MessagingResponse()

    data = handle_ai_chat(language, user_id, user_message)
    # get the last message from the list of messages

    messages = data[0]
    assistant_message = messages[-1].get('content', messages[-1]) if isinstance(messages[-1], dict) else messages[-1]

    resp.message(assistant_message)

    print(assistant_message)

    # Return the TwiML (as XML) response
    return Response(str(resp), mimetype='text/xml')




    

        

    

