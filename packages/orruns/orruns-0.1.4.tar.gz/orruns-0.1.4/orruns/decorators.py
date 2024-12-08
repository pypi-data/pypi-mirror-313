import pickle
import networkx as nx
import functools
import logging
import multiprocessing as mp
from concurrent.futures import ProcessPoolExecutor, as_completed
from typing import Optional, Callable, Any, List, Dict
import time
import cloudpickle
import pathlib
import platform
import hashlib
import uuid
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from tqdm import tqdm
from .tracker import ExperimentTracker
from .utils.utils import get_system_info, print_system_info
import threading

# Configure logging at the start of the module
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Add global semaphore for experiment control
_experiment_semaphore = threading.Semaphore(1)


class ResultsMerger:
    def __init__(self, experiment_name: str, base_dir: str, run_ids: List[str]):
        """Initialize with actual run IDs
        使用实际运行ID初始化"""

        
        # Generate batch ID with timestamp and random hash
        # 使用时间戳和随机哈希生成批次ID
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        random_hash = hashlib.md5(str(uuid.uuid4()).encode()).hexdigest()[:4]
        self.batch_id = f"{timestamp}_{random_hash}"
        self.run_ids = run_ids  # Store actual run IDs
        
        # Create save directory
        # 创建保存目录
        self.save_dir = pathlib.Path(base_dir) / experiment_name / "merged_results" / self.batch_id
        self.save_dir.mkdir(parents=True, exist_ok=True)
        
        self._save_metadata()
    
    def _save_metadata(self):
        """Save metadata about the merge operation
        保存合并操作的元数据"""
        metadata = {
            "batch_id": self.batch_id,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "n_parallel_runs": len(self.run_ids),
            "source_experiments": self.run_ids,  # Use actual run IDs
            "merge_time": time.strftime("%Y-%m-%d %H:%M:%S"),
            "system_info": {
                "platform": platform.platform(),
                "python_version": platform.python_version(), 
                "cpu_count": mp.cpu_count()
            }
        }
        
        # Save metadata to JSON file
        # 将元数据保存到JSON文件
        with open(self.save_dir / "batch_metadata.json", 'w') as f:
            json.dump(metadata, f, indent=4)

    def merge_results(self, results: List[dict], merge_config: Dict) -> None:
        """Merge different types of results according to configuration
        根据配置合并不同类型的结果"""
        for data_type, keys in merge_config.items():
            if data_type == "arrays":
                self._merge_arrays(results, keys)
            elif data_type == "scalars":
                self._merge_scalars(results, keys)
            elif data_type == "images":
                self._merge_images(results, keys)
            elif data_type == "time_series":
                self._merge_time_series(results, keys)
            elif data_type == "graphs":
                self._merge_graphs(results, keys)
            elif data_type == "distributions":
                self._merge_distributions(results, keys)
            elif data_type == "text":
                self._merge_text(results, keys)
            elif data_type == "models":
                self._merge_models(results, keys)

    def _merge_arrays(self, results: List[dict], keys: List[str]) -> None:
        """Merge array data
        合并数组数据"""
        import h5py
        
        # 创建数组数据目录
        array_dir = self.save_dir / "arrays"
        array_dir.mkdir(exist_ok=True)
        
        for key in keys:
            if key in results[0]:
                # 收集所有运行的数据
                all_data = [result[key] for result in results]
                
                # 转换为DataFrame保存
                if isinstance(all_data[0], (list, np.ndarray)):
                    df = pd.DataFrame(all_data)
                    df.to_csv(array_dir / f"{key}.csv")
                else:
                    # 其他类型尝试JSON保存
                    with open(array_dir / f"{key}.json", 'w') as f:
                        json.dump(all_data, f, indent=4)
                    #计算并保存统计信息
                    try:
                        arrays = [r[key] for r in results]
                        if all(arr.shape == arrays[0].shape for arr in arrays):
                            stats = f.create_group("statistics")
                            stacked = np.stack(arrays)
                            stats.create_dataset('mean', data=np.mean(stacked, axis=0))
                            stats.create_dataset('std', data=np.std(stacked, axis=0))
                            stats.create_dataset('min', data=np.min(stacked, axis=0))
                            stats.create_dataset('max', data=np.max(stacked, axis=0))
                    except Exception as e:
                        logging.warning(f"Could not compute statistics for {key}: {e}")

    def _merge_scalars(self, results: List[dict], keys: List[str]) -> None:
        """Merge scalar data
        合并标量数据"""
        # 创建标量数据目录
        scalar_dir = self.save_dir / "scalars"
        scalar_dir.mkdir(exist_ok=True)
        
        # 收集所有标量数据
        data = []
        for i, result in enumerate(results):
            row = {'run': i}
            for key in keys:
                if key in result:
                    row[key] = result[key]
            data.append(row)
        
        # 创建数据框并保存
        df = pd.DataFrame(data)
        
        # 保存原始数据
        df.to_csv(scalar_dir / "raw_values.csv", index=False)
        
        # 计算并保存统计信息
        stats = df.describe()
        stats.to_csv(scalar_dir / "statistics.csv")
        
        # 为每个标量创建分布图
        for key in keys:
            if key in df.columns:
                plt.figure(figsize=(10, 6))
                plt.hist(df[key], bins=20, density=True)
                plt.title(f'{key} Distribution')
                plt.xlabel('Value')
                plt.ylabel('Density')
                plt.savefig(scalar_dir / f"{key}_distribution.png")
                plt.close()
    def _merge_time_series(self, results: List[dict], keys: List[str]) -> None:
        """Merge time series data
        合并时间序列数据"""
        for key in keys:
            if key in results[0]:
                # Create multi-column time series dataframe
                # 创建多列时间序列数据框
                df = pd.DataFrame()
                for i, result in enumerate(results):
                    df[f'run_{i}'] = result[key]
                
                # Calculate statistics
                # 计算统计信息
                df['mean'] = df.mean(axis=1)
                df['std'] = df.std(axis=1)
                
                # Save results
                # 保存结果
                df.to_csv(self.save_dir / f"{key}_timeseries.csv")
                
                # Plot time series
                # 绘制时间序列图
                plt.figure(figsize=(10, 6))
                plt.plot(df['mean'], label='Mean')
                plt.fill_between(
                    df.index,
                    df['mean'] - df['std'],
                    df['mean'] + df['std'],
                    alpha=0.2,
                    label='±1 std'
                )
                plt.title(f'{key} Time Series')
                plt.savefig(self.save_dir / f"{key}_timeseries.png")
                plt.close()

    def _merge_images(self, results: List[dict], keys: List[str]) -> None:
        """Merge image data
        合并图像数据"""
        for key in keys:
            if key in results[0]:
                # Create image grid
                # 创建图像网格
                n_images = len(results)
                cols = min(5, n_images)
                rows = (n_images + cols - 1) // cols
                
                fig, axes = plt.subplots(rows, cols, figsize=(cols*4, rows*4))
                axes = axes.flatten()
                
                for i, result in enumerate(results):
                    if isinstance(result[key], np.ndarray):
                        axes[i].imshow(result[key])
                        axes[i].set_title(f'Run {i}')
                        axes[i].axis('off')
                
                plt.tight_layout()
                plt.savefig(self.save_dir / f"{key}_grid.png")
                plt.close()

    def _merge_graphs(self, results: List[dict], keys: List[str]) -> None:
        """Merge graph structure data
        合并图结构数据"""
        for key in keys:
            if key in results[0]:
                # Save statistics for each graph
                # 保存每个图的统计信息
                stats = []
                for i, result in enumerate(results):
                    if isinstance(result[key], nx.Graph):
                        G = result[key]
                        stats.append({
                            'run': i,
                            'n_nodes': G.number_of_nodes(),
                            'n_edges': G.number_of_edges(),
                            'density': nx.density(G),
                            'avg_clustering': nx.average_clustering(G)
                        })
                
                pd.DataFrame(stats).to_csv(
                    self.save_dir / f"{key}_graph_stats.csv"
                )

    def _merge_distributions(self, results: List[dict], keys: List[str]) -> None:
        """Merge distribution data
        合并分布数据"""
        for key in keys:
            if key in results[0]:
                plt.figure(figsize=(10, 6))
                for i, result in enumerate(results):
                    plt.hist(
                        result[key], 
                        alpha=0.3, 
                        label=f'Run {i}',
                        density=True
                    )
                plt.title(f'{key} Distribution')
                plt.legend()
                plt.savefig(self.save_dir / f"{key}_distribution.png")
                plt.close()

    def _merge_text(self, results: List[dict], keys: List[str]) -> None:
        """Merge text data
        合并文本数据"""
        for key in keys:
            if key in results[0]:
                # Save all texts
                # 保存所有文本
                with open(self.save_dir / f"{key}_all.txt", 'w') as f:
                    for i, result in enumerate(results):
                        f.write(f"=== Run {i} ===\n")
                        f.write(result[key])
                        f.write("\n\n")

    def _merge_models(self, results: List[dict], keys: List[str]) -> None:
        """Merge model data
        合并模型数据"""
        for key in keys:
            if key in results[0]:
                model_dir = self.save_dir / f"{key}_models"
                model_dir.mkdir(exist_ok=True)
                
                for i, result in enumerate(results):
                    with open(model_dir / f"model_{i}.pkl", 'wb') as f:
                        pickle.dump(result[key], f)

