from pathlib import Path
from fasr.data import AudioList, Audio, AudioChannel
from pathlib import Path
from typing import List
from joblib import Parallel, delayed
from fasr.config import Config, registry
from fasr.components.base import BaseComponent
from fasr.preprocessors.audio import FbankExtractor, BaseAudioPreprocessor


@registry.components.register("feature_extractor")
class FeatureExtractor(BaseComponent):
    """this component is responsible for extracting features from the audio signal. it takes the waveform of the audio channel as input and returns the extracted features as output. the component is parallelized to process multiple channels at the same time. the component is also configurable to use different feature extractors.

    Args:
        num_threads (int): the number of threads to use for parallel processing. Defaults to 2.
        preprocessor (BaseAudioPreprocessor): the feature extractor to use. Defaults to None.

    Input Tags:
        channel.waveform: the waveform of the audio channel.

    Output Tags:
        channel.feats: the extracted features of the audio channel.
    """

    name: str = "feature_extractor"
    input_tags: List[str] = ["channel.waveform"]
    output_tags: List[str] = ["channel.feats"]

    num_threads: int = 2
    audio_preprocessor: BaseAudioPreprocessor | None = None

    def predict(self, audios: AudioList[Audio]) -> AudioList[Audio]:
        channels = Parallel(n_jobs=self.num_threads, prefer="threads")(
            delayed(self.predict_channel)(channel)
            for audio in audios
            for channel in audio.channels
        )
        return audios

    def predict_channel(self, channel: AudioChannel) -> AudioChannel:
        channel.feats = self.audio_preprocessor.process_waveform(channel.waveform)
        return channel

    def get_config(self) -> Config:
        data = {
            "component": {
                "@components": "feature_extractor",
                "num_threads": self.num_threads,
                **self.audio_preprocessor.get_config(),
            }
        }
        return Config(data)

    def save(self, save_dir: str = "feature_extractor") -> None:
        save_dir: Path = Path(save_dir)
        if not save_dir.exists():
            save_dir.mkdir(parents=True)
        config = self.get_config()
        config.to_disk(save_dir / "config.cfg")
        self.audio_preprocessor.save(save_dir=save_dir / "audio_preprocessor")

    def load(self, save_dir: str = "feature_extractor") -> "FeatureExtractor":
        save_dir = Path(save_dir)
        config = Config().from_disk(save_dir / "config.cfg")
        feature_extractor: "FeatureExtractor" = registry.resolve(config=config)[
            "component"
        ]
        self.num_threads = feature_extractor.num_threads
        self.audio_preprocessor = feature_extractor.audio_preprocessor.load(
            save_dir / "audio_preprocessor"
        )
        return self

    def from_checkpoint(self, checkpoint_dir: str, **kwargs) -> "FeatureExtractor":
        if not self.audio_preprocessor:
            self.audio_preprocessor = FbankExtractor().from_checkpoint(checkpoint_dir)
        else:
            self.audio_preprocessor = self.audio_preprocessor().from_checkpoint(
                checkpoint_dir
            )
        return self
