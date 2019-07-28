freeze-deps:
	pip freeze > requirements.txt

install-deps:
	pip install -r requirements.txt

run-tests:
	coverage erase
	coverage run -m unittest discover -p '*_test.py'
	coverage report -m

validate:
	make run-tests

clean-dist:
	rm -rf build
	rm -rf dist

publish-test:
	make clean-dist
	make validate
	pip install setuptools wheel twine
	python setup.py sdist bdist_wheel
	python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/* --verbose

publish-prod:
	make clean-dist
	make validate
	pip install setuptools wheel twine
	python setup.py sdist bdist_wheel
	python -m twine upload dist/* --verbose