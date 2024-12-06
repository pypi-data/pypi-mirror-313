from os import path
from dataclasses import dataclass
from enum import Enum

from typing import List, Optional, Union
from tactigon_gear import TSkinState as OldTSkinState

def get_or_default(json: dict, name: str, default):
    try:
        return json[name]
    except:
        return default

@dataclass
class HotWord:
    word: str
    boost: int = 1

    @classmethod
    def FromJSON(cls, config):
        return cls(config["word"], config["boost"])
    
    def toJSON(self) -> object:
        return {
            "word": self.word,
            "boost": self.boost
        }

class TSpeech:
    hotwords: List[HotWord]
    children: Optional["TSpeechObject"]

    def __init__(self, hotwords: Union[List[HotWord], HotWord], children: Optional["TSpeechObject"] = None):
        self.hotwords = hotwords if isinstance(hotwords, list) else [hotwords]
        self.children = children

    @classmethod
    def FromJSON(cls, json_obj, feedback_audio_path = ""):
        try:
            children = json_obj["children"]
        except:
            children = None

        return cls(
            [HotWord.FromJSON(hw) for hw in json_obj["hotwords"]],
            children=TSpeechObject.FromJSON(children, feedback_audio_path) if children else None,
        )

    @property
    def has_children(self):
        return self.children
    
    def toJSON(self) -> dict:
        return {
            "hotwords": [hw.toJSON() for hw in self.hotwords],
            "children": self.children.toJSON() if self.children else None
        }

class TSpeechObject:
    t_speech: List[TSpeech]
    feedback: str

    def __init__(self, t_speech: List[TSpeech], feedback: str = ""):
        self.t_speech = t_speech
        self.feedback = feedback

    @classmethod
    def FromJSON(cls, json_obj, feedback_audio_path = ""):

        try:
            feedback = path.join(feedback_audio_path, json_obj["feedback"])
        except:
            feedback = ""

        return cls(
            [TSpeech.FromJSON(t, feedback_audio_path) for t in json_obj["t_speech"]],
            feedback=feedback
        )
    
    def toJSON(self) -> dict:
        return {
            "t_speech": [ts.toJSON() for ts in self.t_speech],
            "feedback": self.feedback
        }

class TStreamStatus(Enum):
    STREAMING = 1
    STOPPED = 2

class AudioSource(Enum):
    MIC = 1
    TSKIN = 2

class Command(Enum):
    NOT_INITIALIZED = -1
    NONE = 0
    LISTEN = 1
    STOP = 2
    PLAY = 3
    RECORD = 98
    END = 99

@dataclass
class Transcription:
    text: str
    path: Optional[List[HotWord]]
    time: float
    timeout: bool

    def toJSON(self) -> object:
        return {
            "text": self.text,
            "path": [hw.toJSON() for hw in self.path] if self.path else None,
            "time": self.time,
            "timeout": self.timeout
        }
    
@dataclass
class InterfaceObject:
    command: Command
    payload: Union[Transcription, str, bool]

@dataclass
class VoiceConfig:
    model: str
    scorer: Optional[str] = None

    vad_aggressiveness: int = 3
    vad_padding_ms: int = 800
    vad_ratio: float = 0.6
    vad_frame: int = 20
    beam_width: int = 1024

    min_sample_len: int = 180

    voice_timeout: int = 5
    silence_timeout: int = 5

    stop_hotword: Optional[HotWord] = None

    @property
    def model_full_path(self) -> str:
        return path.join(self.model)
    
    @property
    def scorer_full_path(self) -> Optional[str]:
        if self.scorer is None:
            return None
        
        return path.join(self.scorer)

    @classmethod
    def FromJSON(cls, json: dict):
        return cls(
            json["model"],
            get_or_default(json, "scorer", cls.scorer),
            get_or_default(json, "vad_aggressiveness", cls.vad_aggressiveness),
            get_or_default(json, "vad_padding_ms", cls.vad_padding_ms),
            get_or_default(json, "vad_ratio", cls.vad_ratio),
            get_or_default(json, "vad_frame", cls.vad_frame),
            get_or_default(json, "beam_width", cls.beam_width),
            get_or_default(json, "min_sample_len", cls.min_sample_len),
            get_or_default(json, "voice_timeout", cls.voice_timeout),
            get_or_default(json, "silence_timeout", cls.silence_timeout),
        )
    
    def toJSON(self) -> dict:
        return {
            "model": self.model,
            "scorer": self.scorer,
            "vad_aggressiveness": self.vad_aggressiveness,
            "vad_padding_ms": self.vad_padding_ms,
            "vad_ratio": self.vad_ratio,
            "vad_frame": self.vad_frame,
            "beam_width": self.beam_width,
            "min_sample_len": self.min_sample_len,
            "voice_timeout": self.voice_timeout,
            "silence_timeout": self.silence_timeout
        }
    
@dataclass
class TSkinState(OldTSkinState):
    transcription: Optional[Transcription]

    def toJSON(self) -> dict:
        obj = OldTSkinState.toJSON(self)
        obj["transcription"] = self.transcription.toJSON() if self.transcription else None
        return obj