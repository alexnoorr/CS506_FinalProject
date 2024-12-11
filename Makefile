# Variables
VENV_DIR = venv
PYTHON = $(VENV_DIR)/bin/python
PIP = $(VENV_DIR)/bin/pip
REQUIREMENTS = requirements.txt

# Default target
all: install

# Create a virtual environment
$(VENV_DIR):
	python3 -m venv $(VENV_DIR)

# Install dependencies
install: $(VENV_DIR)
	$(PIP) install --upgrade pip
	$(PIP) install -r $(REQUIREMENTS)

# Clean the virtual environment
clean:
	rm -rf $(VENV_DIR)

# Show help
help:
	@echo "Usage:"
	@echo "  make            - Install all requirements in a virtual environment"
	@echo "  make install    - Create a virtual environment and install requirements"
	@echo "  make clean      - Remove the virtual environment"
	@echo "  make help       - Show this help message"
