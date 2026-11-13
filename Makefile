up:
	docker compose up -d

down:
	docker compose down

dev:
	uv run uvicorn backend.api.server:app --reload 

start:
	uv run uvicorn backend.api.server:app 

production:
	uv sync --group cpu --no-group gpu

development:
	uv sync --group gpu --no-group cpu