def _serialize_result(result: Any) -> Any:
    """Serialize results for multiprocessing
    序列化结果用于多进程"""
    if isinstance(result, dict):
        return {k: _serialize_result(v) for k, v in result.items()}
    elif isinstance(result, list):
        return [_serialize_result(x) for x in result]
    elif isinstance(result, np.ndarray):
        return result.tolist()
    elif isinstance(result, (np.integer, np.floating)):
        return float(result)
    elif isinstance(result, pd.DataFrame):
        return result.to_dict()
    elif isinstance(result, pd.Series):
        return result.to_list()
    elif hasattr(result, 'to_dict'):
        return result.to_dict()
    return result
def _run_single_experiment(serialized_func, experiment_name, run_index, times, args, kwargs):
    """Top-level function executed in a process
    在进程中执行的顶层函数"""
    try:
        # Deserialize the function
        # 反序列化函数
        func = cloudpickle.loads(serialized_func)
        # Create a tracker
        # 创建追踪器
        tracker = ExperimentTracker(experiment_name)
        tracker.log_params({
            "run_index": run_index,
            "total_runs": times,
            "parallel": True,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        })
        result = func(tracker, *args, **kwargs)
        # 返回结果和 run_id
        serialized_result = _serialize_result(result)
        return serialized_result, tracker.run_id
    except Exception as e:
        logging.error(f"Run {run_index + 1}/{times} failed: {str(e)}")
        raise

