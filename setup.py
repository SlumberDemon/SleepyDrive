import pathlib
from setuptools import setup, find_packages


here = pathlib.Path(__file__).parent.resolve()

long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='sleepydrive',
    version='0.2.8',
    description='Edited version of AirDrive for personal use',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/SlumberDemon/SleepyDrive',
    author='SlumberDemon',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        "Programming Language :: Python :: 3.10",
        'Programming Language :: Python :: 3 :: Only',
    ],
    keywords='storage, cloud-storage, drive, storage-service, web-storage',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    python_requires='>=3.6, <4',
    install_requires=['deta', 'urllib3'],
    project_urls={
        'Bug Reports': 'https://github.com/jnsougata/AirDrive/issues',
        'Source': 'https://github.com/SlumberDemon/SleepyDrive',
    },
)
