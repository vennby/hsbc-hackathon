from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(15))
    password_hash = db.Column(db.Text, nullable=False)
    annual_income = db.Column(db.Numeric(10, 2), default=0.00)
    employment_status = db.Column(db.String(30), default='Employed')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    accounts = db.relationship('Account', backref='user', lazy=True)
    cards = db.relationship('Card', backref='user', lazy=True)
    loans = db.relationship('Loan', backref='user', lazy=True)


class Account(db.Model):
    __tablename__ = 'accounts'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    account_number = db.Column(db.String(20), unique=True, nullable=False)
    account_type = db.Column(db.String(20))
    balance = db.Column(db.Numeric(15, 2), default=0.00)
    currency = db.Column(db.String(10), default='INR')
    status = db.Column(db.String(20), default='active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    cards = db.relationship('Card', backref='account', lazy=True)
    transactions = db.relationship('Transaction', backref='account', lazy=True)
    loans = db.relationship('Loan', backref='account', lazy=True)


class Card(db.Model):
    __tablename__ = 'cards'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'), nullable=False)
    card_number = db.Column(db.String(16), unique=True, nullable=False)
    card_type = db.Column(db.String(20))  # debit or credit
    status = db.Column(db.String(20), default='active')  # active, blocked, expired
    expiry_date = db.Column(db.Date)
    issued_at = db.Column(db.DateTime, default=datetime.utcnow)


class Loan(db.Model):
    __tablename__ = 'loans'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'), nullable=False)
    loan_type = db.Column(db.String(50))
    amount = db.Column(db.Numeric(15, 2), nullable=False)
    status = db.Column(db.String(20), default='pending')
    term_months = db.Column(db.Integer)
    interest_rate = db.Column(db.Numeric(5, 2))
    applied_at = db.Column(db.DateTime, default=datetime.utcnow)


class Transaction(db.Model):
    __tablename__ = 'transactions'
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'), nullable=False)
    amount = db.Column(db.Numeric(15, 2), nullable=False)
    type = db.Column(db.String(20))  # credit or debit
    description = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# Demo user data creation for development/testing
def create_demo_users(db):
    from werkzeug.security import generate_password_hash
    # Only create if not exists
    if not User.query.filter_by(email="alice@demo.com").first():
        alice = User(
            name="Alice Smith",
            email="alice@demo.com",
            phone="07123456789",
            password_hash=generate_password_hash("password123"),
            annual_income=42000.00,
            employment_status="Employed"
        )
        db.session.add(alice)
        db.session.commit()
    if not User.query.filter_by(email="bob@demo.com").first():
        bob = User(
            name="Bob Jones",
            email="bob@demo.com",
            phone="07987654321",
            password_hash=generate_password_hash("password456"),
            annual_income=35000.00,
            employment_status="Self-employed"
        )
        db.session.add(bob)
        db.session.commit()
