flask-sandbox
=============

A Flask plugin to restrict blueprints to specific users, this depends on flask-login's current_user, so that is required

Goals of this extension are simple code, extendable code, and readability. So far, its only 31 lines of code


Usage
=====

    from flask import Flask, Blueprint, redirect
    from flask.ext.login import LoginManager
    from flask.ext.sandbox import Sandbox

    app = Flask(__name__)
    login_manager = LoginManager(app)
    sandbox = Sandbox(app)

    @app.route("/protected/admin/page")
    @sandbox(lambda user: user.admin)
    def protected_admin_page():
        return render_template("admin.jinja")

    blueprint = Blueprint("admin", __name__)

    @blueprint.route("/admin")
    def admin():
        return render_template("admin.jinja")

    sandbox.register_blueprint(blueprint, lambda user: user.admin == True, redirect("/"))