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

from setuptools import setup, find_packages

setup(
    name="geekros",
    version="1.0.1",
    author="MakerYang",
    author_email="admin@wileho.com",
    description="Python development framework for geekros.",
    long_description="Python development framework for geekros.",
    long_description_content_type="text/markdown",
    url="https://github.com/geekros/geekros",
    packages=find_packages(),
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Topic :: Multimedia :: Sound/Audio",
        "Topic :: Multimedia :: Video",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3 :: Only",
    ],
    python_requires=">=3.9.0",
    license="Apache-2.0",
    project_urls={
        "Documentation": "https://www.geekros.com/docs",
        "Website": "https://geekros.com",
        "Source": "https://github.com/geekros/geekros",
    },
    keywords=["webrtc", "realtime", "audio", "video", "geekros", "ros", "ros2", "ubuntu", "openai", "llm", "llama"],
    install_requires=[
        "logging>=0.4.9.6",
        "colorlog>=6.8.2",
        "numpy>=1.26.4",
        "pyaudio>=0.2.14",
        "requests>=2.32.3",
        "pyserial>=3.2.1",
        "websocket-client==0.48.0",
        "openai>=1.42.0"
    ]
)
