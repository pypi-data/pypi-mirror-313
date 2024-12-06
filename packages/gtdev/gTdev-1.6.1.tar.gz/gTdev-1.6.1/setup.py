import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gTdev",
    version="1.6.1",
    author="Spectre Lee",
    author_email="lxwk1spectre@foxmail.com",
    description="高效碳基测试运算模块",
    long_description=long_description,
    long_description_content_type="text/markdown",
    include_package_data=True,
    url="https://gitee.com/lxwk1spectre/gdevsample",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)