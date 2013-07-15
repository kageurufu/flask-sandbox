try:
	import unittest2 as unittest
except ImportError:
	import unittest

from flask import Flask, Blueprint, Response, session
from flask.ext.sandbox import Sandbox
class User(UserMixin):
	def __init__(self, name, id, type, active=True):
		self.id = id
		self.name = name
		self.type = type
		self.active = active

	def get_id(self):
		return self.id

	def is_active(self):
		return self.active

	def get_auth_token(self):
		return make_secure_token(self.name, key='deterministic')
	
	def is_active(self):
		return True

	def is_authenticated(self):
		return True

	def is_anonymous(self):
		return False

	def get_id(self):
		return self.id

	def __eq__(self, other):
		if isinstance(other, User):
			return self.get_id() == other.get_id()
		return NotImplemented

	def __ne__(self, other):
		equal = self.__eq__(other)
		if equal is NotImplemented:
			return NotImplemented
		return not equal


frank = User('Frank', 1, "admin")
chris = User('Chris', 2, "user")

USERS = {1: frank, 2: chris}
USER_TOKENS = dict((u.get_auth_token(), u) for u in USERS.values())

class InitializationTestCase(unittest.TestCase):
	def setUp(self):
		self.app = Flask(__name__)
		self.app.config['TESTING'] = True

	def test_init_app(self):
		login_manager = LoginManager()