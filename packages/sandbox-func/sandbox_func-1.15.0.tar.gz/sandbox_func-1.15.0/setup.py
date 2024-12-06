from setuptools import setup, find_packages

setup(
    name="sandbox_func",
    description="沙盒函数基础工具包",
    version="1.15.0",
    install_requires="pluggy>=1.0",
    packages=find_packages(),
    python_requires='>=3.11'
)