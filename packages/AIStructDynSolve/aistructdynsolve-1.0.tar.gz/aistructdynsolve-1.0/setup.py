import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
    name="AIStructDynSolve",  # 模块名称
    version="1.0",  # 当前版本
    author="Ke Du(杜轲)",  # 作者
    author_email="duke@iem.ac.cn",  # 作者邮箱
    description="A framework focused on solving structural dynamics problems using artificial intelligence (AI) methods",  # 模块简介
    long_description=long_description,  # 模块详细介绍
    long_description_content_type='text/markdown',  # 模块详细介绍格式
    # url="https://github.com/",  # 模块github地址
    packages=setuptools.find_packages(),  # 自动找到项目中导入的模块
    # 模块相关的元数据
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    # 依赖模块
    install_requires=[
        'pytorch',
        'matplotlib',
        'numpy',
        'scikit-optimize',
        'pandas',
    ],
    python_requires='>=3',
)


