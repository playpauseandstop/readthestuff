.PHONY: clean devserver distclean manage rq server

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

devserver: clean pep8
	HOST=$(HOST) PORT=$(PORT) $(HONCHO) start dev

distclean: clean
	rm -r $(ENV)/ $(PROJECT)/settings_local.py

manage:
	$(PYTHON) manage.py $(COMMAND)

pep8:
	COMMAND=pep8 $(MAKE) manage

rq: clean pep8
	$(HONCHO) start rq

server: clean pep8
	HOST=$(HOST) PORT=$(PORT) $(HONCHO) start server

shell:
	$(IPYTHON) --deep-reload --no-banner --no-confirm-exit --pprint
