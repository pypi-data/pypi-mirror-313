"""Liquid layer implementation for CapibaraModel."""

import jax #type: ignore
import jax.numpy as jnp #type: ignore
from flax import linen as nn #type: ignore
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class Liquid(nn.Module):
    """Liquid layer with dynamic expansion."""
    
    hidden_size: int
    expansion_factor: int = 4
    dropout_rate: float = 0.1
    
    def setup(self):
        """Initialize model parameters."""
        # Capas de expansión
        self.expand = nn.Dense(self.hidden_size * self.expansion_factor)
        self.contract = nn.Dense(self.hidden_size)
        
        # Capas de procesamiento
        self.process = nn.Dense(self.hidden_size)
        self.output = nn.Dense(self.hidden_size)
        
        # Capas auxiliares
        self.norm = nn.LayerNorm()
        self.dropout = nn.Dropout(rate=self.dropout_rate)
    
    def _expand_and_process(
        self,
        x: jnp.ndarray,
        training: bool = False
    ) -> jnp.ndarray:
        """Expand and process input."""
        # Expansión
        x = self.expand(x)
        x = self.norm(x)
        if training:
            x = self.dropout(x, deterministic=not training)
        x = jax.nn.gelu(x)
        
        # Procesamiento
        x = self.process(x)
        x = self.norm(x)
        if training:
            x = self.dropout(x, deterministic=not training)
        return jax.nn.gelu(x)
    
    def _contract_and_output(
        self,
        x: jnp.ndarray,
        residual: jnp.ndarray,
        training: bool = False
    ) -> jnp.ndarray:
        """Contract and generate output."""
        # Contracción
        x = self.contract(x)
        x = self.norm(x)
        if training:
            x = self.dropout(x, deterministic=not training)
        
        # Salida con residual
        x = x + residual
        x = self.output(x)
        return x
    
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
            
            # Guardar residual
            residual = x
            
            # Pipeline de procesamiento
            x = self._expand_and_process(x, training)
            output = self._contract_and_output(x, residual, training)
            
            return output
            
        except Exception as e:
            logger.error(f"Error in forward pass: {e}")
            raise
