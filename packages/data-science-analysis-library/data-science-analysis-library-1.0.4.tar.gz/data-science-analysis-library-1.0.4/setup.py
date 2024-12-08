from setuptools import setup, find_packages

# Read requirements from the requirements.txt file
with open("requirements.txt") as f:
    install_requires = [line.strip() for line in f if line.strip()]

setup(
    name='data-science-analysis-library',
    version='1.0.4',
    author='Kamil Krawiec, Maciej Mądry, Maciej Sieroń',
    author_email='kamil.krawiec9977@gmail.com',
    description='A Python package for analyzing and visualizing data.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Kamil-Krawiec/Data-explorer-library.git',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.9',
    install_requires=install_requires
)
