from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="argilla-dataset-manager",
    version="0.1.6",
    author="Jordan Burger",
    author_email="jordanrburger@gmail.com",
    description="A tool for managing and uploading datasets to Argilla",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jordanrburger/argilla_dataset_manager",
    packages=find_packages(include=["argilla_dataset_manager*"]),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    include_package_data=True,
    package_data={
        "argilla_dataset_manager": ["py.typed", "**/*.py", "**/*.pyi"],
    },
)
