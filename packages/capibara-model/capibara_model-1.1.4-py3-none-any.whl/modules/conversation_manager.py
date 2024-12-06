# capibara/modules/conversation_manager.py

"""Conversation manager implementation for CapibaraModel."""

import jax #type: ignore
import jax.numpy as jnp #type: ignore
from flax import linen as nn #type: ignore
import logging
from typing import Dict, Any, Optional

from capibara_model.modules.coherence_detector import CoherenceDetector
from capibara_model.modules.contextual_activation import ContextualActivation

logger = logging.getLogger(__name__)

class ConversationManager(nn.Module):
    """Manejador de conversaciones con coherencia y contexto."""
    
    hidden_size: int
    num_heads: int = 8
    threshold: float = 0.5
    dropout_rate: float = 0.1
    
    def setup(self):
        """Initialize model parameters."""
        # Capas de procesamiento
        self.context_encoder = nn.Dense(self.hidden_size)
        self.response_encoder = nn.Dense(self.hidden_size)
        self.output = nn.Dense(self.hidden_size)
        
        # Módulos especializados
        self.coherence = CoherenceDetector(
            hidden_size=self.hidden_size,
            threshold=self.threshold,
            dropout_rate=self.dropout_rate
        )
        
        self.activation = ContextualActivation(
            hidden_size=self.hidden_size,
            num_heads=self.num_heads,
            threshold=self.threshold,
            dropout_rate=self.dropout_rate
        )
        
        # Capas auxiliares
        self.norm = nn.LayerNorm()
        self.dropout = nn.Dropout(rate=self.dropout_rate)
    
    def _process_conversation(
        self,
        x: jnp.ndarray,
        context: jnp.ndarray,
        training: bool = False
    ) -> Dict[str, jnp.ndarray]:
        """Process conversation state."""
        # Codificar entradas
        x_encoded = self.context_encoder(x)
        c_encoded = self.response_encoder(context)
        
        # Normalización y dropout
        x_encoded = self.norm(x_encoded)
        c_encoded = self.norm(c_encoded)
        if training:
            x_encoded = self.dropout(x_encoded, deterministic=not training)
            c_encoded = self.dropout(c_encoded, deterministic=not training)
        
        # Verificar coherencia
        coherence = self.coherence(x_encoded, c_encoded, training)
        
        # Activación contextual
        activation = self.activation(x_encoded, c_encoded, training)
        
        # Combinar resultados
        output = self.output(
            x_encoded * activation['is_active'] * coherence
        )
        
        return {
            'output': output,
            'coherence': coherence,
            'activation': activation['is_active']
        }
    
    def __call__(
        self,
        x: jnp.ndarray,
        context: jnp.ndarray,
        training: bool = False
    ) -> Dict[str, jnp.ndarray]:
        """Forward pass."""
        try:
            # Validar entrada
            if x.ndim != 3 or context.ndim != 3:
                raise ValueError(
                    f"Expected 3D inputs, got shapes {x.shape}, {context.shape}"
                )
            
            # Procesar conversación
            return self._process_conversation(x, context, training)
            
        except Exception as e:
            logger.error(f"Error in conversation processing: {e}")
            raise
