"""Meta-LA layer implementation for CapibaraModel."""

import jax #type: ignore
import jax.numpy as jnp #type: ignore
from flax import linen as nn #type: ignore
import logging
from typing import Tuple

logger = logging.getLogger(__name__)

class MetaLA(nn.Module):
    """Meta Learning Attention con decaimiento dinámico."""
    
    hidden_size: int
    num_heads: int = 8
    head_dim: int = 64
    sparsity: float = 0.5
    dropout_rate: float = 0.1
    
    def setup(self):
        """Initialize model parameters."""
        # Capas de atención
        self.to_q = nn.Dense(self.num_heads * self.head_dim)
        self.to_k = nn.Dense(self.num_heads * self.head_dim)
        self.to_v = nn.Dense(self.num_heads * self.head_dim)
        self.to_out = nn.Dense(self.hidden_size)
        
        # Parámetros dinámicos
        self.scale = self.head_dim ** -0.5
        self.alpha = self.param(
            'alpha',
            nn.initializers.ones,
            (self.num_heads, self.head_dim)
        )
        self.aug_param = self.param(
            'aug_param',
            nn.initializers.normal(1.0),
            (1, self.num_heads, self.head_dim)
        )
        
        # Capas auxiliares
        self.norm = nn.LayerNorm()
        self.dropout = nn.Dropout(rate=self.dropout_rate)
    
    def _apply_attention(
        self,
        q: jnp.ndarray,
        k: jnp.ndarray,
        v: jnp.ndarray,
        training: bool = False
    ) -> jnp.ndarray:
        """Apply attention mechanism."""
        # Aplicar sparsidad
        if training:
            mask = jax.random.bernoulli(
                self.make_rng('dropout'),
                1 - self.sparsity,
                q.shape
            )
            q = q * mask
            k = k * mask
            v = v * mask
        
        # Decaimiento dinámico
        decay = jax.nn.sigmoid(self.alpha)
        
        def update_state(carry, inputs):
            state, k_i, v_i = carry, inputs[0], inputs[1]
            # Atención con decaimiento
            attn = jnp.einsum('bhd,bhd->bh', q, k_i) * self.scale
            attn = jax.nn.softmax(attn)
            # Actualizar estado
            new_state = decay * state + (1 - decay) * jnp.einsum('bh,bhd->bhd', attn, v_i)
            return new_state, new_state
        
        # Acumular estados
        init_state = jnp.zeros_like(v[:, 0])
        _, states = jax.lax.scan(update_state, init_state, (k, v))
        
        # Auto-aumentación
        aug = jax.nn.sigmoid(q * self.aug_param)
        output = q * states + aug
        
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
            
            # Proyecciones Q, K, V
            q = self.to_q(x)
            k = self.to_k(x)
            v = self.to_v(x)
            
            # Reshape para heads
            batch_size, seq_len = x.shape[:2]
            q = q.reshape(batch_size, seq_len, self.num_heads, self.head_dim)
            k = k.reshape(batch_size, seq_len, self.num_heads, self.head_dim)
            v = v.reshape(batch_size, seq_len, self.num_heads, self.head_dim)
            
            # Aplicar atención
            output = self._apply_attention(q, k, v, training)
            
            # Proyección final
            output = output.reshape(batch_size, seq_len, -1)
            output = self.to_out(output)
            
            # Normalización y dropout
            output = self.norm(output)
            if training:
                output = self.dropout(output, deterministic=not training)
            
            return output
            
        except Exception as e:
            logger.error(f"Error in forward pass: {e}")
            raise