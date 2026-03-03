"""
Autonomous Self-Improvement Mechanism (ASIM)
Core package for autonomous AI improvement system
"""
__version__ = "1.0.0"
__author__ = "Evolution Ecosystem ASIM Team"

from .config import ASIMConfig
from .performance_monitor import PerformanceMonitor
from .anomaly_detector import AnomalyDetector
from .optimization_strategist import OptimizationStrategist
from .implementer import Implementer
from .firebase_manager import FirebaseManager
from .logger import ASIMLogger

__all__ = [
    'ASIMConfig',
    'PerformanceMonitor',
    'AnomalyDetector',
    'OptimizationStrategist',
    'Implementer',
    'FirebaseManager',
    'ASIMLogger'
]