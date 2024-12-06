"""Contextual activation module for CapibaraModel."""

import jax #type: ignore
import jax.numpy as jnp #type: ignore
from flax import linen as nn #type: ignore
import logging
from typing import Dict, Any

from capibara_model.modules.coherence_detector import CoherenceDetector

logger = logging.getLogger(__name__)

class ContextualActivation(nn.Module):
    """Módulo de activación contextual con scoring."""
    
    hidden_size: int
    num_heads: int = 8
    threshold: float = 0.5
    dropout_rate: float = 0.1
    
    def setup(self):
        """Initialize model parameters."""
        # Capas de codificación
        self.text_encoder = nn.Dense(self.hidden_size)
        self.context_encoder = nn.Dense(self.hidden_size)
        
        # Capas de scoring
        self.relevance = nn.Dense(self.hidden_size)
        self.score = nn.Dense(1)
        
        # Detector de coherencia
        self.coherence = CoherenceDetector(
            hidden_size=self.hidden_size,
            threshold=self.threshold,
            dropout_rate=self.dropout_rate
        )
        
        # Capas auxiliares
        self.norm = nn.LayerNorm()
        self.dropout = nn.Dropout(rate=self.dropout_rate)
    
    def _compute_relevance(
        self,
        x: jnp.ndarray,
        context: jnp.ndarray,
        training: bool = False
    ) -> jnp.ndarray:
        """Compute relevance scores."""
        # Codificar entradas
        x_encoded = self.text_encoder(x)
        c_encoded = self.context_encoder(context)
        
        # Normalización y dropout
        x_encoded = self.norm(x_encoded)
        c_encoded = self.norm(c_encoded)
        if training:
            x_encoded = self.dropout(x_encoded, deterministic=not training)
            c_encoded = self.dropout(c_encoded, deterministic=not training)
        
        # Calcular relevancia
        combined = jnp.concatenate([
            x_encoded,
            c_encoded,
            x_encoded * c_encoded
        ], axis=-1)
        
        scores = self.relevance(combined)
        scores = self.norm(scores)
        if training:
            scores = self.dropout(scores, deterministic=not training)
        scores = jax.nn.gelu(scores)
        
        return jax.nn.sigmoid(self.score(scores))
    
    def __call__(
        self,
        x: jnp.ndarray,
        context: jnp.ndarray,
        training: bool = False
    ) -> Dict[str, jnp.ndarray]:
        """Forward pass."""
        try:
            # Validar entrada
            if x.ndim != 3 or context.ndim != 3:
                raise ValueError(
                    f"Expected 3D inputs, got shapes {x.shape}, {context.shape}"
                )
            
            # Calcular relevancia
            relevance = self._compute_relevance(x, context, training)
            
            # Verificar coherencia
            coherence = self.coherence(x, context, training)
            
            # Activación basada en scores
            is_active = (relevance > self.threshold) & coherence
            
            return {
                'relevance': relevance,
                'coherence': coherence,
                'is_active': is_active
            }
            
        except Exception as e:
            logger.error(f"Error in contextual activation: {e}")
            raise
