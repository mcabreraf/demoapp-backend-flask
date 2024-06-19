from flask import request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from config import app, db, jwt
from werkzeug.security import generate_password_hash, check_password_hash
from model import Contact, User

@app.route('/health')
def health_check():
    return 'Server is running!'

@app.route('/register', methods=['POST'])
def register():
    username  = request.json.get("username")
    password = request.json.get("password")
    full_name = request.json.get("fullName")

    if not username or not password or not full_name:
        return (
            jsonify({"error": "Missing data"}), 
            400
        )
    
    hashed_password = generate_password_hash(password)
    new_user = User(username=username, password=hashed_password, full_name=full_name)

    try:
        db.session.add(new_user)
        db.session.commit()

        return (
            jsonify({"message": "User created successfully"}),
            201
        )
    except Exception as e:
        return (
            jsonify({"error": str(e)}),
            400
        )

@app.route('/login', methods=['POST'])  
def login():
    username = request.json.get("username")
    password = request.json.get("password")

    user = db.session.query(User).filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        access_token = create_access_token(identity=user.id)
        return (
            jsonify(access_token=access_token)
        )
    
    return (
        jsonify({"error": "Invalid username or password"}), 
        401
    )

@app.route('/contacts', methods=['GET'])
@jwt_required()
def get_contacts():
    user_id = get_jwt_identity()
    contacts = db.session.query(Contact).filter_by(user_id=user_id).all()
    json_contacts = list(map(lambda x: x.to_json(), contacts))
    return (
        jsonify({"contacts": json_contacts}),
        200
    )

@app.route('/create_contact', methods=['POST'])
@jwt_required()
def create_contact():
    user_id = get_jwt_identity()
    first_name = request.json.get("firstName")
    last_name = request.json.get("lastName")
    email = request.json.get("email")

    if not first_name or not last_name or not email:
        return (
            jsonify({"error": "Missing data"}),
            400
        )
    
    contact = Contact(first_name=first_name, last_name=last_name, email=email, user_id=user_id)
    try:
        db.session.add(contact)
        db.session.commit()
    except Exception as e:
        return (
            jsonify({"error": str(e)}),
            400
        )
    
    return (
        jsonify({"message": "Contact created successfully"}),
        201
    )

@app.route('/update_contact/<int:contact_id>', methods=['PATCH'])
@jwt_required()
def update_contact(contact_id):
    user_id = get_jwt_identity()
    contact = db.session.query(Contact).filter_by(id=contact_id, user_id=user_id).first()

    if not contact:
        return (
            jsonify({"error": "Contact not found or you do not have permission to update this contact."}),
            404
        )
    
    data = request.json
    contact.first_name = data.get("firstName", contact.first_name)
    contact.last_name = data.get("lastName", contact.last_name)
    contact.email = data.get("email", contact.email)

    db.session.commit()

    return (
        jsonify({"message": "Contact updated successfully"}),
        200
    )

@app.route('/delete_contact/<int:contact_id>', methods=['DELETE'])
@jwt_required()
def delete_contact(contact_id):
    user_id = get_jwt_identity()
    contact = db.session.query(Contact).filter_by(id=contact_id, user_id=user_id).first()

    if not contact:
        return (
            jsonify({"error": "Contact not found or you do not have permission to update this contact."}),
            404
        )
    
    db.session.delete(contact)
    db.session.commit()

    return (
        jsonify({"message": "Contact deleted successfully"}),
        200
    )

@app.route('/validate-token', methods=['GET'])
@jwt_required()
def validate_token():
    try:
        user_id = get_jwt_identity()
        return (
            jsonify(valid=True), 
            200
        )
    except Exception as e:
        return (
            jsonify(valid=False, error=str(e)), 
            401
        )

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', debug=True)