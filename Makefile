API_PORT=80
CONTAINER_NAME=chatbot-api
HOST=0.0.0.0
IMAGE=chatbot-api-img
TAG=latest

DOCKER_IMG=$(IMAGE):$(TAG)
DOCKER_PORT=$(API_PORT):$(API_PORT)


.PHONY: run-app
run-app:
	uvicorn chatbot_api.main:app --host $(HOST) --port $(API_PORT)

.PHONY: run-app-dev
run-app-dev:
	uvicorn chatbot_api.main:app --host $(HOST) --port $(API_PORT) --reload

.PHONY: build-docker-img
build-docker-img:
	docker build --no-cache -t $(DOCKER_IMG) .

.PHONY: run-docker-img
run-docker-img:
	docker run --name $(CONTAINER_NAME) -d -p $(API_PORT):$(API_PORT) $(DOCKER_IMG)
