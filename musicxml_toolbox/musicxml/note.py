import xml.etree.ElementTree as ET
from copy import deepcopy

from .. import xml
from .xmlelementwrapper import XMLElementWrapper
from .fingering import Fingering


class Note(XMLElementWrapper):

    NATURAL = 'natural'
    SHARP = 'sharp'
    FLAT = 'flat'
    NONE = None

    WHOLE = 'whole'
    HALF = 'half'
    QUARTER = 'quarter'
    EIGTH = 'eigth'
    SIXTEENTH = 'sixteenth'


    def __init__(self, xml_element):
        super(Note, self).__init__(xml_element)

        self.rehearsal = None
        self.harmony = None
        self.fingering = None

        xml_notations = self.xml_element.find('notations')
        if xml_notations is not None:
            xml_technical = xml_notations.find('technical')

            if xml_technical is not None:
                xml_fingering = xml_technical.find('fingering')

                if xml_fingering is not None:
                    self.fingering = Fingering(xml_notations)
                    self.xml_element.remove(xml_notations)


    def saveTo(self, xml_parent):
        if self.rehearsal is not None:
            self.rehearsal.saveTo(xml_parent)

        if self.harmony is not None:
            self.harmony.saveTo(xml_parent)

        xml_copy = deepcopy(self.xml_element)

        if self.fingering is not None:
            self.fingering.saveTo(xml_copy)

        xml_parent.append(xml_copy)


    @property
    def name(self):
        xml_pitch = self.xml_element.find('pitch')
        return self.pure_name + xml_pitch.find('octave').text


    @property
    def pure_name(self):
        xml_pitch = self.xml_element.find('pitch')
        name = xml_pitch.find('step').text

        xml_alter = xml_pitch.find('alter')
        if xml_alter is not None:
            if xml_alter.text == '-1':
                name += 'b'
            elif xml_alter.text == '1':
                name += '#'

        return name


    @property
    def duration(self):
        return int(self.xml_element.find('duration').text)


    @property
    def type(self):
        return self.xml_element.find('type').text


    @property
    def voice(self):
        return int(self.xml_element.find('voice').text)


    @property
    def staff(self):
        xml_staff = self.xml_element.find('staff')
        if xml_staff is None:
            return 1

        return int(xml_staff.text)


    @property
    def accidental(self):
        xml_accidental = self.xml_element.find('accidental')
        if xml_accidental is not None:
            return xml_accidental.text

        return Note.NONE


    @accidental.setter
    def accidental(self, value):
        xml_accidental = self.xml_element.find('accidental')

        if xml_accidental is not None:
            if value is not None:
                xml_accidental.text = value
            else:
                self.xml_element.remove(xml_accidental)

        elif value is not None:
            xml_accidental = ET.Element('accidental')
            xml_accidental.text = value

            index = xml.indexOfChild(self.xml_element, 'dot')
            if index == -1:
                index = xml.indexOfChild(self.xml_element, 'type')

            self.xml_element.insert(index + 1, xml_accidental)
