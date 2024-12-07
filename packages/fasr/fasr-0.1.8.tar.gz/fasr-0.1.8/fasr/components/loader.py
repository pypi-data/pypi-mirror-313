from fasr.data.audio import Audio, AudioList, AudioChannel, AudioChannelList
from fasr.config import registry, Config
from .base import BaseComponent
from pydantic import Field
from typing import List
from aiohttp import ClientSession
import asyncio
from io import BytesIO
import librosa
from pathlib import Path
import aiofiles
from joblib import Parallel, delayed


@registry.components.register("loader")
@registry.components.register("loader.v2")
class AudioLoaderV2(BaseComponent):
    """异步音频下载器，负责所有音频的并行下载和下载条件"""

    name: str = "loader"
    input_tags: List[str] = ["audio.url"]
    output_tags: List[str] = [
        "audio.waveform",
        "audio.sample_rate",
        "audio.duration",
        "audio.channels",
    ]

    max_duration_seconds: float | None = Field(
        None, alias="max_duration", description="音频最大时长，超过该时长则截断"
    )
    min_duration_seconds: float | None = Field(
        None, alias="min_duration", description="音频最小时长，小于该时长则不下载"
    )
    reload: bool = Field(False, description="是否重新下载")
    only_num_channels: int | None = Field(
        None, description="只下载指定通道数的音频，None表示不限制"
    )
    mono: bool = Field(False, description="是否合并多通道音频为单通道")

    def predict(self, audios: AudioList) -> AudioList:
        _ = asyncio.run(self.aload_audios(audios=audios))
        return audios

    async def aload_audio(self, audio: Audio, session: ClientSession) -> Audio:
        if not self.reload and audio.is_loaded:
            return audio
        try:
            if Path(audio.url).exists():
                try:
                    async with aiofiles.open(audio.url, "rb") as f:
                        bytes = await f.read()
                        bytes = BytesIO(bytes)
                        waveform, sample_rate = librosa.load(
                            bytes, sr=audio.sample_rate, mono=self.mono
                        )
                        duration = librosa.get_duration(y=waveform, sr=sample_rate)
                        audio.duration = duration
                        audio.sample_rate = sample_rate
                        audio.waveform = waveform
                        if len(audio.waveform.shape) == 1:
                            audio.mono = True
                            audio.channels = AudioChannelList[AudioChannel](
                                [
                                    AudioChannel(
                                        id=audio.id,
                                        waveform=waveform,
                                        sample_rate=sample_rate,
                                    )
                                ]
                            )
                        else:
                            audio.mono = False
                            audio.channels = AudioChannelList[AudioChannel](
                                [
                                    AudioChannel(
                                        id=audio.id,
                                        waveform=channel_waveform,
                                        sample_rate=audio.sample_rate,
                                    )
                                    for channel_waveform in audio.waveform
                                ]
                            )
                except Exception as e:
                    audio.is_bad = True
                    audio.bad_reason = str(e)
                    audio.bad_component = self.name

                return audio

            async with session.get(audio.url) as response:
                if response.status == 200:
                    bytes = await response.read()
                    bytes = BytesIO(bytes)
                    waveform, sample_rate = librosa.load(
                        bytes, sr=audio.sample_rate, mono=self.mono
                    )
                    duration = librosa.get_duration(y=waveform, sr=sample_rate)
                    audio.duration = duration
                    audio.sample_rate = sample_rate
                    audio.waveform = waveform
                    if len(audio.waveform.shape) == 1:
                        audio.mono = True
                        audio.channels = AudioChannelList[AudioChannel](
                            [
                                AudioChannel(
                                    id=audio.id,
                                    waveform=waveform,
                                    sample_rate=sample_rate,
                                )
                            ]
                        )
                    else:
                        audio.mono = False
                        audio.channels = AudioChannelList[AudioChannel](
                            [
                                AudioChannel(
                                    id=audio.id,
                                    waveform=channel_waveform,
                                    sample_rate=audio.sample_rate,
                                )
                                for channel_waveform in audio.waveform
                            ]
                        )

                    if (
                        self.max_duration_seconds
                        and audio.duration > self.max_duration_seconds
                    ):
                        audio.is_bad = True
                        audio.bad_reason = f"音频时长超过最大时长限制{self.max_duration_seconds}s, 当前时长{audio.duration}s"
                    if (
                        self.min_duration_seconds
                        and audio.duration < self.min_duration_seconds
                    ):
                        audio.is_bad = True
                        audio.bad_reason = f"音频时长小于最小时长限制{self.min_duration_seconds}s, 当前时长{audio.duration}s"
                    if (
                        self.only_num_channels
                        and len(audio.channels) != self.only_num_channels
                    ):
                        audio.is_bad = True
                        audio.bad_reason = f"音频通道数不符合要求, 期望{self.only_num_channels}通道，实际{len(audio.channels)}通道"
                    if audio.is_bad:
                        audio.bad_component = self.name
                    audio.channels[-1].is_last = True
                else:
                    audio.is_bad = True
                    audio.bad_reason = f"下载音频失败，状态码{response.status}"
                    audio.bad_component = self.name

                return audio
        except Exception as e:
            audio.is_bad = True
            audio.bad_reason = str(e)
            audio.bad_component = self.name
            return audio

    async def aload_audios(self, audios: AudioList) -> AudioList:
        async with ClientSession() as session:
            tasks = [self.aload_audio(audio, session) for audio in audios]
            results = await asyncio.gather(*tasks)
            return results

    def get_config(self) -> Config:
        data = {
            "component": {
                "@components": "loader.v2",
                "max_duration": self.max_duration_seconds,
                "min_duration": self.min_duration_seconds,
                "reload": self.reload,
                "mono": self.mono,
                "only_num_channels": self.only_num_channels,
            }
        }
        return Config(data=data)

    def save(self, save_dir: str | Path) -> None:
        save_dir = Path(save_dir)
        if not save_dir.exists():
            save_dir.mkdir(parents=True)
        config_path = save_dir / "config.cfg"
        self.get_config().to_disk(config_path)

    def load(self, save_dir: str | Path) -> "AudioLoaderV2":
        config_path = Path(save_dir, "config.cfg")
        config = Config().from_disk(config_path)
        loader = registry.resolve(config)["component"]
        return loader


