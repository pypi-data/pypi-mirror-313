# Copyright 2024 GEEKROS, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from ctypes import *
from enum import Enum
from typing import Sequence, List

CALLBACK = CFUNCTYPE(None, POINTER(c_int16))

class Recorder:
    
    class Status(Enum):
        SUCCESS = 0
        OUT_OF_MEMORY = 1
        INVALID_ARGUMENT = 2
        INVALID_STATE = 3
        BACKEND_ERROR = 4
        DEVICE_ALREADY_INITIALIZED = 5
        DEVICE_NOT_INITIALIZED = 6
        IO_ERROR = 7
        RUNTIME_ERROR = 8
    
    _STATUS_TO_EXCEPTION = {
        Status.OUT_OF_MEMORY: MemoryError,
        Status.INVALID_ARGUMENT: ValueError,
        Status.INVALID_STATE: ValueError,
        Status.BACKEND_ERROR: SystemError,
        Status.DEVICE_ALREADY_INITIALIZED: ValueError,
        Status.DEVICE_NOT_INITIALIZED: ValueError,
        Status.IO_ERROR: IOError,
        Status.RUNTIME_ERROR: RuntimeError
    }

    class CStructure(Structure):
        pass

    _library = None
    _relative_library_path = ""

    def __init__(self):
        self.status = False

    def create(self, frame_length: int, device_index: int = -1, buffered_frames_count: int = 50):
        library = self._get_library()

        init_func = library.pv_recorder_init
        init_func.argtypes = [
            c_int32,
            c_int32,
            c_int32,
            POINTER(POINTER(self.CStructure))
        ]
        init_func.restype = self.Status

        self._handle = POINTER(self.CStructure)()
        self._frame_length = frame_length

        status = init_func(frame_length, device_index, buffered_frames_count, byref(self._handle))
        if status is not self.Status.SUCCESS:
            raise self._STATUS_TO_EXCEPTION[status]("Failed to initialize Recorder.")

        self._delete_func = library.pv_recorder_delete
        self._delete_func.argtypes = [POINTER(self.CStructure)]
        self._delete_func.restype = None

        self._start_func = library.pv_recorder_start
        self._start_func.argtypes = [POINTER(self.CStructure)]
        self._start_func.restype = self.Status

        self._stop_func = library.pv_recorder_stop
        self._stop_func.argtypes = [POINTER(self.CStructure)]
        self._stop_func.restype = self.Status

        self._set_debug_logging_func = library.pv_recorder_set_debug_logging
        self._set_debug_logging_func.argtypes = [POINTER(self.CStructure), c_bool]
        self._set_debug_logging_func.restype = None

        self._read_func = library.pv_recorder_read
        self._read_func.argtypes = [POINTER(self.CStructure), POINTER(c_int16)]
        self._read_func.restype = self.Status

        self._get_is_recording_func = library.pv_recorder_get_is_recording
        self._get_is_recording_func.argtypes = [POINTER(self.CStructure)]
        self._get_is_recording_func.restype = c_bool

        self._get_selected_device_func = library.pv_recorder_get_selected_device
        self._get_selected_device_func.argtypes = [POINTER(self.CStructure)]
        self._get_selected_device_func.restype = c_char_p

        self._version_func = library.pv_recorder_version
        self._version_func.argtypes = None
        self._version_func.restype = c_char_p

        self._sample_rate_func = library.pv_recorder_sample_rate
        self._sample_rate_func.argtypes = None
        self._sample_rate_func.restype = c_int32

        self.start()
    
    def start(self) -> None:
        status = self._start_func(self._handle)
        if status is not self.Status.SUCCESS:
            raise self._STATUS_TO_EXCEPTION[status]("Failed to start device.")
        self.status = True
    
    def stop(self) -> None:
        status = self._stop_func(self._handle)
        if status is not self.Status.SUCCESS:
            raise self._STATUS_TO_EXCEPTION[status]("Failed to stop device.")
        self.status = False

    def process(self) -> List[int]:
        pcm = (c_int16 * self._frame_length)()
        status = self._read_func(self._handle, pcm)
        if status is not self.Status.SUCCESS:
            raise self._STATUS_TO_EXCEPTION[status]("Failed to read from device.")
        return list(pcm[0:self._frame_length])

    def delete(self) -> None:
        self._delete_func(self._handle)

    def set_debug_logging(self, is_debug_logging_enabled: bool) -> None:
        self._set_debug_logging_func(self._handle, is_debug_logging_enabled)

    @property
    def is_recording(self) -> bool:
        return bool(self._get_is_recording_func(self._handle))

    @property
    def selected_device(self) -> str:
        device_name = self._get_selected_device_func(self._handle)
        return device_name.decode("utf-8")

    @property
    def version(self) -> str:
        version = self._version_func()
        return version.decode("utf-8")

    @property
    def frame_length(self) -> int:
        return self._frame_length

    @property
    def sample_rate(self) -> int:
        sample_rate = self._sample_rate_func()
        return sample_rate

    @staticmethod
    def get_available_devices() -> List[str]:
        get_available_devices_func = Recorder._get_library().pv_recorder_get_available_devices
        get_available_devices_func.argstype = [POINTER(c_int32), POINTER(POINTER(c_char_p))]
        get_available_devices_func.restype = Recorder.Status

        free_available_devices_func = Recorder._get_library().pv_recorder_free_available_devices
        free_available_devices_func.argstype = [c_int32, POINTER(c_char_p)]
        free_available_devices_func.restype = None

        count = c_int32()
        devices = POINTER(c_char_p)()

        status = get_available_devices_func(byref(count), byref(devices))
        if status is not Recorder.Status.SUCCESS:
            raise Recorder._STATUS_TO_EXCEPTION[status]("Failed to get device list")

        device_list = list()
        for i in range(count.value):
            device_list.append(devices[i].decode('utf-8'))

        free_available_devices_func(count, devices)

        return device_list

    @classmethod
    def set_default_library_path(cls, relative: str):
        cls._relative_library_path = "/opt/geekros/model/voice/lib/recorder_a55_aarch64.so"

    @classmethod
    def _get_library(cls):
        if len(cls._relative_library_path) == 0:
            cls._relative_library_path = "/opt/geekros/model/voice/lib/recorder_a55_aarch64.so"
        if cls._library is None:
            cls._library = cdll.LoadLibrary(cls._relative_library_path)
        return cls._library
