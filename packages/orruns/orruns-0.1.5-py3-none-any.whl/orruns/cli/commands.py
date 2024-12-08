import click
import sys
import json
from typing import List, Optional
from ..api.experiment import ExperimentAPI

@click.group()
def cli():
    """ORruns command line interface"""
    pass

@cli.command()
@click.option('--last', default=10, help='Number of most recent experiments to show')
@click.option('--pattern', help='Filter experiments by name pattern')
def list_experiments(last: int, pattern: Optional[str]):
    """List experiments with optional filtering"""
    api = ExperimentAPI()
    try:
        experiments = api.list_experiments(last=last, pattern=pattern)
        if not experiments:
            click.echo("No experiments found")
            return
        
        # Format output
        for exp in experiments:
            click.echo(f"\nExperiment: {exp['name']}")
            click.echo(f"Run ID: {exp['run_id']}")
            click.echo(f"Timestamp: {exp['timestamp']}")
            click.echo("Parameters:")
            click.echo(json.dumps(exp['parameters'], indent=2))
            click.echo("Metrics:")
            click.echo(json.dumps(exp['metrics'], indent=2))
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)

@cli.command()
@click.argument('experiment_name')
@click.option('--run-id', help='Specific run ID to get details for')
def get_experiment(experiment_name: str, run_id: Optional[str]):
    """Get details of an experiment or specific run"""
    api = ExperimentAPI()
    try:
        exp_data = api.get_experiment(experiment_name, run_id)
        if run_id:
            # Single run output
            click.echo(json.dumps(exp_data, indent=2))
        else:
            # Full experiment summary
            click.echo(f"\nExperiment: {exp_data['name']}")
            click.echo(f"Total Runs: {exp_data['total_runs']}")
            click.echo(f"Created: {exp_data['created_at']}")
            click.echo(f"Last Updated: {exp_data['last_updated']}")
            click.echo("\nLatest Parameters:")
            click.echo(json.dumps(exp_data['parameters'], indent=2))
            click.echo("\nLatest Metrics:")
            click.echo(json.dumps(exp_data['metrics'], indent=2))
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)

@cli.command()
@click.argument('experiment_name')
@click.option('--run-id', help='Specific run ID to delete')
def delete_experiment(experiment_name: str, run_id: Optional[str]):
    """Delete an experiment or specific run"""
    api = ExperimentAPI()
    try:
        api.delete_experiment(experiment_name, run_id)
        msg = f"Deleted run '{run_id}' from" if run_id else "Deleted"
        click.echo(f"{msg} experiment '{experiment_name}'")
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)

@cli.command()
@click.argument('experiment_names', nargs=-1, required=True)
@click.option('--metrics', help='Comma-separated list of metrics to compare')
def compare_experiments(experiment_names: List[str], metrics: Optional[str]):
    """Compare metrics across multiple experiments"""
    api = ExperimentAPI()
    try:
        metric_list = metrics.split(',') if metrics else None
        results = api.compare_experiments(list(experiment_names), metric_list)
        click.echo(json.dumps(results, indent=2))
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)

@cli.command()
@click.argument('experiment_name')
@click.option('--output', required=True, help='Output CSV file path')
@click.option('--metrics', help='Comma-separated list of metrics to export')
def export_dataframe(experiment_name: str, output: str, metrics: Optional[str]):
    """Export experiment runs to CSV"""
    api = ExperimentAPI()
    try:
        metric_list = metrics.split(',') if metrics else None
        df = api.export_to_dataframe(experiment_name, metric_list)
        df.to_csv(output, index=False)
        click.echo(f"Exported data to {output}")
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)

@cli.command()
@click.argument('experiment_name')
@click.argument('run_id')
@click.option('--output-dir', required=True, help='Directory to export artifacts to')
@click.option('--types', help='Comma-separated list of artifact types to export')
def export_artifacts(experiment_name: str, run_id: str, output_dir: str, types: Optional[str]):
    """Export artifacts to directory"""
    api = ExperimentAPI()
    try:
        type_list = types.split(',') if types else None
        exported = api.export_artifacts(experiment_name, run_id, output_dir, type_list)
        click.echo("Exported artifacts:")
        click.echo(json.dumps(exported, indent=2))
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)

@cli.command()
@click.option('--days', default=30, help='Delete experiments older than this many days')
def clean_old(days: int):
    """Clean up old experiments"""
    api = ExperimentAPI()
    try:
        deleted = api.clean_old_experiments(days)
        if deleted:
            click.echo(f"Deleted {len(deleted)} experiments:")
            for exp in deleted:
                click.echo(f"- {exp}")
        else:
            click.echo("No experiments were old enough to delete")
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)

if __name__ == '__main__':
    cli()