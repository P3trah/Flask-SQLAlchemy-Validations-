from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()

class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    phone_number = db.Column(db.String(10))

    @validates('phone_number')
    def validate_phone_number(self, key, phone_number):
        if len(phone_number) != 10 or not phone_number.isdigit():
            raise ValueError('Phone number must be exactly ten digits.')
        return phone_number

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    summary = db.Column(db.String(255))
    category = db.Column(db.Enum('Fiction', 'Non-Fiction'), nullable=False)

    @validates('title')
    def validate_title(self, key, title):
        clickbait_words = ["Won't Believe", "Secret", "Top", "Guess"]
        if not any(word in title for word in clickbait_words):
            raise ValueError('Title must contain one of: "Won\'t Believe", "Secret", "Top", "Guess"')
        return title

    @validates('content')
    def validate_content(self, key, content):
        if len(content) < 250:
            raise ValueError('Content must be at least 250 characters long.')
        return content

    @validates('summary')
    def validate_summary(self, key, summary):
        if summary and len(summary) > 250:
            raise ValueError('Summary must be a maximum of 250 characters.')
        return summary
