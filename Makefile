.PHONY: clean devserver distclean manage rq server

PROJECT = readthestuff

ENV ?= env
VENV := $(shell echo $(VIRTUAL_ENV))

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
	$(HONCHO) run dev

manage:
	$(PYTHON) manage.py $(COMMAND)

pep8:
	$(FLAKE8) $(PROJECT)/

rq: clean pep8
	$(HONCHO) run rq

server: clean pep8
	$(HONCHO) run server
