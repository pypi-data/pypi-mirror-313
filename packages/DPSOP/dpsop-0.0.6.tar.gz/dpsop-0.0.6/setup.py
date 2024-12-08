from setuptools import setup, find_packages

setup(
    name="DPSOP",
    version="0.0.6",
    description="深度学习 模型训练的流程库",
    author="buffalohlh",
    author_email="buffaloboyhu@gmail.com",
    url="https://github.com/buffaloboyhlh/DPSOP",
    packages=find_packages(), # 自动发现模块
    license="MIT",
    python_requires=">=3.12",
    install_requires=[
        "torch>=2.5.1" # 依赖 pytorch
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)