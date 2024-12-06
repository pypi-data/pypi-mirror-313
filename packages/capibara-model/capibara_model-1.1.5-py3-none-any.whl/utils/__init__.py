"""Utilidades para CapibaraModel."""

import jax #type: ignore
import logging
from typing import Dict, Any

from capibara_model.utils.language_utils import LanguageUtils
from capibara_model.utils.response_generator import ResponseGenerator

logger = logging.getLogger(__name__)

__all__ = [
    # Utilidades de lenguaje
    'LanguageUtils',
    
    # Generación de respuestas
    'ResponseGenerator',
]

def initialize_utils(config: Dict[str, Any]) -> None:
    """Initialize utilities configuration."""
    try:
        # Configurar JAX
        if config.get('use_tpu', False):
            logger.info("Configurando JAX para TPU")
            jax.config.update('jax_xla_backend', 'tpu_driver')
            jax.config.update('jax_backend_target', config.get('tpu_config', ''))
        else:
            logger.info("Usando configuración por defecto de JAX")
            
        # Configurar precisión
        jax.config.update('jax_enable_x64', config.get('enable_x64', False))
        
        # Configurar debugging
        jax.config.update('jax_debug_nans', config.get('debug_nans', False))
        jax.config.update('jax_enable_checks', config.get('enable_checks', True))
        
        # Inicializar utilidades
        logger.info("Utilidades inicializadas correctamente")
        
    except Exception as e:
        logger.error(f"Error inicializando utilidades: {e}")
        raise