def experiment_manager(
    times: int = 1,
    experiment_name: Optional[str] = None,
    parallel: bool = False,
    max_workers: Optional[int] = None,
    merge_config: Optional[Dict] = None,
    system_info_level: str = 'basic',  # 改为 level 参数: 'none', 'basic', 'full'
    print_style: str = 'auto'  # 添加打印样式参数: 'auto', 'rich', 'simple', 'markdown'
):
    """
    实验重复执行装饰器
    
    Args:
        times: 重复次数
        experiment_name: 实验名称
        parallel: 是否并行执行
        max_workers: 最大工作进程数
        merge_config: 结果合并配置
        system_info_level: 系统信息详细程度
            - 'none': 只返回基本实验配置
            - 'basic': 返回运筹学论文常用的关键信息（默认）
            - 'full': 返回所有可获取的系统信息
        print_style: 系统信息打印样式
            - 'auto': 自动选择最佳样式（默认）
            - 'rich': 使用rich库的完整样式
            - 'simple': 简单文本样式
            - 'markdown': Markdown表格样式
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            with _experiment_semaphore:
                nonlocal experiment_name
                logging.info(f"Starting Experiment: {experiment_name}")
                if experiment_name is None:
                    experiment_name = func.__name__

                # 收集系统信息
                system_info = get_system_info(
                    experiment_name=experiment_name,
                    parallel=parallel,
                    times=times,
                    max_workers=max_workers,
                    level=system_info_level  # 使用新的 level 参数
                )
                
                # 打印系统信息
                print_system_info(
                    system_info,
                    style=print_style  # 使用指定的打印样式
                )

                results = []
                run_ids = []  # 收集实际的运行ID

                if parallel:
                    # Serialize the function
                    # 序列化函数
                    serialized_func = cloudpickle.dumps(func)
                    
                    # Create processes using the spawn method
                    # 使用 spawn 方法创建进程
                    ctx = mp.get_context('spawn')
                    with ProcessPoolExecutor(
                        max_workers=max_workers,
                        mp_context=ctx
                    ) as executor:
                        futures = []
                        with tqdm(total=times, desc=f"Running {experiment_name}") as pbar:
                            for i in range(times):
                                future = executor.submit(
                                    _run_single_experiment,
                                    serialized_func,
                                    experiment_name,
                                    i,
                                    times,
                                    args,
                                    kwargs
                                )
                                futures.append(future)
                            
                            for future in as_completed(futures):
                                try:
                                    result, run_id = future.result()  # 修改：解包结果和ID
                                    results.append(result)
                                    run_ids.append(run_id)  # 保存ID
                                except Exception as e:
                                    logging.error(f"Run failed with error: {e}")
                else:
                    # Serial execution remains unchanged
                    # 串行执行保持不变
                    for i in tqdm(range(times), desc=f"Running {experiment_name}"):
                        tracker = ExperimentTracker(experiment_name)
                        tracker.log_params({
                            "run_index": i,
                            "total_runs": times,
                            "parallel": False,
                            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
                        })
                        try:
                            result, run_id = future.result()  # 获取结果和ID
                            results.append(result)
                            run_ids.append(run_id)  # 保存ID
                        except Exception as e:
                            logging.error(f"Run {i} failed with error: {e}")
                if merge_config and results:
                    merger = ResultsMerger(
                        experiment_name=experiment_name,
                        base_dir="./orruns_experiments",
                        run_ids=run_ids  # 传入实际的运行ID列表
                    )
                    merger.merge_results(results, merge_config)      
                logging.info(f"\n=== Completed Experiment: {experiment_name} ===\n")      
                return results
        return wrapper
    return decorator