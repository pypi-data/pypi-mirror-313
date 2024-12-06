VENV_NAME=strideutils
CONDA_BASE := $(shell conda info --base)/envs
VENV_BIN=$(CONDA_BASE)/$(VENV_NAME)/bin
PYTHON=$(VENV_BIN)/python

export ENV=DEV
export STRIDEUTILS_CONFIG_PATH=example-config.yaml

install:
	conda create --name $(VENV_NAME) python=3.11 -y
	$(PYTHON) -m pip install -e .[dev]

lint:
	@echo "Linting..."
	@$(VENV_BIN)/flake8 --max-line-length 120 --exclude .ipynb_checkpoints strideutils tests strideutils-stubs

type-check:
	@echo "Type checking..."
	@$(VENV_BIN)/mypy strideutils tests --exclude strideutils-stubs

format:
	@echo "Formatting..."
	@$(VENV_BIN)/black --skip-string-normalization --line-length 120 strideutils tests strideutils-stubs
	@echo "Sorting imports..."
	@$(VENV_BIN)/isort --profile=black strideutils tests strideutils-stubs

generate-stubs:
	@echo "Generating type stubs..."
	@touch strideutils/py.typed
	@mkdir -p strideutils-stubs
	@$(VENV_BIN)/stubgen --parse-only -p strideutils -o stubs
	@cp stubs/strideutils/*.pyi strideutils-stubs/
	@rm -rf stubs
	@echo "Done! Check strideutils-stubs/ for .pyi files."

tidy: lint type-check format

test:
	@echo "Running unit tests..."
	@$(VENV_BIN)/pytest . -v