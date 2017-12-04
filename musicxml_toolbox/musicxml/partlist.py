from .xmlelementwrapper import XMLElementWrapper
from copy import deepcopy

from .scorepart import ScorePart


class PartList(XMLElementWrapper):

    def __init__(self, xml_element):
        super(PartList, self).__init__(xml_element)

        self.score_parts = []

        # <score-part>
        while True:
            xml_score_part = self.xml_element.find('score-part')
            if xml_score_part is None:
                break

            self.score_parts.append(ScorePart(xml_score_part))
            self.xml_element.remove(xml_score_part)


    def saveTo(self, xml_parent):
        xml_part_list = deepcopy(self.xml_element)

        for score_part in self.score_parts:
            score_part.saveTo(xml_part_list)

        xml_parent.append(xml_part_list)


    def find(self, id=None, name=None):
        if id is not None:
            filtered = [ x for x in self.score_parts if x.id == id ]

        elif name is not None:
            filtered = [ x for x in self.score_parts if x.part_name == name ]

        if len(filtered) == 0:
            return None

        return filtered[0]


    def ids(self):
        return [ x.id for x in self.score_parts ]


    def names(self):
        return [ x.parT_name for x in self.score_parts ]


    def __len__(self):
        return len(self.score_parts)


    def __getitem__(self, index):
        return self.score_parts[index]


    def __iter__(self):
        return iter(self.score_parts)
