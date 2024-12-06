from setuptools import setup, find_packages

setup(
    name="gblog_whisperer",
    version="1.0.1",
    packages=find_packages(),
    install_requires=[
        "google-auth-oauthlib>=1.2.1",
        "google-api-python-client>=2.154.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
