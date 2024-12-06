from setuptools import setup

setup(
    name = 'cameo_geo_query',
    version = '1.0.18',
    description='This is cameo_geo_query',
    url = '',
    author = 'bear',
    author_email='panda19931217@gmail.com',
    license='BSD 2-clause',
    packages=['cameo_geo_query'],
    install_requires=[
        'pandas',
        'geopy',
        'plotly'
    ]
)
