from fasr.components.base import BaseComponent
from typing import List, Dict
from funasr import AutoModel
from pydantic import Field
from fasr.data.audio import Audio, AudioList, AudioSpanList, AudioSpan
from fasr.config import registry
from pathlib import Path
from fasr.components.detector import DEFAULT_CHECKPOINT_DIR


@registry.components.register("online_detector")
class OnlineVoiceDetector(BaseComponent):
    name: str = "online_detector"
    input_tags: List[str] = ["audio.channels"]
    output_tags: List[str] = ["channel.segments"]

    model: AutoModel | None = Field(
        None, description="The model to use for voice detection"
    )
    cache: Dict = {}
    is_detected: bool = False
    offset: int = 0

    def predict(self, audios: AudioList) -> AudioList:
        for audio in audios:
            audio = self.predict_audio(audio)
        return audios

    def predict_audio(self, audio: Audio) -> Audio:
        assert (
            len(audio.channels) == 1
        ), "OnlineVoiceDetector only supports single channel audio"

        channel = audio.channels[0]
        chunk_size_ms = channel.duration_ms
        segments = self.model.generate(
            input=channel.waveform,
            fs=channel.sample_rate,
            chunk_size=chunk_size_ms,
            is_final=audio.is_last,
            cache=self.cache,
        )[0]["value"]
        channel_segments = AudioSpanList[AudioSpan]()
        if len(segments) > 0:
            for segment in segments:
                start, end = segment
                if start != -1 and end == -1:
                    self.is_detected = True
                    start_idx = start * channel.sample_rate // 1000 - self.offset
                    end_idx = len(channel.waveform)
                    segment_waveform = channel.waveform[start_idx:end_idx]
                    channel_segments.append(
                        AudioSpan(
                            start_ms=start,
                            end_ms=end,
                            waveform=segment_waveform,
                            sample_rate=channel.sample_rate,
                            is_last=audio.is_last,
                        )
                    )

                if start == -1 and end != -1:
                    self.is_detected = False
                    start_idx = 0
                    end_idx = end * channel.sample_rate // 1000 - self.offset
                    segment_waveform = channel.waveform[start_idx:end_idx]
                    channel_segments.append(
                        AudioSpan(
                            start_ms=start,
                            end_ms=end,
                            waveform=segment_waveform,
                            sample_rate=channel.sample_rate,
                            is_last=audio.is_last,
                        )
                    )

                if start != -1 and end != -1:
                    self.is_detected = False
                    start_idx = start * channel.sample_rate // 1000 - self.offset
                    end_idx = end * channel.sample_rate // 1000 - self.offset
                    segment_waveform = channel.waveform[start_idx:end_idx]
                    channel_segments.append(
                        AudioSpan(
                            start_ms=start,
                            end_ms=end,
                            waveform=segment_waveform,
                            sample_rate=channel.sample_rate,
                            is_last=audio.is_last,
                        )
                    )
        else:
            if self.is_detected:
                channel_segments.append(
                    AudioSpan(
                        start_ms=-1,
                        end_ms=-1,
                        waveform=channel.waveform,
                        sample_rate=channel.sample_rate,
                        is_last=False,
                    )
                )

        self.offset += len(channel.waveform)
        channel.segments = channel_segments
        return audio

    def reset(self):
        self.cache = {}
        self.is_detected = False
        self.offset = 0

    def from_checkpoint(
        self,
        checkpoint_dir: str | Path | None = None,
        **kwargs,
    ) -> "OnlineVoiceDetector":
        if not checkpoint_dir:
            checkpoint_dir = DEFAULT_CHECKPOINT_DIR
        if isinstance(checkpoint_dir, str):
            checkpoint_dir = Path(checkpoint_dir)
        if not checkpoint_dir.exists():
            raise FileNotFoundError(f"Checkpoint dir {checkpoint_dir} not found")
        self.model = AutoModel(
            model=checkpoint_dir,
            disable_update=True,
            disable_log=True,
            disable_pbar=True,
            **kwargs,
        )
        return self
