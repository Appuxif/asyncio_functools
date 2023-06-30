import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='asyncio_functools',
    version='0.0.2',
    author='Appuxif',
    author_email='app@mail.com',
    description='A Python package with functools working with asyncio coroutines',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Appuxif/asyncio_functools',
    project_urls={
        'Bug Tracker': 'https://github.com/Appuxif/asyncio_functools/issues',
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    package_dir={'': '.'},
    packages=['asyncio_functools'],
    package_data={},
    python_requires='>=3.8',
)
