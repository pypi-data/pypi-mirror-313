from pathlib import Path
from typer.testing import CliRunner

from infra_sdk.cli import app

runner = CliRunner()

def test_create_command():
    """Test the create command with our example S3 bucket module."""
    module_path = Path(__file__).parent.parent / "examples" / "s3_bucket"
    
    # Test without auto-approve (should show confirmation prompt)
    result = runner.invoke(app, ["create", str(module_path)])
    assert result.exit_code == 0
    
    # Test with auto-approve
    result = runner.invoke(app, ["create", str(module_path), "--auto-approve"])
    assert result.exit_code == 0
