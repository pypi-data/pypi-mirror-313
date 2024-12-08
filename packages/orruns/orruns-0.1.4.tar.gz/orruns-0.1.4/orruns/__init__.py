
"""
ORruns Utilities Module

This module provides utility functions for system information collection and display,
designed specifically for Operations Research experiments.

Author: Feng Feng (冯峰)
Email: ffxdd@163.com
License: GPL-3.0
"""

from .tracker import ExperimentTracker
from .decorators import experiment_manager
from .visualization import ExperimentDashboard
from .config import ExperimentConfig
from .api.experiment import ExperimentAPI
from .core.config import Config
from .utils.utils import *  # 如果 utils.py 中有需要导出的工具函数


__version__ = "0.1.2"
__all__ = [
    'ExperimentAPI',
    'Config',
    'ExperimentTracker',
    'ExperimentDashboard',
    'ExperimentConfig',
    'experiment_manager'
]