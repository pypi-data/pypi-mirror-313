from setuptools import setup, find_packages

setup(
    name='isom5650',
    version='0.2.7',
    description='Do not distribute it without permission. ',
    author='Xuhu Wan',
    author_email='xuhu.wan@gmail.com',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
        'plotly',
        'yfinance',
        'statsmodels'
    ],
)
