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

from .detection import Detection
from .recorder import Recorder
from .wakeup import WakeUp

class Voice:

    def __init__(self):
        self.access_key = ""
        self.is_wakeup = True
        self.device_index = -1
        self.wakeup = WakeUp()
        self.detection = Detection()
        self.recorder = Recorder()
    
    def on_start(self):
        if self.is_wakeup:
            self.wakeup.access_key = self.access_key
            self.wakeup.update_library_path()
            self.wakeup.update_model_path()
            self.wakeup.update_keyword_paths()
            self.wakeup.create()
            self.recorder.create(self.wakeup.frame_length, self.device_index)
        else:
             self.detection.access_key = self.access_key
             self.detection.create()
             self.recorder.create(self.detection.frame_length, self.device_index)
    
    def on_process(self):
        result = -1
        keyword = ""
        if self.is_wakeup and self.wakeup.status and self.recorder.status:
            recorder_pcm = self.recorder.process()
            result = self.wakeup.process(recorder_pcm)
            if result > 0:
                keyword = self.wakeup.get_keyword_by_index(result)
        else:
            recorder_pcm = self.recorder.process()
            result = self.detection.process(recorder_pcm)
            if result > 0.09:
                keyword = str(result)
            else:
                result = -1
        return result, keyword

    def on_clean(self):
        pass