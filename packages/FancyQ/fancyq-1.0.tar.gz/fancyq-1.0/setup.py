from setuptools import setup, find_packages

setup(
    name='FancyQ',
    version='1.0',
    author= 'Kingston-Zavier Detwiler',
    author_email= 'kingston.z.detwiler@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        '': ['*.py'],  # Include all .py files
    },
)
