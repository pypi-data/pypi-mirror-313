"""Setup configuration for CapibaraModel."""

from setuptools import setup, find_packages #type: ignore
from pathlib import Path

# Leer README
readme = Path("README.md").read_text(encoding="utf-8")

setup(
    name="capibara_model",
    version="1.1.6",
    description="Language model with contextual processing",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Marco Durán",
    author_email="marco@anachroni.co",
    url="https://github.com/anachroni-io/capibara-model",
    packages=find_packages(),
    package_data={
        "capibara_model": [
            "config/*.yaml",
            "py.typed",
        ],
    },
    install_requires=[
        "jax>=0.4.1",
        "flax>=0.6.0",
        "optax>=0.1.3",
        "numpy>=1.21.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=22.0.0",
            "mypy>=0.950",
        ],
        "tpu": [
            "jax[tpu]>=0.4.1",
        ]
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.8",
    keywords="machine-learning nlp language-model tpu jax",
    project_urls={
        "Documentation": "https://capibara-model.readthedocs.io",
        "Source": "https://github.com/anachroni-io/capibara-model",
        "Issues": "https://github.com/anachroni-io/capibara-model/issues",
    },
)
