"""Test suite for CapibaraModel."""
import pytest  # type: ignore
import jax  # type: ignore
import jax.numpy as jnp  # type: ignore
import optax  # type: ignore

from capibara_model.core.config import CapibaraConfig
from capibara_model.core.model import create_large_capibara_model
from capibara_model.data.data_loader import CapibaraDataLoader

@pytest.fixture
def config():
    """Create test configuration."""
    return CapibaraConfig.from_yaml('config/config_minimal_tpu.yaml')

@pytest.fixture
def model(config):
    """Create test model."""
    model, _ = create_large_capibara_model(config)
    return model

@pytest.fixture
def data_loaders(config):
    """Create test data loaders."""
    return CapibaraDataLoader.get_data_loaders(config)

def test_model_creation(model, config):
    """Test model initialization."""
    assert model is not None
    assert model.config.model.input_dim == config.model.input_dim
    assert model.config.model.hidden_size == config.model.hidden_size

def test_data_loading(data_loaders):
    """Test data loading functionality."""
    train_loader, val_loader = data_loaders
    assert train_loader is not None
    assert val_loader is not None
    
    # Verificar que los loaders tienen datos
    train_batch = next(iter(train_loader))
    assert 'bytes' in train_batch
    assert train_batch['bytes'].shape[1] == train_loader.max_length

def test_forward_pass(model, config):
    """Test model forward pass."""
    batch_size = 2
    input_dim = config.model.input_dim
    
    # Crear datos de prueba
    inputs = jnp.ones((batch_size, input_dim))
    context = jnp.ones((batch_size, input_dim))
    
    # Inicializar parámetros
    rng = jax.random.PRNGKey(0)
    params = model.init(rng, inputs, context)
    
    # Ejecutar forward pass
    output, state = model.apply(params, inputs, context)
    
    # Verificar dimensiones de salida
    assert output.shape[0] == batch_size
    assert output.shape[-1] == config.model.hidden_size

@pytest.mark.parametrize("batch_size", [1, 4, 8])
def test_batch_processing(model, config, batch_size):
    """Test processing of different batch sizes."""
    input_dim = config.model.input_dim
    
    # Crear datos de prueba
    inputs = jnp.ones((batch_size, input_dim))
    context = jnp.ones((batch_size, input_dim))
    
    # Inicializar parámetros
    rng = jax.random.PRNGKey(0)
    params = model.init(rng, inputs, context)
    
    # Ejecutar forward pass
    output, state = model.apply(params, inputs, context)
    
    # Verificar dimensiones de salida
    assert output.shape[0] == batch_size
    assert output.shape[-1] == config.model.hidden_size

def test_model_training_step(model, config):
    """Test single training step."""
    batch_size = 2
    input_dim = config.model.input_dim
    
    # Crear datos de prueba
    inputs = jnp.ones((batch_size, input_dim))
    context = jnp.ones((batch_size, input_dim))
    targets = jnp.ones((batch_size, config.model.hidden_size))
    
    # Inicializar estado de entrenamiento
    rng = jax.random.PRNGKey(0)
    learning_rate = config.training.learning_rate
    
    # Ejecutar paso de entrenamiento
    params = model.init(rng, inputs, context)
    optimizer = optax.adam(learning_rate)
    opt_state = optimizer.init(params)
    
    def loss_fn(params):
        output, _ = model.apply(params, inputs, context)
        return jnp.mean((output - targets) ** 2)
    
    loss_grad_fn = jax.value_and_grad(loss_fn)
    loss, grads = loss_grad_fn(params)
    
    # Verificar que el loss y gradientes son válidos
    assert not jnp.isnan(loss)
    assert all(not jnp.any(jnp.isnan(g)) for g in jax.tree_util.tree_leaves(grads))