"""Core module for CapibaraModel."""

import logging
from typing import Optional
import jax #type: ignore

from capibara_model.core.config import CapibaraConfig
from capibara_model.core.model import create_large_capibara_model
from capibara_model.core.inference import CapibaraInference, create_inference_handler
from capibara_model.utils.logging import setup_logging

__version__ = "1.0.0"

logger = logging.getLogger(__name__)

def initialize_jax() -> None:
    """Initialize JAX platform."""
    try:
        # Configurar JAX para TPU
        jax.config.update('jax_platform_name', 'tpu')
        jax.config.update('jax_enable_x64', False)
        
        # Verificar dispositivo
        devices = jax.devices()
        logger.info(f"JAX initialized with devices: {devices}")
    except Exception as e:
        logger.error(f"Error initializing JAX: {e}")
        raise

def create_model(
    config_path: str,
    checkpoint_path: Optional[str] = None
):
    """
    Create model instance.
    
    Args:
        config_path: Path to configuration file
        checkpoint_path: Optional path to checkpoint
        
    Returns:
        Tuple containing model and inference handler
    """
    try:
        # Cargar configuración
        config = CapibaraConfig.from_yaml(config_path)
        
        # Crear modelo
        model, params = create_large_capibara_model(config)
        
        # Crear manejador de inferencia
        inference = create_inference_handler(config_path, checkpoint_path)
        
        return model, inference
    except Exception as e:
        logger.error(f"Error creating model: {e}")
        raise

# Inicializar al importar
try:
    # Configurar logging
    setup_logging({'log_level': 'INFO'})
    
    # Inicializar JAX
    initialize_jax()
    
    logger.info("Core module initialized successfully")
except Exception as e:
    logger.error(f"Error during core initialization: {e}")
    raise

__all__ = [
    'CapibaraConfig',
    'create_large_capibara_model',
    'CapibaraInference',
    'create_inference_handler',
    'create_model',
    '__version__'
]
