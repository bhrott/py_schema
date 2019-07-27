#
# Lock the python dependencies and include in the requirements.txt
freeze-deps:
	pip freeze > requirements.txt

#
# Install the dependencies from requirements.txt
install-deps:
	pip install -r requirements.txt

run-tests:
	coverage erase
	coverage run -m unittest discover -p '*_test.py'
	coverage report -m