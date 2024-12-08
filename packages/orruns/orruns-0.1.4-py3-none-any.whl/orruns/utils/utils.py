import platform
import psutil
import multiprocessing as mp
import time
from typing import Dict, Optional
from functools import lru_cache
import os
import sys
import cpuinfo

@lru_cache(maxsize=1)
def get_system_info(
    experiment_name: Optional[str] = None, 
    parallel: Optional[bool] = None, 
    times: Optional[int] = None, 
    max_workers: Optional[int] = None,
    level: str = 'basic'  # 'none', 'basic', 或 'full'
) -> Dict:
    """
    收集系统信息，提供三个层级的信息详细程度
    
    Args:
        experiment_name: 实验名称
        parallel: 是否并行执行
        times: 重复次数
        max_workers: 最大工作进程数
        level: 信息详细程度
            - 'none': 只返回最基本的实验配置
            - 'basic': 返回运筹学论文常用的关键信息
            - 'full': 返回所有可获取的系统信息
        
    Returns:
        包含系统信息的字典
    """

    # 基础实验信息（level='none'）
    system_info = {}
    if level == 'none':
        return system_info

    if experiment_name is not None:
        system_info["experiment"] = {
            "name": experiment_name,
            "parallel": parallel,
            "times": times,
            "max_workers": max_workers if parallel else None,
            "start_time": time.strftime("%Y-%m-%d %H:%M:%S")
        }
    

        
    # 运筹学论文常用的关键信息（level='basic'）
    if level in ['basic', 'full']:
        cpu_info = cpuinfo.get_cpu_info()
        
        system_info.update({
            "hardware": {
                "cpu": {
                    "model": cpu_info.get('brand_raw', 'Unknown'),
                    "physical_cores": psutil.cpu_count(logical=False),
                    "logical_cores": psutil.cpu_count(logical=True),
                    "base_frequency_ghz": round(cpu_info.get('hz_advertised_raw', [0])[0] / 1000000000, 2)
                },
                "memory": {
                    "total_gb": round(psutil.virtual_memory().total / (1024 ** 3), 2)
                }
            },
            "software": {
                "os": f"{platform.system()} {platform.release()}",
                "python": platform.python_version(),
                "key_packages": {
                    "numpy": __import__('numpy').__version__,
                    "scipy": __import__('scipy').__version__
                }
            }
        })
        
        # 基础GPU信息
        try:
            import torch
            if torch.cuda.is_available():
                system_info["hardware"]["gpu"] = {
                    "model": torch.cuda.get_device_name(0),
                    "count": torch.cuda.device_count(),
                    "memory_gb": round(torch.cuda.get_device_properties(0).total_memory / (1024**3), 2)
                }
        except ImportError:
            pass
    
    if level == 'basic':
        return system_info
        
    # 完整系统信息（level='full'）
    if level == 'full':
        system_info.update({
            "hardware": {
                "cpu": {
                    **system_info["hardware"]["cpu"],
                    "architecture": cpu_info.get('arch', platform.machine()),
                    "max_frequency_mhz": psutil.cpu_freq().max if hasattr(psutil.cpu_freq(), 'max') else None,
                    "cache_size": cpu_info.get('l2_cache_size', 'Unknown'),
                    "instruction_set": cpu_info.get('flags', [])
                },
                "memory": {
                    **system_info["hardware"]["memory"],
                    "available_gb": round(psutil.virtual_memory().available / (1024 ** 3), 2),
                    "type": "Unknown",
                    "speed": "Unknown"
                },
                "disk": {
                    "total_gb": round(psutil.disk_usage('/').total / (1024 ** 3), 2),
                    "free_gb": round(psutil.disk_usage('/').free / (1024 ** 3), 2)
                }
            },
            "software": {
                "os": {
                    "system": platform.system(),
                    "release": platform.release(),
                    "version": platform.version(),
                    "machine": platform.machine()
                },
                "python": {
                    "version": platform.python_version(),
                    "implementation": platform.python_implementation(),
                    "compiler": platform.python_compiler(),
                    "location": sys.executable
                },
                "packages": {
                    **system_info["software"]["key_packages"],
                    "pandas": __import__('pandas').__version__,
                    "matplotlib": __import__('matplotlib').__version__,
                    "torch": __import__('torch').__version__ if 'torch' in sys.modules else None
                }
            }
        })
        
        # 详细GPU信息
        if "gpu" in system_info["hardware"]:
            system_info["hardware"]["gpu"].update({
                "devices": [
                    {
                        "name": torch.cuda.get_device_name(i),
                        "total_memory_gb": round(torch.cuda.get_device_properties(i).total_memory / (1024**3), 2),
                        "compute_capability": f"{torch.cuda.get_device_capability(i)[0]}.{torch.cuda.get_device_capability(i)[1]}"
                    }
                    for i in range(torch.cuda.device_count())
                ],
                "cuda_version": torch.version.cuda,
                "cudnn_version": torch.backends.cudnn.version() if torch.backends.cudnn.is_available() else None
            })
            
        # 详细实验信息
        if "experiment" in system_info:
            system_info["experiment"].update({
                "process_affinity": list(os.sched_getaffinity(0)) if hasattr(os, 'sched_getaffinity') else None,
                "current_memory_usage_gb": round(psutil.Process().memory_info().rss / (1024 ** 3), 2)
            })
    
    return system_info


