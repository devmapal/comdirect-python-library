"""Pytest configuration for Comdirect API client tests."""

import pytest

# Configure pytest-asyncio
pytest_plugins = ("pytest_asyncio",)


@pytest.fixture(scope="session")
def anyio_backend():
    """Configure async backend for pytest-asyncio."""
    return "asyncio"
