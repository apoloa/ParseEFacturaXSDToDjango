class SimpleType(object):
    # Variables
    __slots__ = ['__type', '__name']

    # Constructor
    def __init__(self):
        self.__name = None
        self.__type = None

    def set_type(self, data):
        self.__type = data

    def set_name(self, data):
        self.__name = data

    def get_name(self):
        return self.__name

    def get_type(self):
        return self.__type


class SimpleTypeWithRestrictions(SimpleType):
    __slots__ = ['__restrictions']

    def __init__(self):
        self.__restrictions = []

    def add_restriction(self, restriction):
        self.__restrictions.append(restriction)

    def get_restrictions(self):
        return self.__restrictions


class EnumerationType(SimpleType):
    __slots__ = ['__values']

    def __init__(self):
        self.__values = []

    def add_enumeration(self, enumeration):
        self.__values.append(enumeration)

    def get_enumerations(self):
        return self.__values


class EnumerationValue(object):
    __slots__ = ['__value', '__annotation']

    def __init__(self, value):
        self.__value = value
        self.__annotation = None

    def set_annotation(self, annotation):
        self.__annotation = annotation

    def get_annotation(self):
        return self.__annotation

    def get_value(self):
        return self.__value

    def __str__(self):
        string_value = str(self.__value.encode('utf-8'))
        if self.__annotation is not None:
            string_value += " - " + str(self.__annotation.encode('utf-8'))
        return string_value


class DataTypeRestriction(object):
    __slots__ = ['__name', '__value']

    def __init__(self, name, value):
        self.__name = name
        self.__value = value

    def get_name(self):
        return self.__name

    def get_value(self):
        return self.__value
