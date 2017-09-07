try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def readme():
    with open('README.md') as f:
        return f.read()

setup(
    name='demeter',
    version='1.0.0',
    packages=['demeter.change', 'demeter.weight', 'demeter', 'demeter.demeter_io'],
    url='https://github.com/IMMM-SFA/demeter',
    license='BSD 2-Clause',
    author='Chris R. Vernon; Yannick le Page',
    author_email='chris.vernon@pnnl.gov; niquya@gmail.com',
    description='A land use land cover disaggregation and land change analytic model',
    long_description=readme(),
    install_requires=[
        'numpy',
        'scipy',
        'matplotlib',
        'fiona',
        'netCDF4',
        'pandas'
    ]
)
