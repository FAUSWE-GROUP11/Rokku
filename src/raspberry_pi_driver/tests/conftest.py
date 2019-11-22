import logging
import os
from logging import config

import pytest
import yaml


@pytest.fixture(scope="package")
def logger():
    """Set up logger for testing."""
    with open(
        f"{os.path.dirname(__file__)}/fixtures/test_logger_config.yaml", "r"
    ) as f:
        log_config = yaml.safe_load(f.read())
        config.dictConfig(log_config)
    yield logging.getLogger("TEST")
