from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

with open("VERSION", "r", encoding="utf-8") as f:
    version = f.read()

setup(
    name='talisman-tools',
    version=version,
    description='Talisman applications',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='ISPRAS Talisman NLP team',
    author_email='modis@ispras.ru',
    maintainer='Vladimir Mayorov',
    maintainer_email='vmayorov@ispras.ru',
    packages=find_packages(include=['talisman_tools', 'talisman_tools.*']),
    install_requires=[
        'talisman-interfaces~=0.8', 'talisman-dm~=1.2',
        'fastapi>=0.73.0', 'pydantic~=1.10.4', 'uvicorn>=0.13.3', 'requests~=2.31.0', 'urllib3~=2.2.0',
        'jsonformatter>=0.3.0',
        'starlette', 'anyio',
        'pyyaml'
    ],
    extras_require={
        'logstash': ['python3-logstash>=0.4.80'],
        'evaluate': ['numpy', 'scipy', 'typing_extensions~=4.8.0'],
        'cuda_metrics': ['torch'],
        "tests": ['parameterized~=0.9.0']
    },
    entry_points={
        'console_scripts': [
            'talisman-tools = talisman_tools.talisman:main',
        ]
    },
    data_files=[('', ['VERSION'])],
    python_requires='>=3.10',
    license='Apache Software License',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: Apache Software License'
    ]
)
