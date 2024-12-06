"""Dataset implementation for CapibaraModel."""

import jax #type: ignore
import jax.numpy as jnp #type: ignore
import logging
from typing import Dict, Any, List, Optional

from capibara_model.utils.language_utils import LanguageUtils

logger = logging.getLogger(__name__)

class CapibaraDataset:
    """Dataset para procesamiento de texto a bytes."""
    
    def __init__(
        self,
        texts: List[str],
        max_length: Optional[int] = None,
        batch_size: int = 32
    ):
        """Initialize dataset."""
        try:
            # Validar entrada
            if not texts:
                raise ValueError("Empty text list provided")
            
            # Guardar configuración
            self.max_length = max_length
            self.batch_size = batch_size
            
            # Procesar textos
            self.data = self._prepare_data(texts)
            
            logger.info(f"Dataset initialized with {len(texts)} texts")
            
        except Exception as e:
            logger.error(f"Error initializing dataset: {e}")
            raise
    
    def _prepare_data(
        self,
        texts: List[str]
    ) -> Dict[str, jnp.ndarray]:
        """Prepare text data."""
        try:
            # Convertir textos a bytes
            processed = LanguageUtils.process_batch(
                texts,
                max_length=self.max_length
            )
            
            # Crear targets (shift circular)
            targets = jnp.roll(processed['bytes'], -1, axis=1)
            
            return {
                'inputs': processed['bytes'],
                'targets': targets,
                'lengths': processed['lengths']
            }
            
        except Exception as e:
            logger.error(f"Error preparing data: {e}")
            raise
    
    def get_batch(
        self,
        idx: int
    ) -> Dict[str, jnp.ndarray]:
        """Get batch by index."""
        try:
            # Calcular índices
            start = idx * self.batch_size
            end = start + self.batch_size
            
            # Validar índices
            if start >= len(self.data['inputs']):
                raise IndexError(f"Batch index {idx} out of range")
            
            # Extraer batch
            return {
                'inputs': self.data['inputs'][start:end],
                'targets': self.data['targets'][start:end],
                'lengths': self.data['lengths'][start:end]
            }
            
        except Exception as e:
            logger.error(f"Error getting batch: {e}")
            raise
    
    def __len__(self) -> int:
        """Get number of batches."""
        return (len(self.data['inputs']) + self.batch_size - 1) // self.batch_size
    
    @classmethod
    def from_file(
        cls,
        file_path: str,
        max_length: Optional[int] = None,
        batch_size: int = 32
    ) -> 'CapibaraDataset':
        """Create dataset from file."""
        try:
            # Leer archivo
            with open(file_path, 'r', encoding='utf-8') as f:
                texts = [line.strip() for line in f]
            
            # Crear dataset
            return cls(texts, max_length, batch_size)
            
        except Exception as e:
            logger.error(f"Error loading from file: {e}")
            raise
