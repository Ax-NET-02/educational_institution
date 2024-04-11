from flask import Blueprint, url_for, redirect, session, flash

logout = Blueprint('logout', __name__)


@logout.route('/logout')
def quit():
    # 清除会话中的用户信息
    session.clear()
    flash("Log out successfully Goodbye", "success")
    return redirect(url_for('home.index'))