from setuptools import find_packages
from setuptools import setup

with open('requirements.txt') as f:
    install_requires = f.read().strip().split('\n')

setup(
    name='yfa',
    version='0.0.1',
    install_requires=install_requires,
    packages=find_packages(),
    url='https://github.com/yourfinance-app/yfa_backend',
    license='MIT',
    author='Fahim Ali Zain',
    author_email='fahimalizain@gmail.com',
    description='YFA Backend',
    entry_points={
        "console_scripts": ["yfa = yfa.cli:entrypoint"]
    }
)
