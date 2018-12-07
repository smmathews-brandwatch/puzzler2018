init:
	pipenv install --skip-lock

test-game:
	pipenv run python -m pygame.examples.aliens

test-server:
	pipenv run nosetests tests

run-server:
	pipenv run python server.py

all: init test-game test-server run-server