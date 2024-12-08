import dash
from dash import html, dcc, Input, Output, State, callback_context, ALL
import dash_bootstrap_components as dbc
from pathlib import Path
import json
import pandas as pd
from typing import Dict, List, Any
from .plots import PlotManager
import plotly.graph_objs as go  # Add this line / 添加这行
import flask
class ExperimentDashboard:
    def __init__(self, base_dir="./orruns_experiments"):
        self.base_dir = Path(base_dir)
        self.app = dash.Dash(
            __name__,
            external_stylesheets=[
                dbc.themes.BOOTSTRAP,
                'https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500&display=swap'
            ],
            suppress_callback_exceptions=True
        )
                
        @self.app.server.route('/artifacts/<path:path>')
        def serve_artifacts(path):
            try:
                # Decompose the path / 分解路径
                parts = path.split('/')
                if len(parts) >= 3:  # experiment/run_id/figures|data/filename
                    exp_name = parts[0]
                    run_id = parts[1]
                    file_type = parts[2]  # 'figures' or 'data'
                    
                    # Construct the full path / 构建完整路径
                    file_path = '/'.join(parts[3:]) if len(parts) > 3 else ''
                    full_path = self.base_dir / exp_name / run_id / 'artifacts' / file_type / file_path
                    
                    print(f"Attempting to serve file: {full_path}")  # Debug log / 调试日志
                    
                    if not full_path.exists():
                        print(f"File not found: {full_path}")
                        return flask.abort(404)
                    
                    # Add MIME type detection / 添加 MIME 类型检测
                    mimetype = None
                    if full_path.suffix.lower() in ['.png', '.jpg', '.jpeg']:
                        mimetype = f'image/{full_path.suffix[1:].lower()}'
                    elif full_path.suffix.lower() == '.csv':
                        mimetype = 'text/csv'
                    
                    return flask.send_file(
                        str(full_path),
                        mimetype=mimetype,
                        as_attachment=False
                    )
                return flask.abort(404)
            except Exception as e:
                print(f"Error serving file {path}: {e}")
                return flask.abort(404)
        
        self.plot_manager = PlotManager()
        self.setup_layout()
        self.setup_callbacks()
        
    def setup_layout(self):
        self.app.layout = dbc.Container([
            # Navbar / 导航栏
            dbc.Navbar([
                dbc.Container([
                    html.A(
                        dbc.Row([
                            dbc.Col(html.H1("ORruns Dashboard", className="nav-title")),
                        ]),
                        href="/",
                        style={"textDecoration": "none"}
                    ),
                    dbc.Row([
                        dbc.Col([
                            dbc.Button("Dark Mode", id="theme-toggle", color="light", className="me-2"),
                            dbc.Button("Export Data", id="export-button", color="success"),
                        ])
                    ])
                ])
            ], color="dark", dark=True, className="mb-4"),

            # Main content area / 主内容区
            dbc.Row([
                # Left sidebar / 左侧边栏
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H4("Experiments"),
                            dcc.Dropdown(id='experiment-dropdown', className="mb-3"),
                            html.H4("Parameters"),
                            html.Div(id='param-filters', className="mb-3"),
                            html.H4("Metrics"),
                            dcc.Dropdown(id='metric-dropdown', className="mb-3"),
                            html.H4("Filters"),
                            dcc.Checklist(id='run-filters', className="mb-3"),
                            dbc.Button("Refresh", id="refresh-button", color="primary", className="w-100")
                        ])
                    ])
                ], width=3),

                # Main content area / 主要内容区
                dbc.Col([
                    # Overview cards / 概览卡片
                    dbc.Row([
                        dbc.Col(dbc.Card([
                            dbc.CardBody([
                                html.H4("Total Runs"),
                                html.H2(id="total-runs")
                            ])
                        ]), width=4),
                        dbc.Col(dbc.Card([
                            dbc.CardBody([
                                html.H4("Best Performance"),
                                html.H2(id="best-performance")
                            ])
                        ]), width=4),
                        dbc.Col(dbc.Card([
                            dbc.CardBody([
                                html.H4("Latest Run"),
                                html.H2(id="latest-run")
                            ])
                        ]), width=4),
                    ], className="mb-4"),

                    # Chart area / 图表区域
                    dbc.Card([
                        dbc.CardBody([
                            dbc.Row([
                                dbc.Col(dcc.Graph(id='metric-plot'), width=6),
                                dbc.Col(dcc.Graph(id='convergence-plot'), width=6),
                            ])
                        ])
                    ], className="mb-4"),

                    # Detailed information tabs / 详细信息标签页
                    dbc.Tabs([
                        dbc.Tab([
                            html.Div(id='statistics-table')
                        ], label="Statistics"),
                        dbc.Tab([
                            html.Div(id='params-table')
                        ], label="Parameters"),
                        dbc.Tab([
                            html.Div(id='artifacts-list')
                        ], label="Artifacts"),
                    ])
                ], width=9)
            ])
        ], fluid=True)

    def setup_callbacks(self):
        @self.app.callback(
            [Output('experiment-dropdown', 'options'),
             Output('experiment-dropdown', 'value')],
            [Input('refresh-button', 'n_clicks')]
        )
        def update_experiment_options(_):
            experiments = [d.name for d in self.base_dir.iterdir() if d.is_dir()]
            options = [{'label': exp, 'value': exp} for exp in experiments]
            return options, options[0]['value'] if options else None

        @self.app.callback(
            [Output('metric-dropdown', 'options'),
             Output('metric-dropdown', 'value')],
            [Input('experiment-dropdown', 'value')]
        )
        def update_metric_options(experiment):
            if not experiment:
                return [], None
            
            metrics = set()
            exp_dir = self.base_dir / experiment
            for run_dir in exp_dir.iterdir():
                if run_dir.is_dir():
                    metrics_file = run_dir / 'metrics' / 'metrics.json'
                    if metrics_file.exists():
                        with open(metrics_file, 'r') as f:
                            run_metrics = json.load(f)
                            metrics.update(run_metrics.keys())
            
            options = [{'label': metric, 'value': metric} for metric in metrics]
            return options, options[0]['value'] if options else None

        @self.app.callback(
            Output('param-filters', 'children'),
            [Input('experiment-dropdown', 'value')]
        )
        def update_param_filters(experiment):
            if not experiment:
                return []
            
            # Collect all parameters and their unique values / 收集所有参数及其唯一值
            param_values = {}
            exp_dir = self.base_dir / experiment
            for run_dir in exp_dir.iterdir():
                if run_dir.is_dir():
                    params_file = run_dir / 'params' / 'params.json'
                    if params_file.exists():
                        with open(params_file, 'r') as f:
                            params = json.load(f)
                            for k, v in params.items():
                                if k not in param_values:
                                    param_values[k] = set()
                                param_values[k].add(str(v))
            
            # Create parameter selector and filter container / 创建参数选择器和过滤器容器
            return [
                # Parameter selection dropdown / 参数选择下拉框
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Select Parameters"),
                        dcc.Dropdown(
                            id='param-selector',
                            options=[{'label': param, 'value': param} for param in sorted(param_values.keys())],
                            value=[],
                            multi=True,
                            className="mb-3"
                        ),
                        # Parameter filter container / 参数过滤器容器
                        html.Div(id='param-filters-container', className="mt-3")
                    ])
                ], className="mb-3")
            ]

        @self.app.callback(
            Output('param-filters-container', 'children'),
            [Input('param-selector', 'value'),
             Input('experiment-dropdown', 'value')]
        )
        def update_selected_param_filters(selected_params, experiment):
            if not experiment or not selected_params:
                return []
            
            # Create filters only for selected parameters / 只为选中的参数创建过滤器
            param_values = {}
            exp_dir = self.base_dir / experiment
            for run_dir in exp_dir.iterdir():
                if run_dir.is_dir():
                    params_file = run_dir / 'params' / 'params.json'
                    if params_file.exists():
                        with open(params_file, 'r') as f:
                            params = json.load(f)
                            for k, v in params.items():
                                if k in selected_params:
                                    if k not in param_values:
                                        param_values[k] = set()
                                    param_values[k].add(str(v))
            
            # Create filters for selected parameters / 为选中的参数创建过滤器
            return [
                html.Div([
                    html.Label(param),
                    dcc.Checklist(
                        id={'type': 'param-filter', 'param': param},
                        options=[{'label': v, 'value': v} for v in sorted(param_values[param])],
                        value=[],
                        className="mb-2"
                    )
                ]) for param in selected_params
            ]

        @self.app.callback(
            [Output('metric-plot', 'figure'),
             Output('convergence-plot', 'figure'),
             Output('statistics-table', 'children'),
             Output('total-runs', 'children'),
             Output('best-performance', 'children'),
             Output('latest-run', 'children')],
            [Input('experiment-dropdown', 'value'),
             Input('metric-dropdown', 'value'),
             Input('param-selector', 'value'),
             Input({'type': 'param-filter', 'param': ALL}, 'value')]
        )
        def update_dashboard(experiment, metric, selected_params, param_filters):
            if not experiment or not metric:
                return {}, {}, [], "N/A", "N/A", "N/A"
            
            ctx = callback_context
            if not ctx.triggered:
                return {}, {}, [], "N/A", "N/A", "N/A"
            
            # Get parameter filter conditions / 获取参数过滤条件
            param_filter_dict = {}
            if param_filters:
                for i, param_values in enumerate(param_filters):
                    if param_values:  # If there are selected values / 如果有选中的值
                        param_name = ctx.inputs_list[3][i]['id']['param']
                        param_filter_dict[param_name] = param_values

            # Collect data / 收集数据
            box_data = []
            convergence_data = []
            exp_dir = self.base_dir / experiment
            runs = [d for d in exp_dir.iterdir() if d.is_dir()]
            
            for run_dir in runs:
                if not run_dir.is_dir():
                    continue
                
                # Read parameter file / 读取参数文件
                params = {}
                params_file = run_dir / 'params' / 'params.json'
                if params_file.exists():
                    with open(params_file, 'r') as f:
                        params = json.load(f)
                        
                    # Check if it meets the filter conditions / 检查是否满足过滤条件
                    if param_filter_dict:
                        match = True
                        for param_name, filter_values in param_filter_dict.items():
                            if str(params.get(param_name)) not in filter_values:
                                match = False
                                break
                        if not match:
                            continue
                
                # Construct parameter information string / 构建参数信息字符串
                if params and selected_params:
                    param_info = '_'.join(f"{k}={v}" for k, v in params.items() 
                                        if k in selected_params)
                else:
                    param_info = "no_params"
                    
                # Read metric data / 读取指标数据
                metrics_file = run_dir / 'metrics' / 'metrics.json'
                if metrics_file.exists():
                    with open(metrics_file, 'r') as f:
                        run_metrics = json.load(f)
                        if metric in run_metrics:
                            metric_data = run_metrics[metric]
                            
                            if isinstance(metric_data, dict) and 'steps' in metric_data:
                                convergence_data.append({
                                    'run': run_dir.name,
                                    'params': param_info,
                                    'steps': metric_data['steps'],
                                    'values': metric_data['values']
                                })
                                box_data.append({
                                    'run': run_dir.name,
                                    'params': param_info,
                                    'value': metric_data['values'][-1]
                                })
                            else:
                                box_data.append({
                                    'run': run_dir.name,
                                    'params': param_info,
                                    'value': metric_data
                                })

            # Create charts / 创建图表
            box_df = pd.DataFrame(box_data)
            if not box_df.empty:
                if len(box_df['params'].unique()) > 1:  # If there are multiple parameter groups / 如果有多个参数组
                    box_fig = self.plot_manager.create_grouped_box_plot(
                        box_df, 
                        'value',
                        'params',
                        metric, 
                        f'{metric} Distribution by Parameters'
                    )
                    
                    conv_fig = self.plot_manager.create_grouped_line_plot(
                        convergence_data,
                        metric,
                        f'{metric} Convergence Curves by Parameters'
                    )
                else:  # Single parameter group or no parameters / 单个参数组或无参数
                    box_fig = self.plot_manager.create_box_plot(
                        box_df, 
                        metric, 
                        f'{metric} Distribution'
                    )
                    
                    conv_fig = self.plot_manager.create_line_plot(
                        convergence_data,
                        metric,
                        f'{metric} Convergence Curves'
                    )
            else:
                # Create empty charts / 创建空图表
                box_fig = go.Figure()
                conv_fig = go.Figure()

            # Calculate statistics / 计算统计信息
            if not box_df.empty:
                stats = box_df['value'].describe()
                stats_table = dbc.Table([
                    html.Thead([
                        html.Tr([html.Th("Statistic"), html.Th("Value")])
                    ]),
                    html.Tbody([
                        html.Tr([html.Td(k), html.Td(f"{v:.4f}")]) 
                        for k, v in stats.items()
                    ])
                ], striped=True, bordered=True, hover=True)

                total_runs = len(runs)
                best_value = box_df['value'].min()
                latest_run = max(runs, key=lambda x: x.stat().st_mtime).name
            else:
                stats_table = html.P("No data available")
                total_runs = 0
                best_value = "N/A"
                latest_run = "N/A"

            return box_fig, conv_fig, stats_table, str(total_runs), str(best_value), latest_run[-8:]

        @self.app.callback(
            Output('params-table', 'children'),
            [Input('experiment-dropdown', 'value')]
        )
        def update_params_table(experiment):
            if not experiment:
                return []
            
            # Collect parameters of all runs / 收集所有运行的参数
            params_data = []
            exp_dir = self.base_dir / experiment
            for run_dir in exp_dir.iterdir():
                if run_dir.is_dir():
                    params_file = run_dir / 'params' / 'params.json'
                    if params_file.exists():
                        with open(params_file, 'r') as f:
                            params = json.load(f)
                            params['run_id'] = run_dir.name[-8:]  # Add run ID / 添加运行ID
                            params_data.append(params)
            
            if not params_data:
                return html.P("No parameters found")
            
            # Get all parameter names / 获取所有参数名
            param_names = set()
            for params in params_data:
                param_names.update(params.keys())
            param_names.discard('run_id')  # Remove run_id / 移除run_id
            
            # Create table / 创建表格
            return dbc.Table([
                html.Thead([
                    html.Tr([html.Th("Run")] + [html.Th(name) for name in sorted(param_names)])
                ]),
                html.Tbody([
                    html.Tr(
                        [html.Td(params.get('run_id', ''))] + 
                        [html.Td(str(params.get(name, ''))) for name in sorted(param_names)]
                    ) for params in params_data
                ])
            ], striped=True, bordered=True, hover=True)

        @self.app.callback(
            Output('artifacts-list', 'children'),
            [Input('experiment-dropdown', 'value')]
        )
        def update_artifacts(experiment):
            if not experiment:
                return []
            
            artifacts = []
            exp_dir = self.base_dir / experiment
            if not exp_dir.exists():
                return []

            for run_dir in exp_dir.iterdir():
                if run_dir.is_dir():
                    run_artifacts = []
                    artifacts_dir = run_dir / "artifacts"
                    
                    # Process figures directory / 处理figures目录
                    figures_dir = artifacts_dir / "figures"
                    if figures_dir.exists():
                        figure_items = []
                        for figure in figures_dir.glob("*"):
                            if figure.is_file():
                                # Modify to: / 修改为:
                                relative_path = f"{experiment}/{run_dir.name}/figures/{figure.name}"
                                figure_items.append(
                                    dbc.ListGroupItem([
                                        html.Div([
                                            html.Img(
                                                src=f"/{relative_path}",  # Removed artifacts / 移除了 artifacts
                                                style={'max-width': '100%', 'height': 'auto', 'margin': '10px 0'}
                                            ),
                                            html.Div(
                                                html.A(
                                                    figure.name,
                                                    href=f"/{relative_path}",  # Removed artifacts / 移除了 artifacts
                                                    target="_blank",
                                                    style={'margin-top': '5px'}
                                                )
                                            )
                                        ])
                                    ])
                                )
                        if figure_items:
                            run_artifacts.append(
                                dbc.Card([
                                    dbc.CardHeader("Figures"),
                                    dbc.ListGroup(figure_items, flush=True)
                                ], className="mb-3")
                            )
                    
                    # Process data directory / 处理data目录
                    data_dir = artifacts_dir / "data"
                    if data_dir.exists():
                        data_items = []
                        for data_file in data_dir.glob("*"):
                            if data_file.is_file():
                                relative_path = f"{experiment}/{run_dir.name}/data/{data_file.name}"
                                data_items.append(
                                    dbc.ListGroupItem(
                                        html.A(
                                            data_file.name,
                                            href=f"/artifacts/{relative_path}",
                                            target="_blank"
                                        )
                                    )
                                )
                        if data_items:
                            run_artifacts.append(
                                dbc.Card([
                                    dbc.CardHeader("Data"),
                                    dbc.ListGroup(data_items, flush=True)
                                ], className="mb-3")
                            )

                    if run_artifacts:
                        artifacts.append(
                            dbc.Card([
                                dbc.CardHeader(f"Run: {run_dir.name}"),
                                dbc.CardBody(run_artifacts)
                            ], className="mb-4")
                        )

            if not artifacts:
                return html.Div("No artifacts found", className="text-muted p-3")

            return dbc.Row([
                dbc.Col(artifact, width=12)
                for artifact in artifacts
            ])

    def run(self, port=8050):
        self.app.run_server(debug=True, port=port)