import setuptools

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="DPTool",
    version="1.0.0",
    author="Jiayu Tan",
    author_email="jtan010@uottawa.ca",
    description="Some scripts based on DrissionPage for Baidu SEO purpose",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    install_requires=['DrissionPage>=1.5.1',
                      'numpy>=1.26.4'],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)