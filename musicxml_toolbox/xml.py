import xml.etree.ElementTree as ET
import logging


#----------------------------------------------------------


def find(element, tags):
    el = element

    for tag in tags:
        el = el.find(tag)
        if el is None:
            return None

    return el


#----------------------------------------------------------


def indexOfChild(element, tag):
    for index, child in enumerate(element):
        if child.tag == tag:
            return index

    return -1


#----------------------------------------------------------


def compare(x1, x2, excludes=[]):
    """
    Compares two xml elements
    :param x1: the first element
    :param x2: the second element
    :param excludes: list of string of attributes to exclude from comparison
    :return:
        True if both elements match
    """
    
    def text_compare(t1, t2):
        """
        Compare two text strings
        :param t1: text one
        :param t2: text two
        :return:
            True if a match
        """
        if not t1 and not t2:
            return True
        if t1 == '*' or t2 == '*':
            return True
        return (t1 or '').strip() == (t2 or '').strip()


    if x1.tag != x2.tag:
        print('Tags do not match: %s and %s' % (x1.tag, x2.tag))
        return False

    for name, value in x1.attrib.items():
        if not name in excludes:
            if x2.attrib.get(name) != value:
                print('Attributes do not match: %s=%r, %s=%r' %
                      (name, value, name, x2.attrib.get(name)))
                return False

    for name in x2.attrib.keys():
        if not name in excludes:
            if name not in x1.attrib:
                print('x2 has an attribute x1 is missing: %s' % name)
                return False

    if not text_compare(x1.text, x2.text):
        print('text: %r != %r' % (x1.text, x2.text))
        return False

    if not text_compare(x1.tail, x2.tail):
        print('tail: %r != %r' % (x1.tail, x2.tail))
        return False

    cl1 = x1.getchildren()
    cl2 = x2.getchildren()
    if len(cl1) != len(cl2):
        print('children length differs, %i != %i' % (len(cl1), len(cl2)))
        return False

    i = 0
    for c1, c2 in zip(cl1, cl2):
        i += 1
        if not c1.tag in excludes:
            if not compare(c1, c2, excludes):
                print('children %i do not match: %s' % (i, c1.tag))
                return False

    return True
