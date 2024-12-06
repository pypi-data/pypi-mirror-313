"""
python setup.py sdist bdist_wheel
"""


import setuptools #导入setuptools打包工具
 
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
 
setuptools.setup(
    name="Teclab", 
    version="0.0.1",    
    author="Teclab",   
    author_email="admin@teclab.org.cn",   
    description="Teclab设备统一控制协议",
    long_description=long_description,   
    long_description_content_type="text/markdown",
    url="https://gitlab.teclab.org.cn/Teclab/iot-protocol",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',   
)