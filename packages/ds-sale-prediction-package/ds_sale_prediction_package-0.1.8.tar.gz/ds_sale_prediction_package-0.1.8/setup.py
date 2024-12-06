from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="ds_sale_prediction_package",
    version="0.1.8",
    description="This package provides a comprehensive toolkit for data\
    preparation, feature extraction, model validation, hyperparameter\
    optimization, and results visualization created for the Kaggle\
    competition Predict Future Sales. The competition's objective is to\
    predict total sales for each product and store in the upcoming month.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Aliona Hrynkevich",
    license="MIT",
    packages=find_packages(),
    install_requires=requirements,
)
