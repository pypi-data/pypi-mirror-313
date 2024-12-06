from setuptools import setup, find_packages

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()
    
with open('requirements.txt', encoding='utf-8') as f:
    install_requires = f.read().splitlines()

setup(
    name='synthetic-eval',
    version='0.1.4',
    author='Seunghwan An',
    author_email='dpeltms79@gmail.com',
    description='Package for Evaluation of Synthetic Tabular Data Quality',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/an-seunghwan/synthetic_eval',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
    python_requires='>=3.8',
    install_requires=install_requires
)