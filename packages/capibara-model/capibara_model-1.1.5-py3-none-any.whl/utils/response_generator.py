"""Response generator implementation for CapibaraModel."""

import jax #type: ignore
import jax.numpy as jnp #type: ignore
import logging
from typing import Dict, Any, Optional

from capibara_model.modules.coherence_detector import CoherenceDetector
from capibara_model.modules.contextual_activation import ContextualActivation
from capibara_model.modules.conversation_manager import ConversationManager
from capibara_model.modules.personality_manager import PersonalityManager

logger = logging.getLogger(__name__)

class ResponseGenerator:
    """Generador de respuestas con procesamiento contextual."""
    
    def __init__(
        self,
        hidden_size: int,
        num_heads: int = 8,
        dropout_rate: float = 0.1
    ):
        """Initialize response generator."""
        try:
            # Inicializar módulos
            self.coherence = CoherenceDetector(
                hidden_size=hidden_size,
                dropout_rate=dropout_rate
            )
            
            self.activation = ContextualActivation(
                hidden_size=hidden_size,
                num_heads=num_heads,
                dropout_rate=dropout_rate
            )
            
            self.conversation = ConversationManager(
                hidden_size=hidden_size,
                num_heads=num_heads,
                dropout_rate=dropout_rate
            )
            
            self.personality = PersonalityManager(
                hidden_size=hidden_size,
                num_heads=num_heads,
                dropout_rate=dropout_rate
            )
            
            logger.info("Response generator initialized")
            
        except Exception as e:
            logger.error(f"Error initializing response generator: {e}")
            raise
    
    def _process_response(
        self,
        x: jnp.ndarray,
        context: jnp.ndarray,
        training: bool = False
    ) -> Dict[str, jnp.ndarray]:
        """Process response with all modules."""
        try:
            # Verificar coherencia
            coherence = self.coherence(x, context, training)
            
            # Activación contextual
            activation = self.activation(x, context, training)
            
            # Manejo de conversación
            conversation = self.conversation(x, context, training)
            
            # Ajuste de personalidad
            personality = self.personality(x, training=training)
            
            # Combinar resultados
            output = x * coherence['is_coherent']
            output = output * activation['is_active']
            output = output * conversation['activation']
            output = output * personality['activation']
            
            return {
                'output': output,
                'coherence': coherence['is_coherent'],
                'activation': activation['is_active'],
                'conversation': conversation['activation'],
                'personality': personality['activation']
            }
            
        except Exception as e:
            logger.error(f"Error processing response: {e}")
            raise
    
    def __call__(
        self,
        x: jnp.ndarray,
        context: Optional[jnp.ndarray] = None,
        training: bool = False
    ) -> Dict[str, jnp.ndarray]:
        """Generate response."""
        try:
            # Validar entrada
            if x.ndim != 3:
                raise ValueError(
                    f"Expected 3D input, got shape {x.shape}"
                )
            
            # Crear contexto si no existe
            if context is None:
                context = jnp.zeros_like(x)
            
            # Procesar respuesta
            return self._process_response(x, context, training)
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            raise 