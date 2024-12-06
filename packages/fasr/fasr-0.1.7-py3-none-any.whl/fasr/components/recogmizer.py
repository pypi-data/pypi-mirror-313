from .base import BaseComponent
from fasr.data.audio import (
    AudioList,
    Audio,
    AudioSpanList,
    AudioSpan,
    AudioToken,
    AudioTokenList,
    AudioChannel,
)
from fasr.config import registry
from funasr import AutoModel
from fasr.models.sensevoice import StreamingSenseVoice
from typing import List, Iterable, Dict
from joblib import Parallel, delayed
import re
from pathlib import Path
import torch
import numpy as np
from pydantic import validate_call


@registry.components.register("recognizer")
@registry.components.register("recognizer.paraformer")
class ParaformerSpeechRecognizer(BaseComponent):
    name: str = "recognizer"
    input_tags: List[str] = ["channel.segments", "channel.waveform"]
    output_tags: List[str] = ["segment.tokens", "channel.tokens", "channel.text"]
    checkpoint: str = "iic/speech_paraformer-large-vad-punc_asr_nat-zh-cn-16k-common-vocab8404-pytorch"

    model: AutoModel | None = None
    num_threads: int = 1
    batch_size_s: int = 100

    def predict(self, audios: AudioList[Audio]) -> AudioList[Audio]:
        _ = Parallel(
            n_jobs=self.num_threads, prefer="threads", pre_dispatch="1 * n_jobs"
        )(
            delayed(self.predict_step)(batch_segments)
            for batch_segments in self.batch_audio_segments(audios=audios)
        )
        return audios

    def predict_step(
        self, batch_segments: List[AudioSpan | AudioChannel]
    ) -> List[AudioSpan | AudioChannel]:
        batch_waveforms = [seg.waveform for seg in batch_segments]
        fs = batch_segments[0].sample_rate  # 一个batch的音频片段采样率相同
        batch_results = self.model.generate(input=batch_waveforms, fs=fs)
        for seg, result in zip(batch_segments, batch_results):
            tokens = []
            result_text = result["text"]
            if result_text:
                texts = result["text"].split(" ")
            else:
                texts = []
            timestamps = result["timestamp"]
            assert len(texts) == len(timestamps), f"{texts} {timestamps}"
            for token_text, timestamp in zip(texts, timestamps):
                if seg.start_ms is not None and seg.end_ms is not None:
                    start_ms = seg.start_ms + timestamp[0]
                    end_ms = seg.start_ms + timestamp[1]
                else:
                    start_ms = timestamp[0]
                    end_ms = timestamp[1]
                token = AudioToken(start_ms=start_ms, end_ms=end_ms, text=token_text)
                assert token.end_ms - token.start_ms > 0, f"{token}"
                tokens.append(token)
            seg.tokens = AudioTokenList(docs=tokens)
        return batch_segments

    def batch_audio_segments(
        self, audios: AudioList[Audio]
    ) -> Iterable[AudioSpanList[AudioSpan]]:
        """将音频片段组成批次。
        步骤：
        - 1. 将音频片段按照时长排序。
        - 2. 将音频片段按照时长分组，每组时长不超过batch_size_s。
        """
        all_segments = []
        for audio in audios:
            if not audio.is_bad:
                for channel in audio.channels:
                    if channel.segments is None:  # 兼容没有vad模型的情况
                        all_segments.append(channel)
                    else:
                        for seg in channel.segments:
                            all_segments.append(seg)
        return self.batch_segments(all_segments)

    def batch_segments(
        self, segments: Iterable[AudioSpan]
    ) -> Iterable[AudioSpanList[AudioSpan]]:
        """将音频片段组成批次。"""
        self.model.kwargs["batch_size"] = self.batch_size_s * 1000
        batch_size_ms = self.batch_size_s * 1000
        segments = [seg for seg in segments]
        sorted_segments = self.sort_segments(segments)
        batch = AudioSpanList()
        for seg in sorted_segments:
            max_duration_ms = max(batch.max_duration_ms, seg.duration_ms)
            current_batch_duration_ms = max_duration_ms * len(batch)
            if current_batch_duration_ms > batch_size_ms:
                yield batch
                batch = AudioSpanList()
                batch.append(seg)
            else:
                batch.append(seg)
        if len(batch) > 0:
            yield batch

    def sort_segments(self, segments: List[AudioSpan]) -> List[AudioSpan]:
        return sorted(segments, key=lambda x: x.duration_ms)

    def from_checkpoint(
        self,
        checkpoint_dir: str | None = None,
        batch_size_s: int = 100,
        num_threads: int = 1,
        **kwargs,
    ) -> "ParaformerSpeechRecognizer":
        if not checkpoint_dir:
            self.download_checkpoint()
            checkpoint_dir = self.checkpoint_dir
        checkpoint_dir = Path(checkpoint_dir)
        assert checkpoint_dir.exists(), f"{checkpoint_dir} not exists, please run `fasr prepare` to download the paraformer model."
        model = AutoModel(model=checkpoint_dir, disable_update=True, **kwargs)
        model.kwargs["batch_size"] = batch_size_s * 1000
        self.model = model
        self.num_threads = num_threads
        self.batch_size_s = batch_size_s
        return self


