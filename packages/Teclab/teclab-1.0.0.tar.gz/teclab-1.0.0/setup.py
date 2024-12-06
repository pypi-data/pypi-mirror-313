"""
python setup.py sdist bdist_wheel
python -m twine upload dist/*
token: pypi-AgEIcHlwaS5vcmcCJDk2ODAwOTZiLWQ1N2YtNGIwNy1iZDk2LWZiYzljNzEwM2NiZAACKlszLCI1NmVkZWE5ZC01OWRjLTQzOWItOGNiNy0xY2YyOWM4MGQ2OGQiXQAABiCMXrBAUcxGTySSMG8iNkL5yRg4VHGjwfXvJgqPjK-aAQ
"""


import setuptools #导入setuptools打包工具
 
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
 
setuptools.setup(
    name="Teclab", 
    version="1.0.0",    
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