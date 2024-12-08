import os
import json
from pathlib import Path
from typing import Optional, Union

class Config:
    _instance = None
    DEFAULT_CONFIG_PATH = Path.home() / ".orruns" / "config.json"
    
    def __init__(self):
        self.config_path = self.DEFAULT_CONFIG_PATH
        self.data_dir: Optional[str] = None
        self._load_config()
    
    @classmethod
    def get_instance(cls) -> 'Config':
        if cls._instance is None:
            cls._instance = Config()
        return cls._instance
    
    def _load_config(self) -> None:
        """Load configuration file
        加载配置文件
        """
        if self.config_path.exists():
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                self.data_dir = config.get('data_dir')
    
    def _save_config(self) -> None:
        """Save configuration file
        保存配置文件
        """
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump({
                'data_dir': self.data_dir
            }, f, indent=2, ensure_ascii=False)
    
    def set_data_dir(self, path: Optional[Union[str, Path]]) -> None:
        """Set data directory
        设置数据目录
        """
        if path is None:
            self.data_dir = None
        else:
            self.data_dir = os.path.abspath(path)
        self._save_config()
    
    def get_data_dir(self) -> Optional[str]:
        """Get data directory
        获取数据目录
        """
        return self.data_dir