#################################################################################
#
# Makefile to build the project
#
#################################################################################

PROJECT_NAME = toatcakes
REGION = eu-west-2
PYTHON_INTERPRETER = python
WD=$(shell pwd)
PYTHONPATH=${WD}
SHELL := /bin/bash
PROFILE = default
PIP:=pip

## Create python interpreter environment.
create-environment:
	@echo ">>> About to create environment: $(PROJECT_NAME)..."
	@echo ">>> check python3 version"
	( \
		$(PYTHON_INTERPRETER) --version; \
	)
	@echo ">>> Setting up VirtualEnv."
	( \
	    $(PYTHON_INTERPRETER) -m venv venv; \
	)

# Define utility variable to help calling Python from the virtual environment
ACTIVATE_ENV := source venv/bin/activate

# Execute python related functionalities from within the project's environment
define execute_in_env
	$(ACTIVATE_ENV) && $1
endef

## Build the environment requirements
requirements: create-environment
	$(call execute_in_env, $(PIP) install pip-tools)
	$(call execute_in_env, $(PIP) install -r ./requirements.txt)

################################################################################################################
# Set Up
## Install bandit
bandit:
	$(call execute_in_env, $(PIP) install bandit)

## Install black
black:
	$(call execute_in_env, $(PIP) install black)

## Install coverage
coverage:
	$(call execute_in_env, $(PIP) install pytest-cov)

## Install flake8
flake8:
	$(call execute_in_env, $(PIP) install flake8)

## Set up dev requirements (bandit, black & coverage)
dev-setup: bandit black coverage flake8

# Build / Run

## Run the security test (bandit + safety)
security-test:
	$(call execute_in_env, bandit -lll */*.py)

## Run the black code check
run-black:
	$(call execute_in_env, black --line-length 79 ./src/*.py ./tests/*.py ./utils/*.py)

## Run the unit tests
unit-test:
	$(call execute_in_env, PYTHONPATH=${PYTHONPATH} pytest tests/ -vv)

## Run the coverage check
check-coverage:
	$(call execute_in_env, PYTHONPATH=${PYTHONPATH} pytest --cov=src --cov=utils tests/)

## Run the flake8 check
run-flake8:
	$(call execute_in_env, flake8  ./src/*.py ./tests/*.py ./utils/*.py)

## Run all checks
run-checks: security-test run-black unit-test check-coverage run-flake8