"""
Test module for the CapibaraModel data loader and model.

This module contains unit tests for the CapibaraDataset, data loading functions,
and model operations using JAX and Flax.

Classes:
    TestCapibaraJAX: Test class for the data loader and model.

Dependencies:
    - unittest: For creating and running unit tests.
    - jax: For array operations and gradients.
    - flax: For neural network layers and model definition.
"""

import unittest
import jax # type: ignore
import jax.numpy as jnp # type: ignore
from jax import random # type: ignore
import optax # type: ignore
from pathlib import Path

from capibara_model.core.config import CapibaraConfig
from capibara_model.core.model import create_large_capibara_model
from capibara_model.data.data_loader import CapibaraDataLoader
from capibara_model.data.dataset import CapibaraDataset


class TestCapibaraJAX(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """
        Set up the test environment for all test methods in the class.
        """
        cls.rng = random.PRNGKey(42)  # Random seed for reproducibility
        cls.test_data_dir = Path('tests/test_data')
        cls.test_data_dir.mkdir(parents=True, exist_ok=True)

    def setUp(self):
        """
        Sets up the test environment for each test method.
        """
        self.config = CapibaraConfig.from_dict({
            'training': {
                'batch_size': 16,
                'max_length': 50,
                'train_data_path': str(self.test_data_dir / 'train'),
                'val_data_path': str(self.test_data_dir / 'val')
            },
            'model': {
                'input_dim': 768,
                'hidden_size': 768,
                'num_layers': 12
            }
        })
        
        # Crear datos de prueba
        self._create_test_data()

    def _create_test_data(self):
        """
        Create test data files.
        """
        for split in ['train', 'val']:
            data_dir = self.test_data_dir / split
            data_dir.mkdir(exist_ok=True)
            
            # Crear archivo de prueba
            with open(data_dir / 'test.txt', 'w') as f:
                f.write('Sample text\n' * 100)

    def test_data_loader_creation(self):
        """
        Tests the creation of the CapibaraDataLoader.
        """
        data_loader = CapibaraDataLoader(
            dataset_path=str(self.test_data_dir / 'train'),
            batch_size=self.config.training.batch_size,
            max_length=self.config.training.max_length
        )
        
        batch = next(iter(data_loader))
        self.assertIn('bytes', batch)
        self.assertEqual(
            batch['bytes'].shape[1],
            self.config.training.max_length
        )

    def test_model_creation(self):
        """
        Tests the creation of the CapibaraModel model.
        """
        model, params = create_large_capibara_model(self.config)
        self.assertIsNotNone(model)
        self.assertIsNotNone(params)

    def test_forward_pass(self):
        """
        Tests a forward pass through the model.
        """
        model, params = create_large_capibara_model(self.config)
        batch_size = 2
        
        # Crear datos de prueba
        inputs = jnp.ones((batch_size, self.config.model.input_dim))
        context = jnp.ones((batch_size, self.config.model.input_dim))
        
        # Forward pass
        output, _ = model.apply(params, inputs, context)
        
        self.assertEqual(
            output.shape,
            (batch_size, self.config.model.hidden_size)
        )

    def test_gradient_computation(self):
        """
        Tests gradient computation for a forward and backward pass.
        """
        model, params = create_large_capibara_model(self.config)
        batch_size = 2
        
        # Crear datos de prueba
        inputs = jnp.ones((batch_size, self.config.model.input_dim))
        context = jnp.ones((batch_size, self.config.model.input_dim))
        targets = jnp.ones((batch_size, self.config.model.hidden_size))
        
        def loss_fn(params):
            output, _ = model.apply(params, inputs, context)
            return jnp.mean((output - targets) ** 2)
        
        grad_fn = jax.value_and_grad(loss_fn)
        loss, grads = grad_fn(params)
        
        self.assertFalse(jnp.isnan(loss))
        self.assertTrue(
            all(not jnp.any(jnp.isnan(g)) 
                for g in jax.tree_util.tree_leaves(grads))
        )


if __name__ == '__main__':
    unittest.main()
