from setuptools import setup, find_packages

setup(
    name="secfi",  
    version="0.1.10",
    description=" Python tool to collect SEC filings for all publicly traded companies. Easily fetch forms like 10-K, 10-Q, and 8-K, along with links and document contents. Ideal for analysts, researchers, and anyone exploring financial reports or SEC data. Simplify your access to essential company information",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Juan Pablo",
    author_email="juanpypython@gmail.com",
    url="https://github.com/gauss314/secfi",
    license="MIT",
    packages=find_packages(), 
    install_requires=[
                        "beautifulsoup4==4.12.3",
                        "certifi==2024.8.30",
                        "charset-normalizer==3.4.0",
                        "idna==3.10",
                        "numpy<2.0.0,>=1.23.5",
                        "pandas==2.2.2",
                        "python-dateutil==2.9.0.post0",
                        "pytz==2024.2",
                        "requests==2.32.3",
                        "setuptools==75.6.0",
                        "six==1.16.0",
                        "soupsieve==2.6",
                        "tzdata==2024.2",
                        "urllib3==2.2.3",

    ], 
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
