import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ttcommon",
    version="0.4.6",
    author="Tron Trading Development",
    author_email="author@example.com",
    description="Tron Trading System Common Library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/trontrading/system/common",
    project_urls={
        "Bug Tracker": "https://gitlab.com/trontrading/system/common/-/issuess",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
)
