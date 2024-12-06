from fasr.preprocessors.audio import FbankExtractor
from fasr.utils.read_file import read_yaml
from fasr.data import AudioList, AudioChannel, AudioSpanList, AudioSpan, Audio
from fasr.config import registry, Config
from typing import Optional, List
from fasr.components.base import BaseComponent
from fasr.components.detector.channel_encoder import ChannelEncoder
from fasr.components.detector.segment_predictor import SegmentPredictor
from pathlib import Path
from joblib import Parallel, delayed
from loguru import logger


DEFAULT_CHECKPOINT_DIR = Path(__file__).parent.parent.parent / "asset" / "fsmn-vad"


@registry.components.register("detector")
class VoiceDetector(BaseComponent):
    name: str = "detector"
    input_tags: List[str] = ["audio.channels"]
    output_tags: List[str] = ["channel.segments"]

    config: dict | None = None
    audio_preprocessor: FbankExtractor | None = None
    channel_encoder: ChannelEncoder | None = None
    segment_predictor: SegmentPredictor | None = None
    threshold: float | None = None
    num_threads: int = 1

    def predict(self, audios: AudioList[Audio]) -> AudioList[Audio]:
        _audios = self.check_audios_threshold(audios)
        all_channels = [channel for audio in _audios for channel in audio.channels]
        batch_size = max(1, len(all_channels) // self.num_threads)
        _ = Parallel(n_jobs=self.num_threads, prefer="threads", batch_size=batch_size)(
            delayed(self.predict_channel)(channel) for channel in all_channels
        )
        return audios

    def predict_audio(self, audio: Audio) -> Audio:
        num_threads = self.num_threads or len(audio.channels)
        _ = Parallel(n_jobs=num_threads, prefer="threads")(
            delayed(self.predict_channel)(channel) for channel in audio.channels
        )
        return audio

    def predict_channel(self, channel: AudioChannel) -> AudioChannel:
        channel.segments = AudioSpanList[AudioSpan]()  # 清空segments
        if channel.sample_rate != self.audio_preprocessor.fs:
            channel.resample(self.audio_preprocessor.fs)
        channel.feats = self.audio_preprocessor.process_waveform(channel.waveform)
        channel = self.channel_encoder.predict_channel(channel)
        predictor = SegmentPredictor.from_config(
            self.config["model_conf"]
        )  # 解决多线程问题
        channel = predictor.predict_channel(channel)
        return channel

    def check_audios_threshold(self, audios: AudioList) -> bool:
        new_audios = AudioList()
        # 大于threshold的音频才进行检测
        if self.threshold is not None:
            for audio in audios:
                if audio.duration > self.threshold:
                    new_audios.append(audio)
                else:
                    logger.warning(
                        f"Audio {audio.id} duration {audio.duration} < threshold {self.threshold}, skip detection"
                    )
        else:
            new_audios = audios
        return new_audios

    def from_checkpoint(
        self,
        checkpoint_dir: str | Path | None = None,
        device_id: Optional[int] = None,
        compile: bool = False,
        num_threads: int = 1,
        threshold: float = None,
    ) -> "VoiceDetector":
        if not checkpoint_dir:
            checkpoint_dir = DEFAULT_CHECKPOINT_DIR
        checkpoint_dir = Path(checkpoint_dir)
        if not checkpoint_dir.exists():
            raise FileNotFoundError(f"Checkpoint dir {checkpoint_dir} not found")
        config = read_yaml(Path(checkpoint_dir) / "config.yaml")
        self.config = config
        audio_preprocessor = FbankExtractor().from_checkpoint(
            checkpoint_dir=checkpoint_dir, compile=compile
        )
        self.audio_preprocessor = audio_preprocessor
        channel_encoder = ChannelEncoder().from_checkpoint(
            checkpoint_dir=checkpoint_dir,
            device_id=device_id,
            intra_op_num_threads=num_threads,
        )
        self.channel_encoder = channel_encoder
        self.num_threads = num_threads
        self.threshold = threshold
        return self

    def get_config(self) -> Config:
        data = {
            "component": {
                "@components": "detector",
                "config": self.config,
                "threshold": self.threshold,
                "num_threads": self.num_threads,
                "audio_preprocessor": {
                    "@audio_preprocessors": "fbank_extractor",
                    **self.audio_preprocessor.get_config()["audio_preprocessor"],
                },
                "channel_encoder": {
                    "@components": "channel_encoder",
                    **self.channel_encoder.get_config()["component"],
                },
            }
        }
        return Config(data)

    def save(self, save_dir: str) -> None:
        save_dir = Path(save_dir)
        if not save_dir.exists():
            save_dir.mkdir(parents=True)
        config = self.get_config()
        config.to_disk(save_dir / "config.cfg")
        self.audio_preprocessor.save(save_dir / "preprocessor")
        self.channel_encoder.save(save_dir / "encoder")

    def load(self, save_dir: str) -> "VoiceDetector":
        save_dir = Path(save_dir)
        config = Config().from_disk(save_dir / "config.cfg")
        detector: "VoiceDetector" = registry.resolve(config)["component"]
        detector.audio_preprocessor.load(save_dir=save_dir / "preprocessor")
        detector.channel_encoder.load(save_dir=save_dir / "encoder")
        return detector


__all__ = ["VoiceDetector"]
