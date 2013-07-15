from flask import (_request_ctx_stack, abort, current_app, flash, redirect, url_for, session, request)
from flask.signals import Namespace

class Sandbox(object):
	"""
	This object restricts users to a sandboxed area of the site, based on restrictions determined by their User object
	"""
	user_type_attr = "type"
	blueprints = {}
	redirect = None
	_app = None

	def __init__(self, app=None, user_type_attr = "type"):
		if app is not None:
			self.init_app(app, user_type_attr)

	def setup_app(self, app=None, user_type_attr = "type"):
		warnings.warn('Warning setup_app is deprecated. Please use init_app')
		self.init_app(app, user_type_attr)

	def init_app(self, app=None, user_type_attr = "type"):
		app.sandbox = self
		app.before_request(self.sandbox)
		self.user_type_attr = user_type_attr
		self._app = app

	def register_blueprint(self, blueprint, user_type, url_prefix = None, redirect = None):
		if not url_prefix:
			url_prefix = "/" + user_type
		if not redirect:
			redirect = self.redirect
		self._app.register_blueprint(blueprint, url_prefix = url_prefix)
		self.blueprints[blueprint.name] = {"type": user_type, "redirect": redirect}

	def sandbox(self):
		if _request_ctx_stack.top.request.blueprint not in self.blueprints:
			return
		bpn = _request_ctx_stack.top.request.blueprint
		bpd = self.blueprints[bpn]
		if not _request_ctx_stack.top.user.is_authenticated():
			return redirect(url_for(bpd['redirect']))
		if _request_ctx_stack.top.user.get(self.user_type_attr).lower() != bpd['type']:
			return redirect(url_for(bpd['redirect']))
		return