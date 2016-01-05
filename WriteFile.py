# -*- coding: utf-8 -*-

from FileUtils import *


class Clase(object):
    __slots__ = ['__name', '__properties', '__annotation']

    def __init__(self, name):
        self.__name = name
        self.__properties = []
        self.__annotation = None

    def set_annotation(self, annotation):
        self.__annotation = annotation

    def get_annotation(self):
        return self.__annotation

    def is_empty(self):
        return self.__properties == 0

    def add_property(self, property):
        self.__properties.append(property)

    def get_name(self):
        return self.__name

    def __str__(self):
        string_value = ""
        if self.__annotation is not None:
            string_value = string_value + self.__annotation + "\n"
        string_value = string_value + "class " + self.__name + "(models.Model):"
        string_value += "\n"
        for property in self.__properties:
            string_value = string_value + "\t" + str(property) + "\n"

        return string_value


class EnumerationConstant(object):
    __slots__ = ['__name', '__show_text']

    def __init__(self, name, show_text):
        self.__name = name
        self.__show_text = show_text

    def __str__(self):
        return "(" + self.__name.encode('utf-8') + ", '" + self.__show_text.encode('utf-8') + "')"


class Enumeration(object):
    __slots__ = ['__name', '__elements']

    def __init__(self, name):
        self.__name = name
        self.__elements = []

    def add_element(self, element):
        self.__elements.append(element)

    def get_name(self):
        return self.__name

    def __str__(self):
        string_return = self.__name + " = ( \n"
        for i in self.__elements:
            string_return += str("\t") + str(i) + str(",\n")
        string_return = string_return[:-2]
        string_return += "\n)\n"
        return string_return

    def __eq__(self, other):
        if type(other).__name__ == Enumeration:
            return other.get_name() == self.__name
        else:
            return False

    def __cmp__(self, other):
        if type(other).__name__ == Enumeration:
            return other.get_name() == self.__name
        else:
            return False


class Method(object):
    __slots__ = ['__name', '__type', '__annotation', '__properties']

    def __init__(self, name, type):
        self.__name = name
        self.__type = type
        self.__annotation = None
        self.__properties = { 'null':True, 'blank':True}

    def set_annotation(self, annotation):
        self.__annotation = annotation

    def add_properties(self, name, value):
        self.__properties[name] = value

    def __str__(self):
        string_value = "" + str(self.__name) + " = models." + self.__type + "("

        for property in self.__properties.keys():
            string_value = string_value + property + '=' + str(self.__properties[property]) + ","

        if len(self.__properties.keys()) > 0:
            string_value = string_value[:-1]

        string_value += ")"

        if self.__annotation is not None:
            string_value = string_value + " # " + self.__annotation.encode('utf-8')

        return string_value

class EnumMethod(Method):
    def __init__(self, name, length, choices):
        super(EnumMethod,self).__init__(name,'CharField')
        self.add_properties('max_length', length)
        self.add_properties('choices',choices)

class DateMethod(Method):
    def __init__(self, name):
        super(DateMethod, self).__init__(name, 'DateTimeField')


class StringMethod(Method):
    def __init__(self, name):
        super(StringMethod, self).__init__(name, 'CharField')
        self.add_properties('max_length', 40)


class LongMethod(Method):
    def __init__(self, name):
        super(LongMethod, self).__init__(name, 'BigIntegerField')


class FloatMethod(Method):
    def __init__(self, name):
        super(FloatMethod, self).__init__(name, 'DecimalField')
        self.add_properties('max_digits', 19)
        self.add_properties('decimal_places', 10)


class ForeignKey(object):
    __slots__ = ['__name', '__foreign_key_value', '__annotation', '__nclass']

    def __init__(self, name, value, nclass):
        self.__name = name
        self.__foreign_key_value = value
        self.__nclass = nclass
        self.__annotation = None

    def set_annotation(self, annotation):
        self.__annotation = annotation

    def __str__(self):
        if self.__annotation is None:
            return self.__name + " = models.ForeignKey(" + self.__foreign_key_value + ", blank=True, null=True, related_name='" + convert_to_variable(self.__name +self.__nclass + self.__foreign_key_value) + "')"
        else:
            return self.__name + " = models.ForeignKey(" + self.__foreign_key_value + ", blank=True, null=True, related_name='" + convert_to_variable(self.__name +self.__nclass + self.__foreign_key_value) + "') #" + self.__annotation.encode(
                'utf-8')


