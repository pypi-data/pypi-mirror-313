from setuptools import setup, find_packages

setup(
    name="arka_python_dev",
    version="0.4",
    description="A Python package to interact with the Arka blockchain network",
    author="Python",
    author_email="support@arka.com",
    packages=find_packages(),
    install_requires=[
        "requests",
        "tqdm",
    ],
    python_requires=">=3.6",
)
