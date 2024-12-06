import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="yplib",
    version="6.4.3",
    author="yangpu",
    author_email="wantwaterfish@gmail.com",
    description="util",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
    install_requires=open('requirements.txt', 'r', encoding='utf-8').readlines(),
)
