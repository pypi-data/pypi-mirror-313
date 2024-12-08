import plotly.graph_objs as go
import plotly.express as px
from typing import Dict, List, Any
import pandas as pd
import numpy as np

class PlotManager:
    def __init__(self):
        # Set default plot theme and colors
        # 设置默认的绘图主题和颜色
        self.theme = 'plotly_dark'
        self.colors = px.colors.qualitative.Set3
        
        # Add default layout configuration
        # 添加默认的布局配置
        self.default_layout = dict(
            template=self.theme,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0.02)',
            margin=dict(l=20, r=20, t=40, b=20),
            hoverlabel=dict(
                bgcolor="white",
                font_size=12,
                font_family="Roboto"
            ),
            font=dict(
                color='rgb(50, 50, 50)'  # Dark gray text
                # 深灰色文字
            ),
            xaxis=dict(
                title_font=dict(color='rgb(50, 50, 50)'),
                tickfont=dict(color='rgb(50, 50, 50)'),
                gridcolor='rgba(128, 128, 128, 0.2)',
                showgrid=True,
                gridwidth=1
            ),
            yaxis=dict(
                title_font=dict(color='rgb(50, 50, 50)'),
                tickfont=dict(color='rgb(50, 50, 50)'),
                gridcolor='rgba(128, 128, 128, 0.2)',
                showgrid=True,
                gridwidth=1
            ),
            legend=dict(
                font=dict(color='rgb(50, 50, 50)'),
                bgcolor="rgba(255, 255, 255, 0.1)",
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01
            )
        )

    def create_box_plot(self, data: pd.DataFrame, metric: str, title: str = None) -> go.Figure:
        """Create basic box plot
        创建基本箱型图
        """
        fig = go.Figure()
        fig.add_trace(go.Box(
            y=data['value'],
            name=metric,
            boxpoints='all',
            jitter=0.3,
            pointpos=-1.8,
            marker=dict(
                color=self.colors[0],
                size=6
            ),
            line=dict(color=self.colors[0])
        ))
        
        layout = self.default_layout.copy()
        layout.update(
            title=dict(
                text=title or f'{metric} Distribution',
                font=dict(color='rgb(50, 50, 50)')
            ),
            yaxis_title=metric
        )
        fig.update_layout(layout)
        return fig

    def create_grouped_box_plot(self, data: pd.DataFrame, value_col: str, group_col: str, metric: str, title: str = None) -> go.Figure:
        """Create grouped box plot
        创建分组箱型图
        """
        fig = go.Figure()
        colors = px.colors.qualitative.Set3
        
        for i, group in enumerate(sorted(data[group_col].unique())):
            group_data = data[data[group_col] == group]
            fig.add_trace(go.Box(
                y=group_data[value_col],
                name=f"s={group}",
                boxpoints='all',
                jitter=0.3,
                pointpos=-1.8,
                marker=dict(
                    color=colors[i],
                    size=6,
                    opacity=0.7
                ),
                line=dict(color=colors[i], width=2),
                boxmean=True
            ))
        
        layout = self.default_layout.copy()
        layout.update(
            title=dict(
                text=title or f'{metric} Distribution by Parameters',
                font=dict(color='rgb(50, 50, 50)')
            ),
            yaxis_title=metric,
            xaxis_title='Parameter Values'
        )
        fig.update_layout(layout)
        return fig

    def create_line_plot(self, data: List[Dict], metric: str, title: str = None) -> go.Figure:
        """Create basic line plot
        创建基本折线图
        """
        fig = go.Figure()
        
        for i, run_data in enumerate(data):
            fig.add_trace(go.Scatter(
                x=run_data['steps'],
                y=run_data['values'],
                name=f"Run {run_data['run'][-8:]}",
                mode='lines',
                line=dict(
                    color=self.colors[i % len(self.colors)],
                    width=2
                ),
                opacity=0.7
            ))
        
        layout = self.default_layout.copy()
        layout.update(
            title=dict(
                text=title or f'{metric} Convergence',
                font=dict(color='rgb(50, 50, 50)')
            ),
            xaxis_title='Step',
            yaxis_title=metric,
            hovermode='x unified'
        )
        fig.update_layout(layout)
        return fig

    def create_grouped_line_plot(self, data: List[Dict], metric: str, title: str = None) -> go.Figure:
        """Create grouped line plot
        创建分组折线图
        """
        fig = go.Figure()
        
        colors = (
            px.colors.qualitative.Set3 +   # 12 colors
            # 12种颜色
            px.colors.qualitative.Set1 +   # 9 colors
            # 9种颜色
            px.colors.qualitative.Pastel1  # 9 colors
            # 9种颜色
        )

        # Group by parameters
        # 按参数分组
        grouped_data = {}
        for run_data in data:
            param_group = run_data['params'].split('=')[1]
            if param_group not in grouped_data:
                grouped_data[param_group] = []
            grouped_data[param_group].append(run_data)
        
        for i, (param_group, group_data) in enumerate(sorted(grouped_data.items())):
            color = colors[i % len(colors)]  # Use modulo operation to ensure index does not exceed range
            # 使用取模运算确保不会超出索引范围
            if isinstance(color, str) and color.startswith('rgb'):
                fill_color = color.replace('rgb', 'rgba').replace(')', ',0.2)')
            else:
                fill_color = f'rgba(0,0,0,0.2)'
            
            steps = group_data[0]['steps']
            values_array = np.array([run_data['values'] for run_data in group_data])
            mean_values = np.mean(values_array, axis=0)
            std_values = np.std(values_array, axis=0)
            
            fig.add_trace(go.Scatter(
                x=steps,
                y=mean_values,
                name=f"s={param_group} (mean)",
                mode='lines',
                line=dict(color=color, width=2),
                legendgroup=param_group
            ))
            
            fig.add_trace(go.Scatter(
                x=steps + steps[::-1],
                y=np.concatenate([mean_values + std_values, (mean_values - std_values)[::-1]]),
                fill='toself',
                fillcolor=fill_color,
                line=dict(color='rgba(255,255,255,0)'),
                name=f"s={param_group} (std)",
                showlegend=False,
                legendgroup=param_group
            ))
        
        layout = self.default_layout.copy()
        layout.update(
            title=dict(
                text=title or f'{metric} Convergence by Parameters',
                font=dict(color='rgb(50, 50, 50)')
            ),
            xaxis_title='Step',
            yaxis_title=metric,
            hovermode='x unified'
        )
        fig.update_layout(layout)
        return fig

    def create_parallel_coordinates(self, data: pd.DataFrame, params: List[str], metric: str) -> go.Figure:
        """Create parallel coordinates plot
        创建平行坐标图
        """
        fig = px.parallel_coordinates(
            data,
            dimensions=params + [metric],
            color=metric,
            color_continuous_scale=px.colors.sequential.Viridis
        )
        
        layout = self.default_layout.copy()
        layout.update(
            title=dict(
                text='Parameter-Metric Relationships',
                font=dict(color='rgb(50, 50, 50)')
            )
        )
        fig.update_layout(layout)
        return fig

    def create_scatter_matrix(self, data: pd.DataFrame, params: List[str], metric: str) -> go.Figure:
        """Create scatter matrix plot
        创建散点矩阵图
        """
        dimensions = params + [metric]
        fig = px.scatter_matrix(
            data,
            dimensions=dimensions,
            color=metric,
            color_continuous_scale=px.colors.sequential.Viridis
        )
        
        layout = self.default_layout.copy()
        layout.update(
            title=dict(
                text='Parameter Relationships Matrix',
                font=dict(color='rgb(50, 50, 50)')
            )
        )
        fig.update_layout(layout)
        return fig