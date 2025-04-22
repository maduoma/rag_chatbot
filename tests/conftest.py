import warnings
import pytest

def pytest_configure(config):
    # Suppress all DeprecationWarnings globally for clean test output
    warnings.filterwarnings("ignore", category=DeprecationWarning)
