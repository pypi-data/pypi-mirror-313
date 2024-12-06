"""
Data loader module for CapibaraGPT model.

This module provides utilities for loading and preprocessing data
in raw byte format for training and inference.
"""

# Standard library imports
from typing import Dict, List, Iterator, Any, Tuple
from pathlib import Path
import logging
import jax #type: ignore
import jax.numpy as jnp  # type: ignore
import tensorflow as tf  # type: ignore
from capibara_model.data.dataset import CapibaraDataset

logger = logging.getLogger(__name__)

class CapibaraDataLoader:
    """
    Data loader for CapibaraGPT model training and inference.

    Handles data loading, preprocessing, and batching operations.
    Works directly with raw byte sequences.
    """

    def __init__(
        self,
        dataset_path: str,
        batch_size: int = 32,
        shuffle: bool = True,
        num_workers: int = 4,
        max_length: int = 512
    ):
        """Initialize the data loader with validation."""
        if not Path(dataset_path).exists():
            raise ValueError(f"Dataset path does not exist: {dataset_path}")
        if batch_size <= 0:
            raise ValueError(f"Batch size must be positive, got {batch_size}")
        if max_length <= 0:
            raise ValueError(f"Max length must be positive, got {max_length}")
        
        self.dataset_path = dataset_path
        self.batch_size = batch_size
        self.shuffle = shuffle
        self.num_workers = num_workers
        self.max_length = max_length
        
        self.dataset = self._load_data()
        self._create_loader()

    def _create_loader(self) -> None:
        """Creates a tf.data.Dataset optimized for TPU."""
        options = tf.data.Options()
        options.experimental_distribute.auto_shard_policy = (
            tf.data.experimental.AutoShardPolicy.DATA
        )
        
        dataset = tf.data.Dataset.from_generator(
            self._data_generator,
            output_signature={
                'bytes': tf.TensorSpec(shape=(self.max_length,), dtype=tf.uint8),
                'labels': tf.TensorSpec(shape=(), dtype=tf.int32)
            }
        )
        
        dataset = dataset.batch(self.batch_size, drop_remainder=True)  # Importante para TPU
        dataset = dataset.prefetch(tf.data.AUTOTUNE)
        dataset = dataset.with_options(options)
        
        self.dataset = dataset

    def _data_generator(self) -> Iterator[Dict[str, Any]]:
        """
        Generator to iterate over the data and yield byte sequences.
        """
        indices = jnp.arange(len(self.dataset))
        if self.shuffle:
            indices = jax.random.permutation(jax.random.PRNGKey(0), indices)

        for idx in indices:
            data_point = self.dataset[idx]
            yield {
                'bytes': self._process_bytes(data_point['bytes']),
                'labels': data_point.get('labels', -1)  # Default label if not provided
            }

    def _process_bytes(self, byte_sequence: bytes) -> jnp.ndarray:
        """Processes raw bytes into a fixed-size array."""
        try:
            byte_array = jnp.frombuffer(byte_sequence, dtype=jnp.uint8)
            if len(byte_array) > self.max_length:
                byte_array = byte_array[:self.max_length]
            else:
                padding = self.max_length - len(byte_array)
                byte_array = jnp.pad(byte_array, (0, padding), mode='constant')
            return byte_array
        except Exception as e:
            logger.error(f"Error processing bytes: {e}")
            # Retornar un array de ceros en caso de error
            return jnp.zeros(self.max_length, dtype=jnp.uint8)

    def _load_data(self) -> List[Dict[str, Any]]:
        """
        Loads the dataset from the specified path.

        Returns:
            List[Dict[str, Any]]: List of data points with byte sequences and optional labels.
        """
        data = []
        try:
            for file_path in Path(self.dataset_path).rglob("*"):
                with open(file_path, "rb") as f:
                    byte_sequence = f.read()
                    data.append({'bytes': byte_sequence})
            logger.info(f"Loaded {len(data)} data points from {self.dataset_path}.")
        except Exception as e:
            logger.error(f"Error loading dataset from {self.dataset_path}: {e}")
        return data

    def __iter__(self) -> Iterator[Dict[str, Any]]:
        """
        Returns an iterator over the batches.
        """
        return iter(self.dataset)

    def __len__(self) -> int:
        """
        Returns the number of batches.
        """
        return (len(self.dataset) + self.batch_size - 1) // self.batch_size

    @staticmethod
    def get_data_loaders(config) -> Tuple['CapibaraDataLoader', 'CapibaraDataLoader']:
        """Creates training and validation data loaders."""
        train_loader = CapibaraDataLoader(
            dataset_path=config.training.train_data_path,
            batch_size=config.training.batch_size,
            max_length=config.training.max_length
        )
        
        val_loader = CapibaraDataLoader(
            dataset_path=config.training.val_data_path,
            batch_size=config.training.batch_size,
            shuffle=False,
            max_length=config.training.max_length
        )
        
        return train_loader, val_loader

    def __del__(self):
        """Cleanup method."""
        try:
            del self.dataset
        except Exception as e:
            logger.warning(f"Error during cleanup: {e}")