class FileToWrite(object):
    __slots__ = ['__constants', '__header', '__objects']

    def __init__(self):
        self.__constants = []
        self.__header = []
        self.__objects = []

    def add_complex_type(self, complex_type):
        clase = Clase(complex_type.get_name())
        if complex_type.get_annotation():
            clase.set_annotation(complex_type.get_annotation())
        for method in complex_type.get_elements():
            if method.get_type() is None:
                part = None
                if method.get_type_name() == 'xs:date':
                    part = DateMethod(method.get_name())
                elif method.get_type_name() == 'xs:string':
                    part = StringMethod(method.get_name())
                elif method.get_type_name() == 'xs:long':
                    part = LongMethod(method.get_name())
                elif method.get_type_name() == 'xs:double':
                    part = FloatMethod(method.get_name())
                else:
                    part = ForeignKey(method.get_name(), method.get_type_name(), complex_type.get_name())
                if method.get_annotation() is not None:
                    part.set_annotation(method.get_annotation())
                clase.add_property(part)
            elif type(method.get_type()).__name__ == 'SimpleTypeWithRestrictions':
                m = None
                if method.get_type().get_type() == 'xs:string':
                    m = Method(method.get_name(), 'CharField')
                    for rs in method.get_type().get_restrictions():
                        m.add_properties(rs.get_name(), rs.get_value())

                elif method.get_type().get_type() == 'xs:double':
                    m = FloatMethod(method.get_name())

                if method.get_annotation() is not None:
                    m.set_annotation(method.get_annotation())

                clase.add_property(m)
            elif type(method.get_type()).__name__ == 'EnumerationType':
                if len(method.get_type().get_enumerations()) == 1:
                    print "SOLO UNO!!!"
                    m = Method(method.get_name(), 'CharField')
                    max_l = len(method.get_type().get_enumerations()[0].get_value())
                    default = "'"+method.get_type().get_enumerations()[0].get_value()+"'"
                    m.add_properties('max_length',max_l)
                    m.add_properties('default', default)
                    clase.add_property(m)
                else:

                    enum = None
                    for enum_header in self.__header:
                        if enum_header.get_name() == method.get_type_name():
                            enum = enum_header
                            break

                    if enum is None:
                        enum = Enumeration(method.get_type_name())
                        for enumerate in method.get_type().get_enumerations():
                            string_constant = ""
                            enumeration_constant = None
                            if enumerate.get_annotation() is None:
                                name = convert_to_upper_python(
                                    enumerate.get_value())
                                show_name = enumerate.get_value()
                                string_constant = name + " = '" + show_name + "'"
                                enumeration_constant = EnumerationConstant(name,show_name)
                            else:
                                name = convert_to_upper_python(enumerate.get_annotation())
                                string_constant = name + " = '" + enumerate.get_value() + "'"
                                enumeration_constant = EnumerationConstant(name,enumerate.get_annotation())
                            enum.add_element(enumeration_constant)
                            if string_constant not in self.__constants:
                                self.__constants.append(string_constant)
                        self.__header.append(enum)


                    max_length = 0
                    for e in method.get_type().get_enumerations():
                        if max_length < len(e.get_value()):
                            max_length = len(e.get_value())

                    enum_method = EnumMethod(method.get_name(),max_length,enum.get_name())
                    clase.add_property(enum_method)
        if not clase.is_empty():
            self.__objects.append(clase)

    def __str__(self):

        string_value = "\n".join(self.__constants)
        header_string = "\n".join(str(x) for x in self.__header)
        object_string = "\n".join(str(x) for x in self.__objects)
        list = [string_value, header_string, object_string]
        return_string = "\n".join(list)

        return_string += "\n\n\n"
        for i in self.__objects:
            return_string += "\n" + "admin.site.register(" + i.get_name() + ")"
        return return_string
