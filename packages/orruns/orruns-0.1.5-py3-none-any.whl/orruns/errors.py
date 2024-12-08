from typing import Optional, Dict, Any
from enum import Enum

class ORRunsError(Exception):
    """Base exception class for ORRuns"""
    pass

class ParameterError(ORRunsError):
    """参数错误"""
    def __init__(self, message: str, param_name: Optional[str] = None):
        self.param_name = param_name
        super().__init__(f"Parameter error: {message}" + 
                        (f" (parameter: {param_name})" if param_name else ""))

class MetricError(ORRunsError):
    """指标错误"""
    def __init__(self, message: str, metric_name: Optional[str] = None):
        self.metric_name = metric_name
        super().__init__(f"Metric error: {message}" +
                        (f" (metric: {metric_name})" if metric_name else ""))

class ArtifactError(ORRunsError):
    """工件错误"""
    def __init__(self, message: str, artifact_path: Optional[str] = None):
        self.artifact_path = artifact_path
        super().__init__(f"Artifact error: {message}" +
                        (f" (path: {artifact_path})" if artifact_path else ""))