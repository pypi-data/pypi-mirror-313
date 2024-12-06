from setuptools import setup

"""
:author: Andrey Kuchebo
:license: MIT
"""

version = 1.4

long_description = """
# autostr 

Небольшой модуль, который добавляет класс `AutostrMixin`   
Вы можете наследоваться от данного класса и тогда вам не придётся писать `__str__ `

Пример: 

```
class A(AutostrMixin):
	b = 0
	def __init__(self):
		self.a = 1


t = A()
print(t)
```

Вывод: 

```
Экземпляр класса: A

Атрибуты класса:
·b: 0 

Атрибуты экземпляра:
·a: 1 
```

"""

setup(
	name='autostr',
	version=version,
	url='https://github.com/number3141/autostr',
	author='Andrey Kuchebo',
	author_email='kucheboandrey@gmail.com',
	long_description=long_description,
	long_description_content_type='text/markdown',
	package=['autostr']
)