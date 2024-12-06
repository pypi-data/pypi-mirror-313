"""Coherence detector implementation for CapibaraModel."""

import jax #type: ignore
import jax.numpy as jnp #type: ignore
from flax import linen as nn #type: ignore
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class CoherenceDetector(nn.Module):
    """Detector de coherencia entre contexto y respuesta."""
    
    hidden_size: int
    threshold: float = 0.5
    dropout_rate: float = 0.1
    
    def setup(self):
        """Initialize model parameters."""
        # Capas de codificación
        self.context_encoder = nn.Dense(self.hidden_size)
        self.response_encoder = nn.Dense(self.hidden_size)
        
        # Capas de comparación
        self.compare = nn.Dense(self.hidden_size)
        self.score = nn.Dense(1)
        
        # Capas auxiliares
        self.norm = nn.LayerNorm()
        self.dropout = nn.Dropout(rate=self.dropout_rate)
    
    def _encode_pair(
        self,
        context: jnp.ndarray,
        response: jnp.ndarray,
        training: bool = False
    ) -> Dict[str, jnp.ndarray]:
        """Encode context and response."""
        # Codificar contexto
        context_encoded = self.context_encoder(context)
        context_encoded = self.norm(context_encoded)
        if training:
            context_encoded = self.dropout(
                context_encoded,
                deterministic=not training
            )
        
        # Codificar respuesta
        response_encoded = self.response_encoder(response)
        response_encoded = self.norm(response_encoded)
        if training:
            response_encoded = self.dropout(
                response_encoded,
                deterministic=not training
            )
        
        return {
            'context': context_encoded,
            'response': response_encoded
        }
    
    def _compute_coherence(
        self,
        encoded: Dict[str, jnp.ndarray],
        training: bool = False
    ) -> jnp.ndarray:
        """Compute coherence score."""
        # Comparar encodings
        combined = jnp.concatenate([
            encoded['context'],
            encoded['response'],
            encoded['context'] * encoded['response']
        ], axis=-1)
        
        # Calcular score
        score = self.compare(combined)
        score = self.norm(score)
        if training:
            score = self.dropout(score, deterministic=not training)
        score = jax.nn.gelu(score)
        
        return jax.nn.sigmoid(self.score(score))
    
    def __call__(
        self,
        context: jnp.ndarray,
        response: jnp.ndarray,
        training: bool = False
    ) -> jnp.ndarray:
        """Forward pass."""
        try:
            # Validar entrada
            if context.ndim != 3 or response.ndim != 3:
                raise ValueError(
                    f"Expected 3D inputs, got shapes {context.shape}, {response.shape}"
                )
            
            # Codificar entradas
            encoded = self._encode_pair(context, response, training)
            
            # Calcular coherencia
            scores = self._compute_coherence(encoded, training)
            
            # Aplicar umbral
            return scores > self.threshold
            
        except Exception as e:
            logger.error(f"Error in coherence detection: {e}")
            raise
