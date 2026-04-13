from flask import jsonify, g

@app.route('/account/<int:user_id>')
def get_account(user_id):
    if not getattr(g, "current_user", None):
        return jsonify({"error": "Authentication required"}), 401

    is_owner = g.current_user.id == user_id
    is_admin = getattr(g.current_user, "role", None) == "admin"

    if not is_owner and not is_admin:
        return jsonify({"error": "Forbidden"}), 403

    user = db.session.query(User).filter_by(id=user_id).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({
        "id": user.id,
        "username": user.username,
        "email": user.email
    })