from setuptools import setup, find_packages

setup(
    name='prompt_program',  # Replace with your package’s name
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        # List your dependencies here
    ],
    author='Krishna Rathore',  
    author_email='krishnarathore393@gmail.com',
    description='A library for creating perfectly intended prompts.',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # License type
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',

)