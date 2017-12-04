import xml.etree.ElementTree as ET


class Harmony(object):

    def __init__(self, xml_element=None, text=None):
        if xml_element is not None:
            xml_root = xml_element.find('root')

            self.root = xml_root.find('root-step').text
            self.alter = 0

            xml_alter = xml_root.find('root-alter')
            if xml_alter is not None:
                self.alter = int(xml_alter.text)

            xml_kind = xml_element.find('kind')
            self.kind = xml_kind.text
            self.kind_text = xml_kind.get('text')

        elif text is not None:
            self.text = text

        else:
            self.root = None
            self.alter = 0
            self.kind = None
            self.kind_text = None


    def saveTo(self, xml_parent):
        xml_harmony = ET.SubElement(xml_parent, 'harmony')
        xml_harmony.set('print-frame', 'no')

        xml_root = ET.SubElement(xml_harmony, 'root')

        xml_root_step = ET.SubElement(xml_root, 'root-step')
        xml_root_step.text = self.root

        if self.alter != 0:
            xml_root_alter = ET.SubElement(xml_root, 'root-alter')
            xml_root_alter.text = str(self.alter)

        xml_kind = ET.SubElement(xml_harmony, 'kind')
        xml_kind.text = self.kind

        if self.kind_text is not None:
            xml_kind.set('text', self.kind_text)


    @property
    def text(self):
        text = self.root

        if self.alter == 1:
            text += '#'
        elif self.alter == -1:
            text += 'b'

        if self.kind_text is not None:
            text += self.kind_text
        elif self.kind == 'minor':
            text += 'm'

        return text


    @text.setter
    def text(self, value):
        self.root = value[0]

        if len(value) > 1:
            if value[1] == '#':
                self.alter = 1
                value = value[2:]
            elif value[1] == 'b':
                self.alter = -1
                value = value[2:]
            else:
                self.alter = 0
                value = value[1:]
        else:
            self.alter = 0
            value = value[1:]

        if len(value) > 0:
            if value == 'm':
                self.kind = 'minor'
                self.kind_text = None
            elif value == '7':
                self.kind = 'dominant'
                self.kind_text = '7'
            elif value == 'M7':
                self.kind = 'major-seventh'
                self.kind_text = 'M7'
            elif value == 'm7':
                self.kind = 'minor-seventh'
                self.kind_text = 'm7'
        else:
            self.kind = 'major'
            self.kind_text = None
