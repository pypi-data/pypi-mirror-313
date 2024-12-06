from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="wauo",
    version="0.6.5.8",
    description="爬虫者的贴心助手",
    url="https://github.com/markadc/wauo",
    author="WangTuo",
    author_email="markadc@126.com",
    packages=find_packages(),
    license="MIT",
    zip_safe=False,
    install_requires=["requests", "fake_useragent", "loguru", "parsel"],
    keywords=["python", "requests", "spider"],
    long_description=long_description,
    long_description_content_type="text/markdown",
)
