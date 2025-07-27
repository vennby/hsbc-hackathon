from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from functools import wraps
from dotenv import load_dotenv
import os
import openai
from models import db, create_demo_users, User
from llm_utils import get_hsbc_response

app = Flask(__name__)
load_dotenv()

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hsbc_demo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.getenv("FLASK_SECRET_KEY", "supersecret")

db.init_app(app)
openai.api_key = os.getenv("OPENAI_API_KEY")

with app.app_context():
    db.create_all()
    create_demo_users(db)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json() or request.form
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return jsonify({"error": "Username and password are required"}), 400

        from werkzeug.security import check_password_hash
        user = User.query.filter_by(name=username).first()

        if not user or not check_password_hash(user.password_hash, password):
            return jsonify({"error": "Invalid username or password"}), 401

        session['username'] = user.name
        session['user_id'] = user.id

        return jsonify({"message": "Login successful", "redirect_url": "/dashboard"})

    except Exception as e:
        app.logger.error(f"Login error: {str(e)}")
        return jsonify({"error": "An error occurred during login"}), 500

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route("/chat", methods=["POST"])
def chat():
    try:
        if request.content_type and request.content_type.startswith('multipart/form-data'):
            user_message = request.form.get("message")
        else:
            data = request.get_json(force=True)
            user_message = data.get("message")

        if not user_message:
            return jsonify({"reply": "Please enter a valid message."})

        username = session.get('username')
        user = User.query.filter_by(name=username).first() if username else None

        reply = get_hsbc_response(user_message, user=user)

        if isinstance(reply, dict):
            if reply.get("require_login") and not user:
                return jsonify({"reply": "Please log in to continue.", "require_login": True})
            return jsonify(reply)

        return jsonify({"reply": reply})

    except Exception as e:
        app.logger.error(f"Chat error: {str(e)}")
        return jsonify({"reply": "I apologize, but I encountered an error. Please try again."})

@app.route("/update-knowledge", methods=["POST"])
def update_knowledge():
    from updater import update_knowledge_base
    try:
        update_knowledge_base()
        return jsonify({"status": "Knowledge base updated."})
    except Exception as e:
        return jsonify({"status": f"Error: {e}"})

from updater import periodic_update
periodic_update(interval_hours=24)

if __name__ == "__main__":
    app.run(debug=True)

