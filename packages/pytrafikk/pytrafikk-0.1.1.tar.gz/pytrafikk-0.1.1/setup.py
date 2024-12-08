from setuptools import setup, find_packages

setup(
    name="pytrafikk",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.0",
        "pandas>=1.3.0",
        "flask>=2.0.0",
        "folium>=0.12.0",
        "plotly>=5.0.0",
        "pandas>=1.3.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "black>=21.0",
            "flake8>=3.9",
        ],
    },
    python_requires=">=3.9",
    author="Paul Skeie",
    author_email="paul.skeie@gmail.com",
    description="A Python client for Norwegian traffic data",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/paulskeie/pytrafikk",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
