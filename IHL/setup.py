from setuptools import setup, find_packages

setup(
    name='IHL',
    version='0.0.1',
    author='Rexlep',
    author_email='rexlepyo@gmail.com',
    description='A package to make a hover window for your widgets in tkinter or ctkinter',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)