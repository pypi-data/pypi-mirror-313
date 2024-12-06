from setuptools import setup, find_packages

setup(
    name='rbac_library',
    version='0.1.0',
    description='Role-Based Access Control Library for Django',
    author='Sravan',
    author_email='your.email@example.com',
    packages=find_packages(),
    install_requires=['django>=3.2'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Framework :: Django",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
