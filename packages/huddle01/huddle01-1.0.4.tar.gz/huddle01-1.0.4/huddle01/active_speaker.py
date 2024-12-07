from pydantic import BaseModel

from .emitter import EnhancedEventEmitter


class ActiveSpeakersOptions(BaseModel):
    size: int = 8


class ActiveSpeakers(EnhancedEventEmitter):
    def __init__(self, options: ActiveSpeakersOptions):
        self.size = options.size
