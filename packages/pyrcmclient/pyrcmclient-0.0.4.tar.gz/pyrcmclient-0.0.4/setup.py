from setuptools import setup, find_packages
from codecs import open
from os import path

package_name = "pyrcmclient"
root_dir = path.abspath(path.dirname(__file__))

# requiwements.txtの中身を読み込む
def _requirements():
    return [name.rstrip() for name in open(path.join(root_dir, 'requirements.txt')).readlines()]

# README.mdをlong_discriptionにするために読み込む
with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name=package_name,
    version='0.0.4',
    description='python client for i4s-rcm',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/quatre-i-science/pyrcmclient',
    author='quatre-i-science',
    author_email='i4s_eng@i4s.co.jp',
    license='MIT',
    keywords='i4s rcm client',
    packages=["i4srcm"],#find_packages(where="src"),
    package_dir={ "": "src"},
    install_requires=_requirements(),
    classifiers=[
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.12',
    ],
)