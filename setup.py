'''
    Flask-Sandbox
    -------------

    Flask-Sandbox provides basic ACL permissions controls on
    a per-route or per-blueprint basis. This is not bound to
    any user type, but uses lambda functions or closures
    passed to it's decorator or register_blueprint
'''


import os
import sys

from setuptools import setup

module_path = os.path.join(os.path.dirname(__file__), 'flask_sandbox.py')
version_line = [line for line in open(module_path)
                if line.startswith('__version_info__')][0]

__version__ = '.'.join(eval(version_line.split('__version_info__ = ')[-1]))

if sys.argv[-1] == 'test':
    status = os.system("make check")
    status >>= 8
    sys.exit(status)

setup(name='Flask-Sandbox',
      version=__version__,
      url='https://github.com/kageurufu/flask-sandbox',
      license='MIT',
      author='Frank Tackitt',
      author_email='franklyn@tackitt.net',
      description='ACL Route controls for Flask',
      long_description=__doc__,
      py_modules=['flask_sandbox'],
      zip_safe=False,
      platforms='any',
      install_requires=['Flask', 'Flask-Login'],
      classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Web Environment',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Framework :: Flask'
      ])
