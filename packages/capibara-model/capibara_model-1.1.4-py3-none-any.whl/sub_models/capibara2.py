"""
Module that implements the Capibara2 model, a recurrent neural network using JAX/Flax.

This module provides an implementation of the Capibara2 model, which applies a
recurrent operation to input data efficiently. It includes functions for training
and evaluating the model.

Classes:
    Capibara2: Implements the Capibara2 model.

Functions:
    loss_fn: Computes the loss function.
    update: Performs a parameter update step.

Dependencies:
    - jax: For array operations and automatic differentiation.
    - flax: For neural network module definitions.
    - optax: For optimization algorithms.
"""

import jax # type: ignore
import jax.numpy as jnp # type: ignore
from flax import linen as nn # type: ignore
from functools import partial
import optax # type: ignore
import logging
from dotenv import load_dotenv # type: ignore
import os
from .capibara_jax_ssm import CapibaraJAXSSM
from typing import Tuple, Optional

# Load environment variables
load_dotenv()

# Consistent logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class Capibara2(nn.Module):
    """
    Implementation of the Capibara2 model with explicit state handling and normalization.

    Attributes:
        config (dict): Configuration for model dimensions and other parameters.
        dropout_rate (float): Dropout rate for regularization.
    """
    hidden_size: int
    dropout_rate: float = 0.1

    def setup(self):
        """Initialize model parameters."""
        # Componentes principales
        self.ssm = CapibaraJAXSSM(hidden_size=self.hidden_size)
        
        # Capas de procesamiento
        self.input_proj = nn.Dense(self.hidden_size)
        self.output_proj = nn.Dense(self.hidden_size)
        
        # Capas auxiliares
        self.norm = nn.LayerNorm()
        self.dropout = nn.Dropout(rate=self.dropout_rate)
    
    def _process_step(
        self,
        x: jnp.ndarray,
        state: jnp.ndarray,
        training: bool = False
    ) -> Tuple[jnp.ndarray, jnp.ndarray]:
        """Process single step."""
        # Proyección de entrada
        x = self.input_proj(x)
        x = self.norm(x)
        if training:
            x = self.dropout(x, deterministic=not training)
        
        # Procesamiento SSM
        x, new_state = self.ssm(x, state, training)
        
        # Proyección de salida
        output = self.output_proj(x)
        output = self.norm(output)
        if training:
            output = self.dropout(output, deterministic=not training)
        
        return output, new_state
    
    def __call__(
        self,
        x: jnp.ndarray,
        initial_state: Optional[jnp.ndarray] = None,
        training: bool = False
    ) -> Tuple[jnp.ndarray, jnp.ndarray]:
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
                initial_state = jnp.zeros((batch_size, self.hidden_size))
            
            # Procesar secuencia
            def scan_fn(carry, x_t):
                state = carry
                output, new_state = self._process_step(x_t, state, training)
                return new_state, output
            
            # Scan sobre la secuencia
            final_state, outputs = jax.lax.scan(
                scan_fn,
                initial_state,
                x.transpose(1, 0, 2)  # (seq_len, batch, dim)
            )
            
            # Transponer salida
            outputs = outputs.transpose(1, 0, 2)  # (batch, seq_len, dim)
            
            return outputs, final_state
            
        except Exception as e:
            logger.error(f"Error in forward pass: {e}")
            raise

    def get_config(self) -> dict:
        """
        Get the configuration of the Capibara2 model.

        Returns:
            dict: A dictionary containing the model's configuration.
        """
        return {
            "input_dim": self.hidden_size,
            "hidden_dim": self.hidden_size,
            "output_dim": self.hidden_size
        }

@jax.jit
def loss_fn(params, model, x, y):
    """
    Computes the loss function.

    Args:
        params: Current model parameters.
        model: The Capibara2 model instance.
        x: Input data for the loss computation.
        y: Target labels for the loss computation.

    Returns:
        A scalar value representing the loss.
    """
    y_pred = model.apply({'params': params}, x)
    return jnp.mean((y_pred - y) ** 2)

@partial(jax.jit, static_argnums=(1,))
def update(params, model, opt_state, x, y):
    """
    Performs a parameter update step.

    Args:
        params: Current model parameters.
        model: The Capibara2 model instance.
        opt_state: Current optimizer state.
        x: Input data for the update step.
        y: Target labels for the update step.

    Returns:
        A tuple containing the updated parameters and optimizer state.
    """
    grads = jax.grad(loss_fn)(params, model, x, y)
    updates, opt_state = optimizer.update(grads, opt_state, params)
    params = optax.apply_updates(params, updates)
    return params, opt_state

# Example usage
if __name__ == "__main__":
    try:
        # Load configurations from .env
        config = {
            "state_dim": int(os.getenv("CAPIBARA_STATE_DIM", 32)),
            "input_dim": int(os.getenv("CAPIBARA_INPUT_DIM", 256)),
            "output_dim": int(os.getenv("CAPIBARA_OUTPUT_DIM", 256)),
        }
        dropout_rate = float(os.getenv("CAPIBARA_DROPOUT_RATE", 0.1))
        learning_rate = float(os.getenv("CAPIBARA_LEARNING_RATE", 1e-3))

        # Create sample data
        key = jax.random.PRNGKey(0)
        batch_size = 32
        num_samples = 1024
        x_data = jax.random.normal(key, (num_samples, 10, config["input_dim"]))
        y_data = jax.random.normal(key, (num_samples, 10, config["output_dim"]))

        # Initialize the model
        model = Capibara2(config, dropout_rate)

        # Initialize parameters and optimizer
        params = model.init(key, x_data[:batch_size])['params']
        optimizer = optax.adam(learning_rate)
        opt_state = optimizer.init(params)

        # Training loop
        num_epochs = 10
        for epoch in range(num_epochs):
            for i in range(0, num_samples, batch_size):
                x_batch = x_data[i:i+batch_size]
                y_batch = y_data[i:i+batch_size]
                params, opt_state = update(params, model, opt_state, x_batch, y_batch)

            # Evaluation
            y_pred = model.apply({'params': params}, x_data)
            loss = jnp.mean((y_pred - y_data) ** 2)
            logger.info(f"Epoch {epoch + 1}, Loss: {loss:.4f}")

    except Exception as e:
        logger.exception(f"An error occurred: {str(e)}")
