from setuptools import setup, find_packages

setup(
    name='hvmnd_api_client',
    version='0.0.1',
    description='Python client library for the Go API application.',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    author='Smarandii',
    author_email='olegsmarandi@gmail.com',
    url='https://github.com/Smarandii/hvmnd-api-client',
    packages=find_packages(),
    install_requires=[
        'requests>=2.0.0',
    ],
    extras_require={
        'dev': [
            'pytest',
            'python-dotenv',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
