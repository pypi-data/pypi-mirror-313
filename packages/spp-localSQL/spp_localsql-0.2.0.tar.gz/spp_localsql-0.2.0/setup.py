from setuptools import setup, find_packages

setup(
    name="spp_localSQL",  # 包名称
    version="0.2.0",  # 版本号
    packages=find_packages(include=['spp_localSQL', 'spp_localSQL.*']),  # 查找包并明确指向主包目录
    description="一个简单的 SQLite 数据库助手类",
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type="text/markdown",  # 指定 Markdown 格式
    author="ShiPanPan",
    author_email="417833515@qq.com",
    url="https://gitee.com/liehuozhuoxin/local-database-operations",  # 项目主页
    classifiers=[
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