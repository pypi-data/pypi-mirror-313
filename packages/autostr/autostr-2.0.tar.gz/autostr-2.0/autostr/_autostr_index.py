class AutostrMixin:
	def __str__(self):
		all_attr = set([item for item in dir(self) if not item.startswith('__')])
		attr_cls_keys = all_attr - set(self.__dict__.keys())
		attr_cls = {}
		for key in attr_cls_keys:
			attr_cls[key] = self.__getattribute__(key)

		result_str = f"""Экземпляр класса: {self.__class__.__name__}\n\n"""

		if len(attr_cls) > 0:
			result_str += "Атрибуты класса:\n"
			for attr in attr_cls:
				result_str += f'·{attr}: {self.__getattribute__(attr)} \n'
			result_str += '\n'

		if len(self.__dict__) > 0:
			result_str += "Атрибуты экземпляра:\n"
			for attr in self.__dict__:
				result_str += f'·{attr}: {self.__getattribute__(attr)} \n'

		return result_str


if __name__ == '__main__':
	class A(AutostrMixin):
		b = 0
		def __init__(self):
			self.a = 1


	t = A()
	print(t)



