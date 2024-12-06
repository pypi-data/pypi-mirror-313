import sys
from setuptools import setup, find_packages

setup(
    name='iges-sentence-splitter',
    version='0.1.14',
    description='A package for sentence splitting using a pre-trained transformer model.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Kathryn Chapman',
    author_email='kathryn.chapman@iges.com',
    url='https://github.com/kathrynchapman/sentence_splitter',
    packages=find_packages(),
    package_data={
        'sentence_splitter': ['model/*'],  # Include model files
    },
    include_package_data=True,
    install_requires=[
        "numpy==2.1.3",
        "requests",
        "gdown==5.2.0",
        "bitsandbytes==0.44.1",
        "accelerate==1.1.1",
        "transformers",
    ],
    extras_require={
        "torch": [
            "torch==2.5.1+cu121",
            "torchvision==0.20.1+cu121",
            "torchaudio==2.5.1+cu121",
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
