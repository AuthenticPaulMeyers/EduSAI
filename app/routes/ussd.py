from flask import request, jsonify, Blueprint
from ..constants.http_status_codes import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_200_OK, HTTP_201_CREATED
from ..utils.functionalities import handle_ai_chat
from app import limiter, get_remote_address

sms_bp = Blueprint('sms', __name__, url_prefix='/v1.0')

LANGUAGES = ['Chichewa', 'English']

@sms_bp.route('/edusai', methods=['POST'])
@limiter.limit("50 per hour", key_func=get_remote_address)
def sms_and_ussd():

    user_id = 1
    
    user_message = request.json.get('content')
    if not user_message:
        return jsonify({'error': 'Input field should not be empty.'}), HTTP_400_BAD_REQUEST
    
    language = 'Chichewa'

    if language not in LANGUAGES:
        return jsonify({'error': 'Invalid language.'}), HTTP_400_BAD_REQUEST
    
    # Session variables for the ussd
    # sessionId = request.json.get('sessionId')
    # input = request.json.get('input')
    # service_code = request.json.get('serviceCode')
    # phoneNumber = request.json.get('phoneNumber')
    # # Determine the users current menu
    # if sessionId not in SESSIONS:
    return handle_ai_chat(language, user_id, user_message), HTTP_200_OK




    

        

    

