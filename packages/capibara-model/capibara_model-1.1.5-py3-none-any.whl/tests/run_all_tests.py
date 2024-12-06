"""Run all tests for the CapibaraModel project."""

import os
import pytest #type: ignore
import jax #type: ignore
import jax.numpy as jnp #type: ignore
from pathlib import Path
import logging
from typing import Dict, Any

from capibara_model.core.config import CapibaraConfig
from capibara_model.data.data_loader import CapibaraDataLoader
from capibara_model.utils.logging import setup_logging

# Configurar logging
logger = logging.getLogger(__name__)

def configure_environment() -> None:
    """Configure test environment."""
    # Configurar variables de entorno
    os.environ.update({
        "JAX_PLATFORM_NAME": "tpu",
        "JAX_ENABLE_XLA": "1",
        "CAPIBARA_TEST_MODE": "TRUE",
        "CAPIBARA_LOG_LEVEL": "DEBUG"
    })
    
    # Configurar logging
    setup_logging({'log_level': 'DEBUG'})
    
    # Crear directorios de test
    test_data_dir = Path('tests/test_data')
    for split in ['train', 'val']:
        (test_data_dir / split).mkdir(parents=True, exist_ok=True)

def create_test_data(config: CapibaraConfig) -> None:
    """
    Create test data files.
    
    Args:
        config: Model configuration.
    """
    test_data_dir = Path('tests/test_data')
    
    for split in ['train', 'val']:
        data_path = test_data_dir / split / 'test.txt'
        with open(data_path, 'w') as f:
            f.write('Sample text\n' * 100)
    
    logger.info("Created test data files")

def run_tests() -> None:
    """Run all tests with pytest."""
    try:
        # Configurar entorno
        configure_environment()
        
        # Cargar configuración
        config = CapibaraConfig.from_yaml('config/config_minimal_tpu.yaml')
        
        # Crear datos de prueba
        create_test_data(config)
        
        # Ejecutar tests
        logger.info("Starting test execution...")
        pytest.main([
            'tests',
            '-v',
            '--tb=short',
            '--capture=no',
            '--log-cli-level=INFO'
        ])
        
    except Exception as e:
        logger.error(f"Error running tests: {e}")
        raise

if __name__ == "__main__":
    run_tests()
