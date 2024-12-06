"""Test module for CapibaraModel layers and submodels."""

import jax #type: ignore
import jax.numpy as jnp #type: ignore
import pytest #type: ignore
import haiku as hk #type: ignore
from typing import Type, Tuple, Optional

from capibara_model.layers.synthetic_embedding import SyntheticEmbedding
from capibara_model.layers.sparse_capibara import SparseCapibara
from capibara_model.sub_models.capibara_jax_ssm import CapibaraJAXSSM
from capibara_model.sub_models.capibara2 import Capibara2
from capibara_model.sub_models.deep_dialog import DeepDialogModel

# Test parameters
BATCH_SIZE = 2
INPUT_DIM = 768
HIDDEN_SIZE = 768
SEQ_LEN = 512

@pytest.fixture
def rng_key():
    """Provide random key for testing."""
    return jax.random.PRNGKey(0)

class TestSyntheticEmbedding:
    """Test suite for SyntheticEmbedding layer."""
    
    def test_forward_pass(self, rng_key):
        """Test forward pass shape and values."""
        def forward_fn(x):
            module = SyntheticEmbedding(dim=HIDDEN_SIZE)
            return module(x)
        
        forward = hk.transform(forward_fn)
        
        x = jnp.ones([BATCH_SIZE, INPUT_DIM])
        params = forward.init(rng_key, x)
        output = forward.apply(params, None, x)
        
        assert output.shape == (BATCH_SIZE, HIDDEN_SIZE)
        assert not jnp.any(jnp.isnan(output))

class TestSparseCapibara:
    """Test suite for SparseCapibara layer."""
    
    def test_forward_pass(self, rng_key):
        """Test forward pass shape and values."""
        def forward_fn(x):
            module = SparseCapibara(dim=HIDDEN_SIZE)
            return module(x)
        
        forward = hk.transform(forward_fn)
        
        x = jnp.ones([BATCH_SIZE, INPUT_DIM])
        params = forward.init(rng_key, x)
        output = forward.apply(params, None, x)
        
        assert output.shape == (BATCH_SIZE, HIDDEN_SIZE)
        assert not jnp.any(jnp.isnan(output))

class TestCapibaraJAXSSM:
    """Test suite for CapibaraJAXSSM model."""
    
    def test_forward_pass(self, rng_key):
        """Test forward pass shape and values."""
        def forward_fn(x):
            model = CapibaraJAXSSM(hidden_size=HIDDEN_SIZE)
            return model(x)
        
        forward = hk.transform(forward_fn)
        
        x = jnp.ones([BATCH_SIZE, SEQ_LEN, INPUT_DIM])
        params = forward.init(rng_key, x)
        output = forward.apply(params, None, x)
        
        assert output.shape == (BATCH_SIZE, SEQ_LEN, HIDDEN_SIZE)
        assert not jnp.any(jnp.isnan(output))

class TestCapibara2:
    """Test suite for Capibara2 model."""
    
    def test_forward_pass(self, rng_key):
        """Test forward pass shape and values."""
        def forward_fn(x):
            model = Capibara2(hidden_size=HIDDEN_SIZE)
            return model(x)
        
        forward = hk.transform(forward_fn)
        
        x = jnp.ones([BATCH_SIZE, INPUT_DIM])
        params = forward.init(rng_key, x)
        output = forward.apply(params, None, x)
        
        assert output.shape == (BATCH_SIZE, HIDDEN_SIZE)
        assert not jnp.any(jnp.isnan(output))

class TestDeepDialog:
    """Test suite for DeepDialog model."""
    
    def test_forward_pass(self, rng_key):
        """Test forward pass shape and values."""
        def forward_fn(inputs, context):
            model = DeepDialogModel(hidden_size=HIDDEN_SIZE)
            return model(inputs, context)
        
        forward = hk.transform(forward_fn)
        
        inputs = jnp.ones([BATCH_SIZE, INPUT_DIM])
        context = jnp.ones([BATCH_SIZE, INPUT_DIM])
        
        params = forward.init(rng_key, inputs, context)
        output, _ = forward.apply(params, None, inputs, context)
        
        assert output.shape == (BATCH_SIZE, HIDDEN_SIZE)
        assert not jnp.any(jnp.isnan(output))

def test_model_integration(rng_key):
    """Test integration between different components."""
    def forward_fn(x):
        embedding = SyntheticEmbedding(dim=HIDDEN_SIZE)
        sparse = SparseCapibara(dim=HIDDEN_SIZE)
        capibara2 = Capibara2(hidden_size=HIDDEN_SIZE)
        
        embedded = embedding(x)
        sparse_out = sparse(embedded)
        final_out = capibara2(sparse_out)
        return final_out
    
    forward = hk.transform(forward_fn)
    
    x = jnp.ones([BATCH_SIZE, INPUT_DIM])
    params = forward.init(rng_key, x)
    output = forward.apply(params, None, x)
    
    assert output.shape == (BATCH_SIZE, HIDDEN_SIZE)
    assert not jnp.any(jnp.isnan(output))
