.PHONY: bootstrap clean deploy deploy-task eslint lint pep8 server shell \
		status test_integrational test_unit

# Project settings
DEV ?= 1
PROJECT = readthestuff

# Virtual environment settings
ENV ?= env
VENV = $(shell python -c "import sys; print(int(hasattr(sys, 'real_prefix')));")

# Python commands
ifeq ($(VENV),1)
	GUNICORN = gunicorn
	IPYTHON = ipython
	PEP8 = flake8
	PYTHON = python
else
	GUNICORN = $(ENV)/bin/gunicorn
	IPYTHON = $(ENV)/bin/ipython
	PEP8 = $(ENV)/bin/flake8
	PYTHON = $(ENV)/bin/python
endif

# Server settings
DEPLOY_HOST ?= readthestuff
GUNICORN_WORKERS ?= $(shell python -c "import multiprocessing; print(multiprocessing.cpu_count() * 2 + 1);")
LOGS_DIR ?= ./logs
SERVER_HOST ?= 0.0.0.0
SERVER_PORT ?= 8201

# Static settings
NPM ?= npm
STATIC_DIR ?= $(PROJECT)/static/dist

# Test settings
COVERAGE_DIR ?= /tmp/$(PROJECT)-coverage

# Setup bootstrapper & Gunicorn args
ifeq ($(DEV),1)
	bootstrapper_args = -d
	gunicorn_args = --reload
else
	gunicorn_args = --access-logfile=$(LOGS_DIR)/gunicorn.access.log \
	--error-logfile=$(LOGS_DIR)/gunicorn.error.log
endif

bootstrap:
	PROJECT=$(PROJECT) bootstrapper -e $(ENV)/ $(bootstrapper_args)
	$(NPM) install

clean:
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -type d -exec rm -rf {} 2> /dev/null +
	find . -type d -empty -delete

deploy: test eslint
	git push
	ssh $(DEPLOY_HOST) "cd projects/$(PROJECT)/ && git pull && make deploy-task"

deploy-task:
	# WARNING: Deploy task should be executed only on remote host!
	DEV=0 $(MAKE) bootstrap
	sudo cp $(PROJECT).upstart /etc/init/$(PROJECT).conf
	sudo service $(PROJECT) restart
	sudo cp $(PROJECT).nginx /etc/nginx/sites-available/$(PROJECT).com
	sudo service nginx restart

distclean: clean
	rm -rf $(ENV)/ node_modules/ $(STATIC_DIR)/
	rm -f .coverage npm-debug.log $(PROJECT)/settings_local.py

eslint:
	$(NPM) run lint

lint: pep8 eslint

pep8:
	$(PEP8) --statistics $(PROJECT)/

server: clean
ifeq ($(DEV),1)
	$(MAKE) pep8
else
	mkdir -p $(LOGS_DIR)/
endif
	DEBUG=$(DEV) $(GUNICORN) -b $(SERVER_HOST):$(SERVER_PORT) -n $(PROJECT) -k aiohttp.worker.GunicornWebWorker -w $(GUNICORN_WORKERS) -t 60 --graceful-timeout=60 $(gunicorn_args) $(GUNICORN_ARGS) $(PROJECT).app:app

shell:
	$(IPYTHON) --deep-reload --no-banner --no-confirm-exit --pprint

status:
ifeq ($(SERVICE),)
	# SERVICE env var should be supplied
else
	ssh $(DEPLOY_HOST) "sudo service $(SERVICE) status"
endif

test: clean pep8 test_unit test_integrational

test_integrational: clean pep8
	$(NOSETESTS) --logging-clear-handlers $(TEST_ARGS) -w $(PROJECT)/ -a integrational

test_unit: clean pep8
	$(NOSETESTS) --logging-clear-handlers $(TEST_ARGS) -w $(PROJECT)/ -a "!integrational" \
	--with-coverage --cover-branches --cover-erase --cover-package=$(PROJECT) \
	--cover-html --cover-html-dir=$(COVERAGE_DIR)
