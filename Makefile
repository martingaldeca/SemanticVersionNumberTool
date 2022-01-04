#!make
include .env
.DEFAULT_GOAL=up
MAKEFLAGS += --no-print-directory

# Constants
TAIL_LOGS = 50
PYTEST_WORKERS = 8
TESTS_MAX_FAILS = 5

up:
	$s make create-nginx-conf
	$s docker-compose up --force-recreate -d

down:
	$s docker-compose down

downup: down up

upbuild:
	$s docker-compose down
	$s make create-nginx-conf
	$s docker-compose up --force-recreate -d --build

build:
	$s make create-nginx-conf
	$s docker-compose build

completebuild:
	$s docker image prune -af
	$s docker-compose build
	$s docker-compose down
	$s docker-compose up --force-recreate -d

logs:
	$s docker logs --tail ${TAIL_LOGS} -f ${PROJECT_NAME}_backend

bash:
	$s docker exec -it ${PROJECT_NAME}_backend bash

sh:
	$s docker exec -it ${PROJECT_NAME}_backend bash

shell:
	$s docker exec -it ${PROJECT_NAME}_backend python manage.py shell_plus

shell_plus:
	$s docker exec -it ${PROJECT_NAME}_backend python manage.py shell_plus

makemigrations:
	$s docker exec -it ${PROJECT_NAME}_backend python manage.py makemigrations

migrate:
	$s docker exec -it ${PROJECT_NAME}_backend python manage.py migrate $(ARGS)

migrations:
	$s docker exec -it ${PROJECT_NAME}_backend python manage.py makemigrations
	$s docker exec -it ${PROJECT_NAME}_backend python manage.py migrate

makemessages:
	$s docker exec -it ${PROJECT_NAME}_backend python manage.py makemessages -a

compilemessages:
	$s docker exec -it ${PROJECT_NAME}_backend python manage.py compilemessages

messages:
	$s docker exec -it ${PROJECT_NAME}_backend python manage.py makemessages -l es -a -i *.txt
	$s docker exec -it ${PROJECT_NAME}_backend python manage.py compilemessages -v 3

workerlogs:
	$s docker exec -it ${PROJECT_NAME}_worker tail -f logs/default_worker.log

celerylogs:
	$s docker logs --tail ${TAIL_LOGS} -f ${PROJECT_NAME}_worker

beatlogs:
	$s docker logs --tail ${TAIL_LOGS} -f ${PROJECT_NAME}_beat

workerbash:
	$s docker exec -it ${PROJECT_NAME}_worker bash

test:
	$s docker exec ${PROJECT_NAME}_backend pytest -n ${PYTEST_WORKERS} --maxfail=${TESTS_MAX_FAILS} -vv -s --log-cli-level=ERROR --disable-pytest-warnings --create-db --ds backend.settings.test_settings

fasttest:
	$s docker exec ${PROJECT_NAME}_backend pytest -n ${PYTEST_WORKERS} --maxfail=${TESTS_MAX_FAILS} -vv -s --log-cli-level=ERROR --disable-pytest-warnings --reuse-db --ds backend.settings.test_settings

localtest:
	$s docker exec ${PROJECT_NAME}_backend pytest -n ${PYTEST_WORKERS} -vv -s --log-cli-level=ERROR --disable-pytest-warnings --reuse-db --ds backend.settings.test_settings

IMAGES := $(shell docker images -qa)
cleanimages:
	$s docker rmi $(IMAGES) --force

CONTAINERS := $(shell docker ps -qa)
removecontainers:
	$s docker rm $(CONTAINERS)

nginxlogs:
	$s docker logs --tail ${TAIL_LOGS} -f ${PROJECT_NAME}_nginx

restart:
	$s docker-compose restart

updaterequirements:
	$s docker exec ${PROJECT_NAME}_backend poetry update

flake8:
	$s docker exec ${PROJECT_NAME}_backend flake8

alllogs:
	$s docker-compose logs --tail ${TAIL_LOGS} -f

demo_data:
	$s docker exec ${PROJECT_NAME}_backend python manage.py demo_data

create-nginx-conf:
	$s rm -f docker/nginx/nginx.conf-final
	$s sed -e "s/BACKEND_PORT/${BACKEND_PORT}/g" docker/nginx/nginx.conf > docker/nginx/nginx.conf-tmp
	$s sed -e "s/NGINX_EXTERNAL_PORT/${NGINX_EXTERNAL_PORT}/g" docker/nginx/nginx.conf-tmp > docker/nginx/nginx.conf-tmp-2
	$s sed -e "s/NGINX_EXTERNAL_SSL_PORT/${NGINX_EXTERNAL_SSL_PORT}/g" docker/nginx/nginx.conf-tmp-2 > docker/nginx/nginx.conf-final
	$s rm -f docker/nginx/nginx.conf-tmp
	$s rm -f docker/nginx/nginx.conf-tmp-2
