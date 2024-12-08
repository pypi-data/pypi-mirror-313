from setuptools import setup, find_packages

setup(
    name="myfirstpkg2412",  # 包名
    version="0.1.1",  # 初始版本号
    author="lys",
    author_email="your.email@example.com",
    description="A sample Python package hhhhh 2024年12月07日21:48:15",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/myfirstpkg",  # 项目的 URL
    packages=find_packages(),  # 自动发现模块
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # 支持的 Python 版本
)
