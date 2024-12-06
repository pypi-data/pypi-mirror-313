"""
maix.audio module
"""
from __future__ import annotations
import maix._maix.err
import typing
__all__ = ['Format', 'Player', 'Recorder']
class Format:
    """
    Members:
    
      FMT_NONE
    
      FMT_S8
    
      FMT_S16_LE
    
      FMT_S32_LE
    
      FMT_S16_BE
    
      FMT_S32_BE
    
      FMT_U8
    
      FMT_U16_LE
    
      FMT_U32_LE
    
      FMT_U16_BE
    
      FMT_U32_BE
    """
    FMT_NONE: typing.ClassVar[Format]  # value = <Format.FMT_NONE: 0>
    FMT_S16_BE: typing.ClassVar[Format]  # value = <Format.FMT_S16_BE: 4>
    FMT_S16_LE: typing.ClassVar[Format]  # value = <Format.FMT_S16_LE: 2>
    FMT_S32_BE: typing.ClassVar[Format]  # value = <Format.FMT_S32_BE: 5>
    FMT_S32_LE: typing.ClassVar[Format]  # value = <Format.FMT_S32_LE: 3>
    FMT_S8: typing.ClassVar[Format]  # value = <Format.FMT_S8: 1>
    FMT_U16_BE: typing.ClassVar[Format]  # value = <Format.FMT_U16_BE: 9>
    FMT_U16_LE: typing.ClassVar[Format]  # value = <Format.FMT_U16_LE: 7>
    FMT_U32_BE: typing.ClassVar[Format]  # value = <Format.FMT_U32_BE: 10>
    FMT_U32_LE: typing.ClassVar[Format]  # value = <Format.FMT_U32_LE: 8>
    FMT_U8: typing.ClassVar[Format]  # value = <Format.FMT_U8: 6>
    __members__: typing.ClassVar[dict[str, Format]]  # value = {'FMT_NONE': <Format.FMT_NONE: 0>, 'FMT_S8': <Format.FMT_S8: 1>, 'FMT_S16_LE': <Format.FMT_S16_LE: 2>, 'FMT_S32_LE': <Format.FMT_S32_LE: 3>, 'FMT_S16_BE': <Format.FMT_S16_BE: 4>, 'FMT_S32_BE': <Format.FMT_S32_BE: 5>, 'FMT_U8': <Format.FMT_U8: 6>, 'FMT_U16_LE': <Format.FMT_U16_LE: 7>, 'FMT_U32_LE': <Format.FMT_U32_LE: 8>, 'FMT_U16_BE': <Format.FMT_U16_BE: 9>, 'FMT_U32_BE': <Format.FMT_U32_BE: 10>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class Player:
    def __init__(self, path: str = '', sample_rate: int = 48000, format: Format = ..., channel: int = 1) -> None:
        ...
    def channel(self) -> int:
        """
        Get sample channel
        
        Returns: returns sample channel
        """
    def format(self) -> Format:
        """
        Get sample format
        
        Returns: returns sample format
        """
    def play(self, data: maix.Bytes(bytes) = b'') -> maix._maix.err.Err:
        """
        Play
        
        Args:
          - data: audio data, must be raw data
        
        
        Returns: error code, err::ERR_NONE means success, others means failed
        """
    def sample_rate(self) -> int:
        """
        Get sample rate
        
        Returns: returns sample rate
        """
    def volume(self, value: int = -1) -> int:
        """
        Set/Get player volume
        
        Args:
          - value: volume value, If you use this parameter, audio will set the value to volume,
        if you don't, it will return the current volume. range is [0, 100].
        
        
        Returns: the current volume
        """
class Recorder:
    @staticmethod
    def record(*args, **kwargs):
        """
        Record, Read all cached data in buffer and return. If there is no audio data in the buffer, may return empty data.
        
        Args:
          - record_ms: Block and record audio data lasting `record_ms` milliseconds and save it to a file, the return value does not return audio data. Only valid if the initialisation `path` is set.
        
        
        Returns: pcm data. datatype @see Bytes. If you pass in record_ms parameter, the return value is an empty Bytes object.
        """
    def __init__(self, path: str = '', sample_rate: int = 48000, format: Format = ..., channel: int = 1) -> None:
        ...
    def channel(self) -> int:
        """
        Get sample channel
        
        Returns: returns sample channel
        """
    def finish(self) -> maix._maix.err.Err:
        """
        Finish the record, if you have passed in the path, this api will save the audio data to file.
        
        Returns: error code, err::ERR_NONE means success, others means failed
        """
    def format(self) -> Format:
        """
        Get sample format
        
        Returns: returns sample format
        """
    def mute(self, data: int = -1) -> bool:
        """
        Mute
        
        Args:
          - data: mute data, If you set this parameter to true, audio will set the value to mute,
        if you don't, it will return the current mute status.
        
        
        Returns: Returns whether mute is currently enabled.
        """
    def sample_rate(self) -> int:
        """
        Get sample rate
        
        Returns: returns sample rate
        """
    def volume(self, value: int = -1) -> int:
        """
        Set/Get record volume
        
        Args:
          - value: volume value, If you use this parameter, audio will set the value to volume,
        if you don't, it will return the current volume. range is [0, 100].
        
        
        Returns: the current volume
        """
