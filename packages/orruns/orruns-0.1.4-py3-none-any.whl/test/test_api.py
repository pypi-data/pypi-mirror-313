import pytest
import tempfile
import shutil
from pathlib import Path
import time
import json
from datetime import datetime
import pandas as pd

from orruns.api.experiment import ExperimentAPI
from orruns.tracker import ExperimentTracker
from orruns.core.config import Config

@pytest.fixture
def temp_dir():
    """Create temporary directory"""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)

@pytest.fixture
def api(temp_dir):
    """Create API instance"""
    config = Config.get_instance()
    config.set_data_dir(temp_dir)
    return ExperimentAPI()

@pytest.fixture
def sample_experiment(api):
    """Create sample experiment"""
    tracker = ExperimentTracker("test_exp", base_dir=api.config.get_data_dir())
    
    # Record parameters
    tracker.log_params({
        "learning_rate": 0.01,
        "batch_size": 32,
        "model": {
            "type": "cnn",
            "layers": [64, 32]
        }
    })
    
    # Record metrics
    tracker.log_metrics({
        "accuracy": 0.85,
        "loss": 0.15,
        "validation": {
            "accuracy": 0.83,
            "loss": 0.17
        }
    })
    
    # Record CSV file
    csv_content = "col1,col2\n1,2\n3,4"
    tracker.log_artifact("data.csv", csv_content, artifact_type="data")
    
    # Record image file
    tracker.log_artifact("plot.png", b"fake_image_data", artifact_type="figure")
    
    time.sleep(0.1)
    return tracker

# 1. 实验管理类方法测试
def test_list_experiments(api, sample_experiment):
    """Test listing experiments"""
    time.sleep(0.1)
    
    experiments = api.list_experiments()
    assert len(experiments) > 0
    
    exp = next(e for e in experiments if e["name"] == "test_exp")
    assert len(exp["runs"]) == 1
    # 移除这两行不合理的断言
    # assert "parameters" in exp
    # assert "metrics" in exp
    
    # 改为检查runs中的数据
    run = exp["runs"][0]
    assert "parameters" in run
    assert "metrics" in run
    assert run["parameters"]["learning_rate"] == 0.01
    assert run["metrics"]["accuracy"] == 0.85

def test_get_experiment(api, sample_experiment):
    """Test getting experiment details"""
    time.sleep(0.1)
    
    # Test getting experiment overview
    exp_info = api.get_experiment("test_exp")
    assert exp_info["name"] == "test_exp"
    assert exp_info["total_runs"] == 1
    assert "last_updated" in exp_info
    
    # Test getting specific run
    run_info = api.get_experiment("test_exp", sample_experiment.run_id)
    assert run_info["run"]["run_id"] == sample_experiment.run_id
    assert run_info["parameters"]["learning_rate"] == 0.01

def test_query_experiments(api, sample_experiment):
    """Test querying experiments"""
    time.sleep(0.1)
    
    # Test parameter filters
    results = api.query_experiments(
        parameter_filters={"learning_rate__eq": 0.01}
    )
    assert len(results) > 0
    assert results[0]["parameters"]["learning_rate"] == 0.01
    
    # Test metric filters
    results = api.query_experiments(
        metric_filters={"accuracy__gte": 0.8}
    )
    assert len(results) > 0
    assert results[0]["metrics"]["accuracy"] >= 0.8

def test_delete_experiment(api, sample_experiment):
    """Test deleting experiment"""
    time.sleep(0.1)
    
    # Test deleting specific run
    api.delete_experiment("test_exp", sample_experiment.run_id)
    with pytest.raises(FileNotFoundError):
        api.get_experiment("test_exp", sample_experiment.run_id)
    
    # Create new experiment for testing full deletion
    new_tracker = ExperimentTracker("test_exp_2", base_dir=api.config.get_data_dir())
    new_tracker.log_params({"test": True})
    time.sleep(0.1)
    
    api.delete_experiment("test_exp_2")
    with pytest.raises(FileNotFoundError):
        api.get_experiment("test_exp_2")

# 2. 工件管理类方法测试
def test_artifact_management(api, sample_experiment):
    """Test artifact management"""
    time.sleep(0.1)
    
    # Test getting artifact without loading
    artifact = api.get_artifact(
        "test_exp",
        sample_experiment.run_id,
        "data.csv",
        artifact_type="data",
        load_content=False
    )
    assert isinstance(artifact, Path)
    assert artifact.exists()
    
    # Test loading artifact content
    content = api.get_artifact(
        "test_exp",
        sample_experiment.run_id,
        "data.csv",
        artifact_type="data",
        load_content=True
    )
    assert isinstance(content, pd.DataFrame)
    assert list(content.columns) == ["col1", "col2"]

# 3. 实验分析类方法测试
def test_compare_experiments(api, sample_experiment):
    """Test comparing experiments"""
    # Create another experiment for comparison
    tracker2 = ExperimentTracker("test_exp_2", base_dir=api.config.get_data_dir())
    tracker2.log_metrics({"accuracy": 0.90, "loss": 0.10})
    time.sleep(0.1)
    
    comparison = api.compare_experiments(
        ["test_exp", "test_exp_2"],
        metrics=["accuracy", "loss"]
    )
    assert len(comparison) == 2
    assert comparison["test_exp"]["accuracy"] == 0.85
    assert comparison["test_exp_2"]["accuracy"] == 0.90

def test_get_experiment_history(api, sample_experiment):
    """Test getting experiment history"""
    time.sleep(0.1)
    
    history = api.get_experiment_history("test_exp")
    assert len(history) == 1
    assert history[0]["run_id"] == sample_experiment.run_id
    assert history[0]["metrics"]["accuracy"] == 0.85

# 4. 数据导出类方法测试
def test_export_to_dataframe(api, sample_experiment):
    """Test exporting to DataFrame"""
    time.sleep(0.1)
    
    df = api.export_to_dataframe("test_exp", metrics=["accuracy", "loss"])
    assert isinstance(df, pd.DataFrame)
    assert "accuracy" in df.columns
    assert "loss" in df.columns
    assert len(df) == 1

def test_export_artifacts(api, sample_experiment, temp_dir):
    """Test exporting artifacts"""
    time.sleep(0.1)
    
    output_dir = Path(temp_dir) / "exported"
    exported = api.export_artifacts(
        "test_exp",
        sample_experiment.run_id,
        str(output_dir),
        artifact_types=["data", "figures"]
    )
    
    assert "data" in exported
    assert "figures" in exported
    assert Path(exported["data"][0]).exists()
    assert Path(exported["figures"][0]).exists()

# 5. 错误处理测试
def test_error_handling(api):
    """Test error handling"""
    with pytest.raises(FileNotFoundError):
        api.get_experiment("nonexistent")
    
    with pytest.raises(ValueError):
        api.query_experiments(parameter_filters={"invalid__op": 0.1})
    
    with pytest.raises(FileNotFoundError):
        api.get_artifact("nonexistent", "run_id", "file.txt")