# -*- coding: utf-8 -*-
import xml.etree.ElementTree

import sys
from ComplexType import ComplexType, ComplexElement
from SimpleType import SimpleType
from SimpleType import EnumerationType
from SimpleType import SimpleTypeWithRestrictions
from SimpleType import EnumerationValue
from SimpleType import DataTypeRestriction
from WriteFile import FileToWrite


reload(sys)
sys.setdefaultencoding('utf8')
print sys.stdout.encoding
root_element = xml.etree.ElementTree.parse('facturae.xml').getroot()
simple_types = {}
complex_types = []




def parseSimpleType(element):
    e_simple_type = SimpleType()
    if element.keys() > 0 and element.keys()[0] == 'name':
        #Cogiendo nombre
        print('Coginedo Nombre: ' + str(element.get('name')))
        e_simple_type.set_name(element.get('name'))
        print(element)
    if len(element._children) > 1:
        print('Raro' + len(element._children))
    else:
        children = element._children[0]
        print children
        e_simple_type.set_type(children)
        if children._children[0].tag == '{http://www.w3.org/2001/XMLSchema}enumeration':
            e = parseEnumeration(e_simple_type,children)
            simple_types[e.get_name()] = e
        else :
            e = parseWithLength(e_simple_type, children)
            simple_types[e.get_name()] = e

def parseEnumeration(element_type, children):
    print('Parsing Enumeration')
    enumeration = EnumerationType()
    enumeration.set_name(element_type.get_name())
    enumeration.set_type(element_type.get_type())
    for enumerationValue in children._children:
        enumeration_text = enumerationValue.get('value')
        enumeration_value = EnumerationValue(enumeration_text)
        if len(enumerationValue._children) > 0:
            annotation = enumerationValue._children[0]
            for documentation in annotation._children:
                if(documentation.get('{http://www.w3.org/XML/1998/namespace}lang') == 'es'):
                    enumeration_value.set_annotation(documentation.text)
        enumeration.add_enumeration(enumeration_value)

    return enumeration


def parseWithLength(element_type, children):
    print('Parsing Length')
    exception = SimpleTypeWithRestrictions()
    exception.set_name(element_type.get_name())
    exception.set_type(element_type.get_type().get('base'))
    for exceptionValue in children._children:
        if exceptionValue.tag == '{http://www.w3.org/2001/XMLSchema}maxLength':
            data_restriction = DataTypeRestriction('max_length', exceptionValue.get('value'))
            exception.add_restriction(data_restriction)
        elif exceptionValue.tag == '{http://www.w3.org/2001/XMLSchema}length':
            data_restriction = DataTypeRestriction('max_length', exceptionValue.get('value'))
            exception.add_restriction(data_restriction)
    return exception

def parseComplexType(element):
    print('Parsing Complex Type: ' + element.get('name'))
    complex_type = ComplexType(element.get('name'))
    for hijos in element._children:
        for children in hijos._children:
            if children.tag == '{http://www.w3.org/2001/XMLSchema}element':
                complex_type.add_element(parseElement(children))
            elif children.tag == '{http://www.w3.org/2001/XMLSchema}choice':
                for children_choice in children._children:
                    complex_type.add_element(parseElement(children_choice))
            elif children.tag == '{http://www.w3.org/2001/XMLSchema}documentation':
                if(children.get('{http://www.w3.org/XML/1998/namespace}lang') == 'es'):
                    complex_type.set_annotation(children.text)
            else:
                print "CASOS ESPECIALES!!!!!!"


    complex_types.append(complex_type)

def parseElement(element):
    name = element.get('name')
    type_name = element.get('type')
    type = simple_types.get(type_name)
    complex_element = ComplexElement(name,type_name, type)
    if len(element._children) > 0:
        annotation = element._children[0]
        for annotation_lang in annotation:
            if(annotation_lang.get('{http://www.w3.org/XML/1998/namespace}lang') == 'es'):
                complex_element.set_annotation(annotation_lang.text)
    return complex_element



print "############################ SIMPLE TYPES ############################"
## Primero los SimpleType
for simple_type in root_element.findall("{http://www.w3.org/2001/XMLSchema}simpleType"):
    parseSimpleType(simple_type)
print "############################ COMPLEX TYPES ############################"
## Segundo los ComplexType
for simple_type in root_element.findall("{http://www.w3.org/2001/XMLSchema}complexType"):
    parseComplexType(simple_type)

print "############################ TYPES ############################"
for element in simple_types:
    print element
print "<<<<----------------------------------->>>>"
for element in complex_types:
    print element.get_name()


print "############################ ORDENACION ############################"

def contains(element, list):
    for i in list:
        if element == i:
            return True
    return False

def contains_with_name(element, list):
    for i in list:
        if element.get_type_name() == i.get_name():
            return True
    return False

elements_not_sorted = []
elements_sorted = []
for i in complex_types:
    elements_not_sorted.append(i)

count = 0

print "Iteracion: " + str(count)
print "Elements Sorted: " + str(len(elements_sorted))
print "Elements Not Sorted: " + str(len(elements_not_sorted))

while len(elements_not_sorted) > 0:
    for i in elements_not_sorted:
        if not i.has_complex_types():
            elements_sorted.append(i)
        else:
            list_none = []
            for element in i.get_elements():
                if element.get_type() is None:
                    list_none.append(element)
            contains_all_list = True
            for element_none in list_none:
                if element_none.get_type_name() == 'xs:date':
                    continue
                if element_none.get_type_name() == 'xs:long':
                    continue
                if element_none.get_type_name() == 'xs:double':
                    continue
                if element_none.get_type_name() == 'xs:string':
                    continue
                if not contains_with_name(element_none, elements_sorted):
                    contains_all_list = False
                    break
            if contains_all_list:
                elements_sorted.append(i)
    for i in elements_sorted:
        if contains(i, elements_not_sorted):
            print "Borrando"
            elements_not_sorted.remove(i)
    count += 1
    print "Iteracion: " + str(count)
    print "Elements Sorted: " + str(len(elements_sorted))
    print "Elements Not Sorted: " + str(len(elements_not_sorted))




print "############################ LOADING IN FILE ############################"
file_to_writer = FileToWrite()
for element in elements_sorted:
    file_to_writer.add_complex_type(element)

file_write = open('file.py','w')
file_write.write(str(file_to_writer))
file_write.close()



