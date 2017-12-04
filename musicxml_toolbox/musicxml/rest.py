import xml.etree.ElementTree as ET
from copy import deepcopy

from .xmlelementwrapper import XMLElementWrapper
from .note import Note


class Rest(XMLElementWrapper):

    def __init__(self, xml_element=None, type=Note.WHOLE, duration=4, staff=1, voice=1):
        if xml_element is None:
            xml_element = ET.Element('note')
            xml_rest = ET.SubElement(xml_element, 'rest')

            xml_duration = ET.SubElement(xml_element, 'duration')
            xml_duration.text = str(duration)

            xml_voice = ET.SubElement(xml_element, 'voice')
            xml_voice.text = str(voice)

            xml_type = ET.SubElement(xml_element, 'type')
            xml_type.text = type

            xml_staff = ET.SubElement(xml_element, 'staff')
            xml_staff.text = str(staff)

        super(Rest, self).__init__(xml_element)

        self.xml_element = xml_element
        self.rehearsal = None
        self.harmony = None


    def saveTo(self, xml_parent):
        if self.rehearsal is not None:
            self.rehearsal.saveTo(xml_parent)

        if self.harmony is not None:
            self.harmony.saveTo(xml_parent)

        xml_parent.append(deepcopy(self.xml_element))


    @property
    def duration(self):
        return int(self.xml_element.find('duration').text)


    @property
    def type(self):
        return self.xml_element.find('type').text


    @property
    def staff(self):
        xml_staff = self.xml_element.find('staff')
        if xml_staff is None:
            return 1

        return int(xml_staff.text)


    @property
    def voice(self):
        return int(self.xml_element.find('voice').text)
