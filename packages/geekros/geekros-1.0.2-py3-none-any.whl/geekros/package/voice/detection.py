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
from typing import Sequence

class Error(Exception):
    def __init__(self, message: str = "", message_stack: Sequence[str] = None):
        super().__init__(message)
        self._message = message
        self._message_stack = list() if message_stack is None else message_stack

    def __str__(self):
        message = self._message
        if len(self._message_stack) > 0:
            message += ":"
            for i in range(len(self._message_stack)):
                message += "\n  [%d] %s" % (i, self._message_stack[i])
        return message

    @property
    def message(self) -> str:
        return self._message

    @property
    def message_stack(self) -> Sequence[str]:
        return self._message_stack

class CobraMemoryError(Error):
    pass

class CobraIOError(Error):
    pass

class CobraInvalidArgumentError(Error):
    pass

class CobraStopIterationError(Error):
    pass

class CobraKeyError(Error):
    pass

class CobraInvalidStateError(Error):
    pass

class CobraRuntimeError(Error):
    pass

class CobraActivationError(Error):
    pass

class CobraActivationLimitError(Error):
    pass

class CobraActivationThrottledError(Error):
    pass

class CobraActivationRefusedError(Error):
    pass

class Detection:

    class Status(Enum):
        SUCCESS = 0
        OUT_OF_MEMORY = 1
        IO_ERROR = 2
        INVALID_ARGUMENT = 3
        STOP_ITERATION = 4
        KEY_ERROR = 5
        INVALID_STATE = 6
        RUNTIME_ERROR = 7
        ACTIVATION_ERROR = 8
        ACTIVATION_LIMIT_REACHED = 9
        ACTIVATION_THROTTLED = 10
        ACTIVATION_REFUSED = 11

    _STATUS_TO_EXCEPTION = {
        Status.OUT_OF_MEMORY: CobraMemoryError,
        Status.IO_ERROR: CobraIOError,
        Status.INVALID_ARGUMENT: CobraInvalidArgumentError,
        Status.STOP_ITERATION: CobraStopIterationError,
        Status.KEY_ERROR: CobraKeyError,
        Status.INVALID_STATE: CobraInvalidStateError,
        Status.RUNTIME_ERROR: CobraRuntimeError,
        Status.ACTIVATION_ERROR: CobraActivationError,
        Status.ACTIVATION_LIMIT_REACHED: CobraActivationLimitError,
        Status.ACTIVATION_THROTTLED: CobraActivationThrottledError,
        Status.ACTIVATION_REFUSED: CobraActivationRefusedError
    }

    class CStructure(Structure):
        pass

    def __init__(self):
        self.library_path = "/opt/geekros/model/voice/lib/detection_a55_aarch64.so"
        self.access_key = ""
        self.status = False
     
    def create(self):
        library = cdll.LoadLibrary(self.library_path)

        set_sdk_func = library.pv_set_sdk
        set_sdk_func.argtypes = [c_char_p]
        set_sdk_func.restype = None
        set_sdk_func("python".encode("utf-8"))

        self._get_error_stack_func = library.pv_get_error_stack
        self._get_error_stack_func.argtypes = [POINTER(POINTER(c_char_p)), POINTER(c_int)]
        self._get_error_stack_func.restype = self.Status

        self._free_error_stack_func = library.pv_free_error_stack
        self._free_error_stack_func.argtypes = [POINTER(c_char_p)]
        self._free_error_stack_func.restype = None

        init_func = library.pv_cobra_init
        init_func.argtypes = [
            c_char_p,
            POINTER(POINTER(self.CStructure))
        ]
        init_func.restype = self.Status
         
        self._handle = POINTER(self.CStructure)()

        status = init_func(self.access_key.encode("utf-8"), byref(self._handle))
        if status is not self.Status.SUCCESS:
            raise self._STATUS_TO_EXCEPTION[status](message="Initialization failed", message_stack=self._get_error_stack())

        self._delete_func = library.pv_cobra_delete
        self._delete_func.argtypes = [POINTER(self.CStructure)]
        self._delete_func.restype = None

        self.process_func = library.pv_cobra_process
        self.process_func.argtypes = [POINTER(self.CStructure), POINTER(c_short), POINTER(c_float)]
        self.process_func.restype = self.Status

        version_func = library.pv_cobra_version
        version_func.argtypes = []
        version_func.restype = c_char_p
        self._version = version_func().decode("utf-8")

        self._frame_length = library.pv_cobra_frame_length()

        self._sample_rate = library.pv_sample_rate()

        self.status = True
    
    def delete(self):
        self._delete_func(self._handle)
    
    def process(self, pcm: Sequence[int]) -> float:
        if len(pcm) != self.frame_length:
            raise ValueError("Invalid frame length. expected %d but received %d" % (self.frame_length, len(pcm)))
        result = c_float()
        status = self.process_func(self._handle, (c_short * len(pcm))(*pcm), byref(result))
        if status is not self.Status.SUCCESS:
            raise self._STATUS_TO_EXCEPTION[status](message="Processing failed", message_stack=self._get_error_stack())
        return result.value
    
    @property
    def version(self) -> str:
        return self._version

    @property
    def frame_length(self) -> int:
        return self._frame_length
    
    @property
    def sample_rate(self) -> int:
        return self._sample_rate

    def _get_error_stack(self) -> Sequence[str]:
        message_stack_ref = POINTER(c_char_p)()
        message_stack_depth = c_int()
        status = self._get_error_stack_func(byref(message_stack_ref), byref(message_stack_depth))
        if status is not self.Status.SUCCESS:
            raise self._STATUS_TO_EXCEPTION[status](message="Unable to get Cobra error state")
        message_stack = list()
        for i in range(message_stack_depth.value):
            message_stack.append(message_stack_ref[i].decode("utf-8"))
        self._free_error_stack_func(message_stack_ref)
        return message_stack