from typing import Dict, List, Optional, Any, Union
from pathlib import Path
from datetime import datetime, timedelta
import fnmatch
import json
import pandas as pd
from matplotlib.figure import Figure

from ..core.config import Config
from ..tracker import ExperimentTracker
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
    
    def __init__(self, data_dir: Optional[str] = None):
        """Initialize the API with optional data directory"""
        self.config = Config.get_instance()
        if data_dir:
            self.config.set_data_dir(data_dir)
    
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