"""
Configuration management for ASIM with validation and defaults.
Architectural choice: Centralized config with validation to ensure
all components use consistent settings and avoid runtime errors.
"""
import os
import json
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from enum import Enum
import logging


class AnomalyAlgorithm(Enum):
    """Supported anomaly detection algorithms"""
    ISOLATION_FOREST = "isolation_forest"
    ONE_CLASS_SVM = "one_class_svm"
    LOCAL_OUTLIER_FACTOR = "local_outlier_factor"


@dataclass
class ASIMConfig:
    """Configuration container with validation"""
    
    # Firebase configuration
    firebase_project_id: str = field(default="")
    firestore_collection_prefix: str = field(default="asim_")
    
    # Performance monitoring
    monitoring_interval_seconds: int = field(default=60)
    metrics_to_track: List[str] = field(default_factory=lambda: [
        "response_time_ms",
        "memory_usage_mb",
        "cpu_utilization_percent",
        "request_throughput_per_second",
        "error_rate_percent"
    ])
    
    # Anomaly detection
    anomaly_detection_algorithm: AnomalyAlgorithm = field(default=AnomalyAlgorithm.ISOLATION_FOREST)
    anomaly_contamination: float = field(default=0.1)  # Expected proportion of anomalies
    training_window_days: int = field(default=7)
    
    # Optimization
    reinforcement_learning_epochs: int = field(default=100)
    exploration_rate: float = field(default=0.2)
    
    # Implementation
    deployment_staging_seconds: int = field(default=300)
    max_rollback_attempts: int = field(default=3)
    
    # Logging
    log_level: str = field(default="INFO")
    log_file_path: Optional[str] = field(default="logs/asim_system.log")
    
    def __post_init__(self):
        """Validate configuration after initialization"""
        self._validate_config()
        self._ensure_directories()
    
    def _validate_config(self) -> None:
        """Validate all configuration parameters"""
        validations = [
            (self.monitoring_interval_seconds > 0, "monitoring_interval_seconds must be positive"),
            (0 <= self.anomaly_contamination <= 0.5, "anomaly_contamination must be between 0 and 0.5"),
            (self.training_window_days > 0, "training_window_days must be positive"),
            (self.reinforcement_learning_epochs > 0, "reinforcement_learning_epochs must be positive"),
            (0 <= self.exploration_rate <= 1, "exploration_rate must be between 0 and 1"),
            (self.deployment_staging_seconds > 0, "deployment_staging_seconds must be positive"),
            (self.max_rollback_attempts >= 0, "max_rollback_attempts must be non-negative"),
            (self.log_level in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], 
             f"Invalid log_level: {self.log_level}")
        ]
        
        for condition, error_message in validations:
            if not condition:
                raise ValueError(f"Configuration validation failed: {error_message}")
    
    def _ensure_directories(self) -> None:
        """Create necessary directories if they don't exist"""
        if self.log_file_path:
            log_dir = os.path.dirname(self.log_file_path)
            if log_dir and not os.path.exists(log_dir):
                os.makedirs(log_dir, exist_ok=True)
    
    @classmethod
    def from_env_file(cls, env_file: str = ".env") -> "ASIMConfig":
        """
        Load configuration from environment file.
        Args:
            env_file: Path to environment file
        Returns:
            ASIMConfig instance
        """
        config = cls()
        
        if os.path.exists(env_file):
            with open(env_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        key = key.strip()
                        value = value.strip().