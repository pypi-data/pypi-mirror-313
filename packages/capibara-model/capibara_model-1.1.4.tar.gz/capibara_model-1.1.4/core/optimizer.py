"""Optimizer implementation for CapibaraModel."""

import jax #type: ignore
import optax #type: ignore
import logging
from typing import Dict, Any, Callable

logger = logging.getLogger(__name__)

def create_optimizer(
    config: Dict[str, Any]
) -> optax.GradientTransformation:
    """Create optimizer from config."""
    try:
        # Obtener parámetros
        learning_rate = config.get('learning_rate', 1e-3)
        weight_decay = config.get('weight_decay', 1e-4)
        
        # Crear schedule
        schedule = optax.warmup_cosine_decay_schedule(
            init_value=0.0,
            peak_value=learning_rate,
            warmup_steps=config.get('warmup_steps', 1000),
            decay_steps=config.get('total_steps', 100000)
        )
        
        # Crear optimizador
        optimizer = optax.chain(
            optax.clip_by_global_norm(1.0),
            optax.adamw(
                learning_rate=schedule,
                weight_decay=weight_decay
            )
        )
        
        logger.info("Optimizer created successfully")
        return optimizer
        
    except Exception as e:
        logger.error(f"Error creating optimizer: {e}")
        raise