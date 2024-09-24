.PHONY: test install-pytest run

# Check if pytest is available
PYTEST := $(shell command -v pytest 2> /dev/null)

test:
ifndef PYTEST
	@echo "pytest not found. Do you want to install it? [y/N]"
	@read answer; \
	if [ "$$answer" = "y" ] || [ "$$answer" = "Y" ]; then \
		make install-pytest; \
		make run-tests; \
	else \
		echo "pytest not installed. Running tests with unittest..."; \
		python -m unittest discover -s tests; \
	fi
else
	@make run-tests
endif

install-pytest:
	@echo "Installing pytest..."
	@pip install pytest

run-tests:
	@echo "Running tests with pytest..."
	@pytest tests

run:
	@echo "Running the FLAC to Apple Music Converter..."
	@python main.py