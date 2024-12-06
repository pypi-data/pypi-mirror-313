from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="openi",
    version="2.0.3",
    description="A package for openi pypi",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://openi.pcl.ac.cn/OpenIOSSG/openi-pypi",
    author="chenzh05",
    author_email="chenzh.ds@outlook.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
    ],
    entry_points={"console_scripts": ["openi = openi.commands.openi_cli:main"]},
    install_requires=["requests", "tqdm", "deprecated", "pwinput"],
    python_requires=">=3.8",
)
