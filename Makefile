install:
	pip install -r requirements.txt
run-api:
	uvicorn app.api.main:app --reload --host 0.0.0.0 --port 8000
run-ui:
	python -m app.ui.flask_app
lint:
	flake8 app/
test:
	pytest tests/
build-docker:
	docker build -t rag-chatbot -f docker/Dockerfile .
