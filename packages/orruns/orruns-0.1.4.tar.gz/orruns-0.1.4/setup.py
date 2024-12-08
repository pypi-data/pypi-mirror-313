from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="orruns",
    version="0.1.4",
    description="Next-generation Experiment Management Platform for Operations Research",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lengff123/ORruns",
    project_urls={
        "Bug Tracker": "https://github.com/lengff123/ORruns/issues",
        "Documentation": "https://orruns.readthedocs.io",
        "Source Code": "https://github.com/lengff123/ORruns",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Education",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: OS Independent",
        "Natural Language :: English",
        "Environment :: Console",
    ],
    python_requires=">=3.8",
    install_requires=[
        "click>=7.0",
        "cloudpickle>=1.6.0",
        "matplotlib>=3.3.0",
        "numpy>=1.19.0",
        "pandas>=1.0.0",
        "tabulate>=0.8.0",
        "dash",
        "dash-bootstrap-components",
        "plotly",
        "flask"
    ],
    extras_require={
        'dev': [
            'pytest>=6.0.0',
            'pytest-cov>=2.0.0',
            'black>=22.0.0',
            'isort>=5.0.0',
            'mypy>=0.900',
            'pylint>=2.0.0',
        ],
        'docs': [
            'sphinx>=4.0.0',
            'sphinx-rtd-theme>=1.0.0',
        ],
    },
    entry_points={
        "console_scripts": [
            "orruns=orruns.cli.commands:cli",
        ],
    },
    package_data={
        "orruns": [
            "py.typed",
            "LICENSE",
            "README.md",
            "api/*",
            "cli/*",
            "core/*",
        ],
    },
    include_package_data=True,
    keywords=[
        "operations research",
        "optimization",
        "experiment tracking",
        "scientific computing",
        "mathematical optimization",
        "research tools",
        "experiment management",
        "reproducible research",
    ],
    platforms=["any"],
    zip_safe=False,
    license="GNU Affero General Public License v3",
)