.PHONY: docs

init:
	pip install --upgrade pipenv
	pipenv install --dev

test:
	# This runs all of the tests, on both Python 2 and Python 3
	tox

test-readme:
	@pipenv run python setup.py check --restructuredtext --strict && ([ $$? -eq 0 ] && echo "README.rst and HISTORY.rst ok") || echo "Invalid markup in README.rst or HISTORY.rst!"

flake8:
	pipenv run flake8 couchutils

coverage:
	pipenv run pytest --cov

publish:
	pip install --upgrade twine
	python setup.py sdist bdist_wheel
	twine upload dist/*
	rm -fr .eggs build dist couchutils.egg-info
