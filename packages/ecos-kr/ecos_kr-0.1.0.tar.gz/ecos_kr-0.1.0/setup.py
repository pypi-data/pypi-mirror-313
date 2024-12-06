from setuptools import setup, find_packages

setup(
    name="ecos-kr",
    version="0.1.0",
    description="한국은행 ECOS API 클라이언트",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="이종욱",
    author_email="eidoslibrary@adhd-infos.com",
    url="https://github.com/leejongwok/ecos-kr",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.0",
        "pandas>=1.2.0",
        "pyyaml>=5.4.0",
        "click>=7.1.2",
        "rich>=10.0.0",
        "beautifulsoup4>=4.9.3",
        "lxml>=4.9.0",
        "cryptography>=3.4.7"
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "ecos=ecos.cli.commands:cli"
        ]
    }
) 