@registry.components.register("recognizer.sensevoice")
class SensevoiceSpeechRecognizer(BaseComponent):
    name: str = "recognizer"
    input_tags: List[str] = ["channel.segments"]
    output_tags: List[str] = [
        "segment.language",
        "segment.emotion",
        "segment.type",
        "segment.text",
        "channel.text",
    ]
    checkpoint: str = "iic/SenseVoiceSmall"

    model: AutoModel = None
    num_threads: int = 1
    batch_size_s: int = 100
    use_itn: bool = False

    def predict(self, audios: AudioList[Audio]) -> AudioList[Audio]:
        _ = Parallel(
            n_jobs=self.num_threads, prefer="threads", pre_dispatch="1 * n_jobs"
        )(
            delayed(self.predict_step)(batch_segments)
            for batch_segments in self.batch_audio_segments(audios=audios)
        )
        return audios

    def sort_audio_segments(self, audios: AudioList[Audio]) -> List[AudioSpan]:
        all_segments = []
        for audio in audios:
            if not audio.is_bad and not audio.channels:
                for channel in audio.channels:
                    for seg in channel.segments:
                        all_segments.append(seg)
        sorted_segments = sorted(all_segments, key=lambda x: x.duration_ms)
        return sorted_segments

    def batch_audio_segments(
        self, audios: AudioList[Audio]
    ) -> Iterable[AudioSpanList[AudioSpan]]:
        """将音频片段组成批次。
        步骤：
        - 1. 将音频片段按照时长排序。
        - 2. 将音频片段按照时长分组，每组时长不超过batch_size_s。
        """
        all_segments = []
        for audio in audios:
            if not audio.is_bad:
                for channel in audio.channels:
                    if channel.segments is None:  # 兼容没有vad模型的情况
                        segments = [
                            AudioSpan(
                                start_ms=0,
                                end_ms=channel.duration_ms,
                                waveform=channel.waveform,
                                sample_rate=channel.sample_rate,
                                is_last=True,
                            )
                        ]
                        channel.segments = segments
                    for seg in channel.segments:
                        all_segments.append(seg)
        return self.batch_segments(all_segments)

    def predict_step(self, batch_segments: List[AudioSpan]) -> List[AudioSpan]:
        batch_waveforms = [seg.waveform for seg in batch_segments]
        fs = batch_segments[0].sample_rate  # 一个batch的音频片段采样率相同
        batch_results = self.model.generate(
            input=batch_waveforms, fs=fs, use_itn=self.use_itn
        )
        for seg, result in zip(batch_segments, batch_results):
            pattern = r"<\|(.+?)\|><\|(.+?)\|><\|(.+?)\|><\|(.+?)\|>(.+)"
            if result["text"]:
                match = re.match(pattern, result["text"])
                if match:
                    language, emotion, audio_type, itn, text = match.groups()
                    seg.language = language
                    seg.emotion = emotion
                    seg.type = audio_type
                    seg.text = text
        return batch_segments

    def batch_segments(
        self, segments: Iterable[AudioSpan]
    ) -> Iterable[AudioSpanList[AudioSpan]]:
        """将音频片段组成批次。"""
        self.model.kwargs["batch_size"] = self.batch_size_s * 1000
        batch_size_ms = self.batch_size_s * 1000
        segments = [seg for seg in segments]
        sorted_segments = self.sort_segments(segments)
        batch = AudioSpanList[AudioSpan]()
        for seg in sorted_segments:
            max_duration_ms = max(batch.max_duration_ms, seg.duration_ms)
            current_batch_duration_ms = max_duration_ms * len(batch)
            if current_batch_duration_ms > batch_size_ms:
                yield batch
                batch = AudioSpanList[AudioSpan]()
                batch.append(seg)
            else:
                batch.append(seg)
        if len(batch) > 0:
            yield batch

    def sort_segments(self, segments: List[AudioSpan]) -> List[AudioSpan]:
        return sorted(segments, key=lambda x: x.duration_ms)

    def from_checkpoint(
        self,
        checkpoint_dir: str | None = None,
        batch_size_s: int = 100,
        num_threads: int = 1,
        use_itn: bool = False,
        **kwargs,
    ) -> "SensevoiceSpeechRecognizer":
        if not checkpoint_dir:
            self.download_checkpoint()
            checkpoint_dir = self.checkpoint_dir
        checkpoint_dir = Path(checkpoint_dir)
        if not checkpoint_dir.exists():
            raise FileNotFoundError(
                f"Checkpoint {checkpoint_dir} not found. if you want to use sensevoice model, please run `fasr prepare` to download the model."
            )
        model = AutoModel(model=checkpoint_dir, disable_update=True, **kwargs)
        model.kwargs["batch_size"] = batch_size_s * 1000
        self.model = model
        self.num_threads = num_threads
        self.batch_size_s = batch_size_s
        self.use_itn = use_itn
        return self


