from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

with open("VERSION", "r", encoding="utf-8") as f:
    version = f.read()

setup(
    name='talisman-ie-ml-base',
    version=version,
    description='Talisman-IE ML base implementations',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='ISPRAS Talisman NLP team',
    author_email='modis@ispras.ru',
    maintainer='Vladimir Mayorov',
    maintainer_email='vmayorov@ispras.ru',
    packages=find_packages(include=['tie_ml_base', 'tie_ml_base.*']),
    install_requires=[
        'talisman-interfaces~=0.8',
        'talisman-tools~=0.8',
        'numpy~=1.23.5',
        'pynvml~=11.5.0',
        'talisman-dm~=1.2',
        'torch~=2.1.0',
        'transformers~=4.35.2',
        'typing-extensions>=4.0.0'
    ],
    entry_points={
        'talisman.plugins': [
            'tie_ml_base = tie_ml_base'
        ]
    },
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
