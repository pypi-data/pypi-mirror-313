import pytest
import tempfile
import shutil
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

from orruns.cli.commands import ExperimentAPI
from orruns.tracker import ExperimentTracker

@pytest.fixture
def temp_dir():
    """创建临时目录"""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)

@pytest.fixture
def api(temp_dir):
    """创建API实例"""
    return ExperimentAPI(data_dir=temp_dir)

@pytest.fixture
def sample_experiment(temp_dir):
    """创建示例实验数据"""
    tracker = ExperimentTracker("test_exp", base_dir=temp_dir)
    tracker.log_params({"param1": 1, "param2": "test"})
    tracker.log_metrics({"metric1": 0.5, "metric2": 100})
    
    # 创建一些工件
    fig = plt.figure()
    plt.plot([1, 2, 3])
    tracker.log_artifact("plot.png", fig, "figure")
    
    df = pd.DataFrame({"A": [1, 2, 3]})
    tracker.log_artifact("data.csv", df, "data")
    
    return tracker

def test_experiment_management(api, sample_experiment):
    """测试实验管理功能"""
    # 列出实验
    experiments = api.list_experiments()
    assert len(experiments) > 0
    assert experiments[0]["name"] == "test_exp"
    
    # 获取实验详情
    exp = api.get_experiment("test_exp")
    assert exp["name"] == "test_exp"
    assert exp["parameters"]["param1"] == 1
    assert exp["metrics"]["metric1"] == 0.5
    
    # 删除实验
    api.delete_experiment("test_exp")
    with pytest.raises(FileNotFoundError):
        api.get_experiment("test_exp")

def test_artifact_management(api, sample_experiment):
    """测试工件管理功能"""
    # 列出工件
    artifacts = api.list_artifacts("test_exp", sample_experiment.run_id)
    assert "figures" in artifacts
    assert "data" in artifacts
    assert "plot.png" in artifacts["figures"]
    assert "data.csv" in artifacts["data"]
    
    # 获取工件 - 修改这里
    artifact = api.get_artifact(
        "test_exp", 
        sample_experiment.run_id, 
        "data.csv",
        artifact_type="data",  # 添加 artifact_type
        load_content=True      # 添加 load_content
    )
    assert isinstance(artifact, pd.DataFrame)

def test_experiment_analysis(api, sample_experiment):
    """测试实验分析功能"""
    # 比较实验
    comparison = api.compare_experiments(["test_exp"])
    assert "test_exp" in comparison
    assert comparison["test_exp"]["metric1"] == 0.5
    
    # 获取历史记录
    history = api.get_experiment_history("test_exp")
    assert len(history) > 0
    assert history[0]["metrics"]["metric1"] == 0.5

def test_data_export(api, sample_experiment):
    """测试数据导出功能"""
    # 导出到DataFrame
    df = api.export_to_dataframe("test_exp")
    assert "metric1" in df.columns
    assert df.iloc[0]["metric1"] == 0.5

def test_maintenance(api, sample_experiment):
    """测试维护功能"""
    # 清理旧实验
    deleted = api.clean_old_experiments(days=0)
    assert "test_exp" in deleted

def test_error_handling(api):
    """测试错误处理"""
    # 不存在的实验
    with pytest.raises(FileNotFoundError):
        api.get_experiment("nonexistent")
    
    # 无效的过滤器
    with pytest.raises(ValueError):
        api._validate_filters({"invalid_filter": 1})