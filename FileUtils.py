# -*- coding: utf-8 -*-

def convert_to_upper_python(value):
    value = remove_accents(value)
    value = value.upper()
    text_new = ""
    for i in value:
        if i == " ":
            text_new += '_'
        elif RepresentsInt(i):
            pass
        elif i == "\"":
            pass
        elif i == ",":
            pass
        elif i == "/":
            text_new += '_'
        elif i == "-":
            text_new += '_'
        elif i == "(":
            break
        elif i == ":":
            break
        elif i == ".":
            break
        else:
            text_new += i

    if text_new.endswith("_"):
        text_new = text_new[:-1]
    return text_new

def remove_accents(s):
    elements = ""
    for i in s:
        if i=='á' or i=='à':
            elements += 'a'
        elif i=='Á' or i=='À':
            elements += 'A'
        elif i=='é' or i=='è':
            elements += 'e'
        elif i=='É' or i=='È':
            elements += 'E'
        elif i=='í' or i=='ì':
            elements += 'i'
        elif i=='Í' or i=='Ì':
            elements += 'I'
        elif i=='ó' or i=='ò':
            elements += 'o'
        elif i=='Ó' or i=='Ò':
            elements += 'O'
        elif i=='ú' or i=='ù':
            elements += 'u'
        elif i=='Ú' or i=='Ù':
            elements += 'U'
        elif i=='ñ':
            elements += 'n'
        elif i=='Ñ':
            elements += 'N'
        else:
            elements += i
    return elements

def convert_to_variable(s):
    first = False
    r = ""
    for i in s:
        if i.isupper():
            if not first:
                first = True
                r += str(i.lower())
            else:
                r += "_" + str(i.lower())
        else:
            r += i

    return r



def RepresentsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False