"""Test configuration and fixtures for CapibaraModel."""
import sys
import os
import pytest #type: ignore
import jax #type: ignore
import jax.numpy as jnp #type: ignore
from pathlib import Path
import logging
from typing import Dict, Any

from capibara_model.core.config import CapibaraConfig
from capibara_model.core.model import create_large_capibara_model

# Configurar logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def initialize_tests() -> None:
    """Initialize test environment."""
    try:
        # Set fixed random seed
        jax.random.PRNGKey(42)

        # Configure environment
        os.environ.update({
            "JAX_PLATFORM_NAME": "tpu",
            "JAX_ENABLE_XLA": "1",
            "CAPIBARA_LOG_LEVEL": "DEBUG",
            "CAPIBARA_TEST_MODE": "TRUE"
        })

        # Create test directories
        test_data_dir = Path(__file__).parent / 'test_data'
        test_data_dir.mkdir(exist_ok=True)

        logger.info("Test initialization completed")
    except Exception as e:
        logger.error(f"Test initialization failed: {str(e)}")
        raise

@pytest.fixture(scope="session")
def config() -> CapibaraConfig:
    """Provide test configuration."""
    return CapibaraConfig.from_yaml('config/config_minimal_tpu.yaml')

@pytest.fixture(scope="function")
def model(config: CapibaraConfig):
    """Provide model instance."""
    model, _ = create_large_capibara_model(config)
    return model

@pytest.fixture(scope="function")
def rng_key() -> jnp.ndarray:
    """Provide PRNG key."""
    return jax.random.PRNGKey(0)

@pytest.fixture(scope="function")
def sample_batch(config: CapibaraConfig, rng_key: jnp.ndarray) -> Dict[str, jnp.ndarray]:
    """Provide sample batch for testing."""
    batch_size = 2
    return {
        'inputs': jnp.ones((batch_size, config.model.input_dim)),
        'context': jnp.ones((batch_size, config.model.input_dim)),
        'targets': jnp.ones((batch_size, config.model.hidden_size))
    }

@pytest.fixture(scope="session")
def test_data_dir() -> Path:
    """Provide test data directory."""
    return Path(__file__).parent / 'test_data'

def pytest_configure(config):
    """Configure test session."""
    logger.info("Starting test session")

def pytest_sessionfinish(session, exitstatus):
    """Clean up after test session."""
    logger.info(f"Test session finished with status: {exitstatus}") 