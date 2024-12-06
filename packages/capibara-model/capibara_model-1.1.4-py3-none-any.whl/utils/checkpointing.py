"""Utilities for model checkpointing."""
import os
import flax #type: ignore
import jax #type: ignore

def save_checkpoint(state, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'wb') as f:
        f.write(flax.serialization.to_bytes(state))

def load_checkpoint(state, path):
    with open(path, 'rb') as f:
        return flax.serialization.from_bytes(state, f.read()) 