@registry.components.register("loader.v1")
class AudioLoaderV1(BaseComponent):
    """多线程音频下载器，负责所有音频的并行下载和下载条件"""

    name: str = "loader"
    input_tags: List[str] = ["audio.url"]
    output_tags: List[str] = [
        "audio.waveform",
        "audio.sample_rate",
        "audio.duration",
        "audio.channels",
    ]

    max_duration_seconds: float | None = Field(
        None, alias="max_duration", description="音频最大时长，超过该时长则截断"
    )
    min_duration_seconds: float | None = Field(
        None, alias="min_duration", description="音频最小时长，小于该时长则不下载"
    )
    reload: bool = Field(False, description="是否重新下载")
    mono: bool = Field(False, description="是否合并多通道音频为单通道")
    num_threads: int = Field(1, description="最大并行线程数")
    only_num_channels: int | None = Field(
        None, description="只下载指定通道数的音频，None表示不限制"
    )

    def predict(self, audios: AudioList[Audio]) -> AudioList[Audio]:
        _ = Parallel(
            n_jobs=self.num_threads,
            prefer="threads",
            pre_dispatch="10 * n_jobs",
        )(delayed(self.load_audio)(audio) for audio in audios)
        return audios

    def load_audio(self, audio: Audio) -> Audio:
        if audio.is_loaded:
            if self.reload:
                try:
                    audio.load(mono=self.mono)
                except Exception as e:
                    audio.is_bad = True
                    audio.bad_reason = str(e)
                    audio.bad_component = self.name
            return audio
        else:
            try:
                audio.load(mono=self.mono)
            except Exception as e:
                audio.is_bad = True
                audio.bad_reason = str(e)
                audio.bad_component = self.name
                self.log_component_error()
                return audio
            if self.max_duration_seconds and audio.duration > self.max_duration_seconds:
                audio.is_bad = True
                audio.bad_reason = f"音频时长超过最大时长限制{self.max_duration_seconds}s, 当前时长{audio.duration}s"
            if self.min_duration_seconds and audio.duration < self.min_duration_seconds:
                audio.is_bad = True
                audio.bad_reason = f"音频时长小于最小时长限制{self.min_duration_seconds}s, 当前时长{audio.duration}s"
            if self.only_num_channels and len(audio.channels) != self.only_num_channels:
                audio.is_bad = True
                audio.bad_reason = f"音频通道数不符合要求, 期望{self.only_num_channels}通道，实际{len(audio.channels)}通道"
            if audio.is_bad:
                audio.bad_component = self.name
            return audio

    def save(self, save_dir: str | Path) -> None:
        save_dir = Path(save_dir)
        if not save_dir.exists():
            save_dir.mkdir(parents=True)
        config_path = save_dir / "config.cfg"
        self.get_config().to_disk(config_path)

    def load(self, save_dir: str | Path) -> "AudioLoaderV1":
        config_path = Path(save_dir, "config.cfg")
        config = Config().from_disk(config_path)
        loader = registry.resolve(config)["component"]
        return loader

    def get_config(self) -> Config:
        data = {
            "component": {
                "@components": "loader.v1",
                "max_duration": self.max_duration_seconds,
                "min_duration": self.min_duration_seconds,
                "reload": self.reload,
                "mono": self.mono,
                "num_threads": self.num_threads,
                "only_num_channels": self.only_num_channels,
            }
        }
        return Config(data=data)
