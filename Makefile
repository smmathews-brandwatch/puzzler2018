#uncomment the w in the following line if you're running anaconda and see a grey box for the visualizer
pythonType=pythonw
init:
	pipenv install --skip-lock

test-visualizer:
	pipenv run ${pythonType} -m pygame.examples.aliens

run-visualizer:
	pipenv run ${pythonType} -m visualizer

test-server:
	pipenv run nosetests tests

print-routes:
	FLASK_APP=server.py pipenv run flask routes

run-server:
	pipenv run python -m server
