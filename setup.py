from setuptools import setup, find_packages

setup(
    name='cerebro',
    description="Brazillian internet mapping tool",
    version='1.0.0',
    author='Davidson Mizael',
    author_email='davidsonmizael@gmail.com',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    python_requires='>=3.9',
    packages=find_packages(),
    install_requires=open('requirements.txt').read()
)