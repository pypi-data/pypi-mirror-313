from abc import ABC, abstractmethod
from pydantic import ConfigDict
from fasr.config import Config
from fasr.data.audio import (
    AudioList,
    Audio,
)
from typing import Any, Dict, List, Union
import torch
from fasr.utils.base import ModelScopeMixin, SerializableMixin
from wasabi import msg
from pathlib import Path
from loguru import logger


class BaseComponent(ModelScopeMixin, SerializableMixin, ABC):
    """A component is a module that can set tag on audio data"""

    model_config = ConfigDict(arbitrary_types_allowed=True, validate_assignment=True)
    timer_data: Dict[str, float] | None = (
        None  # 使用utils.time_it.timer装饰器时，自动记录时间。
    )
    name: str | None = None
    input_tags: List[str] | None = None
    output_tags: List[str] | None = None
    check_tags: bool = False  # 是否检查输入的tag是否存在，但目前不能检查嵌套的tag例如channel.segments.text

    @abstractmethod
    def predict(self, audios: AudioList[Audio]) -> AudioList[Audio]:
        raise NotImplementedError

    def get_config(self) -> Config:
        raise NotImplementedError

    def load(self, save_dir: str):
        raise NotImplementedError

    def save(self, save_dir: str):
        raise NotImplementedError

    def from_checkpoint(cls, checkpoint_dir: str, **kwargs):
        raise NotImplementedError

    def msg_component_error(self):
        msg.fail(
            f"Component {self.name} error, please check the error message from audio.bad_reason."
        )

    def log_component_error(self):
        logger.error(
            f"Component {self.name} error, please check the error message from audio.bad_reason."
        )

    def _filter_bad_audios(self, audios: AudioList[Audio]) -> AudioList[Audio]:
        """filter bad audios"""
        ids = []
        for audio in audios:
            audio: Audio
            if not audio.is_bad:
                ids.append(audio.id)
        return audios.filter_audio_id(ids)

    def _filter_not_tagged_audios(self, audios: AudioList[Audio]) -> AudioList[Audio]:
        """filter not tagged audios"""
        if self.input_tags is None or len(self.input_tags) == 0:
            return audios
        ids = []
        for audio in audios:
            audio: Audio
            for tag in self.input_tags:
                if hasattr(audio, tag):
                    if getattr(audio, tag) is not None:
                        ids.append(audio.id)
        return audios.filter_audio_id(ids)

    def _to_audios(
        self,
        input: Union[str, List[str], Any, Audio, AudioList[Audio], Path, List[Path]],
    ) -> AudioList[Audio]:
        if isinstance(input, str):
            audios = AudioList[Audio].from_urls([input], load=False)
            return audios
        elif isinstance(input, list):
            audios = AudioList()
            for item in input:
                if isinstance(item, str):
                    audio = Audio(url=item)
                    audios.append(audio)
                elif isinstance(item, Audio):
                    audios.append(item)
                elif isinstance(item, Path):
                    audio = Audio(url=item)
                    audios.append(audio)
                else:
                    raise ValueError(
                        f"Invalid item type: {type(item)} for component {self.name}"
                    )
            return audios
        elif isinstance(input, Audio):
            return AudioList[Audio]([input])
        elif isinstance(input, AudioList):
            return input
        elif isinstance(input, Path):
            return AudioList[Audio](docs=[Audio(url=input)])
        else:
            raise ValueError(
                f"Invalid input type: {type(input)} for component {self.name}"
            )

    def __ror__(
        self,
        input: Union[str, List[str], Audio, AudioList],
        *args,
        **kwargs,
    ) -> AudioList[Audio]:
        """组件之间的同步连接符号 `|` 实现"""
        audios = self._to_audios(input=input)
        audios = self._filter_bad_audios(audios)
        if self.check_tags:
            audios = self._filter_not_tagged_audios(audios)
        for audio in audios:
            audio: Audio
            if audio.pipeline is None:
                audio.pipeline = []
            audio.pipeline.append(self.name)
        try:
            audios = self.predict(audios)
        except Exception as e:
            for audio in audios:
                audio.is_bad = True
                audio.bad_reason = str(e)
                audio.bad_component = self.name
                self.log_component_error()
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
                current_gpu_index = torch.cuda.current_device()
                available_memory = torch.cuda.get_device_properties(
                    current_gpu_index
                ).total_memory / (1024**3)
                used_memory = torch.cuda.memory_allocated(current_gpu_index) / (1024**3)
                free_memory = available_memory - used_memory
                if free_memory <= 0:
                    raise MemoryError("Out of GPU memory.")
        return audios
