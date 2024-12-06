from setuptools import setup, find_packages

setup(
    name='pack5',
    version='0.1.1',
    packages=find_packages(),
    install_requires=[
        # List your package dependencies here
    ],
    author='Tommy B',
    author_email='tombancode@gmail.com',
    description='A short description of your package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/your_package',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.9',
)