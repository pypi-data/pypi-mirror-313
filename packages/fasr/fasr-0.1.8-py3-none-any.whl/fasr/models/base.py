from fasr.data.audio import (
    Audio,
    AudioList,
    AudioChannel,
    AudioChannelList,
    AudioSpan,
    AudioSpanList,
    AudioToken,
    AudioTokenList,
)
from fasr.config import Config


class BaseModel:
    def predict_on_audio(self, audios: AudioList[Audio]) -> AudioList[Audio]:
        raise NotImplementedError

    def predict_on_channel(
        self, channels: AudioChannelList[AudioChannel]
    ) -> AudioChannelList[AudioChannel]:
        raise NotImplementedError

    def predict_on_segment(
        self, spans: AudioSpanList[AudioSpan]
    ) -> AudioSpanList[AudioSpan]:
        raise NotImplementedError

    def predict_on_token(
        self, tokens: AudioTokenList[AudioToken]
    ) -> AudioTokenList[AudioToken]:
        raise NotImplementedError

    def get_config(self) -> Config:
        raise NotImplementedError
