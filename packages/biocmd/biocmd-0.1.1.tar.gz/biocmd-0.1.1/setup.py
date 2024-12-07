from setuptools import setup, find_packages

setup(
    name='biocmd',
    version='0.1.1',
    description='BioLab Client',
    author='Yaping-Liu',
    author_email='applesline@163.com',
    license='Apache License 2.0',
    url="https://github.com/BioHubX/biocmd",
    packages = ['biocmd'],
    install_requires=[
        'click',
    ],
    entry_points={
        'console_scripts': [
            'biocmd=biocmd.entry:cli',
        ],

    },
)