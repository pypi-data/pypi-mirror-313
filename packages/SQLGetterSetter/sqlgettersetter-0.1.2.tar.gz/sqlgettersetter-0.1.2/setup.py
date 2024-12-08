from setuptools import setup, find_packages

setup(
    name = 'SQLGetterSetter',
    version = '0.1.2',
    packages = find_packages(),
    install_requires =[
        #library like 'pymongo = 3.2.1',

    ],
    entry_points = {
        "console_scripts": [
            "SQL-tester = SQLGetterSetter:hello",

        ],
    },
)