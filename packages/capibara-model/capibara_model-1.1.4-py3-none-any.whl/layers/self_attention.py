"""Self-attention layer implementation for CapibaraModel."""

import jax #type: ignore
import jax.numpy as jnp #type: ignore
from flax import linen as nn #type: ignore
import logging
from typing import Optional, Dict

logger = logging.getLogger(__name__)

class SelfAttention(nn.Module):
    """Capa de auto-atención multi-cabeza."""
    
    hidden_size: int
    num_heads: int = 8
    dropout_rate: float = 0.1
    
    def setup(self):
        """Initialize model parameters."""
        if self.hidden_size % self.num_heads != 0:
            raise ValueError(
                f"hidden_size {self.hidden_size} debe ser divisible por num_heads {self.num_heads}"
            )
        
        # Dimensión por cabeza
        self.head_dim = self.hidden_size // self.num_heads
        self.scale = self.head_dim ** -0.5
        
        # Capas de proyección
        self.to_q = nn.Dense(self.hidden_size)
        self.to_k = nn.Dense(self.hidden_size)
        self.to_v = nn.Dense(self.hidden_size)
        self.to_out = nn.Dense(self.hidden_size)
        
        # Capas auxiliares
        self.norm = nn.LayerNorm()
        self.dropout = nn.Dropout(rate=self.dropout_rate)
    
    def _split_heads(
        self,
        x: jnp.ndarray,
        batch_size: int
    ) -> jnp.ndarray:
        """Split tensor into attention heads."""
        # Reshape: (batch, seq, hidden) -> (batch, seq, heads, head_dim)
        x = x.reshape(batch_size, -1, self.num_heads, self.head_dim)
        # Transpose: (batch, seq, heads, head_dim) -> (batch, heads, seq, head_dim)
        return x.transpose(0, 2, 1, 3)
    
    def _merge_heads(
        self,
        x: jnp.ndarray,
        batch_size: int
    ) -> jnp.ndarray:
        """Merge attention heads."""
        # Transpose: (batch, heads, seq, head_dim) -> (batch, seq, heads, head_dim)
        x = x.transpose(0, 2, 1, 3)
        # Reshape: (batch, seq, heads, head_dim) -> (batch, seq, hidden)
        return x.reshape(batch_size, -1, self.hidden_size)
    
    def __call__(
        self,
        x: jnp.ndarray,
        mask: Optional[jnp.ndarray] = None,
        training: bool = False
    ) -> jnp.ndarray:
        """Forward pass."""
        try:
            # Validar entrada
            if x.ndim != 3:
                raise ValueError(
                    f"Expected 3D input (batch, seq_len, dim), got shape {x.shape}"
                )
            
            batch_size = x.shape[0]
            
            # Residual
            residual = x
            
            # Normalización
            x = self.norm(x)
            
            # Proyecciones Q, K, V
            q = self.to_q(x)
            k = self.to_k(x)
            v = self.to_v(x)
            
            # Split heads
            q = self._split_heads(q, batch_size)
            k = self._split_heads(k, batch_size)
            v = self._split_heads(v, batch_size)
            
            # Calcular atención
            # (batch, heads, seq, head_dim) @ (batch, heads, head_dim, seq)
            attn = jnp.einsum('bhid,bhjd->bhij', q, k) * self.scale
            
            # Aplicar máscara si existe
            if mask is not None:
                attn = jnp.where(mask[:, None, :, :], attn, float('-inf'))
            
            # Softmax y dropout
            attn = jax.nn.softmax(attn, axis=-1)
            if training:
                attn = self.dropout(attn, deterministic=not training)
            
            # Aplicar atención a valores
            # (batch, heads, seq, seq) @ (batch, heads, seq, head_dim)
            out = jnp.einsum('bhij,bhjd->bhid', attn, v)
            
            # Merge heads y proyección final
            out = self._merge_heads(out, batch_size)
            out = self.to_out(out)
            if training:
                out = self.dropout(out, deterministic=not training)
            
            # Residual
            return out + residual
            
        except Exception as e:
            logger.error(f"Error in forward pass: {e}")
            raise