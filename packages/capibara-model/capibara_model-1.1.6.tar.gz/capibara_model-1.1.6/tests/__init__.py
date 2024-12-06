"""
tests/__init__.py

This module initializes the test package and provides common utilities, configurations,
and fixtures for testing the CapibaraGPT model.

It includes:
- Standard test configurations
- Model creation utilities
- Input generation utilities
- Common pytest fixtures
"""

import jax  # type: ignore
import jax.numpy as jnp  # type: ignore
import pytest  # type: ignore
from typing import Optional, Dict, Any
from pathlib import Path
import os

from capibara_model.core.config import TrainingConfig  
from capibara_model.core.model import CapibaraModel
from capibara_model.utils.logging import CapibaraConfig

# Configure logging for tests
logger = CapibaraConfig.setup_logger(__name__)

# Common test configurations
BASE_TEST_CONFIG = ModelConfig(
    input_dim=64,
    byte_output_dim=128,
    state_dim=256,
    mamba_output_dim=512,
    hidden_dim=1024,
    output_dim=2048,
    vocab_size=1000,
    max_length=50,
    num_layers=4,
    learning_rate=0.001,
    dropout_rate=0.1,
    attention_heads=8
)

SMALL_TEST_CONFIG = CapibaraConfig(
    input_dim=32,
    byte_output_dim=64,
    state_dim=128,
    mamba_output_dim=256,
    hidden_dim=512,
    output_dim=1024,
    vocab_size=1000,
    max_length=25,
    num_layers=2,
    learning_rate=0.001,
    dropout_rate=0.1,
    attention_heads=4
)

LARGE_TEST_CONFIG = CapibaraConfig(
    input_dim=128,
    byte_output_dim=256,
    state_dim=512,
    mamba_output_dim=1024,
    hidden_dim=2048,
    output_dim=4096,
    vocab_size=1000,
    max_length=100,
    num_layers=8,
    learning_rate=0.0001,
    dropout_rate=0.2,
    attention_heads=16
)

# Utility functions for tests


def create_test_model(
    config: Optional[CapibaraConfig] = None
) -> CapibaraTextGenerator:
    """
    Creates a CapibaraTextGenerator model using the specified or default test configuration.

    Args:
        config (Optional[CapibaraConfig]): Configuration to use. If None, uses BASE_TEST_CONFIG.

    Returns:
        CapibaraTextGenerator: A text generator model instance.

    Raises:
        ValueError: If model initialization fails.
    """
    try:
        return CapibaraTextGenerator(config or BASE_TEST_CONFIG)
    except Exception as e:
        logger.error(f"Failed to create test model: {str(e)}")
        raise ValueError(f"Model initialization failed: {str(e)}")


def create_random_input(
    key: jax.random.PRNGKey,
    batch_size: int = 1,
    config: Optional[CapibaraConfig] = None
) -> jnp.ndarray:
    """
    Creates a random input array for testing.

    Args:
        key (jax.random.PRNGKey): PRNG key for random generation.
        batch_size (int): Batch size for the input array.
        config (Optional[CapibaraConfig]): Configuration to use. If None, uses BASE_TEST_CONFIG.

    Returns:
        jnp.ndarray: Random integer array of shape (batch_size, max_length).

    Raises:
        ValueError: If input generation fails.
    """
    try:
        cfg = config or BASE_TEST_CONFIG
        return jax.random.randint(
            key,
            (batch_size, cfg.max_length),
            0,
            cfg.vocab_size
        )
    except Exception as e:
        logger.error(f"Failed to create random input: {str(e)}")
        raise ValueError(f"Input generation failed: {str(e)}")

# Pytest fixtures


@pytest.fixture(scope="function")
def capibara_model():
    """
    Provides a fresh CapibaraTextGenerator model instance for each test.

    Returns:
        CapibaraTextGenerator: A text generator model instance.
    """
    return create_test_model()


@pytest.fixture(scope="function")
def rng_key():
    """
    Provides a fresh JAX random key for each test.

    Returns:
        jax.random.PRNGKey: A JAX PRNG key.
    """
    return jax.random.PRNGKey(0)


@pytest.fixture(scope="session")
def test_configs() -> Dict[str, CapibaraConfig]:
    """
    Provides access to all test configurations.

    Returns:
        Dict[str, CapibaraConfig]: Dictionary containing all test configurations.
    """
    return {
        'base': BASE_TEST_CONFIG,
        'small': SMALL_TEST_CONFIG,
        'large': LARGE_TEST_CONFIG
    }

# Test environment setup


def setup_test_environment() -> None:
    """
    Sets up the test environment with necessary configurations.
    """
    try:
        # Set up JAX platform
        if 'JAX_PLATFORM_NAME' in os.environ:
            jax.config.update('jax_platform_name',
                              os.environ['JAX_PLATFORM_NAME'])

        # Create test directories if needed
        test_data_dir = Path(__file__).parent / 'test_data'
        test_data_dir.mkdir(exist_ok=True)

        logger.info("Test environment setup completed successfully")
    except Exception as e:
        logger.error(f"Test environment setup failed: {str(e)}")
        raise RuntimeError(f"Environment setup failed: {str(e)}")


# Initialize test environment when module is imported
setup_test_environment()