from rich.console import Console
from rich.panel import Panel
from rich.layout import Layout
from rich.json import JSON
from rich.table import Table
from rich.text import Text

def print_system_info(
    system_info: Dict,
    style: str = 'auto',  # 'auto', 'rich', 'simple', 'markdown'
    jupyter: bool = None  # 自动检测是否在 Jupyter 环境
) -> None:
    """
    根据环境智能打印系统信息
    
    Args:
        system_info: 系统信息字典
        style: 打印样式
            - 'auto': 自动选择最佳样式
            - 'rich': 使用rich库的完整样式
            - 'simple': 简单文本样式
            - 'markdown': Markdown表格样式
        jupyter: 是否在Jupyter环境中，None为自动检测
    """
    if  system_info=={ }:
        return
    # 自动检测环境
    if jupyter is None:
        jupyter = 'ipykernel' in sys.modules
    
    # 自动选择样式
    if style == 'auto':
        if jupyter:
            style = 'markdown'
        else:
            style = 'rich'
    
    try:
        if style == 'markdown':
            if jupyter:
                from IPython.display import display, Markdown
                _print_markdown_style(system_info)
            else:
                _print_markdown_style(system_info)
        elif style == 'simple':
            _print_simple_style(system_info)
        elif style == 'rich':
            try:
                from rich.console import Console
                from rich.table import Table
                _print_rich_style(system_info)
            except ImportError:
                print("Rich library not found, falling back to simple style")
                _print_simple_style(system_info)
        else:
            print(f"Unknown style: {style}, falling back to simple style")
            _print_simple_style(system_info)
    except Exception as e:
        print(f"Error printing system info: {e}")
        _print_simple_style(system_info)

def _print_markdown_style(system_info: Dict) -> None:
    """Markdown表格样式，适合Jupyter环境"""
    from IPython.display import display, Markdown
    
    # 硬件信息
    hw_md = "## Hardware\n\n"
    hw_md += "| Component | Specification |\n"
    hw_md += "|-----------|---------------|\n"
    
    cpu_info = system_info["hardware"]["cpu"]
    hw_md += f"| CPU | {cpu_info['model']}<br>Cores: {cpu_info['physical_cores']} Physical / {cpu_info['logical_cores']} Logical<br>Base Frequency: {cpu_info['base_frequency_ghz']} GHz |\n"
    
    hw_md += f"| Memory | Total: {system_info['hardware']['memory']['total_gb']} GB |\n"
    
    if "gpu" in system_info["hardware"]:
        gpu_info = system_info["hardware"]["gpu"]
        hw_md += f"| GPU | {gpu_info['model']}<br>Count: {gpu_info['count']}<br>Memory: {gpu_info['memory_gb']} GB |\n"
    
    # 软件信息
    sw_md = "\n## Software\n\n"
    sw_md += "| Component | Version |\n"
    sw_md += "|-----------|----------|\n"
    
    os_info = system_info["software"]["os"]
    os_str = f"{os_info['system']} {os_info['release']}" if isinstance(os_info, dict) else os_info
    sw_md += f"| OS | {os_str} |\n"
    
    python_info = system_info["software"]["python"]
    python_str = python_info["version"] if isinstance(python_info, dict) else python_info
    sw_md += f"| Python | {python_str} |\n"
    
    packages = (system_info["software"].get("packages") or 
               system_info["software"].get("key_packages") or {})
    for pkg, version in packages.items():
        if version is not None:
            sw_md += f"| {pkg.capitalize()} | {version} |\n"
    
    # 实验信息（如果有）
    if "experiment" in system_info:
        exp_md = "\n## Experiment\n\n"
        exp_md += "| Parameter | Value |\n"
        exp_md += "|-----------|--------|\n"
        
        exp_info = system_info["experiment"]
        exp_md += f"| Name | {exp_info['name']} |\n"
        exp_md += f"| Parallel | {exp_info['parallel']} |\n"
        exp_md += f"| Times | {exp_info['times']} |\n"
        exp_md += f"| Max Workers | {exp_info['max_workers']} |\n"
        exp_md += f"| Start Time | {exp_info['start_time']} |\n"
    else:
        exp_md = ""
    
    # 显示
    display(Markdown(hw_md + sw_md + exp_md))

