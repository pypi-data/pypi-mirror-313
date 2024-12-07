from pydantic import BaseModel, Field
from fasr.config import Config
from abc import ABC, abstractmethod
from pathlib import Path
from .prepare_model import download


class SerializableMixin(BaseModel, ABC):
    @abstractmethod
    def save(self, save_dir: str):
        raise NotImplementedError

    @abstractmethod
    def load(self, save_dir: str):
        raise NotImplementedError

    @abstractmethod
    def get_config(self) -> Config:
        raise NotImplementedError


DEFAULT_CACHE_DIR = Path.home() / ".cache" / "fasr" / "checkpoints"  # 默认缓存目录


class ModelScopeMixin(BaseModel, ABC):
    cache_dir: str | Path = Field(default=DEFAULT_CACHE_DIR, description="默认缓存目录")
    checkpoint: str | None = Field(default=None, description="模型名称")

    def from_checkpoint(self, checkpoint_dir: str, **kwargs):
        raise NotImplementedError

    def download_checkpoint(self, revision: str = None):
        if self.checkpoint is None:
            raise ValueError("checkpoint is None")
        checkpoint_dir = self.cache_dir / self.checkpoint
        if not checkpoint_dir.exists():
            download(model=self.checkpoint, revision=revision, cache_dir=self.cache_dir)

    @property
    def checkpoint_dir(self):
        return self.cache_dir / self.checkpoint


def clear_cache(cache_dir: str | Path = DEFAULT_CACHE_DIR):
    """清空缓存目录

    Args:
        cache_dir (str | Path, optional): 缓存目录. Defaults to DEFAULT_CACHE_DIR = Path.home() / ".cache" / "fasr" / "checkpoints".
    """
    cache_dir = Path(cache_dir)
    if cache_dir.exists():
        for item in cache_dir.iterdir():
            if item.is_dir():
                for sub_item in item.iterdir():
                    sub_item.unlink()
                item.rmdir()
            else:
                item.unlink()
    else:
        cache_dir.mkdir(parents=True)
    return cache_dir
