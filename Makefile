install:
	pip install -e ./

ARGS := $(filter-out run,$(MAKECMDGOALS))
DIR := $(if $(ARGS),$(ARGS),assets/)

run:
	python src/yarea/main.py $(DIR) --print