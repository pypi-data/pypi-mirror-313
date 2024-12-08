import yaml
import json
from pathlib import Path
from typing import Dict, Any, Optional, Union
from copy import deepcopy

class ExperimentConfig:
    """Experiment configuration management class
    实验配置管理类"""
    
    def __init__(self, config_file: Optional[Union[str, Path]] = None):
        """
        Initialize experiment configuration
        初始化实验配置
        
        Args:
            config_file: Path to the configuration file (supports YAML or JSON)
            config_file: 配置文件路径（支持 YAML 或 JSON）
        """
        self._config = {}
        self._config_file = None
        
        if config_file:
            self.load_config(config_file)
    
    def load_config(self, config_file: Union[str, Path]) -> None:
        """
        Load configuration from a file
        从文件加载配置
        
        Args:
            config_file: Path to the configuration file
            config_file: 配置文件路径
        """
        config_file = Path(config_file)
        if not config_file.exists():
            raise FileNotFoundError(f"Config file not found: {config_file}")
            
        self._config_file = config_file
        
        # Choose loading method based on file extension
        # 根据文件扩展名选择加载方式
        if config_file.suffix.lower() in ['.yml', '.yaml']:
            with open(config_file, 'r', encoding='utf-8') as f:
                self._config = yaml.safe_load(f)
        elif config_file.suffix.lower() == '.json':
            with open(config_file, 'r', encoding='utf-8') as f:
                self._config = json.load(f)
        else:
            raise ValueError("Unsupported config file format. Use .yaml, .yml, or .json")
    
    def save_config(self, file_path: Optional[Union[str, Path]] = None) -> None:
        """
        Save configuration to a file
        保存配置到文件
        
        Args:
            file_path: Save path, if None, use the path from loading
            file_path: 保存路径，如果为None则使用加载时的路径
        """
        if file_path is None:
            if self._config_file is None:
                raise ValueError("No config file path specified")
            file_path = self._config_file
        
        file_path = Path(file_path)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Choose saving method based on file extension
        # 根据文件扩展名选择保存方式
        if file_path.suffix.lower() in ['.yml', '.yaml']:
            with open(file_path, 'w', encoding='utf-8') as f:
                yaml.safe_dump(self._config, f, default_flow_style=False)
        elif file_path.suffix.lower() == '.json':
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(self._config, f, indent=4, ensure_ascii=False)
        else:
            raise ValueError("Unsupported config file format. Use .yaml, .yml, or .json")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value
        获取配置值"""
        return self._config.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """Set configuration value
        设置配置值"""
        self._config[key] = value
    
    def update(self, config_dict: Dict) -> None:
        """Update configuration
        更新配置"""
        self._config.update(config_dict)
    
    def copy(self) -> 'ExperimentConfig':
        """Create a deep copy of the configuration
        创建配置的深拷贝"""
        new_config = ExperimentConfig()
        new_config._config = deepcopy(self._config)
        new_config._config_file = self._config_file
        return new_config
    
    @property
    def config(self) -> Dict:
        """Get the complete configuration dictionary
        获取完整配置字典"""
        return deepcopy(self._config)