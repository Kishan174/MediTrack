from functools import wraps

from flask import flash, redirect, session, url_for

from models import AuditLog, db


def current_user():
    if "user_id" not in session:
        return None
    return {"id": session["user_id"], "name": session["user_name"], "role": session["role"]}


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if "user_id" not in session:
            flash("Please sign in to continue.", "warning")
            return redirect(url_for("auth.login"))
        return view(*args, **kwargs)
    return wrapped


def roles_required(*roles):
    def decorator(view):
        @wraps(view)
        def wrapped(*args, **kwargs):
            if "user_id" not in session:
                flash("Please sign in to continue.", "warning")
                return redirect(url_for("auth.login"))
            if session.get("role") not in roles:
                flash("You do not have permission for that action.", "danger")
                return redirect(url_for("dashboard.dashboard"))
            return view(*args, **kwargs)
        return wrapped
    return decorator


def log_action(action):
    user_name = session.get("user_name", "System")
    db.session.add(AuditLog(user_name=user_name, action=action))
    db.session.commit()
