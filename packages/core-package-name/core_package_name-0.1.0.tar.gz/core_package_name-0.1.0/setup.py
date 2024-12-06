from setuptools import setup, find_packages

setup(
    name="core_package_name",  # Name of the package
    version="0.1.0",      # Version of the package
    description="Core machine learning code for platform integration.",
    author="M Umer Sohail Khan",
    author_email="your.email@example.com",
    packages=find_packages(),  # Automatically find packages in the directory
    install_requires=[         # Dependencies, if any
        "numpy>=1.21.0",
        "pandas>=1.3.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',   # Minimum Python version required
)