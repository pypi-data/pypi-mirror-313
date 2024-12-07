import os.path

from .types import *


class DLNApi(object):
    def __init__(self, shared_library_path='C:\\Program Files\\Diolan\\DLN\\redistributable\\direct_library\\dln.dll'):
        self._library = ctypes.cdll.LoadLibrary(os.path.abspath(shared_library_path))
        self._handle = HDLN()

    def __enter__(self):
        self.open_usb_device()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._library.DlnCloseHandle(self._handle)

    @property
    def device_sn(self) -> int:
        sn = ctypes.c_uint32()
        if api_result := DLN_RESULT(self._library.DlnGetDeviceSn(self._handle, ctypes.byref(sn))):
            raise RuntimeError(api_result.value)
        return sn.value

    @property
    def hardware_type(self) -> str:
        hw_type = DLN_HW_TYPE()
        if api_result := DLN_RESULT(self._library.DlnGetHardwareType(self._handle, ctypes.byref(hw_type))):
            raise RuntimeError(api_result.value)
        return hw_type

    @property
    def device_id(self) -> int:
        id = ctypes.c_uint32()
        if api_result := DLN_RESULT(self._library.DlnGetDeviceId(self._handle, ctypes.byref(id))):
            raise RuntimeError(api_result.value)
        return id.value

    def open_usb_device(self):
        if api_result := DLN_RESULT(self._library.DlnOpenUsbDevice(ctypes.byref(self._handle))):
            raise RuntimeError(api_result.value)

    def get_spi_master_c_pol(self, port: int = 0) -> int:
        port = ctypes.c_uint8(port)
        c_pol = ctypes.c_uint8()
        if api_result := DLN_RESULT(self._library.DlnSpiMasterGetCpol(self._handle, port, ctypes.byref(c_pol))):
            raise RuntimeError(api_result.value)
        return c_pol.value

    def set_spi_master_c_pol(self, port: int = 0, c_pol: int = 0):
        port = ctypes.c_uint8(port)
        c_pol = ctypes.c_uint8(c_pol)
        if api_result := DLN_RESULT(self._library.DlnSpiMasterSetCpol(self._handle, port, c_pol)):
            raise RuntimeError(api_result.value)
        return c_pol.value

    def set_spi_master_configuration(self, port: int = 0, frequency: int = 1000000, frame_size: int = 16) -> int:
        port = ctypes.c_uint8(port)
        frequency = ctypes.c_uint32(frequency)
        frame_size = ctypes.c_uint8(frame_size)
        actual_frequency = ctypes.c_uint32()
        if api_result := DLN_RESULT(self._library.DlnSpiMasterSetFrequency(self._handle,
                                                                           port,
                                                                           frequency,
                                                                           ctypes.byref(actual_frequency))):
            raise RuntimeError(api_result.value)
        if frequency.value != actual_frequency.value:
            raise RuntimeError
        conflicts = ctypes.c_uint16()
        if api_result := DLN_RESULT(self._library.DlnSpiMasterEnable(self._handle, port, ctypes.byref(conflicts))):
            raise RuntimeError(api_result.value)
        if conflicts.value:
            raise RuntimeError(conflicts.value)
        if api_result := DLN_RESULT(self._library.DlnSpiMasterSetFrameSize(self._handle, port, frame_size)):
            raise RuntimeError(api_result.value)
        return 0

    def get_spi_master_frequency(self, port: int = 0) -> int:
        frequency = ctypes.c_uint32()
        port = ctypes.c_uint8(port)
        if api_result := DLN_RESULT(
                self._library.DlnSpiMasterGetFrequency(self._handle, port, ctypes.byref(frequency))):
            raise RuntimeError(api_result.value)
        return frequency.value

    def get_spi_master_frame_size(self, port: int = 0) -> int:
        frame_size = ctypes.c_uint8()
        port = ctypes.c_uint8(port)
        if api_result := DLN_RESULT(
                self._library.DlnSpiMasterGetFrameSize(self._handle, port, ctypes.byref(frame_size))):
            raise RuntimeError(api_result.value)
        return frame_size.value

    def full_duplex_transaction(self, tx_data: bytearray, port: int = 0) -> bytearray:
        port = ctypes.c_uint8(port)
        tx_data = (ctypes.c_uint8 * len(tx_data))(*tx_data)
        rx_data = (ctypes.c_uint8 * len(tx_data))(*([0] * len(tx_data)))
        if len(tx_data) <= 8:
            dln_function = self._library.DlnSpiMasterReadWrite
        elif len(tx_data) <= 16:
            dln_function = self._library.DlnSpiMasterReadWrite16
        else:
            raise ValueError(len(tx_data))
        if api_result := DLN_RESULT(dln_function(self._handle, port, ctypes.c_uint16(len(tx_data)), tx_data, rx_data)):
            raise RuntimeError(api_result.value)
        return bytearray(rx_data)
