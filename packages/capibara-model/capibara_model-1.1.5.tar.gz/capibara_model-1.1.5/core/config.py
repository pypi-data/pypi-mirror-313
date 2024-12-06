"""Configuration management for CapibaraModel."""

import os
from typing import Optional, Dict, Any
from dataclasses import dataclass
from marshmallow_dataclass import class_schema #type: ignore
from marshmallow import ValidationError, validates, validates_schema #type: ignore
import yaml #type: ignore
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

@dataclass
class TrainingConfig:
    """Training configuration."""
    train_data_path: str
    val_data_path: str
    seed: int = 42
    batch_size: int = 32
    learning_rate: float = 0.001
    num_epochs: int = 10
    max_length: int = 512
    checkpoint_frequency: int = 1000
    contextual_activation_frequency: int = 100

    @validates('batch_size')
    def validate_batch_size(self, value: int) -> None:
        if value <= 0:
            raise ValidationError("batch_size must be positive")

@dataclass
class ModelConfig:
    """Model architecture configuration."""
    input_dim: int = 768
    hidden_size: int = 768
    seq_len: int = 512
    num_layers: int = 12
    dropout_rate: float = 0.1
    activation_function: str = 'relu'

    @validates('dropout_rate')
    def validate_dropout(self, value: float) -> None:
        if not 0 <= value <= 1:
            raise ValidationError("dropout_rate must be between 0 and 1")

@dataclass
class PruningConfig:
    """Model pruning configuration."""
    mor_threshold: float = 0.7
    sparsity_ratio: float = 0.5
    pruning_method: str = 'magnitude'
    pruning_schedule: str = 'constant'

    @validates_schema
    def validate_values(self, data: Dict, **kwargs) -> None:
        if not 0 <= data['sparsity_ratio'] <= 1:
            raise ValidationError("sparsity_ratio must be between 0 and 1")
        if not 0 <= data['mor_threshold'] <= 1:
            raise ValidationError("mor_threshold must be between 0 and 1")

@dataclass
class WandbConfig:
    """Weights & Biases configuration."""
    project: str = 'capibara_project'
    entity: str = 'default_entity'
    log_model: bool = True
    log_gradients: bool = True
    run_name: str = 'training_run'

@dataclass
class CapibaraConfig:
    """Main configuration container."""
    training: TrainingConfig
    model: ModelConfig
    pruning: PruningConfig
    wandb: WandbConfig

    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> 'CapibaraConfig':
        """Create config from dictionary."""
        try:
            schema = class_schema(cls)()
            return schema.load(config_dict)
        except ValidationError as e:
            logger.error(f"Configuration validation failed: {e}")
            raise

    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary."""
        try:
            schema = class_schema(self.__class__)()
            return schema.dump(self)
        except Exception as e:
            logger.error(f"Error converting config to dict: {e}")
            raise

    @classmethod
    def from_yaml(cls, yaml_path: str) -> 'CapibaraConfig':
        """Load config from YAML file."""
        try:
            path = Path(yaml_path)
            if not path.exists():
                raise FileNotFoundError(f"Config file not found: {path}")
            
            with open(path) as f:
                config_dict = yaml.safe_load(f)
            
            return cls.from_dict(config_dict)
        except Exception as e:
            logger.error(f"Error loading config from {yaml_path}: {e}")
            raise

    @classmethod
    def from_env(cls) -> 'CapibaraConfig':
        """Create config from environment variables."""
        try:
            return cls(
                training=TrainingConfig(
                    train_data_path=os.getenv('TRAIN_DATA_PATH', 'data/train'),
                    val_data_path=os.getenv('VAL_DATA_PATH', 'data/val')
                ),
                model=ModelConfig(),
                pruning=PruningConfig(),
                wandb=WandbConfig()
            )
        except Exception as e:
            logger.error(f"Error loading config from environment: {e}")
            raise
