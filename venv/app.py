from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

# Configuración de la base de datos
if os.getenv('FLASK_ENV') == 'testing':
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['TESTING'] = os.getenv('FLASK_ENV') == 'testing'

db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime, nullable=True)

    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'completed': self.completed,
            'created_at': self.created_at,
            'completed_at': self.completed_at
        }

@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([task.serialize() for task in tasks])

@app.route('/tasks', methods=['POST'])
def add_task():
    data = request.get_json()
    if data['title']:
        new_task = Task(title=data['title'])
        db.session.add(new_task)
        db.session.commit()
        return jsonify(new_task.serialize())
    return jsonify({'error': 'Task needs title'}), 400

@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    task = Task.query.session.get(Task,id)
    if task:
        if request.json.get('title'):
            task.title = request.json.get('title')
        task.completed = request.json.get('completed', task.completed)
        task.completed_at = datetime.utcnow() if task.completed else None
        db.session.commit()
        return jsonify(task.serialize())
    return jsonify({'error': 'Task not found'}), 404

@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    task = Task.query.session.get(Task,id)
    if task:
        db.session.delete(task)
        db.session.commit()
        return '', 204
    return jsonify({'error': 'Task not found'}), 404

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
