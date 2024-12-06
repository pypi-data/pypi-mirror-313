from setuptools import find_packages, setup


with open('docs/python.md', 'r') as fh:
    long_description = fh.read()


setup(
    name='hestia-earth-schema',
    packages=find_packages(),
    version='30.4.0',
    description='HESTIA Schema library',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Guillaume Royer',
    author_email='guillaumeroyer.mail@gmail.com',
    license='MIT',
    url='https://gitlab.com/hestia-earth/hestia-schema',
    keywords=['hestia', 'schema'],
    classifiers=[],
    install_requires=[],
    python_requires='>=3'
)
