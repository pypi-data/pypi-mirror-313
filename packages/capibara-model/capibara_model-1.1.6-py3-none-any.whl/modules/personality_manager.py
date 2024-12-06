# capibara/modules/personality_manager.py

import jax #type: ignore
import jax.numpy as jnp #type: ignore
from flax import linen as nn #type: ignore
import logging
from typing import Dict, Any, Optional

from capibara_model.modules.contextual_activation import ContextualActivation

logger = logging.getLogger(__name__)

class PersonalityManager(nn.Module):
    """Manejador de personalidad para ajuste de respuestas."""
    
    hidden_size: int
    num_heads: int = 8
    num_traits: int = 4  # humor, extraversion, formality, empathy
    dropout_rate: float = 0.1
    
    def setup(self):
        """Initialize model parameters."""
        # Capas de codificación
        self.text_encoder = nn.Dense(self.hidden_size)
        self.trait_encoder = nn.Dense(self.hidden_size)
        
        # Capas de personalidad
        self.traits = self.param(
            'traits',
            nn.initializers.normal(0.02),
            (self.num_traits, self.hidden_size)
        )
        
        # Capas de ajuste
        self.adjust = nn.Dense(self.hidden_size)
        self.output = nn.Dense(self.hidden_size)
        
        # Activación contextual
        self.activation = ContextualActivation(
            hidden_size=self.hidden_size,
            num_heads=self.num_heads,
            dropout_rate=self.dropout_rate
        )
        
        # Capas auxiliares
        self.norm = nn.LayerNorm()
        self.dropout = nn.Dropout(rate=self.dropout_rate)
    
    def _apply_personality(
        self,
        x: jnp.ndarray,
        traits: jnp.ndarray,
        training: bool = False
    ) -> Dict[str, jnp.ndarray]:
        """Apply personality traits."""
        # Codificar entrada
        x_encoded = self.text_encoder(x)
        t_encoded = self.trait_encoder(traits)
        
        # Normalización y dropout
        x_encoded = self.norm(x_encoded)
        t_encoded = self.norm(t_encoded)
        if training:
            x_encoded = self.dropout(x_encoded, deterministic=not training)
            t_encoded = self.dropout(t_encoded, deterministic=not training)
        
        # Activación contextual
        activation = self.activation(x_encoded, t_encoded, training)
        
        # Ajuste de personalidad
        combined = jnp.concatenate([
            x_encoded,
            t_encoded,
            x_encoded * t_encoded
        ], axis=-1)
        
        adjusted = self.adjust(combined)
        adjusted = self.norm(adjusted)
        if training:
            adjusted = self.dropout(adjusted, deterministic=not training)
        adjusted = jax.nn.gelu(adjusted)
        
        # Salida final
        output = self.output(adjusted)
        
        return {
            'output': output,
            'traits': t_encoded,
            'activation': activation['is_active']
        }
    
    def __call__(
        self,
        x: jnp.ndarray,
        traits: Optional[jnp.ndarray] = None,
        training: bool = False
    ) -> Dict[str, jnp.ndarray]:
        """Forward pass."""
        try:
            # Validar entrada
            if x.ndim != 3:
                raise ValueError(
                    f"Expected 3D input, got shape {x.shape}"
                )
            
            # Usar traits por defecto si no se proporcionan
            if traits is None:
                traits = self.traits
            
            # Aplicar personalidad
            return self._apply_personality(x, traits, training)
            
        except Exception as e:
            logger.error(f"Error in personality adjustment: {e}")
            raise
