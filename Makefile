# anaconda requires the use of pythonw for pygame, so check for that
pythonType=python
VER=$(shell python --version 2>&1)
ifneq "$(findstring Anaconda, $(VER))" ""
pythonType=pythonw
endif

init:
	pipenv install --skip-lock

test-visualizer:
	pipenv run $(pythonType) -m pygame.examples.aliens

run-visualizer:
	pipenv run ${pythonType} -m visualizer

test-server:
	pipenv run nosetests tests

print-routes:
	FLASK_APP=server.py pipenv run flask routes

run-server:
	pipenv run python -m server
