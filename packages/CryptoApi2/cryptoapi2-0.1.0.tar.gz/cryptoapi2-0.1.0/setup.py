from setuptools import setup, find_packages

setup(
    name='CryptoApi2',
    version='0.1.0',
    author='Konrad Tercjak',
    author_email='ktercjak0@gmail.com',
    description='CryptoAPI is a powerful Python library designed to simplify interaction with various cryptocurrency APIs. (Binance REST and WebSockets)',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/tercjak/CryptoAPI',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
    install_requires=[
        'numpy>=1.21.0',
        'requests>=2.25.1',
        'websocket_client>=1.8.0',
        'pydantic>=2.10.3'
    ],
)