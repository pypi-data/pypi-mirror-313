from setuptools import setup, find_packages


def readme():
    with open('README.md', 'r') as f:
        return f.read()


setup(
    name='BloomORM',
    version='1.0.1',
    author='JenIKs',
    author_email='fertuv68@gmail.com',
    description='This is Json ORM',
    long_description=readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/JenIK-s/BloomORM-json-project',
    packages=find_packages(),
    install_requires=['requests>=2.25.1'],
    classifiers=[
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    keywords='Json ORM',
    project_urls={
        'Documentation': 'https://github.com/JenIK-s/BloomORM-json-project'
    },
    python_requires='>=3.7'
)

