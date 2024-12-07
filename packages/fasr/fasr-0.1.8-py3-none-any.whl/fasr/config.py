import catalogue
import confection
from confection import Config
from pathlib import Path
from typing import Dict, Any


class registry(confection.registry):
    layers = catalogue.create("fasr", "layers", entry_points=True)
    models = catalogue.create("fasr", "models", entry_points=True)
    components = catalogue.create("fasr", "components", entry_points=True)
    pipelines = catalogue.create("fasr", "pipelines", entry_points=True)
    pipes = catalogue.create("fasr", "pipes", entry_points=True)
    text_preprocessors = catalogue.create(
        "fasr", "text_preprocessors", entry_points=True
    )
    audio_preprocessors = catalogue.create(
        "fasr", "audio_preprocessors", entry_points=True
    )
    runtimes = catalogue.create("fasr", "runtimes", entry_points=True)

    @classmethod
    def create(cls, registry_name: str, entry_points: bool = False) -> None:
        """Create a new custom registry."""
        if hasattr(cls, registry_name):
            raise ValueError(f"Registry '{registry_name}' already exists")
        reg = catalogue.create("fasr", registry_name, entry_points=entry_points)
        setattr(cls, registry_name, reg)

    @classmethod
    def resolve_from_dir(
        cls, save_dir: str, config: str = "config.cfg"
    ) -> Dict[str, Any]:
        """Resolve the registry from a directory."""
        save_dir = Path(save_dir)
        if not save_dir.exists():
            raise FileNotFoundError(f"Directory '{save_dir}' not found")
        config = save_dir / config
        if not config.exists():
            raise FileNotFoundError(f"Config file '{config}' not found")
        config = Config().from_disk(config)
        resolved = cls.resolve(config)
        return resolved


__all__ = ["Config", "registry"]
