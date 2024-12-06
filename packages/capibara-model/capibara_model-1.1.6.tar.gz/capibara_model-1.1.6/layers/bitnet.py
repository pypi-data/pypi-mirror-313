"""BitNet layer implementation for CapibaraModel."""

import jax #type: ignore
import jax.numpy as jnp #type: ignore
from flax import linen as nn #type: ignore
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class BitNet(nn.Module):
    """Capa BitNet con convolución 1D y activación GELU."""
    
    hidden_size: int
    kernel_size: int = 3
    groups: int = 1
    dropout_rate: float = 0.1
    use_norm: bool = True
    
    def setup(self):
        """Initialize model parameters."""
        # Capas principales
        self.conv = nn.Conv(
            features=self.hidden_size,
            kernel_size=(self.kernel_size,),
            padding='SAME',
            feature_group_count=self.groups,
            use_bias=False
        )
        
        # Capas auxiliares
        if self.use_norm:
            self.norm = nn.LayerNorm()
        self.dropout = nn.Dropout(rate=self.dropout_rate)
    
    def _validate_input(
        self,
        x: jnp.ndarray
    ) -> None:
        """Validate input dimensions."""
        if x.ndim != 3:
            raise ValueError(
                f"Expected 3D input (batch, seq_len, dim), got shape {x.shape}"
            )
        
        if x.shape[1] < self.kernel_size:
            raise ValueError(
                f"Sequence length {x.shape[1]} must be >= kernel size {self.kernel_size}"
            )
    
    def _process(
        self,
        x: jnp.ndarray,
        training: bool = False
    ) -> jnp.ndarray:
        """Process input through BitNet."""
        # Convolución
        x = self.conv(x)
        
        # Normalización
        if self.use_norm:
            x = self.norm(x)
        
        # Dropout
        if training:
            x = self.dropout(x, deterministic=not training)
        
        # Activación
        return jax.nn.gelu(x)
    
    def __call__(
        self,
        x: jnp.ndarray,
        training: bool = False
    ) -> jnp.ndarray:
        """Forward pass."""
        try:
            # Validar entrada
            self._validate_input(x)
            
            # Procesar
            return self._process(x, training)
            
        except Exception as e:
            logger.error(f"Error in forward pass: {e}")
            raise
