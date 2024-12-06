from dataclasses import dataclass

# noinspection PyUnresolvedReferences
from .._core._c_uutils_base_platform import (
    _c_oserror, _c_base_getMemInfo, _c_base_initProcInfo,
    _c_base_getProcInfo, _c_base_getProcInfoMax
)

__all__ = [
    'MemInfo',
    'ProcInfo',
    'get_os_error',
    'get_memory_info',
    'init_process_info',
    'get_process_info',
    'get_process_info_max',
]


@dataclass
class MemInfo:
    """
    Class representing system memory information.

    All values are in kilobytes (kB).
    """
    phys_total: int = 0  #: Total physical RAM
    phys_avail: int = 0  #: Available physical RAM
    phys_cache: int = 0  #: Physical RAM cache
    swap_total: int = 0  #: Total swap space
    swap_avail: int = 0  #: Available swap space
    virt_total: int = 0  #: Total virtual memory
    virt_avail: int = 0  #: Available virtual memory


@dataclass
class ProcInfo:
    """
    Class representing process resource usage information.

    Memory values are in kilobytes (kB).
    Time values are in milliseconds.
    """
    mem_virt: int = 0  #: Virtual memory configuration
    mem_work: int = 0  #: Working memory configuration
    mem_swap: int = 0  #: Swap memory configuration
    time_user: int = 0  #: User CPU time usage
    time_sys: int = 0  #: System CPU time usage
    time_real: int = 0  #: Real time usage


def get_os_error(error_code: int) -> str:
    """
    Get OS-specific error description for given error code.

    :param error_code: The error code to get description for
    :type error_code: int
    :return: Error description string
    :rtype: str
    """
    return _c_oserror(error_code)


def get_memory_info() -> MemInfo:
    """
    Get hosting machine memory information.

    :return: Memory information object
    :rtype: MemInfo
    """
    info = MemInfo()
    _c_base_getMemInfo(info)
    return info


def init_process_info() -> None:
    """
    Initialize the process information gathering.
    """
    _c_base_initProcInfo()


def get_process_info() -> ProcInfo:
    """
    Get current process memory and time consumption sample.

    :return: Process information object
    :rtype: ProcInfo
    """
    info = ProcInfo()
    _c_base_getProcInfo(info)
    return info


def get_process_info_max() -> ProcInfo:
    """
    Get current process memory and time consumption sample and store maximum values.

    :return: Process information object with maximum values
    :rtype: ProcInfo
    """
    info = ProcInfo()
    _c_base_getProcInfoMax(info)
    return info
