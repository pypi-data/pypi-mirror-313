import pytest
import tempfile
import shutil
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import json

from orruns.api.experiment import ExperimentAPI
from orruns.core.config import Config
from orruns.tracker import ExperimentTracker



class TestExperimentAPI:
    @pytest.fixture
    def api(self):
        # Create a temporary directory for tests
        with tempfile.TemporaryDirectory() as temp_dir:
            config = Config.get_instance()
            config.set_data_dir(temp_dir)
            api = ExperimentAPI()
            yield api
            
    def test_list_experiments(self, api):
        # Test empty list
        assert api.list_experiments() == []
        
        # Create some test experiments
        tracker1 = ExperimentTracker("test_exp1")
        tracker1.log_params({"param1": 1})
        tracker2 = ExperimentTracker("test_exp2")
        tracker2.log_params({"param2": 2})
        
        # Test listing all experiments
        exps = api.list_experiments()
        assert len(exps) == 2
        assert any(exp["name"] == "test_exp1" for exp in exps)
        assert any(exp["name"] == "test_exp2" for exp in exps)
        
        # Test pattern filtering
        filtered = api.list_experiments(pattern="*exp1")
        assert len(filtered) == 1
        assert filtered[0]["name"] == "test_exp1"

    def test_get_experiment(self, api):
        # Create test experiment
        tracker = ExperimentTracker("test_exp")
        tracker.log_params({"param": 1})
        tracker.log_metrics({"metric": 0.5})
        
        # Test getting experiment
        exp = api.get_experiment("test_exp")
        assert exp["name"] == "test_exp"
        assert exp["parameters"]["param"] == 1
        assert exp["metrics"]["metric"] == 0.5
        
        # Test getting non-existent experiment
        with pytest.raises(FileNotFoundError):
            api.get_experiment("non_existent")

    def test_query_experiments(self, api):
        # Create test experiments
        tracker1 = ExperimentTracker("test_exp1")
        tracker1.log_params({"value": 10})
        tracker1.log_metrics({"score": 0.8})
        
        tracker2 = ExperimentTracker("test_exp2")
        tracker2.log_params({"value": 20})
        tracker2.log_metrics({"score": 0.9})
        
        # Test parameter filters
        results = api.query_experiments(parameter_filters={"value__gt": 15})
        assert len(results) == 1
        assert results[0]["name"] == "test_exp2"
        
        # Test metric filters
        results = api.query_experiments(metric_filters={"score__lt": 0.85})
        assert len(results) == 1
        assert results[0]["name"] == "test_exp1"

    def test_delete_experiment(self, api):
        # Create test experiment
        tracker = ExperimentTracker("test_exp")
        tracker.log_params({"param": 1})
        
        # Verify experiment exists
        assert len(api.list_experiments()) == 1
        
        # Delete experiment
        api.delete_experiment("test_exp")
        
        # Verify experiment was deleted
        assert len(api.list_experiments()) == 0

    def test_artifact_management(self, api):
        # Create test experiment with artifacts
        tracker = ExperimentTracker("test_exp")
        
        # Create and log some test artifacts
        df = pd.DataFrame({"col1": [1, 2, 3]})
        tracker.log_artifact("data.csv", df)
        
        fig, ax = plt.subplots()
        ax.plot([1, 2, 3])
        tracker.log_artifact("plot.png", fig)
        plt.close()
        
        # Test listing artifacts
        artifacts = api.list_artifacts("test_exp", tracker.run_id)
        assert "data" in artifacts
        assert "figures" in artifacts
        assert "data.csv" in artifacts["data"]
        assert "plot.png" in artifacts["figures"]
        
        # Test getting artifact
        artifact_path = api.get_artifact("test_exp", tracker.run_id, "data.csv", "data")
        assert artifact_path.exists()

    def test_clean_old_experiments(self, api):
        # Create old and new experiments
        tracker1 = ExperimentTracker("old_exp")
        tracker1.log_params({"old": True})
        
        tracker2 = ExperimentTracker("new_exp")
        tracker2.log_params({"new": True})
        
        # Modify timestamp of old experiment by directly editing summary.json
        old_time = datetime.now() - timedelta(days=31)
        summary_path = Path(api.config.get_data_dir()) / "old_exp" / tracker1.run_id / "summary.json"
        
        with open(summary_path, 'r') as f:
            summary = json.load(f)
        summary['timestamp'] = old_time.strftime("%Y-%m-%d %H:%M:%S")
        with open(summary_path, 'w') as f:
            json.dump(summary, f)
        
        # Clean old experiments
        deleted = api.clean_old_experiments(days=30)
        
        # Verify only old experiment was deleted
        assert "old_exp" in deleted
        assert len(api.list_experiments()) == 1
        assert api.list_experiments()[0]["name"] == "new_exp"