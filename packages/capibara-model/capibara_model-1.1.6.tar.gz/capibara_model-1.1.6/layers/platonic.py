"""Platonic layer implementation for CapibaraModel."""

import jax #type: ignore
import jax.numpy as jnp #type: ignore
from flax import linen as nn #type: ignore
import logging
from typing import Dict, List, Tuple

logger = logging.getLogger(__name__)

class Platonic(nn.Module):
    """Capa para transformación de conceptos abstractos."""
    
    hidden_size: int
    num_concepts: int = 8
    threshold: float = 0.5
    dropout_rate: float = 0.1
    
    def setup(self):
        """Initialize model parameters."""
        # Capas de proyección
        self.encoder = nn.Dense(self.hidden_size)
        self.concept_proj = nn.Dense(self.hidden_size)
        self.output = nn.Dense(self.hidden_size)
        
        # Conceptos base
        self.concepts = self.param(
            'concepts',
            nn.initializers.normal(0.02),
            (self.num_concepts, self.hidden_size)
        )
        
        # Capas auxiliares
        self.norm = nn.LayerNorm()
        self.dropout = nn.Dropout(rate=self.dropout_rate)
    
    def _compute_similarities(
        self,
        x: jnp.ndarray,
        concepts: jnp.ndarray
    ) -> jnp.ndarray:
        """Compute cosine similarities."""
        # Normalizar vectores
        x_norm = x / jnp.linalg.norm(x, axis=-1, keepdims=True)
        concepts_norm = concepts / jnp.linalg.norm(concepts, axis=-1, keepdims=True)
        
        # Calcular similitud
        return jnp.einsum('bsd,cd->bsc', x_norm, concepts_norm)
    
    def _transform_to_concepts(
        self,
        x: jnp.ndarray,
        training: bool = False
    ) -> Tuple[jnp.ndarray, jnp.ndarray]:
        """Transform inputs to abstract concepts."""
        # Codificar entrada
        encoded = self.encoder(x)
        encoded = self.norm(encoded)
        if training:
            encoded = self.dropout(encoded, deterministic=not training)
        
        # Proyectar conceptos
        concepts = self.concept_proj(self.concepts)
        
        # Calcular similitudes
        similarities = self._compute_similarities(encoded, concepts)
        
        # Aplicar umbral
        mask = similarities > self.threshold
        similarities = similarities * mask
        
        # Combinar con conceptos
        output = jnp.einsum('bsc,cd->bsd', similarities, concepts)
        
        return output, similarities
    
    def __call__(
        self,
        x: jnp.ndarray,
        training: bool = False
    ) -> Tuple[jnp.ndarray, jnp.ndarray]:
        """Forward pass."""
        try:
            # Validar entrada
            if x.ndim != 3:
                raise ValueError(
                    f"Expected 3D input (batch, seq_len, dim), got shape {x.shape}"
                )
            
            # Transformar a conceptos
            concepts, similarities = self._transform_to_concepts(x, training)
            
            # Proyección final
            output = self.output(concepts)
            output = self.norm(output)
            if training:
                output = self.dropout(output, deterministic=not training)
            
            return output, similarities
            
        except Exception as e:
            logger.error(f"Error in forward pass: {e}")
            raise
