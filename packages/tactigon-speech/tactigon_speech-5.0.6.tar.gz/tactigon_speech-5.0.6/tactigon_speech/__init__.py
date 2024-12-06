__version__ = "5.0.6"

__all__ = ['TSkin_Speech', 'TSkinConfig', 'AudioSource', 'HotWord', 'TSpeech', 'TSpeechObject', 'Command', 'VoiceConfig', 'Transcription',
           'Gesture', 'GestureConfig', 'Hand', 'Angle', 'Touch', 'OneFingerGesture', 'TwoFingerGesture', 'Gyro', 'Acceleration']

import logging
import time

from threading import Thread, Event
from typing import Optional
from multiprocessing import Pipe
from multiprocessing.connection import _ConnectionBase

from tactigon_gear import TSkin, TSkinConfig, Gesture, GestureConfig, Hand, Angle, Touch, OneFingerGesture, TwoFingerGesture, Gyro, Acceleration
from .middleware import Tactigon_Speech
from .models import VoiceConfig, AudioSource, Command, HotWord, TSpeech, TSpeechObject, Transcription, TSkinState, InterfaceObject


class TSkin_Speech(TSkin):
    _TICK: float = 0.02
    _audio_rx: _ConnectionBase
    source: AudioSource

    interface: Thread
    _stop_interface: Event

    tactigon_speech: Tactigon_Speech
    _transcription: Optional[Transcription] = None
    text_so_far: str = ""

    def __init__(self, config: TSkinConfig, voice: VoiceConfig, source: AudioSource = AudioSource.TSKIN, debug: bool = False):
        TSkin.__init__(self, config, debug)
        self._audio_rx, self._audio_tx = Pipe(duplex=False)
        self.tactigon_speech_pipe, self.interface_pipe = Pipe()
        self.tactigon_speech = Tactigon_Speech(voice, source, self._audio_rx, self.tactigon_speech_pipe, debug)

        self._stop_interface = Event()
        self.interface = Thread(target=self.interface_thread)

    def interface_thread(self):
        logging.debug("Starting interface thread")
        while not self._stop_interface.is_set():
            if self.interface_pipe.poll():
                data: InterfaceObject = self.interface_pipe.recv()
                current_command = data.command

                if data.payload is False:
                    logging.error("Interface pipe: error for command %s", current_command)
                    self.select_sensors()
                    continue

                if current_command is Command.RECORD:
                    logging.debug("Got RECORD filename: %s", data.payload)
                    self.select_sensors()
                elif current_command is Command.LISTEN:
                    if isinstance(data.payload, Transcription):
                        logging.debug("Got LISTEN Transcription: %s", data.payload)
                        self._transcription = data.payload
                        self.text_so_far = ""
                        self.select_sensors()
                    elif isinstance(data.payload, str):
                        logging.debug("Got LISTEN text_so_far: %s", data)
                        self.text_so_far = data.payload
                    else:
                        logging.error("Interface pipe: LISTEN error")
                        self.select_sensors()
                elif current_command is Command.PLAY:
                    if isinstance(data.payload, str):
                        logging.debug("Got PLAY filename: %s", data.payload)

                    self.select_sensors()
                elif current_command is Command.STOP:
                    logging.debug("Got STOP: %s", data.payload)
                    self.select_sensors()
            
            time.sleep(self._TICK)

    @property
    def initialized(self) -> bool:
        return self.tactigon_speech.initialized
    
    @property
    def is_recording(self) -> bool:
        return self.tactigon_speech.is_recording
    
    @property
    def is_listening(self) -> bool:
        return self.tactigon_speech.is_listening

    @property
    def is_playing(self) -> bool:
        return self.tactigon_speech.is_playing
    
    @property
    def transcription(self) -> Optional[Transcription]:
        return self._get_transcription()
    
    @property
    def state(self) -> TSkinState:
        return TSkinState(
            self.connected,
            self.battery,
            self.selector,
            self.touch,
            self.angle,
            self.gesture,
            self.transcription
        )
    
    def _get_transcription(self, preserve: bool = False):
        t = self._transcription
        if not preserve:
            self._transcription = None
        return t

    def start(self):
        self.tactigon_speech.start()
        self.interface.start()
        TSkin.start(self)

    def join(self, timeout: Optional[float] = None):
        self.stop()
        self.tactigon_speech.clear_audio_pipe()
        self.tactigon_speech.join(timeout)

        self._stop_interface.set()
        self.interface.join(timeout)
        TSkin.join(self, timeout)

    def select_sensors(self):
        TSkin.select_sensors(self)
        if self.tactigon_speech.initialized:
            self.tactigon_speech.clear_audio_pipe()

    def listen(self, speech: TSpeechObject) -> bool:
        if self.tactigon_speech.command != Command.NONE:
            return False
        
        self.tactigon_speech.clear_audio_pipe()
        self.select_audio()
        self.interface_pipe.send(speech)
        self.tactigon_speech.command = Command.LISTEN
        return True

    def play(self, filename: str) -> bool:
        if self.tactigon_speech.command != Command.NONE:
            return False
        
        self.interface_pipe.send(filename)
        self.tactigon_speech.command = Command.PLAY
        return True

    def record(self, filename: str) -> bool:
        if self.tactigon_speech.command != Command.NONE:
            return False
        
        self.tactigon_speech.clear_audio_pipe()
        self.select_audio()
        self.interface_pipe.send(filename)
        self.tactigon_speech.command = Command.RECORD
        return True

    def stop(self):
        self.tactigon_speech.command = Command.STOP