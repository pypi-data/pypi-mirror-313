from setuptools import setup, find_packages

setup(
    name='mkpipe-loader-postgres',
    version='0.1.11',
    license='Apache License 2.0',
    packages=find_packages(),
    install_requires=[],
    include_package_data=True,
    entry_points={
        'mkpipe.loaders': [
            'postgresql = mkpipe_loader_postgres:PostgresLoader',
        ],
    },
    description='PostgreSQL loader for mkpipe.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Metin Karakus',
    author_email='metin_karakus@yahoo.com',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
    ],
    python_requires='>=3.8',
)
