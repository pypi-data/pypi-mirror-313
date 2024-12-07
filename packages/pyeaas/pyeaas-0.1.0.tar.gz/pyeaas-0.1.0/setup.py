from setuptools import setup, find_packages

setup(
    name='pyeaas',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        # List your package dependencies here
    ],
    author='Giuliano Errico',
    author_email='errgioul2@gmail.com',
    description='Build your e-commerce',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/ciulene/eaas',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)