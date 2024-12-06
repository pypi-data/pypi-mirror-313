"""
Defines fixtures for mocking AiiDA codes, with caching at the level of
the executable.
"""
# ruff: noqa: F405

from ._fixtures import *  # noqa: F403
from ._hasher import InputHasher  # noqa: F401

# Note: This is necessary for the sphinx doc - otherwise it does not find aiida_test_cache.mock_code.mock_code_factory
__all__ = (
    "pytest_addoption",
    "testing_config_action",
    "mock_regenerate_test_data",
    "testing_config",
    "mock_code_factory",
)

# ensure aiida's pytest plugin is loaded, which we rely on
pytest_plugins = ['aiida.manage.tests.pytest_fixtures']
