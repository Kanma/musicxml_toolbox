from copy import deepcopy


class XMLElementWrapper(object):

    def __init__(self, xml_element):
        self.xml_element = xml_element


    def saveTo(self, xml_parent):
        xml_parent.append(deepcopy(self.xml_element))


    def removeXmlChild(self, tag):
        xml_child = self.xml_element.find(tag)
        if xml_child is not None:
            self.xml_element.remove(xml_child)
