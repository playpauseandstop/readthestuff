.PHONY: clean devserver distclean manage rq server

PROJECT = readthestuff

ENV ?= env
VENV := $(shell echo $(VIRTUAL_ENV))

HOST ?= 0.0.0.0
PORT ?= 8321

ifneq ($(VENV),)
	FLAKE8 = flake8
	HONCHO = honcho
	IPYTHON = ipython
	PYTHON = python
else
	FLAKE8 = $(ENV)/bin/flake8
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

manage:
	$(PYTHON) manage.py $(COMMAND)

pep8:
	$(FLAKE8) $(PROJECT)/

rq: clean pep8
	$(HONCHO) start rq

server: clean pep8
	HOST=$(HOST) PORT=$(PORT) $(HONCHO) start server
