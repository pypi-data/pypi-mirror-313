from setuptools import setup, find_packages

setup(
    name="pycoze",
    version="0.1.221",
    packages=find_packages(),
    install_requires=[],
    author="Yuan Jie Xiong",
    author_email="aiqqqqqqq@qq.com",
    description="Package for pycoze only!",
    long_description=open('README.md', encoding="utf-8").read(),
    long_description_content_type='text/markdown',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
