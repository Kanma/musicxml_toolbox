import xml.etree.ElementTree as ET
from copy import deepcopy
import re

from .. import xml
from .xmlelementwrapper import XMLElementWrapper
from .barline import Barline
from .note import Note
from .rest import Rest
from .chord import Chord
from .rehearsal import Rehearsal
from .harmony import Harmony


class Measure(XMLElementWrapper):

    def __init__(self, xml_element=None, number=1):
        if xml_element is None:
            xml_element = ET.Element('measure')
            xml_element.set('number', str(number))

        super(Measure, self).__init__(xml_element)

        self.left_barline = None
        self.right_barline = None
        self.notes_by_staff = []
        self.duration = 0
        self.metronome = None

        # <barline>
        while True:
            xml_barline = self.xml_element.find('barline')
            if xml_barline is None:
                break

            barline = Barline(xml_barline)
            if barline.location == 'left':
                self.left_barline = barline
            else:
                self.right_barline = barline

            self.xml_element.remove(xml_barline)

        # <backup>
        while True:
            xml_backup = self.xml_element.find('backup')
            if xml_backup is None:
                break

            self.xml_element.remove(xml_backup)


        harmony = None
        rehearsal = None

        for xml_child in list(self.xml_element):

            # <harmony>
            if xml_child.tag == 'harmony':
                harmony = Harmony(xml_child)
                self.xml_element.remove(xml_child)

            # <direction>
            elif xml_child.tag == 'direction':
                xml_rehearsal = xml.find(xml_child, ['direction-type', 'rehearsal'])
                if xml_rehearsal is not None:
                    rehearsal = Rehearsal(xml_child)
                else:
                    xml_metronome = xml.find(xml_child, ['direction-type', 'metronome'])
                    if xml_metronome is not None:
                        self.metronome = xml_child

                self.xml_element.remove(xml_child)

            # <note>
            elif xml_child.tag == 'note':
                xml_note = xml_child

                xml_staff = xml_note.find('staff')
                if xml_staff is None:
                    staff = 1
                else:
                    staff = int(xml_staff.text)

                if xml_note.find('rest') is not None:
                    note = Rest(xml_note)
                elif xml_note.find('chord') is not None:
                    note = Note(xml_note)
                    previous_note = self.notes_by_staff[staff - 1][-1]
                    if isinstance(previous_note, Chord):
                        previous_note.addNote(note)
                    else:
                        chord = Chord(previous_note)
                        chord.addNote(note)

                        chord.harmony = previous_note.harmony
                        chord.rehearsal = previous_note.rehearsal

                        previous_note.harmony = None
                        previous_note.rehearsal = None

                        self.notes_by_staff[staff - 1] = self.notes_by_staff[staff - 1][:-1]
                        self.notes_by_staff[staff - 1].append(chord)

                    self.xml_element.remove(xml_note)
                    continue
                else:
                    note = Note(xml_note)

                note.harmony = harmony
                note.rehearsal = rehearsal

                harmony = None
                rehearsal = None

                if staff == 1:
                    self.duration += note.duration

                if staff > len(self.notes_by_staff):
                    self.notes_by_staff.append([])

                self.notes_by_staff[staff - 1].append(note)
                self.xml_element.remove(xml_note)


    def saveTo(self, xml_parent):
        xml_measure = deepcopy(self.xml_element)

        if self.left_barline is not None:
            self.left_barline.saveTo(xml_measure)

        if self.metronome is not None:
            xml_measure.append(deepcopy(self.metronome))

        for staff_index, staff in enumerate(self.notes_by_staff):
            for note in staff:
                note.saveTo(xml_measure)

            if (self.nb_staves > 1) and (staff_index < self.nb_staves - 1):
                xml_backup = ET.SubElement(xml_measure, 'backup')
                xml_duration = ET.SubElement(xml_backup, 'duration')
                xml_duration.text = str(self.duration)

        if self.right_barline is not None:
            self.right_barline.saveTo(xml_measure)

        xml_parent.append(xml_measure)


    @property
    def number(self):
        return int(self.xml_element.get('number'))

    @number.setter
    def number(self, value):
        self.xml_element.set('number', str(value))


    @property
    def nb_staves(self):
        return len(self.notes_by_staff)


    def notes(self, staff=1):
        return self.notes_by_staff[staff - 1]


    @property
    def isRepeatStart(self):
        return (self.left_barline is not None) and self.left_barline.isRepeat


    @property
    def isRepeatEnd(self):
        return (self.right_barline is not None) and self.right_barline.isRepeat


    @property
    def volta(self):
        if self.left_barline is not None:
            return self.left_barline.volta

        return None


    def removeVolta(self):
        if self.left_barline is not None:
            self.left_barline.removeVolta()
            if len(self.left_barline.xml_element) == 0:
                self.left_barline = None

        if self.right_barline is not None:
            self.right_barline.removeVolta()
            if len(self.right_barline.xml_element) == 0:
                self.right_barline = None


    def replaceChords(self, staff=1):
        """Replace all the chords found on the given staff by their root note"""

        notes = self.notes(staff=staff)

        for index, note in enumerate(notes):
            if not isinstance(note, Chord):
                continue

            chord = note

            note = None
            for note_index, note_name in enumerate(chord.note_names):
                if re.sub(r'\d', '', note_name) == chord.root:
                    note = chord.notes[note_index]

            note.removeXmlChild('chord')
            note.rehearsal = chord.rehearsal
            notes[index] = note


    def annotateChords(self, staff=1):
        """Annotate all the chords found on the given staff"""

        notes = self.notes(staff=staff)

        for index, note in enumerate(notes):
            if not isinstance(note, Chord):
                continue

            chord = note
            if chord.harmony is not None:
                continue

            if chord.name is not None:
                chord.harmony = Harmony(text=chord.name)


    def removeKeySignature(self):
        """Remove the key signature (if any) and ensure that all accidentals are
        correctly displayed
        """

        def _process_note(note, mapping):
            note_name = note.pure_name

            real_accidental = Note.NONE
            if note_name[-1] == '#':
                real_accidental = Note.SHARP
            elif note_name[-1] == 'b':
                real_accidental = Note.FLAT

            if real_accidental == Note.SHARP:
                if mapping[note_name] != Note.SHARP:
                    note.accidental = Note.SHARP
                    mapping[note_name] = Note.SHARP
                else:
                    note.accidental = Note.NONE

            elif real_accidental == Note.FLAT:
                if mapping[note_name] != Note.FLAT:
                    note.accidental = Note.FLAT
                    mapping[note_name] = Note.FLAT
                else:
                    note.accidental = Note.NONE

            else:
                if mapping[note_name] == Note.SHARP:
                    note.accidental = Note.NATURAL
                    mapping[note_name] = Note.NATURAL
                elif mapping[note_name] == Note.FLAT:
                    note.accidental = Note.NATURAL
                    mapping[note_name] = Note.NATURAL
                else:
                    note.accidental = Note.NONE


        xml_attributes = self.xml_element.find('attributes')
        if xml_attributes is not None:
            xml_key = xml_attributes.find('key')
            xml_attributes.remove(xml_key)

        for notes in self.notes_by_staff:
            mapping = {}
            for name in ['C', 'C#', 'Db', 'D', 'D#', 'Eb', 'E', 'F', 'F#', 'Gb',
                         'G', 'G#', 'Ab', 'A', 'A#', 'Bb', 'B']:
                mapping[name] = Note.NONE

            for note in notes:
                if isinstance(note, Note):
                    _process_note(note, mapping)
                elif isinstance(note, Chord):
                    for chord_note in note.notes:
                        _process_note(chord_note, mapping)
