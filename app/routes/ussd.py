from flask import request, jsonify, Blueprint
from ..schema.models import db, Message, User, Language, Subject
from ..constants.http_status_codes import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_200_OK, HTTP_201_CREATED
from ..services.chat_model import create_chat
from flask_jwt_extended import jwt_required, get_jwt_identity
# from app import limiter, get_remote_address

sms_bp = Blueprint('sms', __name__, url_prefix='/v1.0')

LANGUAGES = ['Chichewa', 'English']

def handle_ussd_registration():
    pass

# character chat route
@sms_bp.route('/edusai', methods=['POST'])
# @limiter.limit("150 per hour", key_func=get_remote_address)
# @jwt_required()
def get_sms_and_ussd():

    user_id = 1
    
    user_message = request.json.get('content')
    if not user_message:
        return jsonify({'error': 'Input field should not be empty.'}), HTTP_400_BAD_REQUEST
    
    language = 'Chichewa'
    if language not in LANGUAGES:
        return jsonify({'error': 'Invalid language.'}), HTTP_400_BAD_REQUEST
    
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

        return jsonify({'response': conversation_history_dicts}), HTTP_200_OK
    except Exception as e:
        print(f'Error: {e}')
    pass

        

    

