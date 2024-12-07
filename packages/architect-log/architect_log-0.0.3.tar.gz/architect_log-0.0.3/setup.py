import setuptools

setuptools.setup(
    name='architect-log',
    version='0.0.3',
    license='MIT',
    author="Alexander Vo",
    author_email='hocthucv@gmail.com',
    packages=setuptools.find_packages(where='src'),
    package_dir={'': 'src'},
    url='https://github.com/hocthucv/architect-log',
    entry_points={
        "console_scripts": [
            "architect_log=architect_log.main:main",
        ],
    },
)
