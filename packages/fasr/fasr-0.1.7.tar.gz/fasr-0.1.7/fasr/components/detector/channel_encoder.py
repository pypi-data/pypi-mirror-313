from pathlib import Path
from fasr.data import AudioChannel, AudioSpan, AudioSpanList, AudioList, Audio
from fasr.runtimes.ort import ORT
import numpy as np
from pathlib import Path
from typing import List, Optional
from joblib import Parallel, delayed
from functools import lru_cache
from fasr.config import Config, registry
from fasr.components.base import BaseComponent
from fasr.utils.read_file import read_yaml


@registry.components.register("channel_encoder")
class ChannelEncoder(BaseComponent):
    name: str = "channel_encoder"
    input_tags: List[str] = ["audio.channels"]
    output_tags: List[str] = ["channel.steps"]
    num_threads: int = 2

    n_fsmn_layers: int = None
    proj_dim: int = None
    lorder: int = None
    runtime: ORT | None = None

    def predict(self, audios: AudioList[Audio]) -> AudioList[Audio]:
        channels = Parallel(n_jobs=self.num_threads, prefer="threads")(
            delayed(self.predict_channel)(channel)
            for audio in audios
            for channel in audio.channels
        )
        return audios

    def predict_channel(self, channel: AudioChannel) -> AudioChannel:
        if channel.feats is None:
            return channel
        steps = AudioSpanList[AudioSpan]()
        in_cache = self.prepare_cache()
        feats = channel.feats[None, :].astype(np.float32)
        feats_len = feats.shape[1]
        waveform = np.array(channel.waveform)[None, :].astype(np.float32)
        t_offset = 0
        step = int(min(feats_len, 6000))
        for t_offset in range(0, int(feats_len), min(step, feats_len - t_offset)):
            if t_offset + step >= feats_len - 1:
                step = feats_len - t_offset
            feats_package = feats[:, t_offset : int(t_offset + step), :]
            waveform_package = waveform[
                :,
                t_offset * 160 : min(
                    waveform.shape[-1], (int(t_offset + step) - 1) * 160 + 400
                ),
            ]
            inputs = [feats_package]
            inputs.extend(in_cache)
            # cache [cache1, cache2, cache3, cache4]
            outputs = self.runtime.run(inputs)
            scores, out_caches = outputs[0], outputs[1:]
            steps.append(
                AudioSpan(waveform=waveform_package, feats=feats_package, scores=scores)
            )
            in_cache = out_caches
        channel.steps = steps
        return channel

    @lru_cache(maxsize=1)
    def prepare_cache(self):
        """Prepare cache for FSMN model.

        Returns:
            List: List of cache for FSMN model. shape = (n_layers, proj_dim, lorder - 1, 1)
        """
        in_cache = []
        for i in range(self.n_fsmn_layers):
            cache = np.zeros((1, self.proj_dim, self.lorder - 1, 1)).astype(np.float32)
            in_cache.append(cache)
        return in_cache

    def from_checkpoint(
        self,
        checkpoint_dir: str = "checkpoints/iic/speech_fsmn_vad_zh-cn-16k-common-pytorch",
        device_id: Optional[int] = None,
        intra_op_num_threads: int = 2,
        num_threads: int = 2,
    ) -> "ChannelEncoder":
        config = read_yaml(Path(checkpoint_dir, "config.yaml"))
        encoder_config = config["encoder_conf"]
        self.n_fsmn_layers = encoder_config["fsmn_layers"]
        self.proj_dim = encoder_config["proj_dim"]
        self.lorder = encoder_config["lorder"]
        runtime = ORT().from_checkpoint(
            checkpoint_dir=checkpoint_dir,
            device_id=device_id,
            intra_op_num_threads=intra_op_num_threads,
        )
        self.runtime = runtime
        self.num_threads = num_threads
        return self

    def get_config(self) -> Config:
        data = {
            "component": {
                "@components": "channel_encoder",
                "n_fsmn_layers": self.n_fsmn_layers,
                "proj_dim": self.proj_dim,
                "lorder": self.lorder,
            }
        }
        return Config(data)

    def save(self, save_dir: str = "channel_encoder") -> None:
        save_dir = Path(save_dir)
        if not save_dir.exists():
            save_dir.mkdir(parents=True)
        config = self.get_config()
        config.to_disk(save_dir / "config.cfg")
        self.runtime.save(save_dir / "runtime")

    def load(self, save_dir: str = "channel_encoder") -> "ChannelEncoder":
        save_dir = Path(save_dir)
        config = Config().from_disk(save_dir / "config.cfg")
        channel_encoder: "ChannelEncoder" = registry.resolve(config)["component"]
        runtime = ORT().load(save_dir / "runtime")
        self.n_fsmn_layers = channel_encoder.n_fsmn_layers
        self.proj_dim = channel_encoder.proj_dim
        self.lorder = channel_encoder.lorder
        self.runtime = runtime
        return self

    def __hash__(self):
        return hash(f"{self.n_fsmn_layers}-{self.proj_dim}-{self.lorder}")
