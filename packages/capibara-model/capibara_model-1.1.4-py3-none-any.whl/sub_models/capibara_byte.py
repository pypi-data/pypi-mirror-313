"""
CapibaraByte: Byte-level state space model.

This model directly processes byte-level inputs with selective state updates.
"""

import jax  # type: ignore
import jax.numpy as jnp  # type: ignore
from flax import linen as nn  # type: ignore
import logging
from typing import Tuple

# Consistent logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class CapibaraByte(nn.Module):
    """
    Byte-level processing model with selective state updates.

    Attributes:
        hidden_size (int): Dimension of the hidden state.
        input_dim (int): Dimension of the input byte-level data.
        conv_dim (int): Dimension for convolutional processing within the state update.
        update_rate (float): Rate for selectively updating states.
    """
    hidden_size: int
    input_dim: int = 256  # Tamaño para bytes
    conv_dim: int = 4
    update_rate: float = 0.1

    def setup(self):
        """Initialize model parameters."""
        # Matrices de transformación
        self.W_in = self.param(
            'W_in',
            nn.initializers.normal(0.02),
            (self.input_dim, self.hidden_size)
        )
        self.W_state = self.param(
            'W_state',
            nn.initializers.normal(0.02),
            (self.hidden_size, self.hidden_size)
        )
        self.W_conv = self.param(
            'W_conv',
            nn.initializers.normal(0.02),
            (self.conv_dim, self.hidden_size)
        )
        
        # Bias
        self.bias = self.param(
            'bias',
            nn.initializers.zeros,
            (self.hidden_size,)
        )

    def _update_state(
        self,
        x: jnp.ndarray,
        state: jnp.ndarray
    ) -> jnp.ndarray:
        """
        Update state selectively.
        
        Args:
            x: Input tensor (batch_size, input_dim)
            state: Current state (batch_size, hidden_size)
            
        Returns:
            Updated state tensor
        """
        # Transformación convolucional
        conv_feat = jnp.dot(x, self.W_conv)
        
        # Actualización de estado
        state_update = (
            jnp.dot(state, self.W_state) +
            conv_feat +
            self.bias
        )
        
        # Actualización selectiva
        new_state = (
            (1 - self.update_rate) * state +
            self.update_rate * jax.nn.gelu(state_update)
        )
        
        return new_state

    def __call__(
        self,
        x: jnp.ndarray,
        training: bool = False
    ) -> Tuple[jnp.ndarray, jnp.ndarray]:
        """
        Forward pass.
        
        Args:
            x: Input tensor (batch_size, seq_len, input_dim)
            training: Whether in training mode
            
        Returns:
            Tuple of (output, final_state)
        """
        try:
            # Inicializar estado
            batch_size = x.shape[0]
            state = jnp.zeros((batch_size, self.hidden_size))
            
            # Procesar secuencia
            for i in range(x.shape[1]):
                byte_input = x[:, i:i+1]
                state = self._update_state(byte_input, state)
            
            # Salida final
            output = jnp.dot(state, self.W_state) + self.bias
            
            return output, state
            
        except Exception as e:
            logger.error(f"Error in forward pass: {e}")
            raise


# Example usage
if __name__ == "__main__":
    try:
        logger.info("Starting CapibaraByteSSM example")

        # Create example byte-level input data
        batch_size, seq_len, input_dim = 32, 10, 256
        key = jax.random.PRNGKey(0)
        x = jax.random.randint(key, (batch_size, seq_len, input_dim), 0, 256).astype(jnp.float32)  # Simulate bytes

        # Initialize the CapibaraByteSSM model
        layer = CapibaraByte(
            hidden_size=128,   # Size of the state
            input_dim=input_dim,   # Size of byte-level input
            conv_dim=4,            # Dimension of internal convolution
            update_rate=0.1        # Selective update rate
        )

        # Initialize parameters
        params = layer.init(key, x)
        logger.info("CapibaraByte parameters initialized")

        # Perform forward pass
        output, final_state = layer.apply(params, x)
        logger.info(f"Forward pass completed. Output shape: {output.shape}, Final state shape: {final_state.shape}")

        print(f"Output shape: {output.shape}")
        print(f"Final state: {final_state.shape}")
        logger.info("CapibaraByte example completed successfully")
    except Exception as e:
        logger.error(f"An error occurred during the CapibaraByte example: {str(e)}")
