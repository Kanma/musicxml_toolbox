from unittest import TestCase
import xml.etree.ElementTree as ET

from ..musicxml import Harmony


class TestHarmony(TestCase):

    def createHarmony(self, note, major, seventh):
        root = '<root><root-step>%s</root-step>' % note[0]

        if len(note) > 1:
            if note[1] == '#':
                root += '<root-later>1</root-alter>'
            elif note[1] == 'b':
                root += '<root-later>-1</root-alter>'

        root += '</root>'

        if seventh:
            if major is None:
                kind = '<kind text="7">dominant</kind>'
            elif major:
                kind = '<kind text="M7">major-dominant</kind>'
            else:
                kind = '<kind text="m7">minor-dominant</kind>'
        else:
            if major:
                kind = '<kind>major</kind>'
            else:
                kind = '<kind>minor</kind>'

        return Harmony(xml_element=ET.fromstring('<harmony print-frame="no">%s%s</harmony>' % (root, kind)))


    def test_C_from_xml(self):
        harmony = self.createHarmony('C', True, False)
        self.assertEqual(harmony.text, 'C')


    def test_Cm_from_xml(self):
        harmony = self.createHarmony('C', False, False)
        self.assertEqual(harmony.text, 'Cm')


    def test_C7_from_xml(self):
        harmony = self.createHarmony('C', None, True)
        self.assertEqual(harmony.text, 'C7')


    def test_CM7_from_xml(self):
        harmony = self.createHarmony('C', True, True)
        self.assertEqual(harmony.text, 'CM7')


    def test_Cm7_from_xml(self):
        harmony = self.createHarmony('C', False, True)
        self.assertEqual(harmony.text, 'Cm7')


    def test_C_from_string(self):
        harmony = Harmony(text='C')
        self.assertEqual(harmony.text, 'C')


    def test_Cm_from_string(self):
        harmony = Harmony(text='Cm')
        self.assertEqual(harmony.text, 'Cm')


    def test_C7_from_string(self):
        harmony = Harmony(text='C7')
        self.assertEqual(harmony.text, 'C7')


    def test_CM7_from_string(self):
        harmony = Harmony(text='CM7')
        self.assertEqual(harmony.text, 'CM7')


    def test_Cm7_from_string(self):
        harmony = Harmony(text='Cm7')
        self.assertEqual(harmony.text, 'Cm7')
