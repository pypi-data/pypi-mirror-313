"""
Test configuration utilities for CapibaraModel.

Provides default test configurations, model creation utilities, and input generators
for testing the CapibaraModel architecture.
"""

import os  # Añadir esta línea
import jax  # type: ignore
import jax.numpy as jnp  # type: ignore
from typing import Dict, Any, Optional
from pathlib import Path

from capibara_model.core.config import CapibaraConfig
from capibara_model.core.model import create_large_capibara_model

# Default configuration for tests
DEFAULT_TEST_CONFIG: Dict[str, Any] = {
    'training': {
        'seed': 42,
        'batch_size': 32,
        'learning_rate': 0.001,
        'num_epochs': 1,
        'train_data_path': str(Path('tests/test_data/train')),
        'val_data_path': str(Path('tests/test_data/val')),
        'max_length': 512,
        'checkpoint_frequency': 100,
        'contextual_activation_frequency': 10
    },
    'model': {
        'input_dim': 768,
        'hidden_size': 768,
        'seq_len': 512,
        'num_layers': 12,
        'dropout_rate': 0.1,
        'activation_function': 'relu'
    },
    'pruning': {
        'mor_threshold': 0.7,
        'sparsity_ratio': 0.5,
        'pruning_method': 'magnitude',
        'pruning_schedule': 'constant'
    },
    'wandb': {
        'project': 'capibara_test',
        'entity': 'test_entity',
        'log_model': False,
        'log_gradients': False,
        'run_name': 'test_run'
    }
}

def create_test_config(overrides: Optional[Dict[str, Any]] = None) -> CapibaraConfig:
    """
    Creates a test configuration with optional overrides.

    Args:
        overrides: Optional configuration overrides.

    Returns:
        CapibaraConfig: Test configuration instance.
    """
    config_dict = DEFAULT_TEST_CONFIG.copy()
    if overrides:
        for section, values in overrides.items():
            if section in config_dict:
                config_dict[section].update(values)
            else:
                config_dict[section] = values
    
    return CapibaraConfig.from_dict(config_dict)

def create_test_model(overrides: Optional[Dict[str, Any]] = None):
    """
    Creates a model instance for testing.

    Args:
        overrides: Optional configuration overrides.

    Returns:
        Tuple[CapibaraModel, Dict]: Model instance and its parameters.
    """
    config = create_test_config(overrides)
    return create_large_capibara_model(config)

def create_test_batch(
    config: CapibaraConfig,
    batch_size: int = 2,
    rng_key: Optional[jnp.ndarray] = None
) -> Dict[str, jnp.ndarray]:
    """
    Creates a test batch of inputs.

    Args:
        config: Model configuration.
        batch_size: Number of samples in batch.
        rng_key: Optional PRNG key.

    Returns:
        Dict[str, jnp.ndarray]: Batch of test inputs.
    """
    if rng_key is None:
        rng_key = jax.random.PRNGKey(0)
    
    return {
        'inputs': jnp.ones((batch_size, config.model.input_dim)),
        'context': jnp.ones((batch_size, config.model.input_dim)),
        'targets': jnp.ones((batch_size, config.model.hidden_size))
    }

def initialize_test_environment() -> None:
    """Initializes the test environment."""
    # Create test data directories
    for split in ['train', 'val']:
        data_dir = Path('tests/test_data') / split
        data_dir.mkdir(parents=True, exist_ok=True)

    # Set environment variables
    os.environ.update({
        "JAX_PLATFORM_NAME": "tpu",
        "JAX_ENABLE_XLA": "1",
        "CAPIBARA_TEST_MODE": "TRUE"
    })

if __name__ == "__main__":
    # Example usage
    initialize_test_environment()
    
    # Create test configuration and model
    config = create_test_config()
    model, params = create_test_model()
    
    # Create test batch
    batch = create_test_batch(config)
    
    print(f"Test model created successfully with {params.size:,} parameters")
    print(f"Test batch shapes: {jax.tree_map(lambda x: x.shape, batch)}")
