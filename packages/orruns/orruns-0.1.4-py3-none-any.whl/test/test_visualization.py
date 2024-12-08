import pytest
from pathlib import Path
import shutil
from orruns.tracker import ExperimentTracker
from orruns.visualization import ExperimentDashboard

def test_dashboard_basic_setup():
    # 创建临时测试目录
    test_dir = Path("./test_experiments")
    if test_dir.exists():
        shutil.rmtree(test_dir)
    test_dir.mkdir()
    
    try:
        # 创建一些测试数据
        tracker = ExperimentTracker("test_exp", base_dir=str(test_dir))
        
        # 记录一些参数
        tracker.log_params({
            "learning_rate": 0.01,
            "batch_size": 32
        })
        
        # 记录一些指标
        for i in range(10):
            tracker.log_metrics({
                "loss": 1.0 - i * 0.1,
                "accuracy": i * 0.1
            }, step=i)
        
        # 创建仪表板实例
        dashboard = ExperimentDashboard(base_dir=str(test_dir))
        
        # 验证基本属性
        assert dashboard.base_dir == test_dir
        assert dashboard.app is not None
        
        # 验证布局组件存在
        layout = dashboard.app.layout
        assert 'experiment-dropdown' in layout.children[1].children[1].id
        assert 'metric-dropdown' in layout.children[2].children[1].id
        assert 'metric-plot' in layout.children[3].children[0].id
        assert 'convergence-plot' in layout.children[3].children[1].id
        
    finally:
        # 清理测试目录
        shutil.rmtree(test_dir)

def test_dashboard_data_loading():
    test_dir = Path("./test_experiments")
    if test_dir.exists():
        shutil.rmtree(test_dir)
    test_dir.mkdir()
    
    try:
        # 创建多个实验运行
        for run in range(3):
            tracker = ExperimentTracker("test_exp", base_dir=str(test_dir))
            tracker.log_params({
                "learning_rate": 0.01 * (run + 1),
                "batch_size": 32 * (run + 1)
            })
            
            for i in range(10):
                tracker.log_metrics({
                    "loss": 1.0 - i * 0.1 * (run + 1),
                    "accuracy": i * 0.1 * (run + 1)
                }, step=i)
        
        # 创建仪表板
        dashboard = ExperimentDashboard(base_dir=str(test_dir))
        
        # 直接调用更新函数
        def find_callback_by_output(output_id):
            for callback in dashboard.app.callback_map.values():
                if hasattr(callback, 'output') and output_id in str(callback.output):
                    return callback.callback
            return None
            
        # 测试实验下拉菜单更新
        update_experiments = find_callback_by_output('experiment-dropdown.options')
        assert update_experiments is not None
        options, value = update_experiments(None)
        assert len(options) > 0
        assert options[0]['value'] == 'test_exp'
        
    finally:
        shutil.rmtree(test_dir)

def test_dashboard_plot_generation():
    test_dir = Path("./test_experiments")
    if test_dir.exists():
        shutil.rmtree(test_dir)
    test_dir.mkdir()
    
    try:
        # 创建测试数据
        tracker = ExperimentTracker("test_exp", base_dir=str(test_dir))
        tracker.log_params({"learning_rate": 0.01})
        for i in range(10):
            tracker.log_metrics({"loss": 1.0 - i * 0.1}, step=i)
        
        # 创建仪表板
        dashboard = ExperimentDashboard(base_dir=str(test_dir))
        
        # 直接调用更新函数
        def find_callback_by_output(output_id):
            for callback in dashboard.app.callback_map.values():
                if hasattr(callback, 'output') and output_id in str(callback.output):
                    return callback.callback
            return None
            
        # 测试图表生成
        update_plots = find_callback_by_output('metric-plot.figure')
        assert update_plots is not None
        box_fig, conv_fig, stats = update_plots('test_exp', 'loss')
        assert isinstance(box_fig, dict)
        assert isinstance(conv_fig, dict)
        assert len(stats) > 0
        
    finally:
        shutil.rmtree(test_dir)

if __name__ == "__main__":
    pytest.main([__file__])