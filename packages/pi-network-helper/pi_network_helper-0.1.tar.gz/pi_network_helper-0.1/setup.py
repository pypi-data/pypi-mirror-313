# setup.py

from setuptools import setup, find_packages

setup(
    name='pi_network_helper',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    license='MIT',
    description='A library for interacting with Pi Network API',
    long_description=open('README.md').read(),
    url='https://github.com/roniahmadi/pi_network_helper',
    author='Roni Ahmadi',
    author_email='roniahmadi30@gmail.com',
    install_requires=[
        'requests',
        'stellar-sdk',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
)
