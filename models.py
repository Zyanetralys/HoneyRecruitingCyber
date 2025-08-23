from datetime import datetime
from app import db
from sqlalchemy import func

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    session_id = db.Column(db.String(128), nullable=False)
    total_score = db.Column(db.Integer, default=0)
    skill_level = db.Column(db.String(20), default='Principiante')
    first_seen = db.Column(db.DateTime, default=datetime.utcnow)
    last_active = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    messages = db.relationship('Message', backref='user', lazy=True, cascade='all, delete-orphan')
    keywords_detected = db.relationship('KeywordDetection', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def update_skill_level(self):
        """Update skill level based on total score"""
        if self.total_score >= 151:
            self.skill_level = 'Avanzado'
        elif self.total_score >= 51:
            self.skill_level = 'Intermedio'
        else:
            self.skill_level = 'Principiante'
    
    def __repr__(self):
        return f'<User {self.username}>'

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    bot_name = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text, nullable=False)
    is_user_message = db.Column(db.Boolean, default=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    score_added = db.Column(db.Integer, default=0)
    
    def __repr__(self):
        return f'<Message {self.id}>'

class KeywordDetection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message_id = db.Column(db.Integer, db.ForeignKey('message.id'), nullable=False)
    keyword = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    points = db.Column(db.Integer, default=0)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<KeywordDetection {self.keyword}>'

class BotActivity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bot_name = db.Column(db.String(50), nullable=False)
    action = db.Column(db.String(100), nullable=False)
    target_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    details = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<BotActivity {self.bot_name}: {self.action}>'
