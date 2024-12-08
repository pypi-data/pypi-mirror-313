from ..errors import *
import traceback
from typing import Optional, Dict, Any
import functools

def handle_parameter_error(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except (TypeError, ValueError) as e:
            raise ParameterError(str(e))
        except Exception as e:
            raise ParameterError(f"Unexpected error while handling parameters: {str(e)}")
    return wrapper

def handle_metric_error(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except (TypeError, ValueError) as e:
            raise MetricError(str(e))
        except Exception as e:
            raise MetricError(f"Unexpected error while handling metrics: {str(e)}")
    return wrapper

def handle_artifact_error(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except (IOError, FileNotFoundError) as e:
            raise ArtifactError(str(e))
        except Exception as e:
            raise ArtifactError(f"Unexpected error while handling artifacts: {str(e)}")
    return wrapper