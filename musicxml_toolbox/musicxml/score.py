import xml.etree.ElementTree as ET
from copy import deepcopy

from .partlist import PartList
from .part import Part
from .barline import Barline
from .measure import Measure
from .rest import Rest
from .note import Note


class Score(object):

    def __init__(self):
        self.xml_document = None
        self.part_list = None
        self.parts = []


    def load(self, filename):
        # Open the file
        try:
            self.xml_document = ET.parse(filename)
        except:
            return False

        xml_root = self.xml_document.getroot()

        # <part-list>
        xml_part_list = xml_root.find('part-list')
        self.part_list = PartList(xml_part_list)
        xml_root.remove(xml_part_list)

        # <part>
        while True:
            xml_part = xml_root.find('part')
            if xml_part is None:
                break

            self.parts.append(Part(xml_part))
            xml_root.remove(xml_part)

        return True


    def save(self, filename):
        xml_document = deepcopy(self.xml_document)

        xml_root = xml_document.getroot()

        self.part_list.saveTo(xml_root)

        for part in self.parts:
            part.saveTo(xml_root)

        xml_document.write(filename)


    def part(self, id):
        try:
            return [ x for x in self.parts if x.id == id ][0]
        except:
            return None


    def partByName(self, name):
        score_part = self.part_list.find(name=name)
        if score_part is None:
            return None

        return self.part(score_part.id)


    @property
    def maximum_measure_duration(self):
        maximum = 0
        for part in self.parts:
            maximum = max(maximum, part.maximum_measure_duration)
        return maximum


    def getPartsAndStaves(self, patterns):
        # No pattern
        if patterns is None:
            result = []

            for part in self.parts:
                for staff in list(range(1, part.nb_staves + 1)):
                    result.append((part, staff))

            return (result, [])

        # Single pattern
        if not isinstance(patterns, list):
            patterns = [patterns]

        # List of patterns
        results = []
        errors = []

        for pattern in patterns:
            try:
                (part_name, staff_number) = pattern.split(':')
                pattern = (part_name, int(staff_number))
            except:
                errors.append('Invalid staff: %s' % pattern)
                continue

            part = self.partByName(pattern[0])
            if part is None:
                errors.append('Part not found: %s' % pattern[0])
                continue

            if pattern[1] > part.nb_staves:
                errors.append("Part '%s' has only %d staves" % (score_part.part_name, part.nb_staves))
                continue

            results.append( (part, pattern[1]) )

        return (results, errors)


    def expandRepeats(self):
        """Expand the repeats"""

        while True:
            # Search the first repeated measures
            part = self.parts[0]
            first_measure = None
            last_measure = None

            for index, measure in enumerate(part.measures):
                if first_measure is None:
                    if measure.isRepeatStart:
                        first_measure = index

                if first_measure is not None:
                    if measure.isRepeatEnd:
                        last_measure = index
                        break

            if first_measure is None:
                return

            # Expand them on all parts
            for part in self.parts:

                # Retrieve the measures to copy
                measures = part.measures[first_measure:last_measure+1]

                start_barline = measures[0].left_barline
                start_barline.style = Barline.LIGHT_LIGHT

                end_barline = measures[-1].right_barline
                measures[-1].right_barline = None

                # Augment the numbers of the following measures
                nb_original_measures = len(measures)
                nb_repeated_measures = nb_original_measures

                if measures[-1].volta is not None:
                    measures[-1].removeVolta()
                    nb_repeated_measures -= 1

                for measure in part.measures[last_measure+1:]:
                    measure.number += nb_repeated_measures

                # Copy the measures
                copied_measures = deepcopy(measures[:nb_repeated_measures])

                for measure in measures:
                    for staff in range(measure.nb_staves):
                        for note in measure.notes(staff=staff):
                            if note.rehearsal is not None:
                                note.rehearsal.text += '1'

                for measure in copied_measures:
                    measure.number += nb_original_measures
                    for staff in range(measure.nb_staves):
                        for note in measure.notes(staff=staff):
                            if note.rehearsal is not None:
                                note.rehearsal.text += '2'

                part.measures = part.measures[:last_measure+1] + copied_measures + part.measures[last_measure+1:]

                # Fix the bar lines of the following measure
                last_measure_index = last_measure + nb_repeated_measures

                if last_measure_index < part.nb_measures - 1:
                    measure = part.measures[last_measure_index + 1]

                    if measure.left_barline is None:
                        measure.left_barline = deepcopy(start_barline)
                    else:
                        measure.removeVolta()
                else:
                    end_barline.style = Barline.LIGHT_HEAVY
                    part.measures[last_measure_index].right_barline = end_barline


    def addEmptyMeasures(self, nb):
        """Add measure at the beginning of each staff"""

        if nb < 1:
            return

        for part in self.parts:
            first_measure = part.measures[0]

            new_measures = []
            for i in range(1, nb):
                measure = Measure(number=i+1)
                measure.notes_by_staff = []
                measure.duration = part.maximum_measure_duration

                for staff in range(1, part.nb_staves+1):
                    voice = first_measure.notes_by_staff[staff - 1][0].voice
                    rest = Rest(type=Note.WHOLE, duration=part.maximum_measure_duration,
                                staff=staff, voice=voice)
                    measure.notes_by_staff.append([rest])

                new_measures.append(measure)

            # Move the notes of the first measure to a new one
            new_measure = Measure(number=nb+1)
            new_measure.left_barline = first_measure.left_barline
            new_measure.right_barline = first_measure.right_barline
            new_measure.notes_by_staff = first_measure.notes_by_staff
            new_measure.duration = first_measure.duration
            new_measures.append(new_measure)

            nb_staves = first_measure.nb_staves

            first_note = first_measure.notes_by_staff[0][0]
            rehearsal = first_note.rehearsal
            first_note.rehearsal = None

            first_measure.left_barline = None
            first_measure.right_barline = None
            first_measure.notes_by_staff = []
            first_measure.duration = part.maximum_measure_duration

            for staff in range(1, nb_staves+1):
                voice = new_measure.notes_by_staff[staff - 1][0].voice
                rest = Rest(type=Note.WHOLE, duration=part.maximum_measure_duration,
                            staff=staff, voice=voice)

                if staff == 1:
                    rest.rehearsal = rehearsal

                first_measure.notes_by_staff.append([rest])

            part.measures = [first_measure] + new_measures + part.measures[1:]

            for index, measure in enumerate(part.measures):
                measure.number = index + 1


    def moveRehearsalsTo(self, dest_part):
        for part in self.parts:
            if part is dest_part:
                continue

            for index, src_measure in enumerate(part.measures):
                dest_measure = dest_part.measures[index]

                src_note = src_measure.notes(staff=1)[0]
                dest_note = dest_measure.notes(staff=1)[0]

                if dest_note.rehearsal is not None:
                    continue

                if src_note.rehearsal is None:
                    continue

                dest_note.rehearsal = src_note.rehearsal
                src_note.rehearsal = None

