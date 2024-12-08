# Copyright (c) 2023-2024 Datalayer, Inc.
#
# Datalayer License

SHELL=/bin/bash

.DEFAULT_GOAL := default

.PHONY: clean build

default: all ## Default target is all.

help: ## display this help.
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

all: clean dev ## Clean Install and Build

install:
	pip install ../solr
	pip install .

dev:
	pip install -r requirements.txt

build:
	pip install build
	python -m build .

publish:
	pip install twine
	python -m twine upload dist/*

start:
	@echo
	@echo open http://localhost:9700/api/iam/version
	@echo open http://localhost:9700/api/iam/v1/ping
	@echo open http://localhost:9700/api/iam/v1/ui
	@echo
	DATALAYER_JWT_CACHE_VALIDATE=false \
	  python datalayer_iam/main.py
		
clean: ## clean
	git clean -fdx
