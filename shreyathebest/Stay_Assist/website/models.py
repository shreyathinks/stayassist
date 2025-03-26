from website import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import json
from website import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    phone_number = db.Column(db.String(20))
    hostel = db.Column(db.String(100))
    block = db.Column(db.String(50))
    room_number = db.Column(db.String(20))
    service_requests = db.relationship('ServiceRequest', backref='user', lazy=True)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

class ServiceRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    service_type = db.Column(db.String(50), nullable=False)
    issue_description = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='pending')
    service_data = db.Column(db.Text)  # Store as JSON
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, **kwargs):
        super(ServiceRequest, self).__init__(**kwargs)
        if self.service_data is None:
            self.service_data = json.dumps({})

    def get_service_data(self):
        return json.loads(self.service_data) if self.service_data else {}

    def set_service_data(self, data):
        self.service_data = json.dumps(data)