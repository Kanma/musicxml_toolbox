from .xmlelementwrapper import XMLElementWrapper
from .. import xml


class ScorePart(XMLElementWrapper):

    @property
    def id(self):
        return self.xml_element.get('id')

    @id.setter
    def id(self, value):
        self.xml_element.set('id', value)


    @property
    def part_name(self):
        return self.xml_element.find('part-name').text

    @part_name.setter
    def part_name(self, value):
        self.xml_element.find('part-name').text = value


    @property
    def part_abbreviation(self):
        return self.xml_element.find('part-abbreviation').text

    @part_abbreviation.setter
    def part_abbreviation(self, value):
        self.xml_element.find('part-abbreviation').text = value


    @property
    def instrument_name(self):
        return xml.find(self.xml_element, ['score-instrument', 'instrument-name']).text

    @instrument_name.setter
    def instrument_name(self, value):
        xml.find(self.xml_element, ['score-instrument', 'instrument-name']).text = value


    @property
    def midi_instrument(self):
        return int(xml.find(self.xml_element, ['midi-instrument', 'midi-program']).text)

    @midi_instrument.setter
    def midi_instrument(self, value):
        xml.find(self.xml_element, ['midi-instrument', 'midi-program']).text = str(value)
