from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

with open("VERSION", "r", encoding="utf-8") as f:
    version = f.read()

setup(
    name='talisman-api',
    version=version,
    description='Python Talisman API client for Talisman-based app',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='ISPRAS Talisman NLP team',
    author_email='modis@ispras.ru',
    maintainer='Vladimir Mayorov',
    maintainer_email='vmayorov@ispras.ru',
    packages=find_packages(include=['talisman_api', 'talisman_api.*']),
    install_requires=[
        'talisman-interfaces~=0.8',
        'aiorwlock~=1.3',
        'gql[aiohttp]~=3.4',
        'requests~=2.31',
        'python-keycloak~=2.16',
        'typing_extensions>=4.0.0'
    ],
    data_files=[('', ['VERSION'])],
    python_requires='>=3.10',
    license='Apache Software License',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.11',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: Apache Software License'
    ]
)
