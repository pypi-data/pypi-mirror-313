"""
未加密的tfduck/setup.py的代码
"""
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tfduck-bsd",
    version="0.18.3",
    author="yuanxiao",
    author_email="yuan6785@163.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    # 需要安装的依赖
    install_requires=[
         'arrow>=0.15.5',   
         'requests>=2.20.0',
         'django==2.2.12',
         'oss2==2.15.0', # 原来是2.5.0
         'ThinkingDataSdk==1.8.0', #1.1.14, 1.6.2 1.8.0支持字典和数组
         'kubernetes==12.0.1',
         'sagemaker==2.183.0', # 2.24.1# modify by yx 2023-02-27, 2023-09-18 到 2.183.0 [最后支持3.7的版本], 上一个版本2.135.0
         'boto3==1.28.49' # 1.24.27 1.18.36 # modify by yx 2023-02-27, 2023-09-18 到 1.28.49, 上一个版本1.26.79
         # 下面的包不能放到这里安装,依赖太多，需要尽量简单
         # 'importlib_metadata==1.6.1',
         # 'duckdb==0.3.4'
    ],
    python_requires=">=3.5",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    scripts=['bin/tfduck'],
)
