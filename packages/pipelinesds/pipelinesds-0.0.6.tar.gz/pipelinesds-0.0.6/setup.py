from setuptools import setup, find_packages

with open("docs/ALTERNATIVE_README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pipelinesds",
    version="0.0.6",
    packages=find_packages(),
       install_requires=[
           'google-cloud-bigquery>=3.22.0',
           'google-cloud-bigquery-storage>=2.25.0',
           'google-cloud-storage>=2.16.0',
           'pandas>=2.2.2',
           'db-dtypes>=1.2.0',
           'evidently==0.4.39'
    ],
    author="DS Team",
    author_email="ds@sts.pl",
    description="Solution for DS Team",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.11",
)
