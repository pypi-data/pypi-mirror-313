"""
pyupbit-for-devs package:
   Copyright 2024 Sanghoon Lee (DSsoli). All Rights Reserved.

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.

Modifications, Additions, and Deletions:
    - Additions: trade_utils.py for Robust API/Function Calls with correct response assurance and retries
    - Deletions: pyupbit's custom error handlings
    - Modifications: functions in quotation_api.py, request_api.py, and exchange_api.py,
        in order to show raw and detailed response from Upbit API directly for debugging purposes.

Base code for pyupbit-for-devs package (pyupbit):
   Copyright 2021 Jonghun Yoo, Brayden Jo, pystock/pyquant (sharebook-kr), (et al.). All Rights Reserved.

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""


from setuptools import setup, find_packages

with open("README.md", "r", encoding='utf-8') as fh:
    README = fh.read()

install_requires = [
   'pyjwt>=2.0.0',
   'pandas',
   'requests',
   'websockets'
]

setup(
    author="Sanghoon Lee (DSsoli)",
    author_email="solisoli3197@gmail.com",
    name="pyupbit-for-devs",
    version="0.1.3",
    description="Augmented pyupbit for Developers",
    long_description=README,
    long_description_content_type="text/markdown",
    install_requires=install_requires,
    url="https://github.com/DSsoli/pyupbit-for-devs.git",
    packages=find_packages(include=['pyupbit_for_devs', 'pyupbit_for_devs.*']),
    package_data={"pyupbit_for_devs": ['LICENSE']},
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6'
)