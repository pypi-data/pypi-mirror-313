"""Test module for utility functions."""

import pytest #type: ignore
import jax #type: ignore
import jax.numpy as jnp #type: ignore
from pathlib import Path

from capibara_model.utils.data_processing import (
    text_to_bytes,
    bytes_to_text,
    prepare_training_data
)
from capibara_model.utils.logging import setup_logging, log_metrics
from capibara_model.utils.checkpointing import save_checkpoint, load_checkpoint


def test_text_to_bytes_conversion():
    """Test text to bytes conversion."""
    text = "Hello, world!"
    bytes_data = text_to_bytes(text)
    
    assert isinstance(bytes_data, list)
    assert all(isinstance(b, int) for b in bytes_data)
    assert all(0 <= b <= 255 for b in bytes_data)
    
    # Test round trip
    recovered_text = bytes_to_text(bytes_data)
    assert recovered_text == text


def test_prepare_training_data():
    """Test training data preparation."""
    texts = ["Hello", "World"]
    training_data = prepare_training_data(texts)
    
    assert len(training_data) == len(texts)
    for input_bytes, target_bytes in training_data:
        assert len(input_bytes) == len(target_bytes)
        assert all(0 <= b <= 255 for b in input_bytes)
        assert all(0 <= b <= 255 for b in target_bytes)


@pytest.fixture
def temp_checkpoint_dir(tmp_path):
    """Create temporary directory for checkpoints."""
    checkpoint_dir = tmp_path / "checkpoints"
    checkpoint_dir.mkdir()
    return checkpoint_dir


def test_checkpointing(temp_checkpoint_dir):
    """Test checkpoint save and load."""
    # Crear datos de prueba
    params = {
        'layer_1': jnp.ones((10, 10)),
        'layer_2': jnp.zeros((5, 5))
    }
    
    # Guardar checkpoint
    checkpoint_path = temp_checkpoint_dir / "test_checkpoint.pkl"
    save_checkpoint(params, str(checkpoint_path))
    
    # Cargar checkpoint
    loaded_params = load_checkpoint(params, str(checkpoint_path))
    
    # Verificar datos
    assert isinstance(loaded_params, dict)
    assert all(k in loaded_params for k in params)
    assert all(jnp.array_equal(loaded_params[k], params[k]) for k in params)


def test_logging(caplog):
    """Test logging configuration and metrics."""
    # Configurar logging
    config = {'log_level': 'DEBUG'}
    setup_logging(config)
    
    # Log metrics
    metrics = {
        'loss': 0.5,
        'accuracy': 0.95
    }
    log_metrics(metrics, step=1)
    
    # Verificar logs
    assert 'loss' in caplog.text
    assert 'accuracy' in caplog.text


def test_data_processing_edge_cases():
    """Test edge cases in data processing."""
    # Test empty text
    assert text_to_bytes("") == []
    
    # Test special characters
    special_text = "Hello 🌍!"
    bytes_data = text_to_bytes(special_text)
    recovered_text = bytes_to_text(bytes_data)
    assert recovered_text == special_text
    
    # Test long text
    long_text = "a" * 1000
    bytes_data = text_to_bytes(long_text)
    assert len(bytes_data) == 1000


def test_invalid_checkpoint_handling(temp_checkpoint_dir):
    """Test handling of invalid checkpoints."""
    invalid_path = temp_checkpoint_dir / "nonexistent.pkl"
    
    with pytest.raises(FileNotFoundError):
        load_checkpoint({}, str(invalid_path))
    
    # Test corrupted file
    corrupted_path = temp_checkpoint_dir / "corrupted.pkl"
    corrupted_path.write_bytes(b"corrupted data")
    
    with pytest.raises(Exception):
        load_checkpoint({}, str(corrupted_path))
