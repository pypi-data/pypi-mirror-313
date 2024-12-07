from setuptools import setup

setup(
    name='byu_accounting',
    version='0.1.1',    
    description='Package for use by BYU Accounting Students',
    url='https://github.com/joshlee84/byu_accounting',
    author='Josh Lee',
    author_email='joshlee84@byu.edu',
    license='MIT',
    packages=['byu_accounting'],
    install_requires=[
        'requests',
        'pypdf',
        'pandas',
        'selenium',
        'tk',
    ],
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Education',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    python_requires='>=3.7',
)