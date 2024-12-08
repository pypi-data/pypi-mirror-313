import pytest
import numpy as np
import time
from pathlib import Path
import tempfile
import shutil
import json
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

from orruns.tracker import ExperimentTracker

@pytest.fixture
def temp_dir():
    """Create temporary directory"""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)

def test_nested_parameters(temp_dir):
    """Test nested parameter recording"""
    tracker = ExperimentTracker("nested_test", base_dir=temp_dir)
    
    # Complex nested parameters
    params = {
        "optimizer": {
            "name": "adam",
            "settings": {
                "learning_rate": 0.001,
                "betas": (0.9, 0.999),
                "epsilon": 1e-8
            }
        },
        "network": {
            "architecture": {
                "layers": [64, 128, 256],
                "activation": "relu",
                "dropout": {
                    "enabled": True,
                    "rate": 0.5
                }
            },
            "input_shape": (28, 28, 1)
        },
        "training": {
            "batch_size": 32,
            "epochs": 100,
            "validation_split": 0.2
        }
    }
    
    # Record parameters
    tracker.log_params(params)
    
    # Verify parameters are saved correctly
    saved_params = tracker.get_params()
    assert saved_params["optimizer"]["settings"]["learning_rate"] == 0.001
    assert saved_params["network"]["architecture"]["dropout"]["rate"] == 0.5
    
    # Update parameters using prefix
    tracker.log_params({"rate": 0.3}, prefix="network.architecture.dropout")
    saved_params = tracker.get_params()
    assert saved_params["network"]["architecture"]["dropout"]["rate"] == 0.3

def test_complex_metrics(temp_dir):
    """Test complex metric recording"""
    tracker = ExperimentTracker("metrics_test", base_dir=temp_dir)
    
    # Simulate metric recording during training
    for epoch in range(5):
        # Training metrics for each epoch
        train_metrics = {
            "loss": {
                "total": 2.5 - epoch * 0.5,
                "components": {
                    "mse": 1.5 - epoch * 0.3,
                    "regularization": 1.0 - epoch * 0.2
                }
            },
            "accuracy": {
                "top1": 0.7 + epoch * 0.05,
                "top5": 0.9 + epoch * 0.02
            },
            "learning_rate": 0.001 * (0.9 ** epoch)
        }
        
        # Validation metrics for each epoch
        val_metrics = {
            "loss": {
                "total": 2.3 - epoch * 0.4,
                "components": {
                    "mse": 1.4 - epoch * 0.25,
                    "regularization": 0.9 - epoch * 0.15
                }
            },
            "accuracy": {
                "top1": 0.75 + epoch * 0.04,
                "top5": 0.92 + epoch * 0.015
            }
        }
        
        # Record metrics
        tracker.log_metrics(train_metrics, prefix="train", step=epoch)
        tracker.log_metrics(val_metrics, prefix="val", step=epoch)
    
    # Verify metrics are saved correctly
    saved_metrics = tracker.get_metrics()
    assert len(saved_metrics["train"]["loss"]["total"]["steps"]) == 5
    assert len(saved_metrics["val"]["accuracy"]["top1"]["values"]) == 5

def test_artifacts_with_complex_data(temp_dir):
    """Test saving and loading complex data artifacts"""
    tracker = ExperimentTracker("artifacts_test", base_dir=temp_dir)
    
    # Create complex plots
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    
    # Generate sample data
    x = np.linspace(0, 10, 100)
    for i, ax in enumerate(axes.flat):
        y = np.sin(x + i) * np.exp(-0.1 * x)
        ax.plot(x, y)
        ax.set_title(f'Subplot {i+1}')
        ax.grid(True)
    
    plt.tight_layout()
    tracker.log_artifact("complex_figure.png", fig, "figure")
    
    # Create multi-level DataFrame
    df = pd.DataFrame({
        'A': np.random.randn(100),
        'B': np.random.randn(100),
        'C': pd.date_range(start='2024-01-01', periods=100)
    })
    df['D'] = df['A'].rolling(window=10).mean()
    df['E'] = df['B'].cumsum()
    
    tracker.log_artifact("complex_data.csv", df, "data")
    
    # Create complex JSON data
    complex_json = {
        "experiment_info": {
            "timestamp": datetime.now().isoformat(),
            "environment": {
                "python_version": "3.8",
                "platform": "Linux",
                "dependencies": ["numpy", "pandas", "matplotlib"]
            }
        },
        "results": {
            "metrics": {
                "accuracy": 0.95,
                "precision": 0.92,
                "recall": 0.94
            },
            "confusion_matrix": [[100, 5], [3, 92]],
            "feature_importance": {
                "feature1": 0.8,
                "feature2": 0.6,
                "feature3": 0.4
            }
        },
        "hyperparameters": {
            "model": {
                "type": "neural_network",
                "layers": [64, 32, 16],
                "activation": "relu"
            },
            "training": {
                "epochs": 100,
                "batch_size": 32,
                "optimizer": {
                    "name": "adam",
                    "learning_rate": 0.001
                }
            }
        }
    }
    
    tracker.log_artifact("complex_results.json", complex_json, "json")
    
    # Verify artifacts are saved and loaded correctly
    artifacts = tracker.get_current_artifacts()
    assert "complex_figure.png" in artifacts["figures"]
    assert "complex_data.csv" in artifacts["data"]
    
    # Load and verify data
    loaded_df = ExperimentTracker.get_artifact(
        tracker.experiment_name,
        tracker.run_id,
        "complex_data.csv",
        artifact_type="data",  # 使用 artifact_type 参数
        base_dir=temp_dir,
        load_content=True      # 添加 load_content=True 来加载内容
    )
    assert isinstance(loaded_df, pd.DataFrame)
    assert loaded_df.shape == (100, 5)

def test_experiment_query(temp_dir):
    """Test complex experiment queries"""
    # Create multiple experiment records
    experiments = []
    for i in range(3):
        for j in range(2):
            tracker = ExperimentTracker(f"exp_{i}", base_dir=temp_dir)
            
            # Record complex parameters
            params = {
                "model": {
                    "type": "cnn" if i % 2 == 0 else "rnn",
                    "layers": [32 * (2 ** j), 64 * (2 ** j)],
                    "dropout": 0.5 - j * 0.1
                },
                "training": {
                    "batch_size": 32 * (2 ** i),
                    "learning_rate": 0.001 / (2 ** j)
                }
            }
            tracker.log_params(params)
            
            # Record complex metrics
            metrics = {
                "performance": {
                    "accuracy": 0.8 + i * 0.05 + j * 0.02,
                    "loss": 0.5 - i * 0.1 - j * 0.05
                },
                "efficiency": {
                    "training_time": 100 + i * 50 + j * 20,
                    "memory_usage": 1000 + i * 200 + j * 100
                }
            }
            tracker.log_metrics(metrics)
            experiments.append(tracker)
            
            time.sleep(0.1)  # Ensure different timestamps
    
    # Test complex queries
    results = ExperimentTracker.query_experiments(
        base_dir=temp_dir,
        parameter_filters={
            "model.type": "cnn",
            "training.batch_size__gte": 64
        },
        metric_filters=[{
            "performance.accuracy__gt": 0.85,
            "efficiency.training_time__lt": 200
        }],
        sort_by="metrics.performance.accuracy",
        sort_ascending=False,
        limit=2
    )
    
    assert len(results) <= 2
    if results:
        assert results[0]["parameters"]["model"]["type"] == "cnn"
        assert results[0]["parameters"]["training"]["batch_size"] >= 64
        assert results[0]["metrics"]["performance"]["accuracy"] > 0.85