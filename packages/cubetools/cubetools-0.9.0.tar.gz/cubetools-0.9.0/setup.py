# -*- coding: utf-8 -*-
# ===============LICENSE_START=======================================================
# Acumos Apache-2.0
# ===================================================================================
# Copyright (C) 2017-2018 AT&T Intellectual Property & Tech Mahindra. All rights reserved.
# ===================================================================================
# This Acumos software file is distributed by AT&T and Tech Mahindra
# under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# This file is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ===============LICENSE_END=========================================================
from setuptools import setup, find_packages


with open("README.md", "r", encoding='utf-8') as file:
    long_description = file.read()


setup(
    name='cubetools',
    version='0.9.0',
    author='cubeai',
    author_email='cubeai@163.com',
    description='CubeAI模型开发常用工具集',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='Apache License 2.0',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pillow',
        'opencv-python',
        'tqdm'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: Apache Software License',
    ],
    entry_points="""
    [console_scripts]
    download_file = cubetools.download_model:download_file_cmd
    download_file_parallel = cubetools.download_model:download_file_parallel_cmd
    download_model = cubetools.download_model:download_model_cmd
    download_model_parallel = cubetools.download_model:download_model_parallel_cmd
    download_huggingface = cubetools.huggingface:download_model_cmd
    download_huggingface_dataset = cubetools.huggingface:download_dataset_cmd
    download_huggingface2 = cubetools.huggingface2:download_model_cmd
    download_huggingface_dataset2 = cubetools.huggingface2:download_dataset_cmd
    download_modelscope = cubetools.modelscope:download_model_cmd
    download_modelscope2 = cubetools.modelscope2:download_model_cmd
    download_modelers = cubetools.modelers:download_model_cmd
    download_modelers2 = cubetools.modelers2:download_model_cmd
    """,
    keywords='AI application tools',
    python_requires='>=3.5',
    url='https://openi.pcl.ac.cn/cubeai/cubetools',
)
