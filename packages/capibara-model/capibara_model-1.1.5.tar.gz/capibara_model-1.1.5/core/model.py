"""Core model implementation for CapibaraModel."""

import jax #type: ignore
import jax.numpy as jnp #type: ignore
from flax import linen as nn #type: ignore
import logging
from typing import Dict, Tuple, Optional

from capibara_model.layers.self_attention import SelfAttention
from capibara_model.layers.synthetic_embedding import SyntheticEmbedding
from capibara_model.layers.sparse_capibara import SparseCapibara
from capibara_model.layers.meta_la import MetaLA

logger = logging.getLogger(__name__)

class CapibaraModel(nn.Module):
    """Modelo principal de Capibara."""
    
    hidden_size: int
    num_heads: int = 8
    num_layers: int = 3
    dropout_rate: float = 0.1
    
    def setup(self):
        """Initialize model parameters."""
        # Capas de entrada
        self.embedding = SyntheticEmbedding(
            hidden_size=self.hidden_size,
            dropout_rate=self.dropout_rate
        )
        
        # Capas de atención
        self.attention = SelfAttention(
            hidden_size=self.hidden_size,
            num_heads=self.num_heads,
            dropout_rate=self.dropout_rate
        )
        
        # Capas de procesamiento
        self.sparse = SparseCapibara(
            hidden_size=self.hidden_size,
            dropout_rate=self.dropout_rate
        )
        
        # Capas meta-learning
        self.meta = MetaLA(
            hidden_size=self.hidden_size,
            num_heads=self.num_heads,
            dropout_rate=self.dropout_rate
        )
        
        # Capas auxiliares
        self.norm = nn.LayerNorm()
        self.dropout = nn.Dropout(rate=self.dropout_rate)
    
    def _process_sequence(
        self,
        x: jnp.ndarray,
        context: jnp.ndarray,
        training: bool = False
    ) -> jnp.ndarray:
        """Process input sequence."""
        # Embedding inicial
        x = self.embedding(x, training=training)
        
        # Atención con contexto
        x = self.attention(x, training=training)
        x = self.norm(x)
        if training:
            x = self.dropout(x, deterministic=not training)
        
        # Procesamiento sparse
        x = self.sparse(x, training=training)
        x = self.norm(x)
        if training:
            x = self.dropout(x, deterministic=not training)
        
        # Meta-learning
        x = self.meta(x, context, training=training)
        
        return x
    
    def __call__(
        self,
        x: jnp.ndarray,
        context: jnp.ndarray,
        training: bool = False
    ) -> jnp.ndarray:
        """Forward pass."""
        try:
            # Validar entrada
            if x.ndim != 3 or context.ndim != 3:
                raise ValueError(
                    f"Expected 3D inputs, got shapes {x.shape}, {context.shape}"
                )
            
            # Procesar secuencia
            return self._process_sequence(x, context, training)
            
        except Exception as e:
            logger.error(f"Error in forward pass: {e}")
            raise

