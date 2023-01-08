HOST=0.0.0.0
PORT=80

.PHONY: run-app
run-app:
	uvicorn chatbot_api.main:app --host $(HOST) --port $(PORT)

.PHONY: run-app-dev
run-app-dev:
	uvicorn chatbot_api.main:app --host $(HOST) --port $(PORT) --reload
