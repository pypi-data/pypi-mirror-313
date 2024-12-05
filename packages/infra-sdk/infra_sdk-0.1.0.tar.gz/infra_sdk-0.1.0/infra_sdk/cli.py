import subprocess
from datetime import datetime
from pathlib import Path
from typing import List, Optional

import beaupy
import rich
import typer
from rich.console import Console
from rich.table import Table

from infra_sdk.config import Config, find_config, load_config, save_config
from infra_sdk.state import StateManager

app = typer.Typer(help="Infrastructure management CLI using OpenTofu")
console = Console()

# Path to OpenTofu binary
TOFU_BINARY = str(Path.home() / ".launchflow/bin/tofu")

# Global state manager instance
state_manager: Optional[StateManager] = None


def get_state_manager() -> StateManager:
    """Get or initialize the state manager."""
    global state_manager
    if state_manager is None:
        config_path = find_config()
        if not config_path:
            # No config found, run init flow
            init()
            config_path = find_config()
            if not config_path:
                console.print("[red]Failed to initialize config[/]")
                raise typer.Exit(1)
        
        config = load_config(config_path)
        state_manager = StateManager(config)
    return state_manager


@app.command()
def init() -> None:
    """Initialize a new infra project."""
    # Check if we're already in a project
    existing_config = find_config()
    if existing_config:
        console.print(f"[yellow]Project already initialized at {existing_config}[/]")
        raise typer.Exit(1)
    
    # Get state path
    console.print("\nWhere would you like to store the infrastructure state?")
    console.print("[dim]Press Enter to use default (./.infra)[/]")
    state_path = beaupy.prompt("State path:") or ".infra"
    
    # Create config
    config = Config(state_path=Path(state_path))
    config_path = Path.cwd() / "infra.yaml"
    
    # Save config
    save_config(config, config_path)
    console.print(f"\n[green]Initialized project at {config_path}[/]")
    console.print(f"State will be stored at: {config.state_path}")


def _select_environment(create_if_missing: bool = True) -> Optional[str]:
    """Prompt user to select an environment."""
    environments = get_state_manager().get_environments()
    
    if not environments and not create_if_missing:
        console.print("[yellow]No environments found.[/yellow]")
        return None
    
    if not environments:
        if not beaupy.confirm("No environments found. Create one now?"):
            return None
        
        name = beaupy.prompt("Enter environment name:")
        if not name:
            return None
        
        description = beaupy.prompt("Enter environment description (optional):")
        get_state_manager().create_environment(name, description or None)
        return name
    
    env_choices = [
        f"{env.name} - {env.description or 'No description'} (Created: {env.created_at.strftime('%Y-%m-%d')})"
        for env in environments
    ]
    
    console.print("\nSelect an environment:")
    selected = beaupy.select(
        options=[env.name for env in environments],  # Just show environment names
        cursor_style="cyan",
    )
    
    if selected is None:
        return None
    
    return selected  # Return the selected environment name directly

def _run_tofu_command(args: list[str], cwd: Path, state_file: Optional[Path] = None) -> None:
    """Run an OpenTofu command with the given arguments."""
    try:
        command = [TOFU_BINARY] + args
        if state_file:
            command.extend(["-state", str(state_file)])
        
        # Run command interactively
        result = subprocess.run(
            command,
            cwd=cwd,
            check=True,
        )
            
    except subprocess.CalledProcessError as e:
        raise typer.Exit(1)
    except FileNotFoundError:
        console.print(f"[red]OpenTofu binary not found at {TOFU_BINARY}[/]")
        console.print("[yellow]Please ensure OpenTofu is installed and the path is correct[/]")
        raise typer.Exit(1)

@app.callback()
def callback():
    """Infrastructure management CLI using OpenTofu."""

@app.command()
def env():
    """Environment management commands."""
    app_env = typer.Typer(help="Environment management commands")
    
    @app_env.command()
    def create(
        name: str = typer.Argument(..., help="Environment name"),
        description: Optional[str] = typer.Option(None, help="Environment description"),
    ):
        """Create a new environment."""
        try:
            env = get_state_manager().create_environment(name, description)
            console.print(f"[green]Created environment: {env.name}[/green]")
        except ValueError as e:
            console.print(f"[red]Error: {e}[/red]")
            raise typer.Exit(code=1)
    
    @app_env.command()
    def list():
        """List all environments."""
        environments = get_state_manager().get_environments()
        
        if not environments:
            console.print("[yellow]No environments found.[/yellow]")
            return
        
        table = Table(title="Environments")
        table.add_column("Name", style="cyan")
        table.add_column("Description", style="green")
        table.add_column("Created", style="blue")
        table.add_column("Modules", style="magenta")
        
        for env in environments:
            table.add_row(
                env.name,
                env.description or "",
                env.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                str(len(env.modules)),
            )
        
        console.print(table)
    
    @app_env.command()
    def update(
        name: str = typer.Argument(..., help="Environment name"),
        new_name: Optional[str] = typer.Option(None, help="New environment name"),
        new_description: Optional[str] = typer.Option(None, help="New environment description"),
    ):
        """Update an environment."""
        try:
            env = get_state_manager().update_environment(name, new_name, new_description)
            if env:
                console.print(f"[green]Updated environment: {env.name}[/green]")
            else:
                console.print(f"[red]Environment '{name}' not found[/red]")
                raise typer.Exit(code=1)
        except ValueError as e:
            console.print(f"[red]Error: {e}[/red]")
            raise typer.Exit(code=1)
    
    @app_env.command()
    def delete(
        name: str = typer.Argument(..., help="Environment name"),
        force: bool = typer.Option(
            False,
            "--force",
            "-f",
            help="Skip confirmation",
        ),
    ):
        """Delete an environment."""
        env = get_state_manager().get_environment(name)
        if not env:
            console.print(f"[red]Environment '{name}' not found[/red]")
            raise typer.Exit(code=1)
        
        if not force:
            module_count = len(env.modules)
            if module_count > 0:
                if not beaupy.confirm(
                    f"This will also delete {module_count} module(s) in this environment. Continue?"
                ):
                    console.print("[yellow]Deletion cancelled.[/yellow]")
                    return
        
        if get_state_manager().delete_environment(name):
            console.print(f"[green]Deleted environment: {name}[/green]")
        else:
            console.print(f"[red]Failed to delete environment: {name}[/red]")
            raise typer.Exit(code=1)
    
    return app_env

