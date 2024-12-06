"""Módulos principales de CapibaraModel."""

import jax #type: ignore
import logging
from typing import Dict, Any

# Módulos principales
from capibara_model.modules.coherence_detector import CoherenceDetector
from capibara_model.modules.contextual_activation import ContextualActivation
from capibara_model.modules.conversation_manager import ConversationManager
from capibara_model.modules.ethics_module import EthicsModule
from capibara_model.modules.personality_manager import PersonalityManager
from capibara_model.modules.capibara_tts import CapibaraTextToSpeech

logger = logging.getLogger(__name__)

__all__ = [
    # Módulos de procesamiento
    'CoherenceDetector',
    'ContextualActivation',
    'ConversationManager',
    
    # Módulos de comportamiento
    'EthicsModule',
    'PersonalityManager',
    
    # Módulos de generación
    'CapibaraTTS',
]

def initialize_modules(config: Dict[str, Any]) -> None:
    """Initialize modules configuration."""
    try:
        # Configurar dispositivo
        if config.get('use_tpu', False):
            logger.info("Configurando JAX para TPU")
            jax.config.update('jax_xla_backend', 'tpu_driver')
            jax.config.update('jax_backend_target', config.get('tpu_config', ''))
        else:
            logger.info("Usando configuración por defecto de JAX")
        
        # Inicializar módulos
        logger.info("Módulos inicializados correctamente")
        
    except Exception as e:
        logger.error(f"Error inicializando módulos: {e}")
        raise
