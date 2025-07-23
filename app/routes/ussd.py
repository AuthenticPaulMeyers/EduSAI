from flask import request, jsonify, Blueprint
from ..constants.http_status_codes import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_200_OK, HTTP_201_CREATED
from ..utils.functionalities import handle_ai_chat, SMS
from app import limiter, get_remote_address
import os
from dotenv import load_dotenv

load_dotenv(override=True)

sms_bp = Blueprint('sms', __name__, url_prefix='/v1.0')

LANGUAGES = ['Chichewa', 'English']

# initiate the send sms class
send_sms = SMS()

@sms_bp.route('/edusai', methods=['POST'])
@limiter.limit("50 per hour", key_func=get_remote_address)
def sms_and_ussd():
    # Session variables for the ussd
    # sessionId = request.json.get('sessionId')
    # input = request.json.get('input')
    # service_code = request.json.get('serviceCode')
    # phoneNumber = request.json.get('phoneNumber')

    user_id = 1 # Placeholder
    shortcode = os.getenv('SHORTCODE')
    receipient_message = request.form.get('text')
    recipient = request.form.get('from')
    phoneNumber = recipient.strip().replace(" ", "")

    if not receipient_message or not recipient:
        return jsonify({'error': 'Required fields should not be empty.'}), HTTP_400_BAD_REQUEST
    
    # Placeholder
    language = 'English'

    if language not in LANGUAGES:
        return jsonify({'error': 'Invalid language.'}), HTTP_400_BAD_REQUEST

    print(phoneNumber)
    print(receipient_message)

    data = handle_ai_chat(language, user_id, receipient_message)
    # get the last message from the list of messages
    messages = data[0] 
    assistant_message = messages[-1]['content']

    response = send_sms.send(assistant_message, [phoneNumber], shortcode)
    print(response)

    return response, HTTP_200_OK




    

        

    

