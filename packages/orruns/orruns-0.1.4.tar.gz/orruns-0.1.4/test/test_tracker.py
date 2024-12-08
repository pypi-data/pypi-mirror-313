import pytest
import tempfile
import shutil
from pathlib import Path
import json
import time
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

from orruns.tracker import ExperimentTracker
from orruns.errors import ParameterError, MetricError

@pytest.fixture
def temp_dir():
    """创建临时目录"""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)

@pytest.fixture
def tracker(temp_dir):
    """创建实验追踪器实例"""
    return ExperimentTracker("test_exp", base_dir=temp_dir)

def test_log_params(tracker):
    """测试参数记录功能"""
    # 基本参数
    tracker.log_params({"lr": 0.01, "batch_size": 32})
    params = tracker.get_params()
    assert params["lr"] == 0.01
    assert params["batch_size"] == 32

    # 嵌套参数
    tracker.log_params({
        "optimizer": {
            "name": "adam",
            "params": {"beta1": 0.9}
        }
    })
    params = tracker.get_params()
    assert params["optimizer"]["name"] == "adam"
    assert params["optimizer"]["params"]["beta1"] == 0.9

    # 带前缀的参数
    tracker.log_params({"gamma": 0.1}, prefix="optimizer.params")
    params = tracker.get_params()
    assert params["optimizer"]["params"]["gamma"] == 0.1

def test_log_metrics(tracker):
    """测试指标记录功能"""
    # 基本指标
    tracker.log_metrics({"loss": 0.5, "acc": 0.95})
    metrics = tracker.get_metrics()
    assert metrics["loss"] == 0.5
    assert metrics["acc"] == 0.95

    # 带步骤的指标
    tracker.log_metrics({"loss": 0.4}, step=1)
    tracker.log_metrics({"loss": 0.3}, step=2)
    metrics = tracker.get_metrics()
    assert metrics["loss"]["steps"] == [1, 2]
    assert metrics["loss"]["values"] == [0.4, 0.3]

    # 嵌套指标
    tracker.log_metrics({
        "train": {"loss": 0.2},
        "val": {"loss": 0.3}
    })
    metrics = tracker.get_metrics()
    assert metrics["train"]["loss"] == 0.2
    assert metrics["val"]["loss"] == 0.3

def test_error_handling(tracker):
    """测试错误处理"""
    # 参数错误
    with pytest.raises(ParameterError):
        tracker.log_params("not a dict")
    
    with pytest.raises(ParameterError):
        tracker.log_params({}, prefix=123)  # prefix 必须是字符串

    # 指标错误
    with pytest.raises(MetricError):
        tracker.log_metrics({"metric": "not a number"})
    
    with pytest.raises(MetricError):
        tracker.log_metrics({"metric": 1.0}, step="not an int")

def test_experiment_management(temp_dir):
    """测试实验管理功能"""
    # 创建实验
    tracker1 = ExperimentTracker("exp1", base_dir=temp_dir)
    tracker1.log_params({"lr": 0.1})
    tracker1.log_metrics({"acc": 0.9})

    tracker2 = ExperimentTracker("exp2", base_dir=temp_dir)
    tracker2.log_params({"lr": 0.01})
    tracker2.log_metrics({"acc": 0.95})

    # 列出实验
    experiments = ExperimentTracker.list_experiments(base_dir=temp_dir)
    assert len(experiments) == 2
    assert any(e["name"] == "exp1" for e in experiments)
    assert any(e["name"] == "exp2" for e in experiments)

    # 查询实验
    results = ExperimentTracker.query_experiments(
        base_dir=temp_dir,
        parameter_filters={"lr__gt": 0.05}
    )
    assert len(results) == 1
    assert results[0]["parameters"]["lr"] == 0.1

def test_artifact_management(tracker):
    """测试工件管理功能"""
    # 保存不同类型的工件
    df = pd.DataFrame({"A": [1, 2, 3]})
    tracker.log_artifact("data.csv", df, "data")

    fig = plt.figure()
    plt.plot([1, 2, 3])
    tracker.log_artifact("plot.png", fig, "figure")

    # 验证工件列表
    artifacts = tracker.get_current_artifacts()
    assert "data.csv" in artifacts["data"]
    assert "plot.png" in artifacts["figures"]

    # 验证文件存在
    assert (tracker.artifacts_dir / "data" / "data.csv").exists()
    assert (tracker.artifacts_dir / "figures" / "plot.png").exists()