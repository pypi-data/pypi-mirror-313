"""Inference module for CapibaraModel."""

import jax #type: ignore
import jax.numpy as jnp #type: ignore
import logging
from typing import Dict, Any, Optional

from capibara_model.core.model import CapibaraModel

logger = logging.getLogger(__name__)

class CapibaraInference:
    """Manejador de inferencia para CapibaraModel."""
    
    def __init__(
        self,
        hidden_size: int,
        num_heads: int = 8,
        num_layers: int = 3,
        dropout_rate: float = 0.1
    ):
        """Initialize inference handler."""
        try:
            # Inicializar modelo
            self.model = CapibaraModel(
                hidden_size=hidden_size,
                num_heads=num_heads,
                num_layers=num_layers,
                dropout_rate=dropout_rate
            )
            
            # Inicializar parámetros
            self.params = self.model.init(
                jax.random.PRNGKey(0),
                jnp.ones((1, 1, hidden_size)),
                jnp.ones((1, 1, hidden_size))
            )
            
            logger.info("Inference handler initialized")
            
        except Exception as e:
            logger.error(f"Error initializing inference: {e}")
            raise
    
    def _preprocess(
        self,
        x: jnp.ndarray,
        context: Optional[jnp.ndarray] = None
    ) -> Dict[str, jnp.ndarray]:
        """Preprocess inputs."""
        try:
            # Validar y ajustar entrada
            if x.ndim == 2:
                x = x[None, ...]
            elif x.ndim != 3:
                raise ValueError(
                    f"Expected 2D or 3D input, got shape {x.shape}"
                )
            
            # Crear contexto si no existe
            if context is None:
                context = jnp.zeros_like(x)
            elif context.ndim == 2:
                context = context[None, ...]
            
            # Validar shapes
            if x.shape != context.shape:
                raise ValueError(
                    f"Input and context must have same shape, got {x.shape} and {context.shape}"
                )
            
            return {
                'x': x,
                'context': context
            }
            
        except Exception as e:
            logger.error(f"Error preprocessing inputs: {e}")
            raise
    
    def __call__(
        self,
        x: jnp.ndarray,
        context: Optional[jnp.ndarray] = None,
        **kwargs: Any
    ) -> jnp.ndarray:
        """Run inference."""
        try:
            # Preprocesar entradas
            inputs = self._preprocess(x, context)
            
            # Forward pass
            return self.model.apply(
                self.params,
                inputs['x'],
                inputs['context'],
                training=False,
                **kwargs
            )
            
        except Exception as e:
            logger.error(f"Error during inference: {e}")
            raise
