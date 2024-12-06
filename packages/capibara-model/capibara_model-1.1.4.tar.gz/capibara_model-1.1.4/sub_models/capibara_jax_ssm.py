"""State Space Model implementation for CapibaraModel."""

import jax #type: ignore
import jax.numpy as jnp #type: ignore
from flax import linen as nn #type: ignore
import logging
from typing import Tuple, Optional

logger = logging.getLogger(__name__)

class CapibaraJAXSSM(nn.Module):
    """State Space Model with selective updates."""
    
    hidden_size: int
    dropout_rate: float = 0.1
    
    def setup(self):
        """Initialize model parameters."""
        # Matrices principales
        self.A = self.param(
            'A',
            self._hippo_init,
            (self.hidden_size, self.hidden_size)
        )
        self.B = self.param(
            'B',
            nn.initializers.normal(0.02),
            (self.hidden_size, self.hidden_size)
        )
        self.C = self.param(
            'C',
            nn.initializers.normal(0.02),
            (self.hidden_size, self.hidden_size)
        )
        
        # Capas adicionales
        self.norm = nn.LayerNorm()
        self.dropout = nn.Dropout(rate=self.dropout_rate)
        self.output = nn.Dense(self.hidden_size)
    
    def _hippo_init(self, key: jnp.ndarray, shape: Tuple) -> jnp.ndarray:
        """Initialize using HiPPO method."""
        N = shape[0]
        P = jnp.sqrt(1.0 / jnp.arange(1, 2 * N, 2))
        A = P[:, None] * P[None, :]
        A = A / (P[:, None] ** 2 + P[None, :] ** 2)
        return A
    
    def _ssm_step(
        self,
        x: jnp.ndarray,
        state: jnp.ndarray,
        training: bool = False
    ) -> Tuple[jnp.ndarray, jnp.ndarray]:
        """Single SSM step."""
        # Normalización y dropout
        x = self.norm(x)
        if training:
            x = self.dropout(x, deterministic=not training)
        
        # Actualización de estado
        new_state = (
            jnp.dot(self.A, state) +
            jnp.dot(self.B, x)
        )
        
        # Salida
        output = jnp.dot(self.C, new_state)
        output = self.output(output)
        
        return output, new_state
    
    def __call__(
        self,
        x: jnp.ndarray,
        state: Optional[jnp.ndarray] = None,
        training: bool = False
    ) -> Tuple[jnp.ndarray, jnp.ndarray]:
        """Forward pass."""
        try:
            batch_size = x.shape[0]
            
            # Inicializar estado si es necesario
            if state is None:
                state = jnp.zeros((batch_size, self.hidden_size))
            
            # Procesar secuencia
            outputs = []
            current_state = state
            
            for i in range(x.shape[1]):
                output, current_state = self._ssm_step(
                    x[:, i],
                    current_state,
                    training
                )
                outputs.append(output)
            
            # Concatenar resultados
            final_output = jnp.stack(outputs, axis=1)
            
            return final_output, current_state
            
        except Exception as e:
            logger.error(f"Error in forward pass: {e}")
            raise
