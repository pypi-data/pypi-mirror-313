
from pathlib import Path
import setuptools


def parse_requirements(requirements: str):
    with open(requirements) as f:
        return [
            l.strip('\n') for l in f if l.strip('\n') and not l.startswith('#')
        ]


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="py_code_cleaner", 
    version=Path('version.txt').read_text(encoding='utf-8'),
    author="Demetry Pascal",
    author_email="qtckpuhdsa@gmail.com",
    maintainer='Demetry Pascal',
    description="Small PyPI package which provides python code cleaning from comments, docstrings, annotations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/PasaOpasen/py-code-cleaner",
    license='MIT',
    keywords=['code', 'clean', 'comments', 'docstrings', 'annotations'],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    install_requires=parse_requirements('./requirements.txt'),
    entry_points={
        'console_scripts': [
            'clean-py=py_code_cleaner.cli.clean_py:main',
            'clean-py-many=py_code_cleaner.cli.clean_py_many:main'
        ],
    },
)
