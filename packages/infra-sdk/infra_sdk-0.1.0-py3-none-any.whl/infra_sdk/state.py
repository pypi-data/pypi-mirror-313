import hashlib
import shutil
import tempfile
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Tuple

from sqlalchemy import ForeignKey, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship

from infra_sdk.config import Config

class Base(DeclarativeBase):
    pass

class Environment(Base):
    """An environment for grouping infrastructure deployments."""
    __tablename__ = "environments"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    description: Mapped[Optional[str]]
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    modules: Mapped[List["Module"]] = relationship(back_populates="environment", cascade="all, delete-orphan")

class Module(Base):
    """A Terraform module tracked by the infra CLI."""
    __tablename__ = "modules"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    path: Mapped[str] = mapped_column(unique=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    last_applied: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    environment_id: Mapped[int] = mapped_column(ForeignKey("environments.id"))
    environment: Mapped[Environment] = relationship(back_populates="modules")
    state_hash: Mapped[str] = mapped_column(unique=True)

class StateManager:
    """Manages the state of Terraform modules and environments."""
    
    def __init__(self, config: Config):
        """Initialize state manager with configuration."""
        self.config = config
        
        # Create state directory if it doesn't exist
        self.state_dir = config.state_path
        self.state_dir.mkdir(parents=True, exist_ok=True)
        
        # Create states directory
        self.states_dir = self.state_dir / "states"
        self.states_dir.mkdir(exist_ok=True)
        
        # Create temp directory
        self.temp_dir = self.state_dir / "temp"
        self.temp_dir.mkdir(exist_ok=True)
        
        # Initialize database
        self.engine = create_engine(f"sqlite:///{self.state_dir}/state.db")
        Base.metadata.create_all(self.engine)
    
    def _get_module_hash(self, path: Path, environment_name: str) -> str:
        """Generate a unique hash for a module in an environment."""
        content = f"{str(path.resolve())}:{environment_name}"
        return hashlib.sha256(content.encode()).hexdigest()[:12]
    
    def _get_state_dir(self, environment_name: str, module_hash: str) -> Path:
        """Get the state directory for a module in an environment."""
        return self.states_dir / environment_name / module_hash
    
    def _setup_state_dir(self, environment_name: str, module_hash: str) -> Path:
        """Create and return the state directory for a module."""
        state_dir = self._get_state_dir(environment_name, module_hash)
        state_dir.mkdir(parents=True, exist_ok=True)
        return state_dir
    
    def _cleanup_state_dir(self, environment_name: str, module_hash: str) -> None:
        """Remove the state directory for a module."""
        state_dir = self._get_state_dir(environment_name, module_hash)
        if state_dir.exists():
            shutil.rmtree(state_dir)
    
    def _copy_module_to_temp(self, module_path: Path, module_hash: str) -> Path:
        """Copy module to a temporary directory."""
        temp_module_dir = self.temp_dir / module_hash
        if temp_module_dir.exists():
            shutil.rmtree(temp_module_dir)
        shutil.copytree(module_path, temp_module_dir)
        return temp_module_dir
    
    def _cleanup_temp_module(self, module_hash: str) -> None:
        """Remove temporary module directory."""
        temp_module_dir = self.temp_dir / module_hash
        if temp_module_dir.exists():
            shutil.rmtree(temp_module_dir)
    
    def prepare_module(self, module_path: Path, environment_name: str) -> Tuple[Path, Path]:
        """Prepare a module for execution by copying it to temp dir and setting up state dir.
        
        Returns:
            Tuple[Path, Path]: (temp_module_dir, state_file_path)
        """
        module_hash = self._get_module_hash(module_path, environment_name)
        temp_module_dir = self._copy_module_to_temp(module_path, module_hash)
        state_dir = self._setup_state_dir(environment_name, module_hash)
        return temp_module_dir, state_dir / "terraform.tfstate"
    
    def cleanup_module(self, module_path: Path, environment_name: str) -> None:
        """Clean up temporary module directory."""
        module_hash = self._get_module_hash(module_path, environment_name)
        self._cleanup_temp_module(module_hash)
    
    # Environment management
    def create_environment(self, name: str, description: Optional[str] = None) -> Environment:
        """Create a new environment."""
        with Session(self.engine) as session:
            # Check if environment already exists
            stmt = select(Environment).where(Environment.name == name)
            existing = session.scalar(stmt)
            if existing:
                raise ValueError(f"Environment '{name}' already exists")
            
            env = Environment(name=name, description=description)
            session.add(env)
            session.commit()
            
            # Create environment state directory
            (self.states_dir / name).mkdir(exist_ok=True)
            
            return env
    
    def get_environment(self, name: str) -> Optional[Environment]:
        """Get an environment by name."""
        with Session(self.engine) as session:
            stmt = select(Environment).where(Environment.name == name)
            return session.scalar(stmt)
    
    def get_environments(self) -> List[Environment]:
        """Get all environments."""
        with Session(self.engine) as session:
            return list(session.scalars(select(Environment).order_by(Environment.name)))
    
    def update_environment(self, name: str, new_name: Optional[str] = None, new_description: Optional[str] = None) -> Optional[Environment]:
        """Update an environment."""
        with Session(self.engine) as session:
            env = session.scalar(select(Environment).where(Environment.name == name))
            if not env:
                return None
            
            if new_name:
                # Check if new name already exists
                if new_name != name:
                    existing = session.scalar(select(Environment).where(Environment.name == new_name))
                    if existing:
                        raise ValueError(f"Environment '{new_name}' already exists")
                
                # Rename environment state directory
                old_state_dir = self.states_dir / name
                new_state_dir = self.states_dir / new_name
                if old_state_dir.exists():
                    old_state_dir.rename(new_state_dir)
                
                env.name = new_name
            
            if new_description is not None:  # Allow empty description
                env.description = new_description
            
            session.commit()
            return env
    
    def delete_environment(self, name: str) -> bool:
        """Delete an environment and all its modules."""
        with Session(self.engine) as session:
            env = session.scalar(select(Environment).where(Environment.name == name))
            if not env:
                return False
            
            # Remove environment state directory
            env_state_dir = self.states_dir / name
            if env_state_dir.exists():
                shutil.rmtree(env_state_dir)
            
            session.delete(env)
            session.commit()
            return True
    
    # Module management
    def add_module(self, path: Path, environment_name: str) -> None:
        """Add a module to the state database."""
        with Session(self.engine) as session:
            # Get environment
            env = session.scalar(select(Environment).where(Environment.name == environment_name))
            if not env:
                raise ValueError(f"Environment '{environment_name}' does not exist")
            
            # Generate state hash
            state_hash = self._get_module_hash(path, environment_name)
            
            # Check if module already exists
            stmt = select(Module).where(Module.path == str(path.resolve()))
            existing = session.scalar(stmt)
            
            if existing:
                existing.last_applied = datetime.utcnow()
                existing.environment = env
                existing.state_hash = state_hash
            else:
                module = Module(
                    path=str(path.resolve()),
                    environment=env,
                    state_hash=state_hash,
                )
                session.add(module)
            
            # Setup state directory
            self._setup_state_dir(environment_name, state_hash)
            
            session.commit()
    
    def get_modules(self, environment_name: Optional[str] = None) -> List[Module]:
        """Get all tracked modules, optionally filtered by environment."""
        with Session(self.engine) as session:
            if environment_name:
                stmt = select(Module).join(Environment).where(
                    Environment.name == environment_name
                ).order_by(Module.last_applied.desc())
            else:
                stmt = select(Module).order_by(Module.last_applied.desc())
            return list(session.scalars(stmt))
    
    def remove_module(self, path: Path) -> None:
        """Remove a module from the state database."""
        with Session(self.engine) as session:
            stmt = select(Module).where(Module.path == str(path.resolve()))
            module = session.scalar(stmt)
            if module:
                # Clean up state directory
                self._cleanup_state_dir(module.environment.name, module.state_hash)
                session.delete(module)
                session.commit()
    
    def get_state_dir(self, path: Path, environment_name: str) -> Optional[Path]:
        """Get the state directory for a module."""
        with Session(self.engine) as session:
            stmt = select(Module).where(
                Module.path == str(path.resolve()),
                Module.environment.has(name=environment_name),
            )
            module = session.scalar(stmt)
            if not module:
                return None
            
            return self._get_state_dir(environment_name, module.state_hash)
