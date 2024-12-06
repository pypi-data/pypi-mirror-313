"""Language utilities for CapibaraModel."""

import jax #type: ignore
import jax.numpy as jnp #type: ignore
import logging
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

class LanguageUtils:
    """Utilidades para procesamiento de texto y bytes."""
    
    @staticmethod
    def text_to_bytes(
        text: str,
        max_length: Optional[int] = None
    ) -> jnp.ndarray:
        """Convert text to byte array."""
        try:
            # Validar entrada
            if not text.strip():
                logger.warning("Empty text provided")
                return jnp.array([], dtype=jnp.uint8)
            
            # Convertir a bytes
            byte_list = list(text.encode("utf-8"))
            
            # Aplicar max_length
            if max_length is not None:
                byte_list = byte_list[:max_length]
            
            return jnp.array(byte_list, dtype=jnp.uint8)
            
        except Exception as e:
            logger.error(f"Error converting text to bytes: {e}")
            raise
    
    @staticmethod
    def bytes_to_text(
        byte_array: jnp.ndarray
    ) -> str:
        """Convert byte array to text."""
        try:
            # Validar entrada
            if byte_array.size == 0:
                logger.warning("Empty byte array provided")
                return ""
            
            # Convertir a texto
            return bytes(byte_array.tolist()).decode(
                "utf-8",
                errors="replace"
            )
            
        except Exception as e:
            logger.error(f"Error converting bytes to text: {e}")
            raise
    
    @staticmethod
    def normalize_text(
        text: str
    ) -> str:
        """Normalize text."""
        try:
            # Validar entrada
            if not text.strip():
                logger.warning("Empty text provided")
                return ""
            
            # Normalizar
            return " ".join(text.lower().split())
            
        except Exception as e:
            logger.error(f"Error normalizing text: {e}")
            raise
    
    @staticmethod
    def process_batch(
        texts: List[str],
        max_length: Optional[int] = None
    ) -> Dict[str, jnp.ndarray]:
        """Process batch of texts."""
        try:
            # Convertir textos
            bytes_arrays = [
                LanguageUtils.text_to_bytes(text, max_length)
                for text in texts
            ]
            
            # Padding a max_length
            if max_length is not None:
                bytes_arrays = [
                    jnp.pad(
                        arr,
                        (0, max_length - len(arr)),
                        mode='constant'
                    )
                    for arr in bytes_arrays
                ]
            
            # Convertir a batch
            return {
                'bytes': jnp.stack(bytes_arrays),
                'lengths': jnp.array([len(arr) for arr in bytes_arrays])
            }
            
        except Exception as e:
            logger.error(f"Error processing batch: {e}")
            raise
