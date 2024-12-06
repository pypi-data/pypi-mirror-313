from setuptools import setup, find_packages

"""
:author: Andrey Kuchebo
:license: MIT
"""

version = 2.0

def write_readme():
	with open('README.md', 'r', encoding='utf-8') as f:
		return f.read()

setup(
	name='autostr',
	version=version,
	author='Andrey Kuchebo',
	author_email='kucheboandrey@gmail.com',
	package=find_packages(),
	description='Automatic __str__ for classes',
	long_description=write_readme(),
	long_description_content_type='text/markdown',
	url='https://github.com/number3141/autostr',
)