from .base import BaseComponent
from fasr.data.audio import (
    AudioSpanList,
    AudioSpan,
    AudioTokenList,
    AudioChannel,
    AudioList,
    Audio,
)
from fasr.config import registry
from funasr import AutoModel
from joblib import Parallel, delayed
from typing import List


@registry.components.register("sentencizer")
@registry.components.register("punctuator")
class SpeechSentencizer(BaseComponent):
    """将语音片段转换为句子级别"""

    name: str = "sentencizer"
    input_tags: List[str] = ["segment.tokens"]
    output_tags: List[str] = ["channel.sents"]
    checkpoint: str = "iic/punc_ct-transformer_zh-cn-common-vocab272727-pytorch"

    model: AutoModel | None = None
    num_threads: int = 1

    def predict(self, audios: AudioList[Audio]) -> AudioList[Audio]:
        try:
            channels = []
            for audio in audios:
                if audio.channels is not None:
                    channels.extend(audio.channels)
            _ = Parallel(n_jobs=self.num_threads, prefer="threads")(
                delayed(self.predict_channel)(channel) for channel in channels
            )
        except Exception as e:
            for audio in audios:
                audio.is_bad = True
                audio.bad_reason = str(e)
                audio.bad_component = self.name
        return audios

    def predict_channel(self, channel: AudioChannel):
        sents = AudioSpanList[AudioSpan]()
        if channel.segments is None:
            return
        all_tokens = []
        for seg in channel.segments:
            if seg.tokens is not None:
                all_tokens.extend(seg.tokens)
        text = " ".join([token.text for token in all_tokens])
        if text.strip() != "":
            res = self.model.generate(text)[0]
            punc_array = res.get("punc_array", []).tolist()
            assert len(all_tokens) == len(
                punc_array
            ), f"{len(all_tokens)} != {len(punc_array)}"
            sent_tokens = []
            for i, punc_res in enumerate(punc_array):
                all_tokens[i].follow = self.id_to_punc(punc_res)
                if punc_res == 1:
                    sent_tokens.append(all_tokens[i])
                else:
                    sent_tokens.append(all_tokens[i])
                    sents.append(
                        AudioSpan(
                            start_ms=sent_tokens[0].start_ms,
                            end_ms=sent_tokens[-1].end_ms,
                            tokens=AudioTokenList(docs=sent_tokens),
                        )
                    )
                    sent_tokens = []
            if len(sent_tokens) > 0:
                sents.append(
                    AudioSpan(
                        start_ms=sent_tokens[0].start_ms,
                        end_ms=sent_tokens[-1].end_ms,
                        tokens=AudioTokenList(docs=sent_tokens),
                    )
                )
        channel.sents = sents
        return channel

    def predict_text(self, text: str) -> dict:
        return self.model.generate(text)[0]

    def id_to_punc(self, id: int):
        punc_list = []
        for pun in self.model.model.punc_list:
            if pun == "_":
                pun = ""
            punc_list.append(pun)
        id2punc = {i: punc for i, punc in enumerate(punc_list)}
        return id2punc[id]

    def from_checkpoint(
        self,
        checkpoint_dir: str | None = None,
        num_threads: int = 1,
        **kwargs,
    ):
        """从funasr模型目录加载组件

        Args:
            checkpoint_dir (str, optional): 模型目录. Defaults to "checkpoints/iic/punc_ct-transformer_zh-cn-common-vocab272727-pytorch".
            num_threads (int, optional): 并行线程数. Defaults to 1.
        """
        if not checkpoint_dir:
            self.download_checkpoint()
            checkpoint_dir = self.checkpoint_dir
        model = AutoModel(model=checkpoint_dir, disable_update=True, **kwargs)
        self.model = model
        self.num_threads = num_threads
        return self
