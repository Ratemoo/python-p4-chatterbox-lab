from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)
db.init_app(app)

@app.route('/messages', methods=['GET'])
def messages():
    """Retrieve all messages."""
    all_messages = Message.query.all()
    return jsonify([msg.to_dict() for msg in all_messages]), 200

@app.route('/messages/<int:id>', methods=['GET'])
def messages_by_id(id):
    """Retrieve a message by its ID."""
    message = Message.query.get_or_404(id)
    return jsonify(message.to_dict()), 200

@app.route('/messages', methods=['POST'])
def create_message():
    """Create a new message."""
    data = request.get_json()
    new_message = Message(body=data['body'], username=data['username'])
    db.session.add(new_message)
    db.session.commit()
    return jsonify(new_message.to_dict()), 201

@app.route('/messages/<int:id>', methods=['PATCH'])
def update_message(id):
    """Update a message by its ID."""
    data = request.get_json()
    message = Message.query.get_or_404(id)
    message.body = data['body']
    db.session.commit()
    return jsonify(message.to_dict()), 200

@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    """Delete a message by its ID."""
    message = Message.query.get_or_404(id)
    db.session.delete(message)
    db.session.commit()
    return '', 204

if __name__ == '__main__':
    app.run(port=5555, debug=True)