def _print_simple_style(system_info: Dict) -> None:
    """简单文本样式，适合普通终端"""
    def print_section(title: str, content: Dict) -> None:
        print(f"\n=== {title} ===")
        for key, value in content.items():
            if isinstance(value, dict):
                print(f"\n{key}:")
                for k, v in value.items():
                    print(f"  {k}: {v}")
            else:
                print(f"{key}: {value}")
    
    print_section("Hardware", system_info["hardware"])
    print_section("Software", system_info["software"])
    if "experiment" in system_info:
        print_section("Experiment", system_info["experiment"])

def _print_rich_style(system_info: Dict) -> None:
    """Rich库完整样式，适合支持富文本的终端"""
    """
    使用rich库美化打印系统信息
    
    Args:
        system_info: 系统信息字典
    """
    console = Console()
    
    # 创建硬件信息表格
    hw_table = Table(show_header=True, header_style="bold magenta")
    hw_table.add_column("Component", style="cyan")
    hw_table.add_column("Specification", style="green")
    
    # CPU信息
    cpu_info = system_info["hardware"]["cpu"]
    hw_table.add_row(
        "CPU",
        f"{cpu_info['model']}\n"
        f"Cores: {cpu_info['physical_cores']} Physical / {cpu_info['logical_cores']} Logical\n"
        f"Base Frequency: {cpu_info['base_frequency_ghz']} GHz"
    )
    
    # 内存信息
    hw_table.add_row(
        "Memory",
        f"Total: {system_info['hardware']['memory']['total_gb']} GB"
    )
    
    # GPU信息（如果有）
    if "gpu" in system_info["hardware"]:
        gpu_info = system_info["hardware"]["gpu"]
        hw_table.add_row(
            "GPU",
            f"{gpu_info['model']}\n"
            f"Count: {gpu_info['count']}\n"
            f"Memory: {gpu_info['memory_gb']} GB"
        )
    
    # 创建软件信息表格
    sw_table = Table(show_header=True, header_style="bold magenta")
    sw_table.add_column("Component", style="cyan")
    sw_table.add_column("Version", style="green")
    
    # 修复 OS 信息显示
    os_info = system_info["software"]["os"]
    if isinstance(os_info, dict):
        os_str = f"{os_info['system']} {os_info['release']}"
    else:
        os_str = os_info
    sw_table.add_row("OS", os_str)
    
    # 修复 Python 信息显示
    python_info = system_info["software"]["python"]
    if isinstance(python_info, dict):
        python_str = python_info["version"]
    else:
        python_str = python_info
    sw_table.add_row("Python", python_str)
    
    # 修复包版本信息显示
    if "packages" in system_info["software"]:
        packages = system_info["software"]["packages"]
    elif "key_packages" in system_info["software"]:
        packages = system_info["software"]["key_packages"]
    else:
        packages = {}
        
    for pkg, version in packages.items():
        if version is not None:  # 只显示已安装的包
            sw_table.add_row(pkg.capitalize(), str(version))
    
    # 创建实验信息表格（如果有）
    if "experiment" in system_info:
        exp_table = Table(show_header=True, header_style="bold magenta")
        exp_table.add_column("Parameter", style="cyan")
        exp_table.add_column("Value", style="green")
        
        exp_info = system_info["experiment"]
        exp_table.add_row("Name", exp_info["name"])
        exp_table.add_row("Parallel", str(exp_info["parallel"]))
        exp_table.add_row("Times", str(exp_info["times"]))
        exp_table.add_row("Max Workers", str(exp_info["max_workers"]))
        exp_table.add_row("Start Time", exp_info["start_time"])
    
    # 创建布局
    layout = Layout()
    layout.split_column(
        Layout(Panel(
            Text("System Information", justify="center", style="bold white"),
            style="bold blue"
        ), size=3),
        Layout(name="main")
    )
    
    # 分割主区域
    if "experiment" in system_info:
        layout["main"].split_row(
            Layout(Panel(hw_table, title="Hardware", border_style="blue")),
            Layout(Panel(sw_table, title="Software", border_style="green")),
            Layout(Panel(exp_table, title="Experiment", border_style="yellow"))
        )
    else:
        layout["main"].split_row(
            Layout(Panel(hw_table, title="Hardware", border_style="blue")),
            Layout(Panel(sw_table, title="Software", border_style="green"))
        )
    
    # 打印布局
    console.print("\n")
    console.print(layout)
    console.print("\n")