# autostr 

Небольшой модуль, который добавляет класс `AutostrMixin`   
Вы можете наследоваться от данного класса и тогда вам не придётся писать `__str__ `

Пример: 

```
from autostr import AutostrMixin

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
