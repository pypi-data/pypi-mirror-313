from setuptools import setup, find_packages

setup(
    name='ecom_data_helpers_lib',
    version='0.0.44',
    description='A library of reusable utilities for AWS Lambda functions in ECOM Data Projects',
    author='Augusto Lorencatto',
    author_email='augusto.lorencatto@ecomenergia.com.br',
    url="https://github.com/ecom-one-stop-solution/ecom-data-helpers-lib",
    packages=find_packages(),
    install_requires=[
        'boto3',
        'python-docx==1.1.2',
        'PyPDF2==3.0.1',
        'pdf2image==1.17.0',
        'pytest',
        'httpx'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.12',
)