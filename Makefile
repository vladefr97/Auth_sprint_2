DOCKER_AUTH = docker-compose.yml
#####---AUTH---#####
auth_api_help:
	$(info ------------------------------------------------------------------------------------------------------------------------------)
	$(info "#####---AUTH---#####" (build, up, start, down, stop)                                                                         )
	$(info ------------------------------------------------------------------------------------------------------------------------------)
auth_api_build:
	docker-compose -f ${DOCKER_AUTH} build
auth_api_up:
	docker-compose -f ${DOCKER_AUTH} up -d
auth_api_start:
	docker-compose -f ${DOCKER_AUTH} start
auth_api_down:
	docker-compose -f ${DOCKER_AUTH} down
auth_api_destroy:
	docker-compose -f ${DOCKER_AUTH} down -v
auth_api_stop:
	docker-compose -f ${DOCKER_AUTH} stop
auth_api_restart:
	docker-compose -f ${DOCKER_AUTH} stop
	docker-compose -f ${DOCKER_AUTH} up -d
auth_api_first_start: auth_api_build_up
	docker-compose -f ${DOCKER_AUTH} exec service sh -c "python -m flask db upgrade  && sleep 5"

