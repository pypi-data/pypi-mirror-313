import pytest
from click.testing import CliRunner
from orruns.cli.commands import cli
from orruns.tracker import ExperimentTracker
from orruns.core.config import Config

@pytest.fixture
def test_data_dir(tmp_path):
    """Create a temporary data directory for testing"""
    data_dir = tmp_path / "test_experiments"
    data_dir.mkdir()
    # Set the data directory in config
    config = Config.get_instance()
    config.set_data_dir(str(data_dir))
    return data_dir

@pytest.fixture
def sample_experiment(test_data_dir):
    """Create a sample experiment for testing"""
    tracker = ExperimentTracker("test_exp")
    tracker.log_params({"learning_rate": 0.01, "batch_size": 32})
    tracker.log_metrics({"accuracy": 0.95, "loss": 0.1})
    return {
        "name": "test_exp",
        "run_id": tracker.run_id
    }

def test_list_experiments_command(test_data_dir, sample_experiment):
    """Test the list_experiments CLI command"""
    runner = CliRunner()
    result = runner.invoke(cli, ['list-experiments'])
    assert result.exit_code == 0
    assert "test_exp" in result.output

def test_get_experiment_command(test_data_dir, sample_experiment):
    """Test the get_experiment CLI command"""
    runner = CliRunner()
    result = runner.invoke(cli, ['get-experiment', 'test_exp'])
    assert result.exit_code == 0
    assert "test_exp" in result.output
    assert "learning_rate" in result.output
    assert "accuracy" in result.output

def test_delete_experiment_command(test_data_dir, sample_experiment):
    """Test the delete_experiment CLI command"""
    runner = CliRunner()
    result = runner.invoke(cli, ['delete-experiment', 'test_exp', '--run-id', sample_experiment["run_id"]])
    assert result.exit_code == 0
    assert "Deleted" in result.output

    # Verify experiment directory is gone
    exp_dir = test_data_dir / "test_exp"
    assert not exp_dir.exists()

def test_compare_experiments_command(test_data_dir):
    """Test the compare_experiments CLI command"""
    # Create two experiments for comparison
    exp1 = ExperimentTracker("exp1")
    exp1.log_metrics({"accuracy": 0.95, "loss": 0.1})
    
    exp2 = ExperimentTracker("exp2")
    exp2.log_metrics({"accuracy": 0.90, "loss": 0.2})
    
    runner = CliRunner()
    result = runner.invoke(cli, ['compare-experiments', 'exp1', 'exp2'])
    assert result.exit_code == 0
    assert "exp1" in result.output
    assert "exp2" in result.output
    assert "accuracy" in result.output

def test_export_dataframe_command(test_data_dir, sample_experiment, tmp_path):
    """Test the export_dataframe CLI command"""
    runner = CliRunner()
    output_file = tmp_path / "output.csv"
    result = runner.invoke(cli, ['export-dataframe', 'test_exp', '--output', str(output_file)])
    assert result.exit_code == 0
    assert output_file.exists()

def test_export_artifacts_command(test_data_dir, sample_experiment, tmp_path):
    """Test the export_artifacts CLI command"""
    runner = CliRunner()
    output_dir = tmp_path / "artifacts"
    result = runner.invoke(cli, ['export-artifacts', 'test_exp', sample_experiment["run_id"], '--output-dir', str(output_dir)])
    assert result.exit_code == 0
    assert output_dir.exists()

def test_clean_old_command(test_data_dir, sample_experiment):
    """Test the clean_old CLI command"""
    runner = CliRunner()
    result = runner.invoke(cli, ['clean-old', '--days', '0'])
    assert result.exit_code == 0
    assert "Deleted" in result.output

@pytest.fixture(autouse=True)
def cleanup():
    """Cleanup after each test"""
    yield
    # Reset the Config singleton
    Config._instance = None