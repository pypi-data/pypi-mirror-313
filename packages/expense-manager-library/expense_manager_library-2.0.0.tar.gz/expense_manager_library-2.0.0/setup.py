from setuptools import setup, find_packages

setup(
    name="expense_manager_library",
    version="2.0.0",
    description="A library to analyze expense data and generate PDF reports.",
    url="https://github.com/berry24a/expense_manager_library",
    packages=find_packages(),
    install_requires=[
        "pandas>=1.3.5",
        "matplotlib>=3.5.1"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
