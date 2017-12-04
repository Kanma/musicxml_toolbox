from .xmlelementwrapper import XMLElementWrapper


class Rehearsal(XMLElementWrapper):

    @property
    def text(self):
        return self.xml_element.find('direction-type').find('rehearsal').text


    @text.setter
    def text(self, value):
        self.xml_element.find('direction-type').find('rehearsal').text = value
