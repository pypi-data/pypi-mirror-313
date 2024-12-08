from typing import Dict, List, Optional, Any, Union
from pathlib import Path
from datetime import datetime, timedelta
import fnmatch
import json
import pandas as pd
from matplotlib.figure import Figure

from ..core.config import Config
from ..tracker import ExperimentTracker

class ExperimentAPI:
    """API for managing experiments and their artifacts
    
    This class provides a high-level interface for:
    - Experiment management (list, get, query, delete)
    - Artifact management (list, get, export)
    - Experiment analysis (compare, history)
    - Data export (DataFrame, artifacts)
    - Maintenance (cleanup)
    """
    
    def __init__(self, data_dir: Optional[str] = None):
        """Initialize API with optional data directory
        
        Args:
            data_dir: Optional custom directory for experiment data
        """
        try:
            self.config = Config.get_instance()
            if data_dir:
                self.config.set_data_dir(data_dir)
        except Exception as e:
            raise RuntimeError(f"Failed to initialize API: {str(e)}")

    # 1. 实验管理类方法 (Experiment Management Methods)
    def list_experiments(self, last: int = 10, pattern: Optional[str] = None) -> List[Dict]:
        """List experiments with optional name pattern filter
        
        Args:
            last: Number of most recent experiments to return
            pattern: Optional glob pattern to filter experiment names
            
        Returns:
            List of experiment dictionaries
            
        Raises:
            RuntimeError: If listing experiments fails
        """
        try:
            # 使用 query_experiments 替代直接调用 list_experiments
            filters = {}
            if pattern:
                filters["name__eq"] = pattern
                
            experiments = ExperimentTracker.query_experiments(
                base_dir=self.config.get_data_dir(),
                filters=filters,
                sort_by="timestamp",
                sort_ascending=False,
                limit=last
            )
            return experiments
        except Exception as e:
            raise RuntimeError(f"Failed to list experiments: {str(e)}")
    

    def get_experiment(self, experiment_name: str, run_id: Optional[str] = None) -> Dict:
        """Get experiment or specific run details
        
        Args:
            experiment_name: Name of the experiment
            run_id: Optional run ID to get specific run details
            
        Returns:
            Dictionary containing experiment/run details
            
        Raises:
            FileNotFoundError: If experiment or run not found
            RuntimeError: If getting experiment details fails
        """
        try:
            # 使用 query_experiments 替代直接调用 get_experiment
            filters = {"name__eq": experiment_name}
            if run_id:
                filters["run_id__eq"] = run_id
            
            results = ExperimentTracker.query_experiments(
                base_dir=self.config.get_data_dir(),
                filters=filters,
                limit=1 if run_id else None
            )
            
            if not results:
                if run_id:
                    raise FileNotFoundError(
                        f"Run '{run_id}' not found in experiment '{experiment_name}'"
                    )
                raise FileNotFoundError(f"Experiment '{experiment_name}' not found")
                
            if run_id:
                return results[0]
            
            # 处理多个运行的情况
            runs = sorted(results, key=lambda x: x["timestamp"], reverse=True)
            latest_run = runs[0]
            first_run = runs[-1]
            
            return {
                "name": experiment_name,
                "runs": runs,
                "total_runs": len(runs),
                "latest_run": latest_run,
                "parameters": latest_run["parameters"],
                "metrics": latest_run["metrics"],
                "created_at": first_run["timestamp"],
                "last_updated": latest_run["timestamp"]
            }
        except FileNotFoundError:
            raise
        except Exception as e:
            raise RuntimeError(f"Failed to get experiment details: {str(e)}")
    
    def query_experiments(self, **filters) -> List[Dict]:
        """Query experiments with filters
        
        Args:
            **filters: Filter parameters
                - filters: Dict of top-level field filters (name, run_id, timestamp)
                - parameter_filters: Dict of parameter filters
                - metric_filters: Dict of metric filters
                - sort_by: Field to sort by ("field" or "parameters.field" or "metrics.field")
                - sort_ascending: Sort direction
                - limit: Maximum number of results
                
        Returns:
            List of matching experiment dictionaries
            
        Raises:
            ValueError: If filter format is invalid
            RuntimeError: If query fails
            
        Examples:
            >>> # Filter by experiment name
            >>> api.query_experiments(filters={"name__eq": "experiment1"})
            >>> # Filter by parameters
            >>> api.query_experiments(parameter_filters={"learning_rate__lt": 0.001})
            >>> # Filter by metrics with sorting
            >>> api.query_experiments(
            ...     metric_filters={"accuracy__gte": 0.9},
            ...     sort_by="metrics.accuracy",
            ...     sort_ascending=False
            ... )
        """
        try:
            # 验证所有过滤器
            # Validate all filters
            top_level_filters = filters.get('filters', {})
            parameter_filters = filters.get('parameter_filters', {})
            metric_filters = filters.get('metric_filters', {})
            
            self._validate_filters(top_level_filters)
            self._validate_filters(parameter_filters)
            self._validate_filters(metric_filters)
            
            # 验证排序字段格式
            # Validate sort field format
            sort_by = filters.get('sort_by')
            if sort_by and not any([
                sort_by.startswith(prefix) 
                for prefix in ['parameters.', 'metrics.', '']
            ]):
                raise ValueError(
                    f"Invalid sort_by format: {sort_by}. "
                    "Should be 'field' or 'parameters.field' or 'metrics.field'"
                )
            
            return ExperimentTracker.query_experiments(
                base_dir=self.config.get_data_dir(),
                filters=top_level_filters,
                parameter_filters=parameter_filters,
                metric_filters=metric_filters,
                sort_by=sort_by,
                sort_ascending=filters.get('sort_ascending', True),
                limit=filters.get('limit')
            )
        except ValueError as e:
            raise ValueError(f"Invalid filter format: {str(e)}")
        except Exception as e:
            raise RuntimeError(f"Failed to query experiments: {str(e)}")

    def delete_experiment(self, experiment_name: str, run_id: Optional[str] = None) -> None:
        """Delete experiment or specific run
        
        Args:
            experiment_name: Name of the experiment to delete
            run_id: Optional run ID to delete specific run
            
        Raises:
            FileNotFoundError: If experiment or run not found
            RuntimeError: If deletion fails
        """
        try:
            ExperimentTracker.delete_experiment(
                experiment_name=experiment_name,
                run_id=run_id,
                base_dir=self.config.get_data_dir()
            )
        except FileNotFoundError:
            if run_id:
                raise FileNotFoundError(
                    f"Run '{run_id}' not found in experiment '{experiment_name}'"
                )
            raise FileNotFoundError(f"Experiment '{experiment_name}' not found")
        except Exception as e:
            raise RuntimeError(f"Failed to delete experiment: {str(e)}")

    # 2. 工件管理类方法 (Artifact Management Methods)
    def list_artifacts(self, experiment_name: str, run_id: str) -> Dict[str, List[str]]:
        """List all artifacts of an experiment run
        
        Args:
            experiment_name: Name of the experiment
            run_id: Run ID
            
        Returns:
            Dictionary mapping artifact types to lists of artifact paths
            
        Raises:
            FileNotFoundError: If experiment or run not found
            RuntimeError: If listing artifacts fails
        """
        try:
            return ExperimentTracker.list_artifacts(
                experiment_name=experiment_name,
                run_id=run_id,
                base_dir=self.config.get_data_dir()
            )
        except FileNotFoundError:
            raise FileNotFoundError(
                f"No artifacts found for experiment '{experiment_name}' run '{run_id}'"
            )
        except Exception as e:
            raise RuntimeError(f"Failed to list artifacts: {str(e)}")
    
    def get_artifact(self, experiment_name: str, run_id: str,
                    artifact_path: str, artifact_type: Optional[str] = None,
                    load_content: bool = False) -> Union[Path, Any]:
        """Get artifact path or content
        
        Args:
            experiment_name: Name of the experiment
            run_id: Run ID
            artifact_path: Path to the artifact
            artifact_type: Optional artifact type ('figure' or 'data')
            load_content: Whether to load and return content
            
        Returns:
            Either Path object or artifact content
            
        Raises:
            FileNotFoundError: If artifact not found
            ValueError: If artifact type is invalid
            RuntimeError: If getting artifact fails
        """
        try:
            return ExperimentTracker.get_artifact(
                experiment_name=experiment_name,
                run_id=run_id,
                artifact_path=artifact_path,
                artifact_type=artifact_type,
                base_dir=self.config.get_data_dir(),
                load_content=load_content
            )
        except FileNotFoundError:
            raise FileNotFoundError(
                f"Artifact '{artifact_path}' not found in "
                f"experiment '{experiment_name}' run '{run_id}'"
            )
        except ValueError as e:
            raise ValueError(f"Invalid artifact type: {str(e)}")
        except Exception as e:
            raise RuntimeError(f"Failed to get artifact: {str(e)}")

    # 3. 实验分析类方法 (Analysis Methods)
    def compare_experiments(self, experiment_names: List[str], 
                          metrics: Optional[List[str]] = None) -> Dict[str, Dict]:
        """Compare metrics across multiple experiments
        
        Args:
            experiment_names: List of experiment names to compare
            metrics: Optional list of specific metrics to compare
            
        Returns:
            Dictionary mapping experiment names to their metrics
            
        Raises:
            FileNotFoundError: If any experiment not found
            RuntimeError: If comparison fails
        """
        try:
            results = {}
            for name in experiment_names:
                exp_data = self.get_experiment(name)
                if metrics:
                    results[name] = {
                        k: exp_data['metrics'][k] 
                        for k in metrics if k in exp_data['metrics']
                    }
                else:
                    results[name] = exp_data['metrics']
            return results
        except FileNotFoundError:
            raise  # Re-raise FileNotFoundError from get_experiment
        except Exception as e:
            raise RuntimeError(f"Failed to compare experiments: {str(e)}")

    def get_experiment_history(self, experiment_name: str) -> List[Dict]:
        """Get complete run history of an experiment
        
        Args:
            experiment_name: Name of the experiment
            
        Returns:
            List of run dictionaries sorted by timestamp
            
        Raises:
            FileNotFoundError: If experiment not found
            RuntimeError: If getting history fails
        """
        try:
            exp_data = self.get_experiment(experiment_name)
            return sorted(exp_data['runs'], key=lambda x: x['timestamp'])
        except FileNotFoundError:
            raise  # Re-raise FileNotFoundError from get_experiment
        except Exception as e:
            raise RuntimeError(f"Failed to get experiment history: {str(e)}")

    # 4. 数据导出类方法 (Export Methods)
    def export_to_dataframe(self, experiment_name: str, 
                           metrics: Optional[List[str]] = None) -> pd.DataFrame:
        """Export experiment runs to DataFrame
        
        Args:
            experiment_name: Name of the experiment
            metrics: Optional list of specific metrics to include
            
        Returns:
            DataFrame containing run data
            
        Raises:
            FileNotFoundError: If experiment not found
            RuntimeError: If export fails
        """
        try:
            exp_data = self.get_experiment_history(experiment_name)
            if metrics:
                return pd.DataFrame([
                    {**{'run_id': run['run_id'], 'timestamp': run['timestamp']},
                     **{k: run['metrics'][k] for k in metrics if k in run['metrics']}}
                    for run in exp_data
                ])
            return pd.DataFrame([
                {**{'run_id': run['run_id'], 'timestamp': run['timestamp']},
                 **run['metrics']}
                for run in exp_data
            ])
        except FileNotFoundError:
            raise  # Re-raise FileNotFoundError from get_experiment_history
        except Exception as e:
            raise RuntimeError(f"Failed to export to DataFrame: {str(e)}")

    def export_artifacts(self, experiment_name: str, run_id: str, 
                        output_dir: str, 
                        artifact_types: Optional[List[str]] = None) -> Dict[str, List[str]]:
        """Export artifacts to specified directory
        
        Args:
            experiment_name: Name of the experiment
            run_id: Run ID
            output_dir: Directory to export artifacts to
            artifact_types: Optional list of artifact types to export
            
        Returns:
            Dictionary mapping artifact types to exported file paths
            
        Raises:
            FileNotFoundError: If artifacts not found
            RuntimeError: If export fails
        """
        try:
            artifacts = self.list_artifacts(experiment_name, run_id)
            exported = {}
            output_path = Path(output_dir)
            output_path.mkdir(parents=True, exist_ok=True)
            
            for type_name, files in artifacts.items():
                if artifact_types and type_name not in artifact_types:
                    continue
                exported[type_name] = []
                for file in files:
                    content = self.get_artifact(
                        experiment_name, run_id, file,
                        artifact_type=type_name, load_content=True
                    )
                    target_path = output_path / type_name / file
                    target_path.parent.mkdir(parents=True, exist_ok=True)
                    self._save_content(content, target_path)
                    exported[type_name].append(str(target_path))
            return exported
        except (FileNotFoundError, ValueError):
            raise  # Re-raise exceptions from list_artifacts and get_artifact
        except Exception as e:
            raise RuntimeError(f"Failed to export artifacts: {str(e)}")

    # 5. 维护类方法 (Maintenance Methods)
    def clean_old_experiments(self, days: int = 30) -> List[str]:
        """Clean experiments older than specified days
        
        Args:
            days: Number of days to keep experiments for
            
        Returns:
            List of deleted experiment names
            
        Raises:
            RuntimeError: If cleanup fails
        """
        try:
            cutoff = datetime.now() - timedelta(days=days)
            experiments = self.list_experiments(last=None)
            deleted = []
            for exp in experiments:
                # 修改：使用 runs[0] 中的时间戳
                if exp['runs'] and datetime.strptime(exp['runs'][0]['timestamp'], '%Y%m%d') < cutoff:
                    self.delete_experiment(exp['name'])
                    deleted.append(exp['name'])
            return deleted
        except Exception as e:
            raise RuntimeError(f"Failed to clean old experiments: {str(e)}")

    # 内部辅助方法 (Internal Helper Methods)
    def _validate_filters(self, filters: Dict[str, Any]) -> None:
        """Validate filter format and operators
        
        Args:
            filters: Dictionary of filters to validate
            
        Raises:
            ValueError: If filter format is invalid
        """
        for key in filters:
            if '__' not in key:
                raise ValueError(
                    f"Invalid filter format: {key}. "
                    "Format should be 'field__operator'"
                )
            field, op = key.split('__')
            if op not in ['gt', 'lt', 'eq', 'gte', 'lte']:
                raise ValueError(
                    f"Invalid operator: {op}. "
                    "Valid operators are: gt, lt, eq, gte, lte"
                )
    
    def _save_content(self, content: Any, path: Path) -> None:
        """Save content based on its type
        
        Args:
            content: Content to save
            path: Path to save to
            
        Raises:
            RuntimeError: If saving content fails
        """
        try:
            if isinstance(content, (pd.DataFrame, pd.Series)):
                content.to_csv(path)
            elif isinstance(content, Figure):
                content.savefig(path)
            elif isinstance(content, bytes):
                path.write_bytes(content)
            else:
                path.write_text(str(content))
        except Exception as e:
            raise RuntimeError(f"Failed to save content: {str(e)}")