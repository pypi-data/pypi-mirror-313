from setuptools import setup

"""
:author: Andrey Kuchebo
:license: MIT
"""

version = 1.0

long_description = """Автоматический дандер-метод __str__ для вашего класса"""

setup(
	name='autostr',
	version=version,
	author='Andrey Kuchebo',
	author_email='kucheboandrey@gmail.com',
	long_description=long_description,
	long_description_content_type='text/markdown',
	package=['autostr']
)