from flask import Blueprint, flash, redirect, render_template, session, url_for
from werkzeug.security import check_password_hash

from forms import LoginForm
from models import User
from utils import login_required, log_action


auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower().strip(), active=True).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            session.clear()
            session["user_id"] = user.id
            session["user_name"] = user.name
            session["role"] = user.role
            log_action("Signed in")
            flash(f"Welcome back, {user.name}.", "success")
            return redirect(url_for("dashboard.dashboard"))
        flash("Invalid email or password.", "danger")
    return render_template("auth/login.html", form=form)


@auth_bp.route("/logout")
@login_required
def logout():
    log_action("Signed out")
    session.clear()
    flash("You have been signed out.", "info")
    return redirect(url_for("auth.login"))
