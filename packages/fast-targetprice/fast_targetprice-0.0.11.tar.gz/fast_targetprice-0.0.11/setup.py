from setuptools import setup, find_packages

setup(
    name="fast_targetprice",  # Tên thư viện (phải duy nhất trên PyPI)
    version="0.0.11",  # Phiên bản
    author="Your Name",
    packages=find_packages(),  # Tự động tìm các package
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
    python_requires=">=3.6",
)
