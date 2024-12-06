"""Sparse Capibara layer implementation for CapibaraModel."""

import jax #type: ignore
import jax.numpy as jnp #type: ignore
from flax import linen as nn #type: ignore
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class SparseCapibara(nn.Module):
    """Capa con pesos dispersos para computación eficiente."""
    
    hidden_size: int
    sparsity: float = 0.5
    dropout_rate: float = 0.1
    
    def setup(self):
        """Initialize model parameters."""
        # Capas principales
        self.dense = nn.Dense(self.hidden_size, use_bias=False)
        
        # Máscara de sparsidad
        self.mask = self.param(
            'mask',
            self._init_mask,
            (self.hidden_size, self.hidden_size)
        )
        
        # Bias
        self.bias = self.param(
            'bias',
            nn.initializers.zeros,
            (self.hidden_size,)
        )
        
        # Capas auxiliares
        self.norm = nn.LayerNorm()
        self.dropout = nn.Dropout(rate=self.dropout_rate)
    
    def _init_mask(
        self,
        key: jnp.ndarray,
        shape: tuple
    ) -> jnp.ndarray:
        """Initialize sparsity mask."""
        # Generar máscara aleatoria
        mask = jax.random.uniform(key, shape) > self.sparsity
        return mask.astype(jnp.float32)
    
    def _apply_sparse(
        self,
        x: jnp.ndarray,
        training: bool = False
    ) -> jnp.ndarray:
        """Apply sparse weights."""
        # Proyección densa
        dense = self.dense(x)
        
        # Aplicar máscara de sparsidad
        sparse = dense * self.mask
        
        # Añadir bias
        output = sparse + self.bias
        
        # Normalización y dropout
        output = self.norm(output)
        if training:
            output = self.dropout(output, deterministic=not training)
        
        return output
    
    def __call__(
        self,
        x: jnp.ndarray,
        training: bool = False
    ) -> jnp.ndarray:
        """Forward pass."""
        try:
            # Validar entrada
            if x.ndim != 3:
                raise ValueError(
                    f"Expected 3D input (batch, seq_len, dim), got shape {x.shape}"
                )
            
            # Residual
            residual = x
            
            # Aplicar pesos dispersos
            output = self._apply_sparse(x, training)
            
            # Conexión residual
            return output + residual
            
        except Exception as e:
            logger.error(f"Error in forward pass: {e}")
            raise
