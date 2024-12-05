from setuptools import find_packages, setup

setup(
    name="snail-job-python",  # 项目名称
    version="0.0.2",  # 项目版本
    packages=find_packages(),  # 自动发现项目中的包
    install_requires=[  # 项目依赖包
        "pydantic",
        "python-dotenv",
        "aiohttp",
        "protobuf",
        "grpcio",
    ],
    long_description=open("README.md").read(),  # 读取 README.md 文件作为长描述
    long_description_content_type="text/markdown",  # 长描述格式
    author="dhb52",
    author_email="dhb52@126.com",
    description="SnailJob is a high performance distributed task scheduler and retry management center",
    url="https://gitee.com/opensnail/snail-job-python",  # 项目主页
    classifiers=[  # 项目的分类信息
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
)
