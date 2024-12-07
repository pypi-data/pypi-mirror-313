from setuptools import setup, find_packages

setup(
    name='Advanced-Py-Functions',
    version='0.2',
    packages=find_packages(),
    UserName='Induprakash11',
    Email='prakashindu212@gmail.com',
    install_requires=[
        'numpy',
    ],
    test_suite='test',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    license='MIT',
)
