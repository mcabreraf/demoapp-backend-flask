from flask import request, jsonify
from config import app, db
from model import Contact

@app.route('/')
def hello_world():
    return 'Hello, World! How are you doing today? I am doing great!'

@app.route('/contacts', methods=['GET'])
def get_contacts():
    contacts = db.session.query(Contact).all()
    json_contacts = list(map(lambda x: x.to_json(), contacts))
    return (
        jsonify({"contacts": json_contacts}),
        200
    )

@app.route('/create_contact', methods=['POST'])
def create_contact():
    first_name = request.json.get("firstName")
    last_name = request.json.get("lastName")
    email = request.json.get("email")

    if not first_name or not last_name or not email:
        return (
            jsonify({"error": "Missing data"}),
            400
        )
    
    contact = Contact(first_name=first_name, last_name=last_name, email=email)
    try:
        db.session.add(contact)
        db.session.commit()
    except Exception as e:
        return (
            jsonify({"error": str(e)}),
            400
        )
    
    return jsonify({"message": "Contact created successfully"}, 201)

@app.route('/update_contact/<int:user_id>', methods=['PATCH'])
def update_contact(user_id):
    contact = db.session.get(Contact, user_id)

    if not contact:
        return (
            jsonify({"error": "Contact not found"}),
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

@app.route('/delete_contact/<int:user_id>', methods=['DELETE'])
def delete_contact(user_id):
    contact = db.session.get(Contact, user_id)

    if not contact:
        return (
            jsonify({"error": "Contact not found"}),
            404
        )
    
    db.session.delete(contact)
    db.session.commit()

    return (
        jsonify({"message": "Contact deleted successfully"}),
        200
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)