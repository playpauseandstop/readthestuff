.PHONY: bootstrap clean createdb dbshell devserver distclean dropdb initdb manage rq server

PROJECT = readthestuff

ENV ?= env
VENV := $(shell echo $(VIRTUAL_ENV))

HOST ?= 0.0.0.0
PORT ?= 8321

ifneq ($(VENV),)
	HONCHO = honcho
	IPYTHON = ipython
	PYTHON = python
else
	HONCHO = . $(ENV)/bin/activate && honcho
	IPYTHON = $(ENV)/bin/ipython
	PYTHON = $(ENV)/bin/python
endif

bootstrap:
	PROJECT=$(PROJECT) bootstrapper -e $(ENV)

clean:
	find . -name "*.pyc" -delete

createdb:
	psql -c '\du' | grep "^ $(PROJECT)" && : || createuser -s -P $(PROJECT)
	psql -l | grep "^ $(PROJECT)" && : || createdb -U $(PROJECT) $(PROJECT)

dbshell:
	psql -U $(PROJECT) -d $(PROJECT)

devserver: clean pep8
	COMMAND="runserver --host=$(HOST) --port=$(PORT)" $(MAKE) manage

distclean: clean dropdb
	rm -r $(ENV)/ $(PROJECT)/settings_local.py

dropdb:
	dropdb -U $(PROJECT) $(PROJECT)

initdb: createdb
	psql -U $(PROJECT) -d $(PROJECT) -f $(PROJECT)/sql/initial.sql -v client_min_messages=warning

manage:
	$(PYTHON) manage.py $(COMMAND)

pep8:
	COMMAND=pep8 $(MAKE) manage

rq: clean pep8
	$(HONCHO) start rq

server: clean pep8
	HOST=$(HOST) PORT=$(PORT) $(HONCHO) start web

shell:
	$(IPYTHON) --deep-reload --no-banner --no-confirm-exit --pprint
