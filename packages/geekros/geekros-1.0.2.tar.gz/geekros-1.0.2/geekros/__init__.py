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

import sys
import signal
from threading import Thread, Event
from .module import Module
from .package import Package
from .utils import Utils

class Framework:

    def __init__(self):
        signal.signal(signal.SIGINT, self.sigint_handler)
        signal.signal(signal.SIGTERM, self.sigint_handler)
        self.main_module = sys.modules.get("__main__")
        self.module = Module()
        self.package = Package()
        self.utils = Utils()
        self.quit_event = Event()
        self.quit_thread = Thread(name="quit_thread_task", target=self.quit_task)
        self.quit_thread.start()

    def quit_task(self):
        on_start = "on_start"
        if on_start in dir(self.main_module):
            getattr(self.main_module, on_start)(self)
        self.quit_event.wait()

    def sigint_handler(self, signum, frame):
        on_exit = "on_exit"
        if on_exit in dir(self.main_module):
            getattr(self.main_module, on_exit)(self)
        self.quit_event.set()