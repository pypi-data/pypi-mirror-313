from typing import Dict, List, Optional, Any, Union
from pathlib import Path
from datetime import datetime, timedelta
import fnmatch
import json
import pandas as pd
from matplotlib.figure import Figure
import shutil
import os

from ..core.config import Config
from ..tracker import ExperimentTracker
from typing import Dict, List, Optional, Any, Union
from pathlib import Path
from datetime import datetime, timedelta
import fnmatch
import json
import pandas as pd
from matplotlib.figure import Figure



class ExperimentAPI:
    """
    API for managing experiments and their artifacts.
    
    This API provides methods in the following categories:
    1. Basic Operations - Core experiment management (init, list, get, query, delete)
    2. Artifact Management - Handle experiment artifacts (list, get, export)
    3. Analysis - Compare and analyze experiments
    4. Export - Export experiments to different formats
    5. Maintenance - Clean up and maintain experiments
    """
    
    #######################
    # 1. Basic Operations #
    #######################
    
    def __init__(self):
        """Initialize the API with optional data directory"""
        self.config = Config.get_instance()
    
    def list_experiments(self, last: int = 10, pattern: Optional[str] = None) -> List[Dict]:
        """List experiments with optional name pattern filter"""
        experiments = ExperimentTracker.query_experiments(
            base_dir=self.config.get_data_dir(),
            limit=last
        )
        if pattern:
            experiments = [exp for exp in experiments if fnmatch.fnmatch(exp['name'], pattern)]
        return experiments
    
    def get_experiment(self, experiment_name: str, run_id: Optional[str] = None) -> Dict:
        """Get experiment or specific run details"""
        filters = {"name__eq": experiment_name}
        if run_id:
            filters["run_id__eq"] = run_id
        
        results = ExperimentTracker.query_experiments(
            base_dir=self.config.get_data_dir(),
            filters=filters,
            limit=1
        )
        
        if not results:
            raise FileNotFoundError(f"Experiment {experiment_name} not found")
        return results[0]
    
    def query_experiments(self, **filters) -> List[Dict]:
        """Query experiments with filters"""
        parameter_filters = filters.get('parameter_filters', {})
        self._validate_filters(parameter_filters)
        return ExperimentTracker.query_experiments(
            base_dir=self.config.get_data_dir(),
            **filters
        )

    def delete_experiment(self, experiment_name: str, run_id: Optional[str] = None) -> None:
        """Delete experiment or specific run"""
        ExperimentTracker.delete_experiment(
            experiment_name=experiment_name,
            run_id=run_id,
            base_dir=self.config.get_data_dir()
        )

    ###########################
    # 2. Artifact Management  #
    ###########################

    def list_artifacts(self, experiment_name: str, run_id: str) -> Dict[str, List[str]]:
        """List all artifacts of an experiment run"""
        return ExperimentTracker.list_artifacts(
            experiment_name=experiment_name,
            run_id=run_id,
            base_dir=self.config.get_data_dir()
        )
    
    def get_artifact(self, experiment_name: str, run_id: str,
                    artifact_path: str, artifact_type: Optional[str] = None,
                    load_content: bool = False) -> Union[Path, Any]:
        """Get artifact path or content"""
        return ExperimentTracker.get_artifact(
            experiment_name=experiment_name,
            run_id=run_id,
            artifact_path=artifact_path,
            artifact_type=artifact_type,
            base_dir=self.config.get_data_dir(),
            load_content=load_content
        )

    ##################
    # 3. Analysis    #
    ##################

    def compare_experiments(self, experiment_names: List[str], 
                          metrics: Optional[List[str]] = None) -> Dict[str, Dict]:
        """Compare metrics across multiple experiments"""
        results = {}
        for name in experiment_names:
            exps = ExperimentTracker.query_experiments(
                base_dir=self.config.get_data_dir(),
                filters={"name__eq": name},
                sort_by="timestamp",
                sort_ascending=False,
                limit=1
            )
            if exps:
                exp_data = exps[0]
                if metrics:
                    results[name] = {k: exp_data['metrics'][k] 
                                   for k in metrics if k in exp_data['metrics']}
                else:
                    results[name] = exp_data['metrics']
        return results

    def get_experiment_history(self, experiment_name: str) -> List[Dict]:
        """Get complete run history of an experiment"""
        return ExperimentTracker.query_experiments(
            base_dir=self.config.get_data_dir(),
            filters={"name__eq": experiment_name},
            sort_by="timestamp",
            sort_ascending=True
        )

    ##################
    # 4. Export      #
    ##################

    def export_to_dataframe(self, experiment_name: str, 
                           metrics: Optional[List[str]] = None) -> pd.DataFrame:
        """Export experiment runs to DataFrame"""
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

    def export_artifacts(self, experiment_name: str, run_id: str, 
                        output_dir: str, artifact_types: Optional[List[str]] = None) -> Dict[str, List[str]]:
        """Export artifacts to specified directory"""
        artifacts = self.list_artifacts(experiment_name, run_id)
        exported = {}
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        for type_name, files in artifacts.items():
            if artifact_types and type_name not in artifact_types:
                continue
            exported[type_name] = []
            for file in files:
                content = self.get_artifact(experiment_name, run_id, file, 
                                         artifact_type=type_name, load_content=True)
                target_path = output_path / type_name / file
                target_path.parent.mkdir(parents=True, exist_ok=True)
                self._save_content(content, target_path)
                exported[type_name].append(str(target_path))
        return exported

    ##################
    # 5. Maintenance #
    ##################

    def clean_old_experiments(self, days: int = 30) -> List[str]:
        """Clean experiments older than specified days"""
        cutoff = datetime.now() - timedelta(days=days)
        experiments = self.list_experiments(last=None)
        deleted = []
        for exp in experiments:
            if datetime.fromisoformat(exp['timestamp']) < cutoff:
                self.delete_experiment(exp['name'])
                deleted.append(exp['name'])
        return deleted

    def compress_data_dir(self) -> str:
        """压缩整个数据目录并返回zip文件路径"""
        # 获取 orruns_experiments 目录
        base_path = Path(self.config.get_data_dir())
        if not base_path.exists():
            raise FileNotFoundError(f"数据目录 {base_path} 不存在")

        # 检查目录是否为空
        if not any(base_path.iterdir()):
            raise ValueError("数据目录为空，无法压缩")

        # 创建zip文件路径 (在父目录创建zip文件)
        zip_path = base_path.parent/ "orruns_experiments.zip"
        
        try:
            # 使用shutil创建zip文件，压缩整个orruns_experiments目录
            archive_path = shutil.make_archive(
                str(zip_path.with_suffix('')),  # 不包含.zip后缀的路径
                'zip',
                base_path.parent,  # 从父目录开始压缩
                base_path.name     # 只压缩orruns_experiments目录
            )
            
            # 压缩完成后删除原数据目录
            shutil.rmtree(base_path)
            
            return archive_path
        except Exception as e:
            raise RuntimeError(f"压缩过程出错: {str(e)}")

    def decompress_data_dir(self) -> str:
        """解压数据目录"""
        # 获取数据目录路径
        data_dir = Path(self.config.get_data_dir())
        zip_path = data_dir.parent / "orruns_experiments.zip"
        
        if not zip_path.exists():
            raise FileNotFoundError(f"Zip文件 {zip_path} 不存在")

        try:
            # 设置解压目标目录为zip文件所在目录
            output_dir = zip_path.parent
            
            # 确保目标目录存在
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # 解压文件
            shutil.unpack_archive(str(zip_path), str(output_dir))
            
            # 删除zip文件
            zip_path.unlink()
            
            # 创建数据目录
            data_dir.mkdir(parents=True, exist_ok=True)
            
            # 返回解压后的数据目录路径
            return str(data_dir)
        except Exception as e:
            raise RuntimeError(f"解压过程出错: {str(e)}")

    #########################
    # Internal Helpers      #
    #########################

    def _validate_filters(self, filters: Dict[str, Any]) -> None:
        """Validate filter format and operators"""
        for key in filters:
            if '__' not in key:
                raise ValueError(f"Invalid filter format: {key}")
            field, op = key.split('__')
            if op not in ['gt', 'lt', 'eq', 'gte', 'lte']:
                raise ValueError(f"Invalid operator: {op}")
    
    def _save_content(self, content: Any, path: Path) -> None:
        """Save content based on its type"""
        if isinstance(content, (pd.DataFrame, pd.Series)):
            content.to_csv(path)
        elif isinstance(content, Figure):
            content.savefig(path)
        elif isinstance(content, bytes):
            path.write_bytes(content)
        else:
            path.write_text(str(content))