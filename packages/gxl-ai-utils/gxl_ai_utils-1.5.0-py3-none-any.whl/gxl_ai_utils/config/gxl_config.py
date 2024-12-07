import yaml


def indent(s_, num_spaces):
    """
    第一行前不加空格, 后面的行均加num个空格
    """
    s = s_.split("\n")
    if len(s) == 1:
        return s_
    first = s.pop(0)
    s = [(num_spaces * " ") + line for line in s]
    s = "\n".join(s)
    s = first + "\n" + s
    return s


class GxlNode(dict):
    frozen = False

    def __init__(self, input_dict):
        super(GxlNode, self).__init__(input_dict)
        for key, value in input_dict.items():
            if isinstance(value, dict):
                self[key] = GxlNode(value)
            else:
                if value == 'None':
                    value = None
                if value == 'True':
                    value = True
                if value == 'False':
                    value = False
                super().__setitem__(key, value)

    def __getattr__(self, name):
        """
        当你访问一个对象的属性，而该属性不存在时，Python 会自动调用 __getattr__ 方法
        ，以便你有机会定义一个默认的行为或返回一个替代值
        """
        if name in self:
            value = self[name]
            if isinstance(value, dict):
                return GxlNode(value)
            else:
                return value
            # return value
        else:
            return None

    def __getitem__(self, name):
        """
        当你使用[key]访问一个对象的属性,会自动调用 __getitem__ 方法
        """
        if name in self:
            value = super().__getitem__(name)
            return value
        else:
            return None

    def __setitem__(self, name, value):
        """
        当我们使用obj[key] = value 时,自动调用该函数
        :param name:
        :param value:
        :return:
        """
        if self.is_frozen:
            raise AttributeError(
                "Attempted to set {} to {}, but GxlNode is immutable".format(
                    name, value
                )
            )
        else:
            if isinstance(value, dict):
                super().__setitem__(name, GxlNode(value))
            else:
                super().__setitem__(name, value)

    def __setattr__(self, name, value):
        """
        当我们使用obj.attr = value 时,自动调用该函数
        :param name:
        :param value:
        :return:
        """
        if self.is_frozen:
            raise AttributeError(
                "Attempted to set {} to {}, but GxlNode is immutable".format(
                    name, value
                )
            )
        else:
            if isinstance(value, dict):
                self[name] = GxlNode(value)
            else:
                self[name] = value

    def __str__(self):
        """
        当你使用 str(obj) 函数或内置的 print(obj) 函数时，如果对象定义了
        __str__ 方法，Python 将调用该方法来获取对象的字符串表示形式。打印为yaml格式
        """
        r = ""
        s = []
        for k, v in sorted(self.items()):
            seperator = "\n" if isinstance(v, GxlNode) else " "
            attr_str = "{}:{}{}".format(str(k), seperator, str(v))
            attr_str = indent(attr_str, 2)
            s.append(attr_str)
        r += "\n".join(s)
        r = 'GxlNode--------------------------start\n' + r + '\nGxlNode------------------------end'
        return r
        # return self.dict_f().__str__()

    def __repr__(self):
        """
        当你使用 repr(obj) 函数时，如果对象定义了 __repr__ 方法, Python 将调用该方法
        """
        # return "{}({})".format(self.__class__.__name__, super(GxlNode, self).__repr__())
        return self.dict_f().__repr__()
    def copy(self):
        """
        复制self,得到一个新的GxlNode对象
        :return:
        """
        return GxlNode(self)

    def dict_f(self):
        """
        将self转化为dict
        :return:
        """
        res = {}
        for k, v in self.items():
            if isinstance(v, GxlNode):
                res[k] = v.dict_f()
            else:
                res[k] = v
        return res

    def dump(self):
        """
        得到yaml格式的str,用于存入一个yaml文件
        :return:
        """
        return yaml.dump(self.dict_f())

    def write_to_yaml(self, yaml_path: str):
        """
        将self写入yaml文件
        :param yaml_path:
        :return:
        """
        with open(yaml_path, 'w', encoding='utf-8') as f:
            f.write(self.dump())

    @property
    def is_frozen(self):
        return self.frozen

    def make_frozen(self):
        self.frozen = True

    def break_frozen(self):
        self.frozen = False

    @classmethod
    def get_config_from_yaml(cls, file_path: str):
        with open(file_path, 'rt', encoding='utf-8') as f:
            dict_1 = yaml.load(f, Loader=yaml.FullLoader)
        return cls(dict_1)

    @classmethod
    def get_dict_from_yaml(cls, file_path: str):
        return cls.get_config_from_yaml(file_path).dict_f()
