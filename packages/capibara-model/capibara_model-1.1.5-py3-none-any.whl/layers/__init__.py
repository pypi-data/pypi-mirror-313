"""Layers module for CapibaraModel."""

# Capas básicas
from capibara_model.layers.self_attention import SelfAttention
from capibara_model.layers.synthetic_embedding import SyntheticEmbedding

# Capas especializadas
from capibara_model.layers.bitnet import BitNet
from capibara_model.layers.bitnet_quantizer import BitNetQuantizer
from capibara_model.layers.game_theory import GameTheory
from capibara_model.layers.mixture_of_rookies import MixtureOfRookies
from capibara_model.layers.platonic import Platonic
from capibara_model.layers.quineana import Quineana
from capibara_model.layers.sparse_capibara import SparseCapibara

__all__ = [
    # Capas básicas
    "SelfAttention",
    "SyntheticEmbedding",
    
    # Capas especializadas
    "BitNet",
    "BitNetQuantizer",
    "GameTheory",
    "MixtureOfRookies",
    "Platonic",
    "Quineana",
    "SparseCapibara",
]
