import json
import os
import shutil
from datetime import datetime
from matplotlib.figure import Figure
import numpy as np
import pandas as pd
import random
from pathlib import Path
import pathlib
import logging
from typing import Union, Dict, List, Any, Optional, Tuple

from .core.config import Config
from .errors import *
from .utils.error_handlers import handle_metric_error, handle_parameter_error

class ExperimentTracker:
    """
    ORruns's core tracking class, used to manage the parameters and metrics of operations research experiments.
    
    Args:
        experiment_name: Name of the experiment
        base_dir: Base directory for storing experiment data
    """
    def __init__(self, experiment_name: str):
        self.experiment_name = experiment_name
        self.config = Config.get_instance()

        # 如果没有提供 base_dir，则从全局配置中获取
        base_dir = self.config.get_data_dir()
        if base_dir is None:
            raise ValueError("Base directory must be specified or set in the global configuration.")
        
        self.base_dir = pathlib.Path(base_dir).resolve()
        logging.info(f" experiment directory: {self.base_dir}")
        # Generate a unique run ID
        # 生成唯一的运行ID
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        random_suffix = str(random.randint(1000, 9999))
        self.run_id = f"{timestamp}_{random_suffix}"
        
        # Create the main run directory
        # 创建主要的运行目录
        self.run_dir = self.base_dir / experiment_name / self.run_id
        
        # Create directories for parameters, metrics, and artifacts
        # 创建参数、指标和工件的目录
        self.params_dir = self.run_dir / "params"
        self.metrics_dir = self.run_dir / "metrics"
        self.artifacts_dir = self.run_dir / "artifacts"
        self.figures_dir = self.artifacts_dir / "figures"
        self.data_dir = self.artifacts_dir / "data"
        
        # Create all necessary directories
        # 创建所有必要的目录
        for directory in [self.params_dir, self.metrics_dir, 
                         self.figures_dir, self.data_dir]:
            directory.mkdir(parents=True, exist_ok=True)
            
        self._params = {}
        self._metrics = {}


    #####初始化和核心实例方法：
    #####Initialization and core instance methods:
    @handle_parameter_error
    def log_params(self, params: Dict[str, Any], prefix: Optional[str] = None) -> None:
        """Log parameters to the params directory
        将参数记录到params目录
        """
        if not isinstance(params, dict):
            raise ParameterError("Parameters must be a dictionary", "params")
        if prefix is not None and not isinstance(prefix, str):
            raise ParameterError("Prefix must be a string", "prefix")
        params = self._process_nested_input(params, prefix)
        self._params = self._deep_update(self._params, params)
        
        with open(self.params_dir / "params.json", "w", encoding='utf-8') as f:
            json.dump(self._params, f, indent=4, ensure_ascii=False)
        
        # Save experiment information
        # 保存实验信息
        self._save_experiment_info()
    
    @handle_metric_error
    def log_metrics(self, metrics: Dict[str, Union[float, int, dict]], 
                   prefix: Optional[str] = None, 
                   step: Optional[int] = None) -> None:
        """Log metrics to the metrics directory
        记录指标到metrics目录"""
        if not isinstance(metrics, dict):
            raise MetricError("Metrics must be a dictionary", "metrics")
        if step is not None and not isinstance(step, int):
            raise MetricError("Step must be an integer", "step")
        
        processed_metrics = {}
        for key, value in metrics.items():
            processed_metrics[key] = self._process_value(value)
        # Validate metric values
        # 验证指标值
        self._validate_metrics(processed_metrics)
        
        # Process prefix
        # 处理前缀
        if prefix:
            parts = prefix.split('.')
            for part in reversed(parts):
                processed_metrics = {part: processed_metrics}
            
        self._validate_metrics(processed_metrics)
        metrics = self._process_nested_metrics(processed_metrics, step=step)
        self._metrics = self._deep_update(self._metrics, metrics)
        
        with open(self.metrics_dir / "metrics.json", "w", encoding='utf-8') as f:
            json.dump(self._metrics, f, indent=4)
            
        # Save experiment information
        # 保存实验信息
        self._save_experiment_info()

    def log_artifact(self, filename: str, content: Union[str, bytes, Figure, pd.DataFrame, np.ndarray, List, Dict], 
                    artifact_type: Optional[str] = None) -> None:
        """Log file artifact with enhanced type support
        
        Args:
            filename: Name of the file
            content: Content of the file (supports more types now)
            artifact_type: Type of the file
        """
        if not isinstance(filename, str):
            raise ArtifactError("Filename must be a string", filename)
        if not filename:
            raise ArtifactError("Filename cannot be empty")

        # Determine target directory
        file_ext = Path(filename).suffix.lower()
        
        if artifact_type in ["csv", "data"] or file_ext in [".csv", ".json", ".txt"]:
            target_dir = self.data_dir
        elif artifact_type in ["figure", "png", "jpg"] or file_ext in [".png", ".jpg", ".jpeg", ".svg"]:
            target_dir = self.figures_dir
        else:
            target_dir = self.artifacts_dir

        path = target_dir / filename
        
        try:
            # Enhanced content saving
            if isinstance(content, pd.DataFrame):
                content.to_csv(path, index=False)
            elif isinstance(content, Figure):
                content.savefig(path)
            elif isinstance(content, np.ndarray):
                # Convert numpy array to DataFrame
                pd.DataFrame(content).to_csv(path, index=False)
            elif isinstance(content, (list, dict)):
                # Convert list/dict to DataFrame
                pd.DataFrame(content).to_csv(path, index=False)
            elif isinstance(content, bytes):
                path.write_bytes(content)
            else:
                # Convert to string and save
                path.write_text(str(content))
        except Exception as e:
            raise ArtifactError(f"Failed to write artifact {filename}: {str(e)}")
  
    def get_params(self) -> Dict:
        """获取当前所有参数
        Get all current parameters"""
        return self._params.copy()
    
    def get_metrics(self) -> Dict:
        """获取当前所有指标
        Get all current metrics"""
        return self._metrics.copy()
    


    #####内部辅助方法：
    #####Internal helper methods:
    def _save_content(self, content: Any, path: Path) -> None:
        """Enhanced content saving with better type support
        增强的内容保存，支持更多类型"""
        try:
            if isinstance(content, (pd.DataFrame, pd.Series)):
                content.to_csv(path)
            elif isinstance(content, Figure):
                content.savefig(path)
            elif isinstance(content, np.ndarray):
                if path.suffix == '.csv':
                    pd.DataFrame(content).to_csv(path)
                else:
                    np.save(path, content)
            elif isinstance(content, (list, dict)):
                if path.suffix == '.json':
                    with open(path, 'w', encoding='utf-8') as f:
                        json.dump(content, f, indent=4)
                elif path.suffix == '.csv':
                    pd.DataFrame(content).to_csv(path)
                else:
                    with open(path, 'w', encoding='utf-8') as f:
                        json.dump(content, f)
            elif isinstance(content, bytes):
                path.write_bytes(content)
            else:
                path.write_text(str(content))
        except Exception as e:
            raise RuntimeError(f"Failed to save content to {path}: {str(e)}")

    def _process_value(self, value: Any) -> Any:
        """Convert values to serializable types
        将值转换为可序列化类型"""
        if isinstance(value, np.ndarray):
            return value.tolist()
        elif isinstance(value, (np.integer, np.floating)):
            return float(value)
        elif isinstance(value, pd.DataFrame):
            return value.to_dict()
        elif isinstance(value, pd.Series):
            return value.to_list()
        elif hasattr(value, 'to_dict'):
            return value.to_dict()
        elif hasattr(value, '__dict__'):
            return value.__dict__
        return value

    def _deep_update(self, source: Dict, updates: Dict) -> Dict:
        """Deeply update nested dictionaries
        深度更新嵌套字典
        """
        for key, value in updates.items():
            if key in source and isinstance(source[key], dict) and isinstance(value, dict):
                self._deep_update(source[key], value)
            else:
                source[key] = value
        return source
        
    def _process_nested_input(self, data: Dict, prefix: Optional[str] = None) -> Dict:
        """Process nested input data with an optional prefix
        处理带有可选前缀的嵌套输入数据
        """
        if prefix:
            nested_data = {}
            current = nested_data
            parts = prefix.split('.')
            for part in parts[:-1]:
                current[part] = {}
                current = current[part]
            current[parts[-1]] = data
            return nested_data
        return data

    def _save_experiment_info(self):
        """Save experiment information to summary.json
        将实验信息保存到summary.json
        """
        summary = {
            "name": self.experiment_name,
            "run_id": self.run_id,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "parameters": self._params,
            "metrics": self._metrics,
            "status": "completed"  # Add status field
            # 添加状态字段
        }
        
        # Ensure the directory exists
        # 确保目录存在
        self.run_dir.mkdir(parents=True, exist_ok=True)
        
        # Save as dictionary format
        # 以字典格式保存
        summary_path = self.run_dir / "summary.json"
        with open(summary_path, "w", encoding='utf-8') as f:
            json.dump(summary, f, indent=4, ensure_ascii=False)

    def _validate_metrics(self, metrics: Dict[str, Any], path: str = "") -> None:
        """Recursively validate metric values
        递归验证指标值"""
        for key, value in metrics.items():
            current_path = f"{path}.{key}" if path else key
            if isinstance(value, dict):
                self._validate_metrics(value, current_path)
            elif not isinstance(value, (float, int)):
                raise ValueError(
                    f"Invalid metric value for {current_path}: must be float or int"
                )

    def _get_current_metric(self, path: List[str]) -> Any:
        """Get the metric value for the current path
        获取当前路径的指标值"""
        current = self._metrics
        for p in path:
            if p not in current:
                return None
            current = current[p]
        return current

    def _process_metric_value(self, path: List[str], value: Union[float, int], step: Optional[int] = None) -> Dict:
        """Process a single metric value
        处理单个指标值"""
        if step is not None:
            current_metric = self._get_current_metric(path)
            if current_metric is None:
                return {"steps": [step], "values": [value]}
            elif isinstance(current_metric, dict) and "steps" in current_metric:
                return {
                    "steps": current_metric["steps"] + [step],
                    "values": current_metric["values"] + [value]
                }
            else:
                return {"steps": [step], "values": [value]}
        return value

    def _process_nested_metrics(self, metrics: Dict, current_path: List[str] = None, step: Optional[int] = None) -> Dict:
        """Recursively process nested metrics
        递归处理嵌套指标"""
        if current_path is None:
            current_path = []
            
        result = {}
        for key, value in metrics.items():
            path = current_path + [key]
            if isinstance(value, dict):
                result[key] = self._process_nested_metrics(value, path, step)
            else:
                result[key] = self._process_metric_value(path, value, step)
        return result

    def _get_storage_dir(self) -> str:
        """Get the storage directory
        获取存储目录
        """
        data_dir = self.config.get_data_dir()
        if not data_dir:
            raise ValueError("Data directory not set. Please run 'orruns config --data-dir PATH' first")
        return os.path.join(data_dir, 'experiments')
    
    


    @classmethod 
    def query_experiments(cls, 
                        base_dir: str = "./orruns_experiments",
                        filters: Optional[Dict[str, Any]] = None,
                        parameter_filters: Optional[Dict[str, Any]] = None,
                        metric_filters: Optional[Dict[str, Any]] = None,
                        sort_by: Optional[str] = None,
                        sort_ascending: bool = True,
                        limit: Optional[int] = None) -> List[Dict]:
        """查询实验
        Query experiments

        Args:
            base_dir: Base directory for experiments
            filters: Filters for top-level fields (name, run_id, timestamp)
            parameter_filters: Filters for parameters
            metric_filters: Filters for metrics
            sort_by: Field to sort by (format: "field" or "parameters.field" or "metrics.field")
            sort_ascending: Sort direction
            limit: Maximum results to return

        Returns:
            List[Dict]: List of matching experiment information

        Examples:
            >>> # Filter by experiment name
            >>> query_experiments(filters={"name__eq": "tsp_study"})
            >>> # Filter by parameters
            >>> query_experiments(parameter_filters={"batch_size__gt": 32})
            >>> # Filter by metrics with sorting
            >>> query_experiments(
            ...     metric_filters={"accuracy__gte": 0.9},
            ...     sort_by="metrics.accuracy",
            ...     sort_ascending=False
            ... )
        """
        def parse_filter_key(key: str) -> Tuple[str, str]:
            """解析过滤器键
            Parse filter key"""
            if "__" in key:
                field, op = key.split("__")
                return field, op
            return key, "eq"

        def match_value(value: Any, filter_value: Any, op: str) -> bool:
            """匹配值
            Match value"""
            try:
                if op == "eq":
                    return value == filter_value
                elif op == "gt":
                    return float(value) > float(filter_value)
                elif op == "lt":
                    return float(value) < float(filter_value)
                elif op == "gte":
                    return float(value) >= float(filter_value)
                elif op == "lte":
                    return float(value) <= float(filter_value)
                return False
            except (TypeError, ValueError):
                # 如果无法进行数值比较，回退到字符串比较
                # Fallback to string comparison if numeric comparison fails
                str_value = str(value)
                str_filter = str(filter_value)
                if op == "eq":
                    return str_value == str_filter
                elif op == "gt":
                    return str_value > str_filter
                elif op == "lt":
                    return str_value < str_filter
                elif op == "gte":
                    return str_value >= str_filter
                elif op == "lte":
                    return str_value <= str_filter
                return False

        def match_filters(exp: Dict, filters: Dict[str, Any], data_key: Optional[str] = None) -> bool:
            """匹配过滤器
            Match filters"""
            if not filters:
                return True
                
            for key, filter_value in filters.items():
                field, op = parse_filter_key(key)
                
                # 处理嵌套字段
                # Handle nested fields
                if data_key is None:
                    exp_data = exp
                else:
                    exp_data = exp.get(data_key, {})
                    
                # 支持点号分隔的嵌套字段
                # Support dot-separated nested fields
                if "." in field:
                    parts = field.split(".")
                    current_data = exp_data
                    for part in parts[:-1]:
                        current_data = current_data.get(part, {})
                    field = parts[-1]
                    exp_data = current_data

                if field not in exp_data:
                    return False
                if not match_value(exp_data[field], filter_value, op):
                    return False
            return True

        def get_sort_value(exp: Dict, sort_field: str) -> Any:
            """获取排序值
            Get value for sorting"""
            try:
                if sort_field.startswith('parameters.'):
                    field = sort_field.split('.', 1)[1]
                    current = exp.get('parameters', {})
                elif sort_field.startswith('metrics.'):
                    field = sort_field.split('.', 1)[1]
                    current = exp.get('metrics', {})
                else:
                    return exp.get(sort_field)

                # 处理嵌套字段
                # Handle nested fields
                if "." in field:
                    parts = field.split(".")
                    for part in parts[:-1]:
                        current = current.get(part, {})
                    return current.get(parts[-1])
                return current.get(field)
            except Exception:
                return None

        # 获取所有实验
        # Get all experiments
        experiments = []
        base_path = pathlib.Path(base_dir)
        if not base_path.exists():
            return []

        # 遍历所有实验目录
        # Traverse all experiment directories
        for exp_dir in base_path.iterdir():
            if not exp_dir.is_dir():
                continue
                
            # 遍历实验下的所有运行
            # Traverse all runs under the experiment
            for run_dir in exp_dir.iterdir():
                if not run_dir.is_dir():
                    continue
                    
                # 读取实验信息
                # Read experiment information
                summary_file = run_dir / "summary.json"
                if not summary_file.exists():
                    continue
                    
                try:
                    with open(summary_file, 'r', encoding='utf-8') as f:
                        exp_info = json.load(f)
                        
                    # 应用过滤器
                    # Apply filters
                    if not match_filters(exp_info, filters):  # 顶层字段过滤
                        continue
                    if not match_filters(exp_info, parameter_filters, "parameters"):
                        continue
                    if not match_filters(exp_info, metric_filters, "metrics"):
                        continue
                        
                    experiments.append(exp_info)
                except Exception as e:
                    logging.warning(f"Failed to load experiment file {summary_file}: {e}")

        # 排序
        # Sort
        if sort_by:
            experiments.sort(
                key=lambda x: get_sort_value(x, sort_by),
                reverse=not sort_ascending
            )

        # 限制结果数量
        # Limit the number of results
        if limit is not None:
            experiments = experiments[:limit]

        return experiments


    ###工件管理类方法：列出实验运行的所有文件工件
    @classmethod
    def list_artifacts(cls, experiment_name: str, run_id: str, base_dir: str = "./orruns_experiments") -> Dict[str, List[str]]:
        """获取指定实验运行的所有文件工件
        Get all file artifacts of the specified experiment run"""
        run_dir = pathlib.Path(base_dir) / experiment_name / run_id
        if not run_dir.exists():
            raise FileNotFoundError(f"Run directory not found: {run_dir}")

        def get_files(directory: pathlib.Path) -> List[str]:
            if not directory.exists():
                return []
            return [str(file_path.relative_to(directory)) 
                    for file_path in directory.rglob("*")
                    if file_path.is_file()]

        artifacts_dir = run_dir / "artifacts"
        return {
            "figures": get_files(artifacts_dir / "figures"),
            "data": get_files(artifacts_dir / "data"),
            "others": [str(p.relative_to(artifacts_dir)) 
                    for p in artifacts_dir.glob("*") 
                    if p.is_file() and p.parent == artifacts_dir]
        }

    @classmethod
    def get_artifact(cls, experiment_name: str, run_id: str, artifact_path: str,
                    artifact_type: str = None, base_dir: str = "./orruns_experiments",
                    load_content: bool = False) -> Union[pathlib.Path, Any]:
        """Get artifact path or content"""
        run_dir = pathlib.Path(base_dir) / experiment_name / run_id
        artifacts_dir = run_dir / "artifacts"

        # 修改这里的判断逻辑
        if artifact_type in ['figure', 'figures']:  # 支持两种写法
            full_path = artifacts_dir / "figures" / artifact_path
        elif artifact_type in ['data']:
            full_path = artifacts_dir / "data" / artifact_path
        else:
            full_path = artifacts_dir / artifact_path

        if not full_path.exists():
            raise FileNotFoundError(f"Artifact not found: {full_path}")
            
        if not load_content:
            return full_path
            
        # Load content based on file type
        suffix = full_path.suffix.lower()
        if suffix in ['.npy']:
            return np.load(full_path)
        elif suffix in ['.npz']:
            return np.load(full_path, allow_pickle=True)
        elif suffix in ['.csv']:
            return pd.read_csv(full_path)
        elif suffix in ['.json']:
            with open(full_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        elif suffix in ['.txt', '.log']:
            with open(full_path, 'r', encoding='utf-8') as f:
                return f.read()
        elif suffix in ['.png', '.jpg', '.jpeg', '.bmp']:  # 添加图片支持
            with open(full_path, 'rb') as f:
                return f.read()
        else:
            raise ValueError(f"Unsupported file type: {suffix}")



    ###实验清理类方法：删除实验或特定运行
    @classmethod
    def delete_experiment(cls, 
                         experiment_name: str, 
                         base_dir: str = "./orruns_experiments",
                         run_id: Optional[str] = None) -> None:
        """
        Delete the specified experiment or a specific run within the experiment

        Args:
            experiment_name: Name of the experiment to delete
            base_dir: Base directory where experiment data is stored 
            run_id: Optional run ID. If specified, only delete that run; if None, delete the entire experiment

        Raises:
            FileNotFoundError: When the specified experiment or run does not exist
        """
        base_path = pathlib.Path(base_dir)
        exp_path = base_path / experiment_name

        if not exp_path.exists():
            raise FileNotFoundError(f"Experiment '{experiment_name}' not found in {base_dir}")

        if run_id is not None:
            # 删除特定运行
            # Delete specific run
            run_path = exp_path / run_id
            if not run_path.exists():
                raise FileNotFoundError(f"Run '{run_id}' not found in experiment '{experiment_name}'")
            shutil.rmtree(run_path)
            # 如果实验目录为空，删除它
            # If the experiment directory is empty, delete it
            if not any(exp_path.iterdir()):
                exp_path.rmdir()
        else:
            # 删除整个实验
            # Delete the entire experiment
            shutil.rmtree(exp_path)

    @classmethod
    def delete_all_experiments(cls, base_dir: str = "./orruns_experiments") -> None:
        """
        Delete all experiment data

        Args:
            base_dir: Base directory where experiment data is stored
        """
        base_path = pathlib.Path(base_dir)
        if base_path.exists():
            shutil.rmtree(base_path)

