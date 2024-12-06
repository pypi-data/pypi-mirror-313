from fasr.utils.base import SerializableMixin
from pydantic import ConfigDict


class BaseRuntime(SerializableMixin):
    model_config: ConfigDict = ConfigDict(arbitrary_types_allowed=True)

    def run(self, **kwargs):
        raise NotImplementedError
