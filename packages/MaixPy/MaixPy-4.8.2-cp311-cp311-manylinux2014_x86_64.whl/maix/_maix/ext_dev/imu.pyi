"""
maix.ext_dev.imu module
"""
from __future__ import annotations
import maix._maix.err
import typing
__all__ = ['AccOdr', 'AccScale', 'Gcsv', 'GyroOdr', 'GyroScale', 'IMU', 'Mode']
class AccOdr:
    """
    Members:
    
      ACC_ODR_8000
    
      ACC_ODR_4000
    
      ACC_ODR_2000
    
      ACC_ODR_1000
    
      ACC_ODR_500
    
      ACC_ODR_250
    
      ACC_ODR_125
    
      ACC_ODR_62_5
    
      ACC_ODR_31_25
    
      ACC_ODR_128
    
      ACC_ODR_21
    
      ACC_ODR_11
    
      ACC_ODR_3
    """
    ACC_ODR_1000: typing.ClassVar[AccOdr]  # value = <AccOdr.ACC_ODR_1000: 3>
    ACC_ODR_11: typing.ClassVar[AccOdr]  # value = <AccOdr.ACC_ODR_11: 14>
    ACC_ODR_125: typing.ClassVar[AccOdr]  # value = <AccOdr.ACC_ODR_125: 6>
    ACC_ODR_128: typing.ClassVar[AccOdr]  # value = <AccOdr.ACC_ODR_128: 12>
    ACC_ODR_2000: typing.ClassVar[AccOdr]  # value = <AccOdr.ACC_ODR_2000: 2>
    ACC_ODR_21: typing.ClassVar[AccOdr]  # value = <AccOdr.ACC_ODR_21: 13>
    ACC_ODR_250: typing.ClassVar[AccOdr]  # value = <AccOdr.ACC_ODR_250: 5>
    ACC_ODR_3: typing.ClassVar[AccOdr]  # value = <AccOdr.ACC_ODR_3: 15>
    ACC_ODR_31_25: typing.ClassVar[AccOdr]  # value = <AccOdr.ACC_ODR_31_25: 8>
    ACC_ODR_4000: typing.ClassVar[AccOdr]  # value = <AccOdr.ACC_ODR_4000: 1>
    ACC_ODR_500: typing.ClassVar[AccOdr]  # value = <AccOdr.ACC_ODR_500: 4>
    ACC_ODR_62_5: typing.ClassVar[AccOdr]  # value = <AccOdr.ACC_ODR_62_5: 7>
    ACC_ODR_8000: typing.ClassVar[AccOdr]  # value = <AccOdr.ACC_ODR_8000: 0>
    __members__: typing.ClassVar[dict[str, AccOdr]]  # value = {'ACC_ODR_8000': <AccOdr.ACC_ODR_8000: 0>, 'ACC_ODR_4000': <AccOdr.ACC_ODR_4000: 1>, 'ACC_ODR_2000': <AccOdr.ACC_ODR_2000: 2>, 'ACC_ODR_1000': <AccOdr.ACC_ODR_1000: 3>, 'ACC_ODR_500': <AccOdr.ACC_ODR_500: 4>, 'ACC_ODR_250': <AccOdr.ACC_ODR_250: 5>, 'ACC_ODR_125': <AccOdr.ACC_ODR_125: 6>, 'ACC_ODR_62_5': <AccOdr.ACC_ODR_62_5: 7>, 'ACC_ODR_31_25': <AccOdr.ACC_ODR_31_25: 8>, 'ACC_ODR_128': <AccOdr.ACC_ODR_128: 12>, 'ACC_ODR_21': <AccOdr.ACC_ODR_21: 13>, 'ACC_ODR_11': <AccOdr.ACC_ODR_11: 14>, 'ACC_ODR_3': <AccOdr.ACC_ODR_3: 15>}
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
class AccScale:
    """
    Members:
    
      ACC_SCALE_2G
    
      ACC_SCALE_4G
    
      ACC_SCALE_8G
    
      ACC_SCALE_16G
    """
    ACC_SCALE_16G: typing.ClassVar[AccScale]  # value = <AccScale.ACC_SCALE_16G: 3>
    ACC_SCALE_2G: typing.ClassVar[AccScale]  # value = <AccScale.ACC_SCALE_2G: 0>
    ACC_SCALE_4G: typing.ClassVar[AccScale]  # value = <AccScale.ACC_SCALE_4G: 1>
    ACC_SCALE_8G: typing.ClassVar[AccScale]  # value = <AccScale.ACC_SCALE_8G: 2>
    __members__: typing.ClassVar[dict[str, AccScale]]  # value = {'ACC_SCALE_2G': <AccScale.ACC_SCALE_2G: 0>, 'ACC_SCALE_4G': <AccScale.ACC_SCALE_4G: 1>, 'ACC_SCALE_8G': <AccScale.ACC_SCALE_8G: 2>, 'ACC_SCALE_16G': <AccScale.ACC_SCALE_16G: 3>}
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
class Gcsv:
    def __init__(self) -> None:
        ...
    def close(self) -> maix._maix.err.Err:
        """
        Close file
        
        Returns: error code
        """
    def is_opened(self) -> bool:
        """
        Check if the object is already open
        
        Returns: true, opened; false, not opened
        """
    def open(self, path: str, tscale: float = 0.001, gscale: float = 1, ascale: float = 1, mscale: float = 1, version: str = '1.3', id: str = 'imu', orientation: str = 'YxZ') -> maix._maix.err.Err:
        """
        Open a file
        
        Args:
          - path: the path where data will be saved
          - tscale: time scale, default is 0.001
          - gscale: gyroscope scale factor, default is 1, unit:g
          - ascale: accelerometer scale factor, default is 1, unit:radians/second
          - mscale: magnetometer scale factor, default is 1(unused)
          - version: version number, default is "1.3"
          - id: identifier for the IMU, default is "imu"
          - orientation: sensor orientation, default is "YxZ"
        
        
        Returns: error code
        """
    def write(self, timestamp: float, gyro: list[float], acc: list[float], mag: list[float] = []) -> maix._maix.err.Err:
        """
        Write imu data to gcsv file
        
        Args:
          - t: Timestamp of the current data. The actual value is equal to t * tscale. unit:s
          - gyro: Gyroscope data must be an array consisting of x, y, and z-axis data. The actual value is equal to gyro * gscale. unit:g
          - acc: Acceleration data must be an array consisting of x, y, and z-axis data. The actual value is equal to acc * ascale.unit:radians/second
          - mag: Magnetic data must be an array consisting of x, y, and z-axis data. Currently not supported.
        """
