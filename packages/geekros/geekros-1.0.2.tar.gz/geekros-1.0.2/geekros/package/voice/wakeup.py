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

import os
from ctypes import *
from enum import Enum
from typing import Sequence
from ...utils import Utils

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
    
class PorcupineMemoryError(Error):
    pass

class PorcupineIOError(Error):
    pass

class PorcupineInvalidArgumentError(Error):
    pass

class PorcupineStopIterationError(Error):
    pass

class PorcupineKeyError(Error):
    pass

class PorcupineInvalidStateError(Error):
    pass

class PorcupineRuntimeError(Error):
    pass

class PorcupineActivationError(Error):
    pass

class PorcupineActivationLimitError(Error):
    pass

class PorcupineActivationThrottledError(Error):
    pass

class PorcupineActivationRefusedError(Error):
    pass

class WakeUp(object):

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
        Status.OUT_OF_MEMORY: PorcupineMemoryError,
        Status.IO_ERROR: PorcupineIOError,
        Status.INVALID_ARGUMENT: PorcupineInvalidArgumentError,
        Status.STOP_ITERATION: PorcupineStopIterationError,
        Status.KEY_ERROR: PorcupineKeyError,
        Status.INVALID_STATE: PorcupineInvalidStateError,
        Status.RUNTIME_ERROR: PorcupineRuntimeError,
        Status.ACTIVATION_ERROR: PorcupineActivationError,
        Status.ACTIVATION_LIMIT_REACHED: PorcupineActivationLimitError,
        Status.ACTIVATION_THROTTLED: PorcupineActivationThrottledError,
        Status.ACTIVATION_REFUSED: PorcupineActivationRefusedError
    }

    class CStructure(Structure):
        pass

    def __init__(self):
        self.language = "en"
        self.library_path = None
        self.model_path = None
        self.keyword_paths = []
        self.sensitivities = []
        self.keywords = [];
        self.access_key = ""
        self.status = False
    
    def update_language(self, language):
        self.language = language

    def update_library_path(self):
        self.library_path = "/opt/geekros/model/voice/lib/wakeup_a55_aarch64.so"

    def update_model_path(self):
        self.model_path = "/opt/geekros/model/voice/language/model_params_" + self.language + ".pv"
    
    def update_keyword_paths(self):
        list_string = ""
        self.keywords = []
        self.keyword_paths = []
        self.sensitivities = []
        for root, dirs, files in os.walk("/opt/geekros/model/voice/keyword/" + self.language):
            for file in files:
                if file.endswith(".ppn"):
                    abs_path = os.path.join(root, file)
                    formatted_name = os.path.splitext(file)[0]
                    list_string += formatted_name + " "
                    self.keywords.append((formatted_name, abs_path))
        for name, path in self.keywords:
            self.keyword_paths.append(path)
            self.sensitivities.append(0.5)
        Utils().log.info("Current language " + self.language + " Supported wake words " + list_string.rstrip(" "))
    
    def get_keyword_by_index(self, index=None):
        if index is None:
            return None, None
        if index > len(self.keywords) or index < 0:
            return None, None
        return self.keywords[index][0]

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

        init_func = library.pv_porcupine_init
        init_func.argtypes = [
            c_char_p,
            c_char_p,
            c_int,
            POINTER(c_char_p),
            POINTER(c_float),
            POINTER(POINTER(self.CStructure))
        ]
        init_func.restype = self.Status

        self._handle = POINTER(self.CStructure)()

        status = init_func(
            self.access_key.encode("utf-8"),
            self.model_path.encode("utf-8"),
            len(self.keyword_paths),
            (c_char_p * len(self.keyword_paths))(*[os.path.expanduser(x).encode("utf-8") for x in self.keyword_paths]),
            (c_float * len(self.keyword_paths))(*self.sensitivities),
            byref(self._handle)
        )
        if status is not self.Status.SUCCESS:
            raise self._STATUS_TO_EXCEPTION[status](message="Initialization failed", message_stack=self._get_error_stack())
        
        self._delete_func = library.pv_porcupine_delete
        self._delete_func.argtypes = [POINTER(self.CStructure)]
        self._delete_func.restype = None

        self._process_func = library.pv_porcupine_process
        self._process_func.argtypes = [POINTER(self.CStructure), POINTER(c_short), POINTER(c_int)]
        self._process_func.restype = self.Status

        version_func = library.pv_porcupine_version
        version_func.argtypes = []
        version_func.restype = c_char_p
        self._version = version_func().decode("utf-8")

        self._frame_length = library.pv_porcupine_frame_length()

        self._sample_rate = library.pv_sample_rate()

        self.status = True

    def delete(self):
        self._delete_func(self._handle)
    
    def process(self, pcm: Sequence[int]) -> int:
        if len(pcm) != self.frame_length:
            raise ValueError("Invalid frame length. expected %d but received %d" % (self.frame_length, len(pcm)))
        result = c_int()
        status = self._process_func(self._handle, (c_short * len(pcm))(*pcm), byref(result))
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
            raise self._STATUS_TO_EXCEPTION[status](message="Unable to get Porcupine error state")
        message_stack = list()
        for i in range(message_stack_depth.value):
            message_stack.append(message_stack_ref[i].decode("utf-8"))
        self._free_error_stack_func(message_stack_ref)
        return message_stack