from setuptools import setup, find_packages
setup(
    name = 'otto',
    version = '0.0',
    packages = find_packages(),
    install_requires = [
        'Click',
        'networkx',
    ],
    entry_points='''
    [console_scripts]
    otto=otto.cli:main
    ''',
)
