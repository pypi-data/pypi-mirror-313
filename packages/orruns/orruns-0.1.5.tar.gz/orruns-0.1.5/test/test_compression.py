import pytest
import tempfile
import shutil
from pathlib import Path
import time
import os

from orruns.api.experiment import ExperimentAPI
from orruns.tracker import ExperimentTracker
from orruns.core.config import Config

@pytest.fixture
def api(tmp_path):
    """创建API实例，使用临时数据目录"""
    data_dir = tmp_path / "orruns_experiments"
    data_dir.mkdir(parents=True, exist_ok=True)
    config = Config.get_instance()
    config.set_data_dir(str(data_dir))
    return ExperimentAPI()

@pytest.fixture
def sample_data(api):
    """创建示例数据"""
    # 创建多个实验记录
    trackers = []
    for i in range(3):
        tracker = ExperimentTracker(f"test_exp_{i}")
        tracker.log_params({
            "learning_rate": 0.01 * (i + 1),
            "batch_size": 32,
            "model_type": "cnn"
        })
        tracker.log_metrics({
            "accuracy": 0.85 + 0.01 * i,
            "loss": 0.15 - 0.01 * i
        })
        
        # 创建不同类型的文件
        tracker.log_artifact(
            f"data_{i}.csv", 
            f"col1,col2\n{i},{i+1}", 
            artifact_type="data"
        )
        tracker.log_artifact(
            f"plot_{i}.png", 
            b"fake_image_data", 
            artifact_type="figure"
        )
        trackers.append(tracker)
        time.sleep(0.1)  # 确保时间戳不同
    
    return trackers

def test_compress_data_dir_basic(api, sample_data):
    """测试基本的压缩功能"""
    # 执行压缩
    zip_path = api.compress_data_dir()
    zip_file = Path(zip_path)
    
    # 基本验证
    assert zip_file.exists(), f"压缩文件未创建: {zip_path}"
    assert zip_file.stat().st_size > 0, "压缩文件为空"
    assert zip_file.name == "orruns_experiments.zip", "压缩文件名称不正确"
    assert zip_file.parent == Path(api.config.get_data_dir()).parent, "压缩文件位置不正确"

def test_compress_data_dir_empty(api):
    """测试压缩空目录的情况"""
    with pytest.raises(ValueError, match="数据目录为空"):
        api.compress_data_dir()

def test_compress_data_dir_nonexistent(api):
    """测试压缩不存在目录的情况"""
    # 删除数据目录
    shutil.rmtree(api.config.get_data_dir(), ignore_errors=True)
    
    with pytest.raises(FileNotFoundError):
        api.compress_data_dir()

def test_decompress_data_dir_basic(api, sample_data):
    """测试基本的解压功能"""
    # 先压缩
    zip_path = api.compress_data_dir()
    original_dir = Path(api.config.get_data_dir())
    
    # 记录原始文件信息
    original_files = set(f.relative_to(original_dir) for f in original_dir.rglob("*") if f.is_file())
    
    # 解压
    output_dir = api.decompress_data_dir()
    output_path = Path(output_dir)
    
    # 验证
    assert output_path.exists(), "解压目录不存在"
    assert not Path(zip_path).exists(), "压缩文件未被删除"
    
    # 验证文件完整性
    decompressed_files = set(f.relative_to(output_path) for f in output_path.rglob("*") if f.is_file())
    assert original_files == decompressed_files, "解压后文件不完整"

def test_decompress_data_dir_invalid_zip(api, tmp_path):
    """测试解压无效的zip文件"""
    # 创建一个无效的zip文件
    invalid_zip = tmp_path / "orruns_experiments.zip"
    invalid_zip.write_bytes(b"not a zip file")
    
    with pytest.raises(RuntimeError, match="解压过程出错"):
        api.decompress_data_dir()

def test_decompress_data_dir_nonexistent(api):
    """测试解压不存在的文件"""
    with pytest.raises(FileNotFoundError):
        api.decompress_data_dir()

def test_compress_decompress_cycle(api, sample_data):
    """测试完整的压缩-解压周期"""
    original_dir = Path(api.config.get_data_dir())
    
    # 记录原始状态
    original_files = {}
    for f in original_dir.rglob("*"):
        if f.is_file():
            relative_path = f.relative_to(original_dir)
            original_files[str(relative_path)] = f.read_bytes()
    
    # 执行压缩
    zip_path = api.compress_data_dir()
    assert Path(zip_path).exists(), "压缩文件未创建"
    
    # 删除原始目录
    shutil.rmtree(original_dir)
    assert not original_dir.exists(), "原始目录未被删除"
    
    # 执行解压
    output_dir = api.decompress_data_dir()
    output_path = Path(output_dir)
    
    # 验证文件内容
    for relative_path, original_content in original_files.items():
        decompressed_file = output_path / relative_path
        assert decompressed_file.exists(), f"文件 {relative_path} 未被恢复"
        assert decompressed_file.read_bytes() == original_content, f"文件 {relative_path} 内容不匹配"

def test_compress_with_special_chars(api):
    """测试包含特殊字符的文件压缩"""
    # 创建包含特殊字符的实验
    tracker = ExperimentTracker("test_特殊字符")
    tracker.log_params({"参数": "值"})
    tracker.log_artifact("测试.txt", "测试内容", artifact_type="data")
    time.sleep(0.1)
    
    # 压缩和解压
    zip_path = api.compress_data_dir()
    output_dir = api.decompress_data_dir()
    
    # 验证特殊字符文件是否正确恢复
    output_path = Path(output_dir)
    special_files = list(output_path.rglob("测试.txt"))
    assert len(special_files) > 0, "包含特殊字符的文件未被恢复"

@pytest.fixture(autouse=True)
def cleanup():
    """每次测试后清理"""
    yield
    # 重置Config单例
    Config._instance = None