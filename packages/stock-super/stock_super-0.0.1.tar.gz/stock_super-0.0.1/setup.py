# setup.py
from setuptools import setup, find_packages

setup(
    name="stock_super",  # 包名称
    version="0.0.1",        # 版本号
    author="冯帅",     # 作者姓名
    author_email="ucjmhfeng@126.com",  # 作者邮箱
    description="简单实现获取股票数据",  # 简短描述
    long_description=open('README.md').read(),  # 详细描述（通常从 README.md 读取）
    long_description_content_type="text/markdown",  # 描述内容类型
    url="",  # 项目主页（通常是 GitHub 仓库）
    packages=find_packages(),  # 自动查找所有包
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # 选择合适的许可证
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',  # 指定支持的 Python 版本
    install_requires=[
        "requests>=2.25.1",  # 列出依赖项
        "pandas>=1.1.0",
        # 添加其他依赖项
    ],
    entry_points={
        'console_scripts': [
            'stock_super=data_get:data_get',  # 可选：添加命令行入口点
        ],
    },
)