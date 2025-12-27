"""Matrix Guardian Test Suite.

This package contains comprehensive tests for the Matrix Guardian control plane,
including unit tests, integration tests, and smoke tests.

Test Organization:
    - Unit tests: Fast, isolated tests for individual components
    - Integration tests: Tests that verify component interactions
    - Smoke tests: High-level tests that verify basic functionality

Running Tests:
    Run all tests:
        $ make test
        $ pytest

    Run specific test types:
        $ pytest -m unit           # Unit tests only
        $ pytest -m integration    # Integration tests only
        $ pytest -m slow          # Slow tests only

    Run with coverage:
        $ make coverage
        $ pytest --cov=src/guardian --cov-report=html

Test Markers:
    @pytest.mark.unit - Fast, isolated unit tests
    @pytest.mark.integration - Integration tests requiring external services
    @pytest.mark.slow - Slow-running tests (can be skipped in development)

Author:
    Ruslan Magana (ruslanmv.com)

License:
    Apache 2.0
"""

__version__ = "1.0.0"
__author__ = "Ruslan Magana"
__email__ = "contact@ruslanmv.com"
