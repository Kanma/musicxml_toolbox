from .xmlelementwrapper import XMLElementWrapper
from copy import deepcopy
from piano_fingering import computeFingering
from piano_fingering import listToMidi

from .measure import Measure
from .note import Note
from .chord import Chord
from .rest import Rest
from .fingering import Fingering


class Part(XMLElementWrapper):

    def __init__(self, xml_element):
        super(Part, self).__init__(xml_element)

        self.measures = []

        # <measure>
        while True:
            xml_measure = self.xml_element.find('measure')
            if xml_measure is None:
                break

            self.measures.append(Measure(xml_measure))
            self.xml_element.remove(xml_measure)


    def saveTo(self, xml_parent):
        xml_part = deepcopy(self.xml_element)

        for measure in self.measures:
            measure.saveTo(xml_part)

        xml_parent.append(xml_part)


    @property
    def id(self):
        return self.xml_element.get('id')

    @id.setter
    def id(self, value):
        self.xml_element.set('id', value)


    @property
    def nb_measures(self):
        return len(self.measures)


    @property
    def nb_staves(self):
        if len(self.measures) > 0:
            return self.measures[0].nb_staves

        return 0


    @property
    def maximum_measure_duration(self):
        maximum = 0
        for measure in self.measures:
            maximum = max(maximum, measure.duration)
        return maximum


    def replaceChords(self, staff=1):
        """Replace all the chords found on the given staff by their root note"""

        for measure in self.measures:
            measure.replaceChords(staff=staff)


    def annotateChords(self, staff=1):
        """Annotate all the chords found on the given staff"""

        for measure in self.measures:
            measure.annotateChords(staff=staff)


    def removeKeySignature(self):
        """Remove the key signature (if any) and ensure that all accidentals are
        correctly displayed
        """

        for measure in self.measures:
            measure.removeKeySignature()


    def addFingering(self, staff=1):
        """Add fingering to the notes of the given staff"""

        def _process(all_notes):
            notes = []
            for note in all_notes:
                if isinstance(note, Note):
                    if note.fingering is not None:
                        notes.append(dict(notes=[note.name], fingers=[note.fingering.finger]))
                    else:
                        notes.append(note.name)
                elif isinstance(note, Chord):
                    if note.fingering is not None:
                        notes.append(dict(notes=note.note_names, fingers=note.fingering))
                    else:
                        notes.append(note.note_names)
                elif isinstance(note, Rest):
                    notes.append([])

            if staff == 1:
                left_or_right = 'right'
            else:
                left_or_right = 'left'

            midi_notes = listToMidi(notes)
            fingered_notes = computeFingering(midi_notes, left_or_right)

            for note_index, fingered_note in enumerate(fingered_notes):
                note = all_notes[note_index]

                if isinstance(note, Note):
                    if note.fingering is not None:
                        note.fingering.finger = fingered_note['fingers'][0]
                    else:
                        note.fingering = Fingering(finger=fingered_note['fingers'][0])

                elif isinstance(note, Chord):
                    note.fingering = fingered_note['fingers']


        all_notes = []

        for index, measure in enumerate(self.measures):
            staff_notes = measure.notes(staff=staff)

            if (len(staff_notes) == 1) and isinstance(staff_notes[0], Rest):
                _process(all_notes)
                all_notes = []

            else:
                all_notes += staff_notes

        if len(all_notes) > 0:
            _process(all_notes)
