# Infra SDK

A powerful CLI tool that simplifies infrastructure management using OpenTofu (a Terraform fork).

## Features

- Environment-based infrastructure management
- Interactive module selection
- State management with SQLite
- Project configuration with `infra.yaml`
- Support for multiple infrastructure modules

## Installation

```bash
pip install infra-sdk
```

## Quick Start

1. Initialize a new project:
```bash
infra init
```

2. Create an environment:
```bash
infra env create dev
```

3. Create infrastructure from a module:
```bash
infra create path/to/module
```

## Project Structure

After initialization, your project will have this structure:
```
your-project/
├── infra.yaml          # Project configuration
└── .infra/            # State directory (configurable)
    ├── state.db       # SQLite database
    ├── states/        # OpenTofu state files
    └── temp/          # Temporary module copies
```

## Commands

- `infra init` - Initialize a new project
- `infra env create <name>` - Create a new environment
- `infra env list` - List all environments
- `infra create <module>` - Create infrastructure from a module
- `infra destroy [module]` - Destroy infrastructure

## Requirements

- Python >= 3.8
- OpenTofu binary (default path: `~/.launchflow/bin/tofu`)

## License

MIT License
