up:
	docker compose up -d

down:
	docker compose down

dev:
	uv run uvicorn backend.api.server:app --reload 

start:
	uv run uvicorn backend.api.server:app 