@app.command()
def create(
    module_path: Path = typer.Argument(
        ...,
        help="Path to the Terraform module to create",
        exists=True,
        file_okay=False,
        dir_okay=True,
        resolve_path=True,
    ),
    auto_approve: bool = typer.Option(
        False,
        "--yes",
        "-y",
        help="Skip interactive approval",
    ),
) -> None:
    """Create infrastructure from a Terraform module."""
    env_name = _select_environment(create_if_missing=True)
    if env_name is None:
        return
    
    typer.echo(f"Creating infrastructure from module: {module_path}")
    
    # Add to state first so we have the state directory
    get_state_manager().add_module(module_path, env_name)
    
    try:
        # Prepare module (copy to temp dir and setup state)
        temp_module_dir, state_file = get_state_manager().prepare_module(module_path, env_name)
        
        try:
            # First run init
            _run_tofu_command(["init"], temp_module_dir)
            
            # Then run apply
            apply_args = ["apply"]
            if auto_approve:
                apply_args.append("-auto-approve")
            
            _run_tofu_command(apply_args, temp_module_dir, state_file)
            
        finally:
            # Clean up temp directory
            get_state_manager().cleanup_module(module_path, env_name)
            
    except Exception as e:
        # If anything fails, clean up the state
        get_state_manager().remove_module(module_path)
        raise e

@app.command()
def list():
    """List all tracked infrastructure modules."""
    # Select environment
    env_name = _select_environment(create_if_missing=False)
    if env_name is None:
        return
    
    modules = get_state_manager().get_modules(env_name)
    
    if not modules:
        console.print("[yellow]No modules found in this environment.[/yellow]")
        return
    
    table = Table(title=f"Tracked Infrastructure Modules - Environment: {env_name}")
    table.add_column("Path", style="cyan")
    table.add_column("Created", style="green")
    table.add_column("Last Applied", style="blue")
    
    for module in modules:
        table.add_row(
            module.path,
            module.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            module.last_applied.strftime("%Y-%m-%d %H:%M:%S"),
        )
    
    console.print(table)

@app.command()
def destroy(
    module_path: Optional[Path] = typer.Argument(
        None,
        help="Path to the Terraform module to destroy",
        exists=True,
        file_okay=False,
        dir_okay=True,
        resolve_path=True,
    ),
    auto_approve: bool = typer.Option(
        False,
        "--yes",
        "-y",
        help="Skip interactive approval",
    ),
) -> None:
    """Destroy infrastructure from a Terraform module."""
    env_name = _select_environment()
    if env_name is None:
        return
    
    # Get modules in the environment
    modules = get_state_manager().get_modules(env_name)
    if not modules:
        console.print(f"[yellow]No modules found in environment '{env_name}'[/]")
        raise typer.Exit(1)
    
    if module_path:
        # Destroy specific module
        target_path = module_path
    else:
        # Select module to destroy
        module_choices = [
            f"{Path(module.path).name} (Created: {module.created_at.strftime('%Y-%m-%d')})"
            for module in modules
        ]
        
        console.print("\nSelect a module to destroy:")
        selected_index = beaupy.select(
            options=module_choices,
            cursor_style="cyan",
            return_index=True,  # Return the index instead of the value
        )
        
        if selected_index is None:
            raise typer.Exit(1)
        
        target_path = Path(modules[selected_index].path)
    
    try:
        # Prepare module (copy to temp dir and setup state)
        temp_module_dir, state_file = get_state_manager().prepare_module(target_path, env_name)
        
        try:
            # First run init
            _run_tofu_command(["init"], temp_module_dir)
            
            # Then destroy
            destroy_args = ["destroy"]
            if auto_approve:
                destroy_args.append("-auto-approve")
            
            _run_tofu_command(destroy_args, temp_module_dir, state_file)
            
        finally:
            # Clean up temp directory
            get_state_manager().cleanup_module(target_path, env_name)
        
        # Remove from state
        get_state_manager().remove_module(target_path)
        console.print(f"[green]Successfully destroyed infrastructure from {target_path}[/]")
    except Exception as e:
        console.print(f"[red]Failed to destroy infrastructure: {str(e)}[/]")
        raise typer.Exit(1)

if __name__ == "__main__":
    app()
