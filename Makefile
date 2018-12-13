
# anaconda requires the use of pythonw for pygame, so check for that
pythonType=python
ifneq (, $(shell which pythonw))
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

run-base-bot:
	pipenv run python -m baseBot

run-your-bot:
	pipenv run python -m yourBot
	
install-js-bot:
	npm install javascript-client
	npm link javascript-client

run-your-js-bot:
	node yourBot.js