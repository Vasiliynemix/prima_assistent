init:
	alembic init -t async migrations

create_db:
	createdb -h localhost -p 5432 -U $(user) $(db_name)

generate:
	alembic revision --m "$(name)" --autogenerate

migrate:
	alembic upgrade head

downgrade:
	alembic downgrade -1

ngrok:
	ngrok http --domain=factual-warthog-witty.ngrok-free.app 8080