@registry.components.register("online_recognizer")
@registry.components.register("online_recognizer.sensevoice")
class SensevoiceOnlineSpeechRecognizer(BaseComponent):
    name: str = "online_recognizer"
    input_tags: List[str] = ["channel.waveform", "audio.is_last"]
    output_tags: List[str] = [
        "channel.stream",
    ]
    checkpoint: str = "iic/SenseVoiceSmall"

    model: StreamingSenseVoice = None

    def predict(self, audios: AudioList[Audio]) -> AudioList[Audio]:
        for audio in audios:
            audio[0].stream = self.stream_tokens(audio)
        return audios

    def predict_audio(self, audio: Audio) -> AudioTokenList:
        audio[0].tokens = self.stream_tokens(audio)
        return audio[0].tokens

    def stream(self, audios: AudioList[Audio]) -> Iterable[AudioToken]:
        for audio in audios:
            yield from self.stream_tokens(audio)

    def stream_tokens(self, audio_chunk: Audio) -> Iterable[AudioToken]:
        assert (
            len(audio_chunk.channels) == 1
        ), "RealtimeSpeechRecognizer only support single channel audio."
        channel = audio_chunk.channels[0]
        if channel.segments is None:
            stream = self.model.streaming_inference(
                audio=channel.waveform, is_last=audio_chunk.is_last
            )
            for result in stream:
                yield AudioToken(text=result["text"], start_ms=result["timestamp"])
        else:
            for seg in channel.segments:
                stream = self.model.streaming_inference(
                    audio=seg.waveform, is_last=seg.is_last
                )
                for result in stream:
                    yield AudioToken(text=result["text"], start_ms=result["timestamp"])
        if audio_chunk.is_last:
            self.reset()

    def reset(self):
        self.model.reset()

    def from_checkpoint(
        self,
        checkpoint_dir: str | None = None,
        device: str | None = None,
        **kwargs,
    ):
        if not checkpoint_dir:
            self.download_checkpoint()
            checkpoint_dir = self.checkpoint_dir
        checkpoint_dir = Path(checkpoint_dir)
        if not checkpoint_dir.exists():
            raise FileNotFoundError(
                f"Checkpoint {checkpoint_dir} not found. if you want to use sensevoice model, please run `fasr prepare` to download the model."
            )
        if device is None:
            device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = StreamingSenseVoice(model=checkpoint_dir, device=device, **kwargs)
        self.model.reset()
        return self


