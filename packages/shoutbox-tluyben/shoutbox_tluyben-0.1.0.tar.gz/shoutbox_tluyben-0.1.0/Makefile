# Include .env file if it exists
ifneq (,$(wildcard .env))
    include .env
    export
endif

# Check for required environment variables
check-env:
	@if [ -z "$(SHOUTBOX_API_KEY)" ]; then \
		echo "Error: SHOUTBOX_API_KEY is not set"; \
		exit 1; \
	fi
	@if [ -z "$(SHOUTBOX_FROM)" ]; then \
		echo "Error: SHOUTBOX_FROM is not set"; \
		exit 1; \
	fi
	@if [ -z "$(SHOUTBOX_TO)" ]; then \
		echo "Error: SHOUTBOX_TO is not set"; \
		exit 1; \
	fi

# Install dependencies
install:
	pip install -e .
	pip install -r requirements-dev.txt

# Update dependencies
update:
	pip install --upgrade -e .
	pip install --upgrade -r requirements-dev.txt

# Run tests (requires environment variables)
test: check-env
	python -m pytest tests/ -v --cov=shoutbox

# Test direct API specifically
test-direct-api:
	bash -c "set -a && source ./.env && set +a && python -m pytest -s tests/test_direct_api.py -v"

# Test API client specifically
test-api-client:
	bash -c "set -a && source ./.env && set +a && python -m pytest -s tests/test_api_client.py -v"

# Test client specifically
test-client:
	bash -c "set -a && source ./.env && set +a && python -m pytest -s tests/test_client.py -v"

# Test SMTP specifically
test-smtp:
	bash -c "set -a && source ./.env && set +a && python -m pytest -s tests/test_smtp.py -v"

# Test models specifically
test-models:
	bash -c "set -a && source ./.env && set +a && python -m pytest -s tests/test_models.py -v"

# Test exceptions specifically
test-exceptions:
	bash -c "set -a && source ./.env && set +a && python -m pytest -s tests/test_exceptions.py -v"

# Test Flask specifically
test-flask:
	bash -c "set -a && source ./.env && set +a && python -m pytest -s tests/test_flask.py -v"

# Test Django specifically
test-django:
	bash -c "set -a && source ./.env && set +a && python -m pytest -s tests/test_django.py -v"

# Run direct API example
run-direct-api: check-env
	bash -c "set -a && source ./.env && set +a && python examples/direct_api.py"

# Run API client example
run-api-client: check-env
	python examples/api_client.py

# Run SMTP example
run-smtp: check-env
	python examples/smtp_client.py

# Run Flask example
run-flask: check-env
	FLASK_APP=examples/flask_integration.py flask run --port 5001

# Run code style checks
cs:
	flake8 src/ tests/ examples/
	black --check src/ tests/ examples/

# Fix code style issues
cs-fix:
	black src/ tests/ examples/

# Clean up
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# Create .env template file
env-template:
	@echo "SHOUTBOX_API_KEY=" > .env.template
	@echo "SHOUTBOX_FROM=" >> .env.template
	@echo "SHOUTBOX_TO=" >> .env.template
	@echo "Created .env.template file"

# Show help
help:
	@echo "Available commands:"
	@echo "  make install      - Install dependencies"
	@echo "  make update      - Update dependencies"
	@echo "  make test        - Run tests (requires env vars)"
	@echo "  make test-direct-api - Run direct API tests"
	@echo "  make test-api-client - Run API client tests"
	@echo "  make test-client - Run client tests"
	@echo "  make test-smtp   - Run SMTP tests"
	@echo "  make test-models - Run models tests"
	@echo "  make test-exceptions - Run exceptions tests"
	@echo "  make test-flask  - Run Flask tests"
	@echo "  make test-django - Run Django tests"
	@echo "  make run-direct-api - Run direct API example"
	@echo "  make run-api-client - Run API client example"
	@echo "  make run-smtp    - Run SMTP example"
	@echo "  make run-flask   - Run Flask example"
	@echo "  make cs          - Run code style checks"
	@echo "  make cs-fix      - Fix code style issues"
	@echo "  make clean       - Clean build artifacts"
	@echo "  make env-template - Create .env.template file"
	@echo ""
	@echo "Required environment variables (can be set in .env file):"
	@echo "  SHOUTBOX_API_KEY - Your Shoutbox API key"
	@echo "  SHOUTBOX_FROM    - Sender email address"
	@echo "  SHOUTBOX_TO      - Recipient email address"

.PHONY: check-env install update test test-direct-api test-api-client test-client test-smtp test-models test-exceptions test-flask test-django run-direct-api run-api-client run-smtp run-flask cs cs-fix clean env-template help
