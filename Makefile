init:
	pipenv install --skip-lock

test-game:
	pipenv run python -m pygame.examples.aliens