@registry.components.register("online_recognizer.paraformer")
class ParaformerOnlineSpeechRecognizer(BaseComponent):
    name: str = "online_recognizer"
    input_tags: List[str] = ["channel.waveform", "audio.is_last"]
    output_tags: List[str] = [
        "channel.stream",
    ]
    checkpoint: str = (
        "iic/speech_paraformer-large_asr_nat-zh-cn-16k-common-vocab8404-online"
    )

    model: AutoModel | None = None

    encoder_chunk_look_back: int = (
        4  # number of chunks to lookback for encoder self-attention
    )
    decoder_chunk_look_back: int = 1
    cache: Dict = {}
    buffer: np.ndarray = np.array([])

    def predict(self, audios: AudioList[Audio]) -> AudioList[Audio]:
        for audio in audios:
            _ = self.predict_audio(audio)
        return audios

    def predict_audio(self, audio: Audio) -> AudioTokenList:
        audio[0].stream = self.stream_tokens(audio)
        return audio[0].tokens

    def stream(self, audios: AudioList[Audio]) -> Iterable[AudioToken]:
        for audio in audios:
            yield from self.stream_tokens(audio)

    def stream_tokens(self, audio_chunk: Audio) -> Iterable[AudioToken]:
        assert (
            len(audio_chunk.channels) == 1
        ), "RealtimeSpeechRecognizer only support single channel audio."
        channel = audio_chunk.channels[0]
        chunk_size = 600 * channel.sample_rate // 1000

        if channel.segments is None:
            self.buffer = np.concatenate([self.buffer, channel.waveform])
            while len(self.buffer) > chunk_size:
                chunk = self.buffer[:chunk_size]
                self.buffer = self.buffer[chunk_size:]
                stream = self.model.generate(
                    input=chunk,
                    fs=channel.sample_rate,
                    cache=self.cache,
                    is_final=False,
                    chunk_size=[0, 10, 5],  # chunk size 10 * 60ms
                    encoder_chunk_look_back=self.encoder_chunk_look_back,
                    decoder_chunk_look_back=self.decoder_chunk_look_back,
                )
                for result in stream:
                    if result["text"]:
                        yield AudioToken(text=result["text"])
            if audio_chunk.is_last:
                stream = self.model.generate(
                    input=self.buffer,
                    fs=channel.sample_rate,
                    cache=self.cache,
                    is_final=True,
                    chunk_size=[0, 10, 5],
                    encoder_chunk_look_back=self.encoder_chunk_look_back,
                    decoder_chunk_look_back=self.decoder_chunk_look_back,
                )
                for result in stream:
                    if result["text"]:
                        yield AudioToken(text=result["text"])
                self.reset()
        else:
            for seg in channel.segments:
                self.buffer = np.concatenate([self.buffer, seg.waveform])
                while len(self.buffer) > chunk_size:
                    chunk = self.buffer[:chunk_size]
                    self.buffer = self.buffer[chunk_size:]
                    stream = self.model.generate(
                        input=chunk,
                        fs=channel.sample_rate,
                        cache=self.cache,
                        is_final=False,
                        chunk_size=[0, 10, 5],
                        encoder_chunk_look_back=self.encoder_chunk_look_back,
                        decoder_chunk_look_back=self.decoder_chunk_look_back,
                    )
                    for result in stream:
                        if result["text"]:
                            yield AudioToken(text=result["text"])
                if seg.is_last:
                    stream = self.model.generate(
                        input=self.buffer,
                        fs=channel.sample_rate,
                        cache=self.cache,
                        is_final=True,
                        chunk_size=[0, 10, 5],
                        encoder_chunk_look_back=self.encoder_chunk_look_back,
                        decoder_chunk_look_back=self.decoder_chunk_look_back,
                    )
                    for result in stream:
                        if result["text"]:
                            yield AudioToken(text=result["text"])
                    self.reset()

    def reset(self):
        self.cache.clear()
        self.buffer = np.array([])

    @validate_call
    def from_checkpoint(
        self,
        checkpoint_dir: str | None = None,
        encoder_chunk_look_back: int = 4,
        decoder_chunk_look_back: int = 1,
        **kwargs,
    ):
        if not checkpoint_dir:
            self.download_checkpoint()
            checkpoint_dir = self.checkpoint_dir
        checkpoint_dir = Path(checkpoint_dir)
        if not checkpoint_dir.exists():
            raise FileNotFoundError(
                f"Checkpoint {checkpoint_dir} not found. if you want to use paraformer model, please run `fasr prepare` to download the model."
            )
        self.model = AutoModel(
            model=checkpoint_dir, disable_update=True, disable_log=True, **kwargs
        )

        self.encoder_chunk_look_back = encoder_chunk_look_back
        self.decoder_chunk_look_back = decoder_chunk_look_back
        return self
