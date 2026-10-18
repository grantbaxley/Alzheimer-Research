"""Connectome-based spreading models (network diffusion, FKPP) with mandatory null tests."""

from .graph import graph_laplacian, synthetic_connectome
from .models import fit_diffusion_time, fkpp, network_diffusion
from .nulls import NullTestResult, distance_null, null_test, rewire_preserving_degree

__all__ = [
    "NullTestResult",
    "distance_null",
    "fit_diffusion_time",
    "fkpp",
    "graph_laplacian",
    "network_diffusion",
    "null_test",
    "rewire_preserving_degree",
    "synthetic_connectome",
]
