from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import yaml


@dataclass
class Config:
    """Configuration for the infra CLI."""
    state_path: Path
    
    @classmethod
    def from_dict(cls, data: dict, config_path: Path) -> "Config":
        """Create a Config from a dictionary, resolving paths relative to config file."""
        state_path = Path(data.get("state_path", ".infra"))
        if not state_path.is_absolute():
            state_path = (config_path.parent / state_path).resolve()
        return cls(state_path=state_path)
    
    def to_dict(self, config_path: Path) -> dict:
        """Convert Config to a dictionary, making paths relative to config file."""
        try:
            state_path = Path(self.state_path).relative_to(config_path.parent)
        except ValueError:
            # If state_path is not relative to config_path, use absolute path
            state_path = self.state_path
        return {
            "state_path": str(state_path),
        }


def find_config(start_path: Optional[Path] = None) -> Optional[Path]:
    """Find infra.yaml by scanning up from start_path."""
    if start_path is None:
        start_path = Path.cwd()
    
    current = start_path.resolve()
    while current != current.parent:
        config_path = current / "infra.yaml"
        if config_path.exists():
            return config_path
        current = current.parent
    return None


def load_config(config_path: Path) -> Config:
    """Load configuration from a YAML file."""
    with open(config_path) as f:
        data = yaml.safe_load(f) or {}
    return Config.from_dict(data, config_path)


def save_config(config: Config, config_path: Path) -> None:
    """Save configuration to a YAML file."""
    data = config.to_dict(config_path)
    with open(config_path, "w") as f:
        yaml.dump(data, f, default_flow_style=False)
