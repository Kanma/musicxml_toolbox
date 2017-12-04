import xml.etree.ElementTree as ET


class Fingering(object):

    def __init__(self, xml_element=None, finger=None):
        if xml_element is not None:
            self.finger = int(xml_element.find('technical').find('fingering').text)

        elif finger is not None:
            self.finger = finger

        else:
            self.finger = None


    def saveTo(self, xml_parent):
        xml_notations = ET.SubElement(xml_parent, 'notations')
        xml_technical = ET.SubElement(xml_notations, 'technical')
        xml_fingering = ET.SubElement(xml_technical, 'fingering')
        xml_fingering.text = str(self.finger)
