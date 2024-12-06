from setuptools import setup, find_packages

setup(
    name='groclake',  # Name of the package
    version='0.1.8',
    packages=find_packages(),
    namespace_packages=['groclake'],  # Declare the namespace
    install_requires=['requests', ],  # Add external dependencies if any
)
