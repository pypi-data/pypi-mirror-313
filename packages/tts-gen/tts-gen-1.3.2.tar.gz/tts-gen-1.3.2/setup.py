# Copyright 2017 The NPU Compiler Authors. All Rights Reserved.
#
# Licensed under the Proprietary License;
# you may not use this file except in compliance with the License.

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
from setuptools import find_packages, setup
from codecs import open
from os import path

from tts_generator import __version__

REQUIRED_PACKAGES = [
    'requests',
    'tqdm',
]

here = path.abspath(path.dirname(__file__))

setup(
    name='tts-gen',
    version=__version__,
    description='',
    long_description='',
    long_description_content_type='text/markdown',
    url='http://ai.nationalchip.com/',
    author='Hangzhou Nationalchip Inc.',
    author_email='zhengdi@nationalchip.com',
    license='MIT Licence',

    # PyPI package information.
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        ],

    keywords='tts',

    # Contained modules and scripts.
    packages=find_packages(),
    install_requires=REQUIRED_PACKAGES,

    scripts=['tts_generator/tts-gen'],
    entry_points={
    },
    )
