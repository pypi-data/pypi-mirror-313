from setuptools import setup, find_packages

from pathlib import Path

 
long_description = Path('README.md').read_text() if Path('README.md').exists() else ''
 
setup(
    name='python_test_video_fp',
    version='0.3.0',

    packages=find_packages(),
    install_requires=[
        'requests'  # Note the quotes
    ],
    author='subbaraju',
    author_email='subba3295@gmail.com',
    description='Video SDK for processing',
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.7',
)
