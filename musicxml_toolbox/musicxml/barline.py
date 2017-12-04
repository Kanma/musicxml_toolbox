from .xmlelementwrapper import XMLElementWrapper
import xml.etree.ElementTree as ET


class Barline(XMLElementWrapper):

    LEFT = 'left'
    RIGHT = 'right'

    FORWARD = 'forward'
    BACKWARD = 'backward'

    LIGHT_LIGHT = 'light-light'
    LIGHT_HEAVY = 'light-heavy'


    @property
    def location(self):
        return self.xml_element.get('location')


    @property
    def isRepeat(self):
        return (self.xml_element.find('repeat') is not None)


    @property
    def repeatDirection(self):
        xml_repeat = self.xml_element.find('repeat')
        if xml_repeat is not None:
            return xml_repeat.get('direction')

        return None


    @property
    def volta(self):
        xml_ending = self.xml_element.find('ending')
        if xml_ending is not None:
            return int(xml_ending.get('number'))

        return None


    def removeVolta(self):
        self.removeXmlChild('ending')


    @property
    def style(self):
        xml_bar_style = self.xml_element.find('bar-style')
        if xml_bar_style is not None:
            return xml_bar_style.text

        return None


    @style.setter
    def style(self, value):
        xml_repeat = self.xml_element.find('repeat')
        if xml_repeat is not None:
            self.xml_element.remove(xml_repeat)

        xml_bar_style = self.xml_element.find('bar-style')
        if xml_bar_style is None:
            xml_bar_style = ET.SubElement(self.xml_element, 'bar-style')
        xml_bar_style.text = value
