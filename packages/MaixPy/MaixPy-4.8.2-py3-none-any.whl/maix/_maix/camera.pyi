"""
maix.camera module, access camera device and get image from it
"""
from __future__ import annotations
import maix._maix.err
import maix._maix.image
__all__ = ['Camera', 'get_device_name', 'list_devices', 'set_regs_enable']
class Camera:
    def __init__(self, width: int = -1, height: int = -1, format: maix._maix.image.Format = ..., device: str = None, fps: float = -1, buff_num: int = 3, open: bool = True, raw: bool = False) -> None:
        ...
    def add_channel(self, width: int = -1, height: int = -1, format: maix._maix.image.Format = ..., fps: float = -1, buff_num: int = 3, open: bool = True) -> Camera:
        """
        Add a new channel and return a new Camera object, you can use close() to close this channel.
        
        Args:
          - width: camera width, default is -1, means auto, mostly means max width of camera support
          - height: camera height, default is -1, means auto, mostly means max height of camera support
          - format: camera output format, default is RGB888
          - fps: camera fps, default is -1, means auto, mostly means max fps of camera support
          - buff_num: camera buffer number, default is 3, means 3 buffer, one used by user, one used for cache the next frame,
        more than one buffer will accelerate image read speed, but will cost more memory.
          - open: If true, camera will automatically call open() after creation. default is true.
        
        
        Returns: new Camera object
        """
    def awb_mode(self, value: int = -1) -> int:
        """
        Set/Get white balance mode (deprecated interface)
        
        Args:
          - value: value = 0, means set white balance to auto mode, value = 1, means set white balance to manual mode, default is auto mode.
        
        
        Returns: returns awb mode
        """
    def buff_num(self) -> int:
        """
        Get camera buffer number
        
        Returns: camera buffer number
        """
    def clear_buff(self) -> None:
        """
        Clear buff to ensure the next read image is the latest image
        """
    def close(self) -> None:
        """
        Close camera
        """
    def constrast(self, value: int = -1) -> int:
        """
        Set/Get camera constrast
        
        Args:
          - value: constrast value, range is [0, 100]
        If value == -1, returns constrast value.
        If value != 0, set and return constrast value.
        
        
        Returns: returns constrast value
        """
    def device(self) -> str:
        """
        Get camera device path
        
        Returns: camera device path
        """
    def exp_mode(self, value: int = -1) -> int:
        """
        Set/Get exposure mode (deprecated interface)
        
        Args:
          - value: value = 0, means set exposure to auto mode, value = 1, means set exposure to manual mode, default is auto mode.
        
        
        Returns: returns exposure mode
        """
    def exposure(self, value: int = -1) -> int:
        """
        Set/Get camera exposure
        
        Args:
          - value: exposure time. unit: us
        If value == -1, return exposure time.
        If value != 0, set and return exposure time.
        
        
        Returns: camera exposure time
        """
    def format(self) -> maix._maix.image.Format:
        """
        Get camera output format
        
        Returns: camera output format, image::Format object
        """
    def fps(self) -> float:
        """
        Get camera fps
        
        Returns: camera fps
        """
    def gain(self, value: int = -1) -> int:
        """
        Set/Get camera gain
        
        Args:
          - value: camera gain.
        If value == -1, returns camera gain.
        If value != 0, set and return camera gain.
        
        
        Returns: camera gain
        """
    def get_ch_nums(self) -> int:
        """
        Get the number of channels supported by the camera.
        
        Returns: Returns the maximum number of channels.
        """
    def get_channel(self) -> int:
        """
        Get channel of camera
        
        Returns: channel number
        """
    def height(self) -> int:
        """
        Get camera height
        
        Returns: camera height
        """
    def hmirror(self, value: int = -1) -> int:
        """
        Set/Get camera horizontal mirror
        
        Returns: camera horizontal mirror
        """
    def is_closed(self) -> bool:
        """
        check camera device is closed or not
        
        Returns: closed or not, bool type
        """
    def is_opened(self) -> bool:
        """
        Check if camera is opened
        
        Returns: true if camera is opened, false if not
        """
    def luma(self, value: int = -1) -> int:
        """
        Set/Get camera luma
        
        Args:
          - value: luma value, range is [0, 100]
        If value == -1, returns luma value.
        If value != 0, set and return luma value.
        
        
        Returns: returns luma value
        """
    def open(self, width: int = -1, height: int = -1, format: maix._maix.image.Format = ..., fps: float = -1, buff_num: int = -1) -> maix._maix.err.Err:
        """
        Open camera and run
        
        Args:
          - width: camera width, default is -1, means auto, mostly means max width of camera support
          - height: camera height, default is -1, means auto, mostly means max height of camera support
          - format: camera output format, default same as the constructor's format argument
          - fps: camera fps, default is -1, means auto, mostly means max fps of camera support
          - buff_num: camera buffer number, default is 3, means 3 buffer, one used by user, one used for cache the next frame,
        more than one buffer will accelerate image read speed, but will cost more memory.
        
        
        Returns: error code, err::ERR_NONE means success, others means failed
        """
    def read(self, buff: capsule = None, buff_size: int = 0, block: bool = True, block_ms: int = -1) -> maix._maix.image.Image:
        """
        Get one frame image from camera buffer, must call open method before read.
        If open method not called, will call it automatically, if open failed, will throw exception!
        So call open method before read is recommended.
        
        Args:
          - buff: buffer to store image data, if buff is nullptr, will alloc memory automatically.
        In MaixPy, default to None, you can create a image.Image object, then pass img.data() to buff.
          - block: block read, default is true, means block util read image successfully,
        if set to false, will return nullptr if no image in buffer
          - block_ms: block read timeout
        
        
        Returns: image::Image object, if failed, return nullptr, you should delete if manually in C++
        """
    def read_raw(self) -> maix._maix.image.Image:
        """
        Read the raw image and obtain the width, height, and format of the raw image through the returned Image object.
        
        Returns: image::Image object, if failed, return nullptr, you should delete if manually in C++
        """
    def read_reg(self, addr: int, bit_width: int = 8) -> int:
        """
        Read camera register
        
        Args:
          - addr: register address
          - bit_width: register data bit width, default is 8
        
        
        Returns: register data, -1 means failed
        """
    def saturation(self, value: int = -1) -> int:
        """
        Set/Get camera saturation
        
        Args:
          - value: saturation value, range is [0, 100]
        If value == -1, returns saturation value.
        If value != 0, set and return saturation value.
        
        
        Returns: returns saturation value
        """
    def set_awb(self, mode: int = -1) -> int:
        """
        Set/Get white balance mode
        
        Args:
          - value: value = 0, means set white balance to manual mode, value = 1, means set white balance to auto mode, default is auto mode.
        
        
        Returns: returns awb mode
        """
    def set_fps(self, fps: float) -> maix._maix.err.Err:
        """
        Set camera fps
        
        Args:
          - fps: new fps
        
        
        Returns: error code, err::ERR_NONE means success, others means failed
        """
    def set_resolution(self, width: int, height: int) -> maix._maix.err.Err:
        """
        Set camera resolution
        
        Args:
          - width: new width
          - height: new height
        
        
        Returns: error code, err::ERR_NONE means success, others means failed
        """
    def set_windowing(self, roi: list[int]) -> maix._maix.err.Err:
        """
        Set window size of camera
        
        Args:
          - roi: Support two input formats, [x,y,w,h] set the coordinates and size of the window;
        [w,h] set the size of the window, when the window is centred.
        
        
        Returns: error code
        """
    def show_colorbar(self, enable: bool) -> maix._maix.err.Err:
        """
        Camera output color bar image for test
        
        Args:
          - enable: enable/disable color bar
        
        
        Returns: error code, err::ERR_NONE means success, others means failed
        """
    def skip_frames(self, num: int) -> None:
        """
        Read some frames and drop, this is usually used avoid read not stable image when camera just opened.
        
        Args:
          - num: number of frames to read and drop
        """
    def vflip(self, value: int = -1) -> int:
        """
        Set/Get camera vertical flip
        
        Returns: camera vertical flip
        """
    def width(self) -> int:
        """
        Get camera width
        
        Returns: camera width
        """
    def write_reg(self, addr: int, data: int, bit_width: int = 8) -> maix._maix.err.Err:
        """
        Write camera register
        
        Args:
          - addr: register address
          - data: register data
          - bit_width: register data bit width, default is 8
        
        
        Returns: error code, err::ERR_NONE means success, others means failed
        """
def get_device_name() -> str:
    """
    Get device name. Most of the time, the returned name is the name of the sensor.
    """
def list_devices() -> list[str]:
    """
    List all supported camera devices.
    
    Returns: Returns the path to the camera device.
    """
def set_regs_enable(enable: bool = True) -> None:
    """
    Enable set camera registers, default is false, if set to true, will not set camera registers, you can manually set registers by write_reg API.
    
    Args:
      - enable: enable/disable set camera registers
    """
