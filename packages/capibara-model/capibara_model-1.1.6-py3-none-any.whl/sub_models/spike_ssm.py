"""Spike-SSM implementation for CapibaraModel."""

import jax #type: ignore
import jax.numpy as jnp #type: ignore
from flax import linen as nn #type: ignore
import logging
from typing import NamedTuple, Tuple, Optional

logger = logging.getLogger(__name__)

class SpikeState(NamedTuple):
    """Estado de neurona con spikes."""
    hidden: jnp.ndarray
    voltage: jnp.ndarray
    spikes: jnp.ndarray

class SpikeSSM(nn.Module):
    """SSM con neuronas que disparan."""
    
    hidden_size: int
    tau: float = 10.0  # Constante de tiempo
    threshold: float = 1.0  # Umbral de disparo
    reset_value: float = 0.0  # Valor post-spike
    dropout_rate: float = 0.1
    
    def setup(self):
        """Initialize model parameters."""
        # Capas de procesamiento
        self.input_proj = nn.Dense(self.hidden_size)
        self.hidden_proj = nn.Dense(self.hidden_size)
        self.output = nn.Dense(self.hidden_size)
        
        # Capas auxiliares
        self.norm = nn.LayerNorm()
        self.dropout = nn.Dropout(rate=self.dropout_rate)
    
    def _spike_step(
        self,
        x: jnp.ndarray,
        state: SpikeState,
        training: bool = False
    ) -> Tuple[jnp.ndarray, SpikeState]:
        """Single spike-based step."""
        # Procesar entrada
        input_current = self.input_proj(x)
        hidden_current = self.hidden_proj(state.hidden)
        
        if training:
            input_current = self.dropout(
                input_current,
                deterministic=not training
            )
            hidden_current = self.dropout(
                hidden_current,
                deterministic=not training
            )
        
        # Actualizar estado oculto
        dh = (-state.hidden + input_current + hidden_current) / self.tau
        new_hidden = state.hidden + dh
        
        # Actualizar voltaje
        dv = (-state.voltage + new_hidden) / self.tau
        new_voltage = state.voltage + dv
        
        # Generar spikes
        spikes = (new_voltage >= self.threshold).astype(jnp.float32)
        
        # Reset post-spike
        new_voltage = jnp.where(
            spikes > 0,
            self.reset_value,
            new_voltage
        )
        
        return spikes, SpikeState(new_hidden, new_voltage, spikes)
    
    def __call__(
        self,
        x: jnp.ndarray,
        initial_state: Optional[SpikeState] = None,
        training: bool = False
    ) -> Tuple[jnp.ndarray, SpikeState]:
        """Forward pass."""
        try:
            # Validar entrada
            if x.ndim != 3:
                raise ValueError(
                    f"Expected 3D input (batch, seq_len, dim), got shape {x.shape}"
                )
            
            batch_size = x.shape[0]
            
            # Inicializar estado si es necesario
            if initial_state is None:
                initial_state = SpikeState(
                    hidden=jnp.zeros((batch_size, self.hidden_size)),
                    voltage=jnp.zeros((batch_size, self.hidden_size)),
                    spikes=jnp.zeros((batch_size, self.hidden_size))
                )
            
            # Procesar secuencia
            def scan_fn(carry, x_t):
                state = carry
                spikes, new_state = self._spike_step(x_t, state, training)
                return new_state, spikes
            
            # Scan sobre la secuencia
            final_state, outputs = jax.lax.scan(
                scan_fn,
                initial_state,
                x.transpose(1, 0, 2)  # (seq_len, batch, dim)
            )
            
            # Procesar salida
            outputs = outputs.transpose(1, 0, 2)  # (batch, seq_len, dim)
            outputs = self.output(outputs)
            
            return outputs, final_state
            
        except Exception as e:
            logger.error(f"Error in forward pass: {e}")
            raise
