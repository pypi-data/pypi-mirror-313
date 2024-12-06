"""
maix.comm module
"""
from __future__ import annotations
import maix._maix.err
from . import modbus
__all__ = ['CommProtocol', 'add_default_comm_listener', 'modbus', 'rm_default_comm_listener']
class CommProtocol:
    def __init__(self, buff_size: int = 1024, header: int = 3148663466) -> None:
        ...
    def get_msg(self, timeout: int = 0) -> ...:
        """
        Read data to buffer, and try to decode it as maix.protocol.MSG object
        
        Args:
          - timeout: unit ms, 0 means return immediatly, -1 means block util have msg, >0 means block until have msg or timeout.
        
        
        Returns: decoded data, if nullptr, means no valid frame found.
        Attentioin, delete it after use in C++.
        """
    def report(self, cmd: int, body: maix.Bytes(bytes) = None) -> maix._maix.err.Err:
        """
        Send report message
        
        Args:
          - cmd: CMD value
          - body: report body, can be null
        
        
        Returns: encoded data, if nullptr, means error, and the error code is -err.Err.
        Attentioin, delete it after use in C++.
        """
    def resp_err(self, cmd: int, code: maix._maix.err.Err, msg: str) -> maix._maix.err.Err:
        """
        Encode response error message to buffer
        
        Args:
          - cmd: CMD value
          - code: error code
          - msg: error message
        
        
        Returns: encoded data, if nullptr, means error, and the error code is -err.Err.
        Attentioin, delete it after use in C++.
        """
    def resp_ok(self, cmd: int, body: maix.Bytes(bytes) = None) -> maix._maix.err.Err:
        """
        Send response ok(success) message
        
        Args:
          - cmd: CMD value
          - body: response body, can be null
        
        
        Returns: encoded data, if nullptr, means error, and the error code is -err.Err.
        Attentioin, delete it after use in C++.
        """
def add_default_comm_listener() -> None:
    """
    Add default CommProtocol listener.
    When the application uses this port, the listening thread will immediately
    release the port resources and exit. If you need to start the default listening thread again,
    please release the default port resources and then call this function.
    """
def rm_default_comm_listener() -> bool:
    """
    Remove default CommProtocol listener.
    
    Returns: bool type.
    """
