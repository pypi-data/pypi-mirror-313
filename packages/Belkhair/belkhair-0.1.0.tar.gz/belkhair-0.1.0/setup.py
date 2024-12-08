from setuptools import setup, find_packages

setup(
    name='Belkhair',
    version='0.1.0',
    author='Ali Belkhair',
    description='A utility package for math, string, and date operations',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    license='MIT' ,
    zip_safe=False ,
)