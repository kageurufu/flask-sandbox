try:
    import unittest2 as unittest
except ImportError:
    import unittest

from flask import Flask, Blueprint
from flask.ext.sandbox import Sandbox
from flask.ext.login import LoginManager, UserMixin, login_user, \
    current_user, logout_user, make_secure_token


class User(UserMixin):

    def __init__(self, id, name, type="User", admin=False, active=True):
        self.id = id
        self.name = name
        self.type = type
        self.admin = admin
        self.active = active

        def get_id(self):
            return self.id

        def is_active(self):
            return self.active

        def get_auth_token(self):
            return make_secure_token(self.name, key="deterministic")

frank = User(1, "Frank", "User", True)
notch = User(2, "Notch", "Dev", True)
pig = User(3, "Pig", "Dev", False)
steve = User(4, "Steve", "User", False)
creeper = User(5, "Creeper", "User", False, False)

USERS = {
    1: frank,
    2: notch,
    3: pig,
    4: steve,
    5: creeper
}


class InitializationTestCase(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.login = LoginManager(self.app)

    def test_init_app(self):
        sandbox = Sandbox()
        sandbox.init_app(self.app)
        self.assertIsInstance(sandbox, Sandbox)

    def test_class_init(self):
        sandbox = Sandbox(self.app)
        self.assertIsInstance(sandbox, Sandbox)

    def test_setup_app(self):
        sandbox = Sandbox()
        sandbox.setup_app(self.app)
        self.assertIsInstance(sandbox, Sandbox)


class testBasicFiltering(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = 'deterministic'
        self.app.config['TESTING'] = True
        self.login = LoginManager(self.app)
        self.sandbox = Sandbox(self.app)

        @self.login.user_loader
        def load_user(id):
            return USERS[int(id)]

        @self.app.route("/")
        def index():
            return u'Welcome'

        @self.app.route("/login-frank")
        def login_frank():
            return unicode(login_user(frank))

        @self.app.route("/login-notch")
        def login_notch():
            return unicode(login_user(notch))

        @self.app.route("/login-pig")
        def login_pig():
            return unicode(login_user(pig))

        @self.app.route("/login-steve")
        def login_steve():
            return unicode(login_user(steve))

        @self.app.route("/login-creeper")
        def login_creeper():
            return unicode(login_user(creeper))

        @self.app.route("/logout")
        def logout():
            return logout_user()

        @self.app.route("/current_user")
        def currentuser():
            return current_user.name

        @self.app.route("/admin")
        @self.sandbox(lambda u: u.admin)
        def admin():
            return "admin"

        @self.app.route("/user")
        @self.sandbox(lambda u: u.type == 'User')
        def user():
            return "user"

        @self.app.route("/dev")
        @self.sandbox(lambda u: u.type == "Dev")
        def dev():
            return "dev"

    def test_unauth_user(self):
        with self.app.test_client() as c:
            result = c.get("/user")
            self.assertEqual(result.status, '403 FORBIDDEN')

    def test_user(self):
        with self.app.test_client() as c:
            c.get("/login-steve")
            current = c.get("/current_user")
            self.assertEquals(current.data.decode("utf-8"), "Steve")
            dev = c.get('/dev')
            user = c.get('/user')
            admin = c.get('/admin')
            self.assertEquals(dev.status, '403 FORBIDDEN')
            self.assertEquals(user.data.decode("utf-8"), "user")
            self.assertEquals(admin.status, '403 FORBIDDEN')

    def test_dev(self):
        with self.app.test_client() as c:
            c.get("/login-pig")
            current = c.get("/current_user")
            self.assertEquals(current.data.decode("utf-8"), "Pig")
            dev = c.get('/dev')
            user = c.get('/user')
            admin = c.get('/admin')
            self.assertEquals(dev.data.decode("utf-8"), "dev")
            self.assertEquals(user.status, "403 FORBIDDEN")
            self.assertEquals(admin.status, "403 FORBIDDEN")

    def test_user_admin(self):
        with self.app.test_client() as c:
            c.get("/login-frank")
            current = c.get("/current_user")
            self.assertEquals(current.data.decode("utf-8"), "Frank")
            dev = c.get('/dev')
            user = c.get('/user')
            admin = c.get('/admin')
            self.assertEquals(dev.status, '403 FORBIDDEN')
            self.assertEquals(user.data.decode("utf-8"), "user")
            self.assertEquals(admin.data.decode("utf-8"), "admin")

    def test_dev_admin(self):
        with self.app.test_client() as c:
            c.get("/login-notch")
            current = c.get("/current_user")
            self.assertEquals(current.data.decode("utf-8"), "Notch")
            dev = c.get('/dev')
            user = c.get('/user')
            admin = c.get('/admin')
            self.assertEquals(dev.data.decode("utf-8"), "dev")
            self.assertEquals(user.status, "403 FORBIDDEN")
            self.assertEquals(admin.data.decode("utf-8"), "admin")


class testBlueprintFiltering(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = 'deterministic'
        self.app.config['TESTING'] = True
        self.login = LoginManager(self.app)
        self.sandbox = Sandbox(self.app)

        @self.login.user_loader
        def load_user(id):
            return USERS[int(id)]

        @self.app.route("/")
        def index():
            return u'Welcome'

        self.login_blueprint = Blueprint("login", __name__)
        self.user_blueprint = Blueprint("user", __name__)
        self.dev_blueprint = Blueprint("dev", __name__)
        self.admin_blueprint = Blueprint("admin", __name__)

        @self.login_blueprint.route("/login-frank")
        def login_frank():
            return unicode(login_user(frank))

        @self.login_blueprint.route("/login-notch")
        def login_notch():
            return unicode(login_user(notch))

        @self.login_blueprint.route("/login-pig")
        def login_pig():
            return unicode(login_user(pig))

        @self.login_blueprint.route("/login-steve")
        def login_steve():
            return unicode(login_user(steve))

        @self.login_blueprint.route("/login-creeper")
        def login_creeper():
            return unicode(login_user(creeper))

        @self.login_blueprint.route("/logout")
        def logout():
            return logout_user()

        @self.app.route("/current_user")
        def currentuser():
            return current_user.name

        @self.admin_blueprint.route("/admin")
        @self.sandbox(lambda u: u.admin)
        def admin():
            return "admin"

        @self.user_blueprint.route("/user")
        @self.sandbox(lambda u: u.type == 'User')
        def user():
            return "user"

        @self.dev_blueprint.route("/dev")
        @self.sandbox(lambda u: u.type == "Dev")
        def dev():
            return "dev"

        self.sandbox.register_blueprint(self.login_blueprint)
        self.sandbox.register_blueprint(
            self.admin_blueprint, lambda u: u.admin)
        self.sandbox.register_blueprint(
            self.user_blueprint, lambda u: u.type == 'User')
        self.sandbox.register_blueprint(
            self.dev_blueprint, lambda u: u.type == 'Dev')

    def test_unauth_user(self):
        with self.app.test_client() as c:
            result = c.get("/user")
            self.assertEqual(result.status, '403 FORBIDDEN')

    def test_user(self):
        with self.app.test_client() as c:
            c.get("/login-steve")
            current = c.get("/current_user")
            self.assertEquals(current.data.decode("utf-8"), "Steve")
            dev = c.get('/dev')
            user = c.get('/user')
            admin = c.get('/admin')
            self.assertEquals(dev.status, '403 FORBIDDEN')
            self.assertEquals(user.data.decode("utf-8"), "user")
            self.assertEquals(admin.status, '403 FORBIDDEN')

    def test_dev(self):
        with self.app.test_client() as c:
            c.get("/login-pig")
            current = c.get("/current_user")
            self.assertEquals(current.data.decode("utf-8"), "Pig")
            dev = c.get('/dev')
            user = c.get('/user')
            admin = c.get('/admin')
            self.assertEquals(dev.data.decode("utf-8"), "dev")
            self.assertEquals(user.status, "403 FORBIDDEN")
            self.assertEquals(admin.status, "403 FORBIDDEN")

    def test_user_admin(self):
        with self.app.test_client() as c:
            c.get("/login-frank")
            current = c.get("/current_user")
            self.assertEquals(current.data.decode("utf-8"), "Frank")
            dev = c.get('/dev')
            user = c.get('/user')
            admin = c.get('/admin')
            self.assertEquals(dev.status, '403 FORBIDDEN')
            self.assertEquals(user.data.decode("utf-8"), "user")
            self.assertEquals(admin.data.decode("utf-8"), "admin")

    def test_dev_admin(self):
        with self.app.test_client() as c:
            c.get("/login-notch")
            current = c.get("/current_user")
            self.assertEquals(current.data.decode("utf-8"), "Notch")
            dev = c.get('/dev')
            user = c.get('/user')
            admin = c.get('/admin')
            self.assertEquals(dev.data.decode("utf-8"), "dev")
            self.assertEquals(user.status, "403 FORBIDDEN")
            self.assertEquals(admin.data.decode("utf-8"), "admin")
