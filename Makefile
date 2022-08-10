local_up:
	docker-compose -f docker-compose.local.yml up -d $(c)
local_up_build:
	docker-compose -f docker-compose.local.yml up -d --build $(c)
local_down:
	docker-compose -f docker-compose.local.yml down $(c)
local_restart:
	docker-compose -f docker-compose.local.yml stop $(c)
	docker-compose -f docker-compose.local.yml up -d $(c)
local_logs:
	docker-compose -f docker-compose.local.yml logs $(c)
local_logs_real:
	docker-compose -f docker-compose.local.yml logs -f $(c)
local_create_superuser:
	docker-compose -f docker-compose.local.yml exec auth_app flask create-superuser $(login) $(password) $(email)
local_db_migrate:
	docker-compose -f docker-compose.local.yml exec auth_app flask db migrate -m "$(m)" --rev-id="$(rev-id)"
local_db_upgrade:
	docker-compose -f docker-compose.local.yml exec auth_app flask db upgrade

up:
	docker-compose -f docker-compose.yml up -d $(c)
up_build:
	docker-compose -f docker-compose.yml up -d --build $(c)
down:
	docker-compose -f docker-compose.yml down $(c)
restart:
	docker-compose -f docker-compose.yml stop $(c)
	docker-compose -f docker-compose.yml up -d $(c)
logs:
	docker-compose -f docker-compose.yml logs $(c)
create_superuser:
	docker-compose -f docker-compose.yml exec auth_app flask create-superuser $(login) $(password) $(email)
db_migrate:
	docker-compose -f docker-compose.yml exec auth_app flask db migrate -m "$(m)" --rev-id="$(rev-id)"
db_upgrade:
	docker-compose -f docker-compose.yml exec auth_app flask db upgrade


test_environment_up:
	docker-compose -f src/tests/functional/docker-compose.yml up -d --build
test_environment_down:
	docker-compose -f src/tests/functional/docker-compose.yml down
test:
	docker-compose -f src/tests/functional/docker-compose.yml up -d --build
	docker-compose -f  src/tests/functional/docker-compose-tests.yml up
	docker-compose -f src/tests/functional/docker-compose.yml down
	docker-compose -f  src/tests/functional/docker-compose-tests.yml down
