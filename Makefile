migrate:
	alembic revision --autogenerate
	alembic upgrade head

run:
	uvicorn main:app --reload