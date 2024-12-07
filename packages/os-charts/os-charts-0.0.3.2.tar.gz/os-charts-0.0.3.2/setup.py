import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
    name="os-charts",  # 模块名称
    version="0.0.3.2",  # 当前版本
    author="LiuFeng",  # 作者
    author_email="yuyu62488@gmail.com",  # 作者邮箱
    description=long_description,  # 模块简介
    long_description=long_description,  # 模块详细介绍
    long_description_content_type="text/markdown",  # 模块详细介绍格式
    # url="",  # 模块github地址
    packages=setuptools.find_packages(),  # 自动找到项目中导入的模块
    # 模块相关的元数据
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    # 依赖模块
    install_requires=[
        "DBUtils==2.0",
        "elasticsearch==7.1.0",
        "PyMySQL==1.1.0"

    ],
    python_requires='>=3',
)