.PHONY: all test clean_coverage clean pep8 pyflakes check

all:
	@echo 'test         run the unit tests'
	@echo 'coverage     generate coverage statistics'
	@echo 'pep8	        check for pep8 compliance'
	@echo 'pyflakes     check for unused imports'
	@echo 'check        make sure you are ready to commit'
	@echo 'clean        cleanup the source tree'

test: clean_coverage
	@echo 'Running all tests'
	@VERBOSE=1 PATH=${PATH} ./run-tests.sh

clean_coverage:
	@rm -f .coverage

pep8:
	@echo 'Checking pep8 compliance'
	@pep8 flask_sandbox.py test_sandbox.py

pyflakes:
	@echo 'Running pyflakes'
	@pyflakes flask_sandbox.py test_sandbox.py

check: pep8 pyflakes test