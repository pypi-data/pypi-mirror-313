from setuptools import setup, find_packages

setup(
    name="spp_localSQL",  # 包名称
    version="0.1.2",   # 版本号
    packages=find_packages(),  # 查找所有包，包含 __init__.py
    description="一个简单的 SQLite 数据库助手类",
    long_description=open('README.md', encoding='utf-8').read(),  # 指定编码为 UTF-8

    long_description_content_type="text/markdown",  # 如果 README 是 Markdown 格式
    author="ShiPanPan",  # 替换成你的名字
    author_email="417833515@qq.com",  # 替换成你的邮箱
    url="https://gitee.com/liehuozhuoxin/local-database-operations",  # 替换成项目主页
    classifiers=[  # PyPI 上常用的分类标签
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # 支持的 Python 版本
)

# pip install setuptools twine
# python setup.py clean
# python setup.py sdist bdist_wheel
# twine upload dist/*
# -i https://pypi.org/simple