class GyroOdr:
    """
    Members:
    
      GYRO_ODR_8000
    
      GYRO_ODR_4000
    
      GYRO_ODR_2000
    
      GYRO_ODR_1000
    
      GYRO_ODR_500
    
      GYRO_ODR_250
    
      GYRO_ODR_125
    
      GYRO_ODR_62_5
    
      GYRO_ODR_31_25
    """
    GYRO_ODR_1000: typing.ClassVar[GyroOdr]  # value = <GyroOdr.GYRO_ODR_1000: 3>
    GYRO_ODR_125: typing.ClassVar[GyroOdr]  # value = <GyroOdr.GYRO_ODR_125: 6>
    GYRO_ODR_2000: typing.ClassVar[GyroOdr]  # value = <GyroOdr.GYRO_ODR_2000: 2>
    GYRO_ODR_250: typing.ClassVar[GyroOdr]  # value = <GyroOdr.GYRO_ODR_250: 5>
    GYRO_ODR_31_25: typing.ClassVar[GyroOdr]  # value = <GyroOdr.GYRO_ODR_31_25: 8>
    GYRO_ODR_4000: typing.ClassVar[GyroOdr]  # value = <GyroOdr.GYRO_ODR_4000: 1>
    GYRO_ODR_500: typing.ClassVar[GyroOdr]  # value = <GyroOdr.GYRO_ODR_500: 4>
    GYRO_ODR_62_5: typing.ClassVar[GyroOdr]  # value = <GyroOdr.GYRO_ODR_62_5: 7>
    GYRO_ODR_8000: typing.ClassVar[GyroOdr]  # value = <GyroOdr.GYRO_ODR_8000: 0>
    __members__: typing.ClassVar[dict[str, GyroOdr]]  # value = {'GYRO_ODR_8000': <GyroOdr.GYRO_ODR_8000: 0>, 'GYRO_ODR_4000': <GyroOdr.GYRO_ODR_4000: 1>, 'GYRO_ODR_2000': <GyroOdr.GYRO_ODR_2000: 2>, 'GYRO_ODR_1000': <GyroOdr.GYRO_ODR_1000: 3>, 'GYRO_ODR_500': <GyroOdr.GYRO_ODR_500: 4>, 'GYRO_ODR_250': <GyroOdr.GYRO_ODR_250: 5>, 'GYRO_ODR_125': <GyroOdr.GYRO_ODR_125: 6>, 'GYRO_ODR_62_5': <GyroOdr.GYRO_ODR_62_5: 7>, 'GYRO_ODR_31_25': <GyroOdr.GYRO_ODR_31_25: 8>}
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
class GyroScale:
    """
    Members:
    
      GYRO_SCALE_16DPS
    
      GYRO_SCALE_32DPS
    
      GYRO_SCALE_64DPS
    
      GYRO_SCALE_128DPS
    
      GYRO_SCALE_256DPS
    
      GYRO_SCALE_512DPS
    
      GYRO_SCALE_1024DPS
    
      GYRO_SCALE_2048DPS
    """
    GYRO_SCALE_1024DPS: typing.ClassVar[GyroScale]  # value = <GyroScale.GYRO_SCALE_1024DPS: 6>
    GYRO_SCALE_128DPS: typing.ClassVar[GyroScale]  # value = <GyroScale.GYRO_SCALE_128DPS: 3>
    GYRO_SCALE_16DPS: typing.ClassVar[GyroScale]  # value = <GyroScale.GYRO_SCALE_16DPS: 0>
    GYRO_SCALE_2048DPS: typing.ClassVar[GyroScale]  # value = <GyroScale.GYRO_SCALE_2048DPS: 7>
    GYRO_SCALE_256DPS: typing.ClassVar[GyroScale]  # value = <GyroScale.GYRO_SCALE_256DPS: 4>
    GYRO_SCALE_32DPS: typing.ClassVar[GyroScale]  # value = <GyroScale.GYRO_SCALE_32DPS: 1>
    GYRO_SCALE_512DPS: typing.ClassVar[GyroScale]  # value = <GyroScale.GYRO_SCALE_512DPS: 5>
    GYRO_SCALE_64DPS: typing.ClassVar[GyroScale]  # value = <GyroScale.GYRO_SCALE_64DPS: 2>
    __members__: typing.ClassVar[dict[str, GyroScale]]  # value = {'GYRO_SCALE_16DPS': <GyroScale.GYRO_SCALE_16DPS: 0>, 'GYRO_SCALE_32DPS': <GyroScale.GYRO_SCALE_32DPS: 1>, 'GYRO_SCALE_64DPS': <GyroScale.GYRO_SCALE_64DPS: 2>, 'GYRO_SCALE_128DPS': <GyroScale.GYRO_SCALE_128DPS: 3>, 'GYRO_SCALE_256DPS': <GyroScale.GYRO_SCALE_256DPS: 4>, 'GYRO_SCALE_512DPS': <GyroScale.GYRO_SCALE_512DPS: 5>, 'GYRO_SCALE_1024DPS': <GyroScale.GYRO_SCALE_1024DPS: 6>, 'GYRO_SCALE_2048DPS': <GyroScale.GYRO_SCALE_2048DPS: 7>}
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
class IMU:
    def __init__(self, driver: str, i2c_bus: int = -1, addr: int = 107, freq: int = 400000, mode: Mode = ..., acc_scale: AccScale = ..., acc_odr: AccOdr = ..., gyro_scale: GyroScale = ..., gyro_odr: GyroOdr = ..., block: bool = True) -> None:
        ...
    def calculate_calibration(self, time_ms: int = 30000) -> maix._maix.err.Err:
        """
        Caculate calibration, save calibration data to /maixapp/shart/imu_calibration
        
        Args:
          - time_ms: caculate max time, unit:ms
        
        
        Returns: err::Err
        """
    def get_calibration(self) -> list[float]:
        """
        Get calibration data
        
        Returns: return an array, format is [acc_x_bias, acc_y_bias, acc_z_bias, gyro_x_bias, gyro_y_bias, gyro_z_bias]
        If the calibration file cannot be found, an empty array will be returned.
        """
    def read(self) -> list[float]:
        """
        Read data from IMU.
        
        Returns: list type. If only one of the outputs is initialized, only [x,y,z] of that output will be returned.
        If all outputs are initialized, [acc_x, acc_y, acc_z, gyro_x, gyro_y, gyro_z] is returned.
        """
class Mode:
    """
    Members:
    
      ACC_ONLY
    
      GYRO_ONLY
    
      DUAL
    """
    ACC_ONLY: typing.ClassVar[Mode]  # value = <Mode.ACC_ONLY: 0>
    DUAL: typing.ClassVar[Mode]  # value = <Mode.DUAL: 2>
    GYRO_ONLY: typing.ClassVar[Mode]  # value = <Mode.GYRO_ONLY: 1>
    __members__: typing.ClassVar[dict[str, Mode]]  # value = {'ACC_ONLY': <Mode.ACC_ONLY: 0>, 'GYRO_ONLY': <Mode.GYRO_ONLY: 1>, 'DUAL': <Mode.DUAL: 2>}
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
