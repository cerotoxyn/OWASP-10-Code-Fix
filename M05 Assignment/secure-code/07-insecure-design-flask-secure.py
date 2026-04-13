from datetime import datetime, timedelta
import secrets
from argon2 import PasswordHasher
from flask import request, jsonify

ph = PasswordHasher()

@app.route('/request-password-reset', methods=['POST'])
def request_password_reset():
    email = request.form.get('email', '').strip().lower()
    user = User.query.filter_by(email=email).first()

    if user:
        user.reset_token = secrets.token_urlsafe(32)
        user.reset_token_expires_at = datetime.utcnow() + timedelta(minutes=15)
        db.session.commit()
        # send email with reset link here

    return jsonify({"message": "If the account exists, a reset link has been sent."})

@app.route('/reset-password', methods=['POST'])
def reset_password():
    token = request.form.get('token', '')
    new_password = request.form.get('new_password', '')

    user = User.query.filter_by(reset_token=token).first()
    if not user or not user.reset_token_expires_at or user.reset_token_expires_at < datetime.utcnow():
        return jsonify({"error": "Invalid or expired token"}), 400

    user.password_hash = ph.hash(new_password)
    user.reset_token = None
    user.reset_token_expires_at = None
    db.session.commit()

    return jsonify({"message": "Password reset successful"})