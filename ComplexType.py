class ComplexElement(object):
    __slots__ = ['__name', '__annotation', '__type_name', '__type']

    def __init__(self, name, type_name, type):
        self.__name = name
        self.__annotation = None
        self.__type_name = type_name
        self.__type = type

    def set_annotation(self, annotation):
        self.__annotation = annotation

    def get_name(self):
        return self.__name

    def get_type(self):
        return self.__type

    def get_type_name(self):
        return self.__type_name

    def get_annotation(self):
        return self.__annotation

    def __str__(self):
        return str(self.__name) + " - " + str(self.__type_name)

class ComplexType(object):
    __slots__ = ['__name','__elements', '__annotation']

    def __init__(self, name):
        self.__name = name
        self.__elements = []
        self.__annotation = None

    def add_element(self, element):
        self.__elements.append(element)

    def get_name(self):
        return self.__name

    def get_elements(self):
        return self.__elements

    def set_annotation(self,annotation):
        self.__annotation = annotation

    def get_annotation(self):
        return self.__annotation

    def has_complex_types(self):
        for element in self.__elements:
            if(element.get_type() == None):
                return True

        return False

    def __str__(self):
        return self.__name
