import os
from setuptools import setup


def read(rel_path: str) -> str:
    here = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(here, rel_path), 'r', encoding='UTF-8') as fp:
        return fp.read()


long_description = read("README.rst")

setup(
    name='pltx',
    packages=['pltx'],
    description="Tools of matplotlib",
    long_description=long_description,
    long_description_content_type='text/markdown',
    version='0.0.2',
    install_requires=[
       "numpy>=1.0.0",
      "matplotlib>=2.0.0",
    ],
    url='https://gitee.com/summry/pltx',
    author='summy',
    author_email='xiazhongbiao@126.com',
    keywords=['matplotlib'],
    package_data={
        # include json and txt files
        '': ['*.rst', '*.dtd', '*.tpl'],
    },
    include_package_data=True,
    python_requires='>=3.6',
    zip_safe=False
)
