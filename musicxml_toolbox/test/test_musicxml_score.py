from unittest import TestCase
import os
import xml.etree.ElementTree as ET

from ..musicxml import Score
from ..musicxml import Rest
from ..musicxml import Chord
from ..musicxml import Note
from ..musicxml import Barline
from .. import xml
from . import data_dir


class TestScore(TestCase):

    def setUp(self):
        self.filenames = []


    def tearDown(self):
        for filename in self.filenames:
            os.remove(filename)


    def save(self, score, filename):
        score.save(filename)
        self.filenames.append(filename)


    def check_file(self, test_file_name, reference_file_name):
        test_file = ET.parse(test_file_name)
        reference_file = ET.parse(reference_file_name)

        self.assertTrue(xml.compare(test_file.getroot(), reference_file.getroot()))


    def check_twelve_notes(self, part, staff, nb_staves):
        measure = part.measures[0]
        self.assertEqual(measure.number, 1)
        self.assertEqual(measure.nb_staves, nb_staves)
        self.assertEqual(measure.duration, 4)

        notes = measure.notes(staff=staff)
        self.assertEqual(len(notes), 4)

        note = notes[0]
        self.assertEqual(note.name, 'C4')
        self.assertEqual(note.duration, 1)
        self.assertEqual(note.staff, staff)

        note = notes[1]
        self.assertEqual(note.name, 'C#4')
        self.assertEqual(note.duration, 1)
        self.assertEqual(note.staff, staff)

        note = notes[2]
        self.assertEqual(note.name, 'D4')
        self.assertEqual(note.duration, 1)
        self.assertEqual(note.staff, staff)

        note = notes[3]
        self.assertEqual(note.name, 'D#4')
        self.assertEqual(note.duration, 1)
        self.assertEqual(note.staff, staff)

        measure = part.measures[1]
        self.assertEqual(measure.number, 2)
        self.assertEqual(measure.nb_staves, nb_staves)
        self.assertEqual(measure.duration, 4)

        notes = measure.notes(staff=staff)
        self.assertEqual(len(notes), 4)

        note = notes[0]
        self.assertEqual(note.name, 'E4')
        self.assertEqual(note.duration, 1)
        self.assertEqual(note.staff, staff)

        note = notes[1]
        self.assertEqual(note.name, 'F4')
        self.assertEqual(note.duration, 1)
        self.assertEqual(note.staff, staff)

        note = notes[2]
        self.assertEqual(note.name, 'F#4')
        self.assertEqual(note.duration, 1)
        self.assertEqual(note.staff, staff)

        note = notes[3]
        self.assertEqual(note.name, 'G4')
        self.assertEqual(note.duration, 1)
        self.assertEqual(note.staff, staff)

        measure = part.measures[2]
        self.assertEqual(measure.number, 3)
        self.assertEqual(measure.nb_staves, nb_staves)
        self.assertEqual(measure.duration, 4)

        notes = measure.notes(staff=staff)
        self.assertEqual(len(notes), 4)

        note = notes[0]
        self.assertEqual(note.name, 'G#4')
        self.assertEqual(note.duration, 1)
        self.assertEqual(note.staff, staff)

        note = notes[1]
        self.assertEqual(note.name, 'A4')
        self.assertEqual(note.duration, 1)
        self.assertEqual(note.staff, staff)

        note = notes[2]
        self.assertEqual(note.name, 'A#4')
        self.assertEqual(note.duration, 1)
        self.assertEqual(note.staff, staff)

        note = notes[3]
        self.assertEqual(note.name, 'B4')
        self.assertEqual(note.duration, 1)
        self.assertEqual(note.staff, staff)


    def check_whole_rest(self, measure, staff):
        self.assertEqual(measure.duration, 4)

        notes = measure.notes(staff=staff)
        self.assertEqual(len(notes), 1)

        note = notes[0]
        self.assertTrue(isinstance(note, Rest))
        self.assertEqual(note.duration, 4)
        self.assertEqual(note.staff, staff)


    def test_creation(self):
        score = Score()
        self.assertTrue(score.xml_document is None)


    def test_unknown_file(self):
        score = Score()
        self.assertFalse(score.load(os.path.join(data_dir, 'unknown.xml')))


    def test_one_part_twelve_notes(self):
        filename = os.path.join(data_dir, 'one_part', 'twelve_notes.xml')

        score = Score()
        self.assertTrue(score.load(filename))

        self.assertTrue(score.xml_document is not None)
        self.assertTrue(score.part_list is not None)

        self.assertEqual(len(score.part_list.score_parts), 1)

        score_part = score.part_list.score_parts[0]
        self.assertEqual(score_part.id, 'P1')
        self.assertEqual(score_part.part_name, 'Piano')
        self.assertEqual(score_part.part_abbreviation, 'Pno.')
        self.assertEqual(score_part.instrument_name, 'Piano')
        self.assertEqual(score_part.midi_instrument, 1)

        self.assertEqual(len(score.parts), 1)

        part = score.parts[0]
        self.assertEqual(part.id, 'P1')
        self.assertEqual(len(part.measures), 3)

        self.check_twelve_notes(part, 1, 1)

        self.save(score, filename + '2')

        self.check_file(filename + '2', filename)


    def test_one_part_two_staves_twelve_notes_on_staff_1(self):
        filename = os.path.join(data_dir, 'one_part', 'twelve_notes_on_staff_1.xml')

        score = Score()
        self.assertTrue(score.load(filename))

        self.assertTrue(score.xml_document is not None)
        self.assertTrue(score.part_list is not None)

        self.assertEqual(len(score.part_list.score_parts), 1)

        score_part = score.part_list.score_parts[0]
        self.assertEqual(score_part.id, 'P1')
        self.assertEqual(score_part.part_name, 'Piano')
        self.assertEqual(score_part.part_abbreviation, 'Pno.')
        self.assertEqual(score_part.instrument_name, 'Piano')
        self.assertEqual(score_part.midi_instrument, 1)

        self.assertEqual(len(score.parts), 1)

        part = score.parts[0]
        self.assertEqual(part.id, 'P1')
        self.assertEqual(len(part.measures), 3)

        self.check_twelve_notes(part, 1, 2)
        
        for measure in part.measures:
            self.check_whole_rest(measure, 2)

        self.save(score, filename + '2')

        self.check_file(filename + '2', filename)


    def test_one_part_two_staves_twelve_notes_on_staff_2(self):
        filename = os.path.join(data_dir, 'one_part', 'twelve_notes_on_staff_2.xml')

        score = Score()
        self.assertTrue(score.load(filename))

        self.assertTrue(score.xml_document is not None)
        self.assertTrue(score.part_list is not None)

        self.assertEqual(len(score.part_list.score_parts), 1)

        score_part = score.part_list.score_parts[0]
        self.assertEqual(score_part.id, 'P1')
        self.assertEqual(score_part.part_name, 'Piano')
        self.assertEqual(score_part.part_abbreviation, 'Pno.')
        self.assertEqual(score_part.instrument_name, 'Piano')
        self.assertEqual(score_part.midi_instrument, 1)

        self.assertEqual(len(score.parts), 1)

        part = score.parts[0]
        self.assertEqual(part.id, 'P1')
        self.assertEqual(len(part.measures), 3)

        self.check_twelve_notes(part, 2, 2)
        
        for measure in part.measures:
            self.check_whole_rest(measure, 1)

        self.save(score, filename + '2')

        self.check_file(filename + '2', filename)


    def test_two_parts_three_staves_one_note_per_staff(self):
        filename = os.path.join(data_dir, 'two_parts', 'one_whole_note.xml')

        score = Score()
        self.assertTrue(score.load(filename))

        self.assertTrue(score.xml_document is not None)
        self.assertTrue(score.part_list is not None)

        self.assertEqual(len(score.part_list.score_parts), 2)

        score_part = score.part_list.score_parts[0]
        self.assertEqual(score_part.id, 'P1')
        self.assertEqual(score_part.part_name, 'Voice')
        self.assertEqual(score_part.part_abbreviation, 'Vo.')
        self.assertEqual(score_part.instrument_name, 'Voice')
        self.assertEqual(score_part.midi_instrument, 53)

        score_part = score.part_list.score_parts[1]
        self.assertEqual(score_part.id, 'P2')
        self.assertEqual(score_part.part_name, 'Piano')
        self.assertEqual(score_part.part_abbreviation, 'Pno.')
        self.assertEqual(score_part.instrument_name, 'Piano')
        self.assertEqual(score_part.midi_instrument, 1)

        self.assertEqual(len(score.parts), 2)


        part = score.parts[0]
        self.assertEqual(part.id, 'P1')
        self.assertEqual(len(part.measures), 1)

        measure = part.measures[0]
        self.assertEqual(measure.number, 1)
        self.assertEqual(measure.nb_staves, 1)
        self.assertEqual(measure.duration, 4)

        notes = measure.notes(staff=1)
        self.assertEqual(len(notes), 1)

        note = notes[0]
        self.assertEqual(note.name, 'G4')
        self.assertEqual(note.duration, 4)
        self.assertEqual(note.staff, 1)


        part = score.parts[1]
        self.assertEqual(part.id, 'P2')
        self.assertEqual(len(part.measures), 1)

        measure = part.measures[0]
        self.assertEqual(measure.number, 1)
        self.assertEqual(measure.nb_staves, 2)
        self.assertEqual(measure.duration, 4)

        notes = measure.notes(staff=1)
        self.assertEqual(len(notes), 1)

        note = notes[0]
        self.assertEqual(note.name, 'E4')
        self.assertEqual(note.duration, 4)
        self.assertEqual(note.staff, 1)

        notes = measure.notes(staff=2)
        self.assertEqual(len(notes), 1)

        note = notes[0]
        self.assertEqual(note.name, 'C3')
        self.assertEqual(note.duration, 4)
        self.assertEqual(note.staff, 2)


        self.save(score, filename + '2')

        self.check_file(filename + '2', filename)


    def test_one_part_four_chords(self):
        filename = os.path.join(data_dir, 'one_part', 'four_chords.xml')

        score = Score()
        self.assertTrue(score.load(filename))

        self.assertTrue(score.xml_document is not None)
        self.assertTrue(score.part_list is not None)

        self.assertEqual(len(score.part_list.score_parts), 1)

        score_part = score.part_list.score_parts[0]
        self.assertEqual(score_part.id, 'P1')
        self.assertEqual(score_part.part_name, 'Piano')
        self.assertEqual(score_part.part_abbreviation, 'Pno.')
        self.assertEqual(score_part.instrument_name, 'Piano')
        self.assertEqual(score_part.midi_instrument, 1)

        self.assertEqual(len(score.parts), 1)


        part = score.parts[0]
        self.assertEqual(part.id, 'P1')
        self.assertEqual(len(part.measures), 1)

        measure = part.measures[0]
        self.assertEqual(measure.number, 1)
        self.assertEqual(measure.nb_staves, 1)
        self.assertEqual(measure.duration, 4)

        notes = measure.notes(staff=1)
        self.assertEqual(len(notes), 4)


        chord = notes[0]
        self.assertTrue(isinstance(chord, Chord))
        self.assertEqual(chord.duration, 1)
        self.assertEqual(chord.staff, 1)

        self.assertEqual(len(chord.notes), 3)

        note = chord.notes[0]
        self.assertEqual(note.name, 'C4')
        self.assertEqual(note.duration, 1)
        self.assertEqual(note.staff, 1)

        note = chord.notes[1]
        self.assertEqual(note.name, 'E4')
        self.assertEqual(note.duration, 1)
        self.assertEqual(note.staff, 1)

        note = chord.notes[2]
        self.assertEqual(note.name, 'G4')
        self.assertEqual(note.duration, 1)
        self.assertEqual(note.staff, 1)


        chord = notes[1]
        self.assertTrue(isinstance(chord, Chord))
        self.assertEqual(chord.duration, 1)
        self.assertEqual(chord.staff, 1)

        self.assertEqual(len(chord.notes), 3)

        note = chord.notes[0]
        self.assertEqual(note.name, 'F4')
        self.assertEqual(note.duration, 1)
        self.assertEqual(note.staff, 1)

        note = chord.notes[1]
        self.assertEqual(note.name, 'A4')
        self.assertEqual(note.duration, 1)
        self.assertEqual(note.staff, 1)

        note = chord.notes[2]
        self.assertEqual(note.name, 'C5')
        self.assertEqual(note.duration, 1)
        self.assertEqual(note.staff, 1)


        chord = notes[2]
        self.assertTrue(isinstance(chord, Chord))
        self.assertEqual(chord.duration, 1)
        self.assertEqual(chord.staff, 1)

        self.assertEqual(len(chord.notes), 3)

        note = chord.notes[0]
        self.assertEqual(note.name, 'E4')
        self.assertEqual(note.duration, 1)
        self.assertEqual(note.staff, 1)

        note = chord.notes[1]
        self.assertEqual(note.name, 'G4')
        self.assertEqual(note.duration, 1)
        self.assertEqual(note.staff, 1)

        note = chord.notes[2]
        self.assertEqual(note.name, 'C5')
        self.assertEqual(note.duration, 1)
        self.assertEqual(note.staff, 1)


        chord = notes[3]
        self.assertTrue(isinstance(chord, Chord))
        self.assertEqual(chord.duration, 1)
        self.assertEqual(chord.staff, 1)

        self.assertEqual(len(chord.notes), 3)

        note = chord.notes[0]
        self.assertEqual(note.name, 'E4')
        self.assertEqual(note.duration, 1)
        self.assertEqual(note.staff, 1)

        note = chord.notes[1]
        self.assertEqual(note.name, 'G4')
        self.assertEqual(note.duration, 1)
        self.assertEqual(note.staff, 1)

        note = chord.notes[2]
        self.assertEqual(note.name, 'B4')
        self.assertEqual(note.duration, 1)
        self.assertEqual(note.staff, 1)


        self.save(score, filename + '2')

        self.check_file(filename + '2', filename)


    def test_harmonies(self):
        filename = os.path.join(data_dir, 'one_part', 'harmonies.xml')

        score = Score()
        self.assertTrue(score.load(filename))

        self.assertTrue(score.xml_document is not None)
        self.assertTrue(score.part_list is not None)

        self.assertEqual(len(score.part_list.score_parts), 1)

        score_part = score.part_list.score_parts[0]
        self.assertEqual(score_part.id, 'P1')
        self.assertEqual(score_part.part_name, 'Piano')
        self.assertEqual(score_part.part_abbreviation, 'Pno.')
        self.assertEqual(score_part.instrument_name, 'Piano')
        self.assertEqual(score_part.midi_instrument, 1)

        self.assertEqual(len(score.parts), 1)

        part = score.parts[0]
        self.assertEqual(part.id, 'P1')
        self.assertEqual(len(part.measures), 3)


        measure = part.measures[0]
        notes = measure.notes(staff=1)

        note = notes[0]
        self.assertTrue(note.harmony is not None)
        self.assertEqual(note.harmony.text, 'C')

        note = notes[1]
        self.assertTrue(note.harmony is not None)
        self.assertEqual(note.harmony.text, 'D')

        note = notes[2]
        self.assertTrue(note.harmony is not None)
        self.assertEqual(note.harmony.text, 'C')

        note = notes[3]
        self.assertTrue(note.harmony is not None)
        self.assertEqual(note.harmony.text, 'Gm')


        measure = part.measures[1]
        notes = measure.notes(staff=1)

        note = notes[0]
        self.assertTrue(note.harmony is not None)
        self.assertEqual(note.harmony.text, 'F7')

        note = notes[1]
        self.assertTrue(note.harmony is None)

        note = notes[2]
        self.assertTrue(note.harmony is None)

        note = notes[3]
        self.assertTrue(note.harmony is None)


        measure = part.measures[2]
        notes = measure.notes(staff=1)

        note = notes[0]
        self.assertTrue(note.harmony is not None)
        self.assertEqual(note.harmony.text, 'G#')

        note = notes[1]
        self.assertTrue(note.harmony is None)

        note = notes[2]
        self.assertTrue(note.harmony is None)

        note = notes[3]
        self.assertTrue(note.harmony is None)


        self.save(score, filename + '2')

        self.check_file(filename + '2', filename)


    def test_rehearsals(self):
        filename = os.path.join(data_dir, 'one_part', 'rehearsals.xml')

        score = Score()
        self.assertTrue(score.load(filename))

        self.assertTrue(score.xml_document is not None)
        self.assertTrue(score.part_list is not None)

        self.assertEqual(len(score.part_list.score_parts), 1)

        score_part = score.part_list.score_parts[0]
        self.assertEqual(score_part.id, 'P1')
        self.assertEqual(score_part.part_name, 'Piano')
        self.assertEqual(score_part.part_abbreviation, 'Pno.')
        self.assertEqual(score_part.instrument_name, 'Piano')
        self.assertEqual(score_part.midi_instrument, 1)

        self.assertEqual(len(score.parts), 1)

        part = score.parts[0]
        self.assertEqual(part.id, 'P1')
        self.assertEqual(len(part.measures), 3)


        measure = part.measures[0]
        notes = measure.notes(staff=1)

        note = notes[0]
        self.assertTrue(note.rehearsal is not None)
        self.assertEqual(note.rehearsal.text, 'A')


        measure = part.measures[1]
        notes = measure.notes(staff=1)

        note = notes[0]
        self.assertTrue(note.rehearsal is not None)
        self.assertEqual(note.rehearsal.text, 'B')

        note = notes[1]
        self.assertTrue(note.rehearsal is not None)
        self.assertEqual(note.rehearsal.text, 'C')


        measure = part.measures[2]
        notes = measure.notes(staff=1)

        note = notes[0]
        self.assertTrue(note.rehearsal is not None)
        self.assertEqual(note.rehearsal.text, 'D')


        self.save(score, filename + '2')

        self.check_file(filename + '2', filename)


    def test_key_signature(self):
        filename = os.path.join(data_dir, 'one_part', 'key_signature.xml')

        score = Score()
        self.assertTrue(score.load(filename))

        self.assertTrue(score.xml_document is not None)
        self.assertTrue(score.part_list is not None)

        self.assertEqual(len(score.part_list.score_parts), 1)

        score_part = score.part_list.score_parts[0]
        self.assertEqual(score_part.id, 'P1')
        self.assertEqual(score_part.part_name, 'Piano')
        self.assertEqual(score_part.part_abbreviation, 'Pno.')
        self.assertEqual(score_part.instrument_name, 'Piano')
        self.assertEqual(score_part.midi_instrument, 1)

        self.assertEqual(len(score.parts), 1)

        part = score.parts[0]
        self.assertEqual(part.id, 'P1')
        self.assertEqual(len(part.measures), 1)


        measure = part.measures[0]
        notes = measure.notes(staff=1)

        note = notes[0]
        self.assertEqual(note.name, 'C#5')
        self.assertEqual(note.accidental, Note.NONE)

        note = notes[1]
        self.assertEqual(note.name, 'C5')
        self.assertEqual(note.accidental, Note.NATURAL)

        note = notes[2]
        self.assertEqual(note.name, 'C#5')
        self.assertEqual(note.accidental, Note.SHARP)

        note = notes[3]
        self.assertEqual(note.name, 'D#5')
        self.assertEqual(note.accidental, Note.SHARP)


        self.save(score, filename + '2')

        self.check_file(filename + '2', filename)


    def test_repeat_n1_r2(self):
        filename = os.path.join(data_dir, 'one_part', 'repeat_n1_r2.xml')

        score = Score()
        self.assertTrue(score.load(filename))

        self.assertTrue(score.xml_document is not None)
        self.assertTrue(score.part_list is not None)

        self.assertEqual(len(score.part_list.score_parts), 1)
        self.assertEqual(len(score.parts), 1)

        part = score.parts[0]
        self.assertEqual(part.id, 'P1')
        self.assertEqual(len(part.measures), 3)


        measure = part.measures[0]
        self.assertTrue(measure.left_barline is None)
        self.assertTrue(measure.right_barline is None)


        measure = part.measures[1]
        self.assertTrue(measure.left_barline is not None)
        self.assertTrue(measure.right_barline is None)

        self.assertEqual(measure.left_barline.location, Barline.LEFT)
        self.assertTrue(measure.left_barline.isRepeat)
        self.assertEqual(measure.left_barline.repeatDirection, Barline.FORWARD)


        measure = part.measures[2]
        self.assertTrue(measure.left_barline is None)
        self.assertTrue(measure.right_barline is not None)

        self.assertEqual(measure.right_barline.location, Barline.RIGHT)
        self.assertTrue(measure.right_barline.isRepeat)
        self.assertEqual(measure.right_barline.repeatDirection, Barline.BACKWARD)


        self.save(score, filename + '2')

        self.check_file(filename + '2', filename)


    def test_repeat_n1_r2_n1(self):
        filename = os.path.join(data_dir, 'one_part', 'repeat_n1_r2_n1.xml')

        score = Score()
        self.assertTrue(score.load(filename))

        self.assertTrue(score.xml_document is not None)
        self.assertTrue(score.part_list is not None)

        self.assertEqual(len(score.part_list.score_parts), 1)
        self.assertEqual(len(score.parts), 1)

        part = score.parts[0]
        self.assertEqual(part.id, 'P1')
        self.assertEqual(len(part.measures), 4)


        measure = part.measures[0]
        self.assertTrue(measure.left_barline is None)
        self.assertTrue(measure.right_barline is None)


        measure = part.measures[1]
        self.assertTrue(measure.left_barline is not None)
        self.assertTrue(measure.right_barline is None)

        self.assertEqual(measure.left_barline.location, Barline.LEFT)
        self.assertTrue(measure.left_barline.isRepeat)
        self.assertEqual(measure.left_barline.repeatDirection, Barline.FORWARD)


        measure = part.measures[2]
        self.assertTrue(measure.left_barline is None)
        self.assertTrue(measure.right_barline is not None)

        self.assertEqual(measure.right_barline.location, Barline.RIGHT)
        self.assertTrue(measure.right_barline.isRepeat)
        self.assertEqual(measure.right_barline.repeatDirection, Barline.BACKWARD)


        measure = part.measures[3]
        self.assertTrue(measure.left_barline is None)
        self.assertTrue(measure.right_barline is not None)

        self.assertEqual(measure.right_barline.location, Barline.RIGHT)
        self.assertFalse(measure.right_barline.isRepeat)
        self.assertEqual(measure.right_barline.style, Barline.LIGHT_HEAVY)


        self.save(score, filename + '2')

        self.check_file(filename + '2', filename)


    def test_repeat_n1_r1_r1_n1(self):
        filename = os.path.join(data_dir, 'one_part', 'repeat_n1_r1_r1_n1.xml')

        score = Score()
        self.assertTrue(score.load(filename))

        self.assertTrue(score.xml_document is not None)
        self.assertTrue(score.part_list is not None)

        self.assertEqual(len(score.part_list.score_parts), 1)
        self.assertEqual(len(score.parts), 1)

        part = score.parts[0]
        self.assertEqual(part.id, 'P1')
        self.assertEqual(len(part.measures), 4)


        measure = part.measures[0]
        self.assertTrue(measure.left_barline is None)
        self.assertTrue(measure.right_barline is None)


        measure = part.measures[1]
        self.assertTrue(measure.left_barline is not None)
        self.assertTrue(measure.right_barline is not None)

        self.assertEqual(measure.left_barline.location, Barline.LEFT)
        self.assertTrue(measure.left_barline.isRepeat)
        self.assertEqual(measure.left_barline.repeatDirection, Barline.FORWARD)

        self.assertEqual(measure.right_barline.location, Barline.RIGHT)
        self.assertTrue(measure.right_barline.isRepeat)
        self.assertEqual(measure.right_barline.repeatDirection, Barline.BACKWARD)


        measure = part.measures[2]
        self.assertTrue(measure.left_barline is not None)
        self.assertTrue(measure.right_barline is not None)

        self.assertEqual(measure.left_barline.location, Barline.LEFT)
        self.assertTrue(measure.left_barline.isRepeat)
        self.assertEqual(measure.left_barline.repeatDirection, Barline.FORWARD)

        self.assertEqual(measure.right_barline.location, Barline.RIGHT)
        self.assertTrue(measure.right_barline.isRepeat)
        self.assertEqual(measure.right_barline.repeatDirection, Barline.BACKWARD)


        measure = part.measures[3]
        self.assertTrue(measure.left_barline is None)
        self.assertTrue(measure.right_barline is not None)

        self.assertEqual(measure.right_barline.location, Barline.RIGHT)
        self.assertFalse(measure.right_barline.isRepeat)
        self.assertEqual(measure.right_barline.style, Barline.LIGHT_HEAVY)


        self.save(score, filename + '2')

        self.check_file(filename + '2', filename)


    def test_repeat_n1_r2_n1_voltas(self):
        filename = os.path.join(data_dir, 'one_part', 'repeat_n1_r2_n1_voltas.xml')

        score = Score()
        self.assertTrue(score.load(filename))

        self.assertTrue(score.xml_document is not None)
        self.assertTrue(score.part_list is not None)

        self.assertEqual(len(score.part_list.score_parts), 1)
        self.assertEqual(len(score.parts), 1)

        part = score.parts[0]
        self.assertEqual(part.id, 'P1')
        self.assertEqual(len(part.measures), 5)


        measure = part.measures[0]
        self.assertTrue(measure.left_barline is None)
        self.assertTrue(measure.right_barline is None)


        measure = part.measures[1]
        self.assertTrue(measure.left_barline is not None)
        self.assertTrue(measure.right_barline is None)

        self.assertEqual(measure.left_barline.location, Barline.LEFT)
        self.assertTrue(measure.left_barline.isRepeat)
        self.assertEqual(measure.left_barline.repeatDirection, Barline.FORWARD)


        measure = part.measures[2]
        self.assertTrue(measure.left_barline is not None)
        self.assertTrue(measure.right_barline is not None)

        self.assertEqual(measure.left_barline.location, Barline.LEFT)
        self.assertFalse(measure.left_barline.isRepeat)
        self.assertEqual(measure.left_barline.volta, 1)

        self.assertEqual(measure.right_barline.location, Barline.RIGHT)
        self.assertTrue(measure.right_barline.isRepeat)
        self.assertEqual(measure.right_barline.repeatDirection, Barline.BACKWARD)
        self.assertEqual(measure.right_barline.volta, 1)


        measure = part.measures[3]
        self.assertTrue(measure.left_barline is not None)
        self.assertTrue(measure.right_barline is not None)

        self.assertEqual(measure.left_barline.location, Barline.LEFT)
        self.assertFalse(measure.left_barline.isRepeat)
        self.assertTrue(measure.left_barline.style is None)
        self.assertEqual(measure.left_barline.volta, 2)

        self.assertEqual(measure.right_barline.location, Barline.RIGHT)
        self.assertFalse(measure.right_barline.isRepeat)
        self.assertEqual(measure.right_barline.style, Barline.LIGHT_LIGHT)
        self.assertEqual(measure.right_barline.volta, 2)


        measure = part.measures[4]
        self.assertTrue(measure.left_barline is None)
        self.assertTrue(measure.right_barline is not None)

        self.assertEqual(measure.right_barline.location, Barline.RIGHT)
        self.assertFalse(measure.right_barline.isRepeat)
        self.assertEqual(measure.right_barline.style, Barline.LIGHT_HEAVY)
        self.assertTrue(measure.right_barline.volta is None)


        self.save(score, filename + '2')

        self.check_file(filename + '2', filename)


    def test_expandRepeats_n1_r2(self):
        filename = os.path.join(data_dir, 'one_part', 'repeat_n1_r2.xml')

        score = Score()
        self.assertTrue(score.load(filename))

        score.expandRepeats()

        part = score.parts[0]
        self.assertEqual(part.id, 'P1')
        self.assertEqual(len(part.measures), 5)


        measure = part.measures[0]
        self.assertEqual(measure.number, 1)

        self.assertTrue(measure.left_barline is None)
        self.assertTrue(measure.right_barline is None)

        rehearsal = measure.notes(staff=1)[0].rehearsal
        self.assertTrue(rehearsal)
        self.assertEqual(rehearsal.text, 'A')


        measure = part.measures[1]
        self.assertEqual(measure.number, 2)

        self.assertTrue(measure.left_barline is not None)
        self.assertTrue(measure.right_barline is None)

        self.assertEqual(measure.left_barline.location, Barline.LEFT)
        self.assertFalse(measure.left_barline.isRepeat)
        self.assertEqual(measure.left_barline.style, Barline.LIGHT_LIGHT)

        rehearsal = measure.notes(staff=1)[0].rehearsal
        self.assertTrue(rehearsal)
        self.assertEqual(rehearsal.text, 'B1')


        measure = part.measures[2]
        self.assertEqual(measure.number, 3)

        self.assertTrue(measure.left_barline is None)
        self.assertTrue(measure.right_barline is None)


        measure = part.measures[3]
        self.assertEqual(measure.number, 4)

        self.assertTrue(measure.left_barline is not None)
        self.assertTrue(measure.right_barline is None)

        self.assertEqual(measure.left_barline.location, Barline.LEFT)
        self.assertFalse(measure.left_barline.isRepeat)
        self.assertEqual(measure.left_barline.style, Barline.LIGHT_LIGHT)

        rehearsal = measure.notes(staff=1)[0].rehearsal
        self.assertTrue(rehearsal)
        self.assertEqual(rehearsal.text, 'B2')


        measure = part.measures[4]
        self.assertEqual(measure.number, 5)

        self.assertTrue(measure.left_barline is None)
        self.assertTrue(measure.right_barline is not None)

        self.assertEqual(measure.right_barline.location, Barline.RIGHT)
        self.assertFalse(measure.right_barline.isRepeat)
        self.assertEqual(measure.right_barline.style, Barline.LIGHT_HEAVY)


    def test_expandRepeats_n1_r2_n1(self):
        filename = os.path.join(data_dir, 'one_part', 'repeat_n1_r2_n1.xml')

        score = Score()
        self.assertTrue(score.load(filename))

        score.expandRepeats()

        part = score.parts[0]
        self.assertEqual(part.id, 'P1')
        self.assertEqual(len(part.measures), 6)


        measure = part.measures[0]
        self.assertEqual(measure.number, 1)

        self.assertTrue(measure.left_barline is None)
        self.assertTrue(measure.right_barline is None)


        measure = part.measures[1]
        self.assertEqual(measure.number, 2)

        self.assertTrue(measure.left_barline is not None)
        self.assertTrue(measure.right_barline is None)

        self.assertEqual(measure.left_barline.location, Barline.LEFT)
        self.assertFalse(measure.left_barline.isRepeat)
        self.assertEqual(measure.left_barline.style, Barline.LIGHT_LIGHT)

        rehearsal = measure.notes(staff=1)[0].rehearsal
        self.assertTrue(rehearsal)
        self.assertEqual(rehearsal.text, 'A1')


        measure = part.measures[2]
        self.assertEqual(measure.number, 3)

        self.assertTrue(measure.left_barline is None)
        self.assertTrue(measure.right_barline is None)


        measure = part.measures[3]
        self.assertEqual(measure.number, 4)

        self.assertTrue(measure.left_barline is not None)
        self.assertTrue(measure.right_barline is None)

        self.assertEqual(measure.left_barline.location, Barline.LEFT)
        self.assertFalse(measure.left_barline.isRepeat)
        self.assertEqual(measure.left_barline.style, Barline.LIGHT_LIGHT)

        rehearsal = measure.notes(staff=1)[0].rehearsal
        self.assertTrue(rehearsal)
        self.assertEqual(rehearsal.text, 'A2')


        measure = part.measures[4]
        self.assertEqual(measure.number, 5)

        self.assertTrue(measure.left_barline is None)
        self.assertTrue(measure.right_barline is None)


        measure = part.measures[5]
        self.assertEqual(measure.number, 6)

        self.assertTrue(measure.left_barline is not None)
        self.assertTrue(measure.right_barline is not None)

        self.assertEqual(measure.left_barline.location, Barline.LEFT)
        self.assertFalse(measure.left_barline.isRepeat)
        self.assertEqual(measure.left_barline.style, Barline.LIGHT_LIGHT)

        self.assertEqual(measure.right_barline.location, Barline.RIGHT)
        self.assertFalse(measure.right_barline.isRepeat)
        self.assertEqual(measure.right_barline.style, Barline.LIGHT_HEAVY)


    def test_expandRepeats_n1_r1_r1_n1(self):
        filename = os.path.join(data_dir, 'one_part', 'repeat_n1_r1_r1_n1.xml')

        score = Score()
        self.assertTrue(score.load(filename))

        score.expandRepeats()

        part = score.parts[0]
        self.assertEqual(part.id, 'P1')
        self.assertEqual(len(part.measures), 6)


        measure = part.measures[0]
        self.assertEqual(measure.number, 1)

        self.assertTrue(measure.left_barline is None)
        self.assertTrue(measure.right_barline is None)


        measure = part.measures[1]
        self.assertEqual(measure.number, 2)

        self.assertTrue(measure.left_barline is not None)
        self.assertTrue(measure.right_barline is None)

        self.assertEqual(measure.left_barline.location, Barline.LEFT)
        self.assertFalse(measure.left_barline.isRepeat)
        self.assertEqual(measure.left_barline.style, Barline.LIGHT_LIGHT)

        rehearsal = measure.notes(staff=1)[0].rehearsal
        self.assertTrue(rehearsal)
        self.assertEqual(rehearsal.text, 'A1')


        measure = part.measures[2]
        self.assertEqual(measure.number, 3)

        self.assertTrue(measure.left_barline is not None)
        self.assertTrue(measure.right_barline is None)

        self.assertEqual(measure.left_barline.location, Barline.LEFT)
        self.assertFalse(measure.left_barline.isRepeat)
        self.assertEqual(measure.left_barline.style, Barline.LIGHT_LIGHT)

        rehearsal = measure.notes(staff=1)[0].rehearsal
        self.assertTrue(rehearsal)
        self.assertEqual(rehearsal.text, 'A2')


        measure = part.measures[3]
        self.assertEqual(measure.number, 4)

        self.assertTrue(measure.left_barline is not None)
        self.assertTrue(measure.right_barline is None)

        self.assertEqual(measure.left_barline.location, Barline.LEFT)
        self.assertFalse(measure.left_barline.isRepeat)
        self.assertEqual(measure.left_barline.style, Barline.LIGHT_LIGHT)

        rehearsal = measure.notes(staff=1)[0].rehearsal
        self.assertTrue(rehearsal)
        self.assertEqual(rehearsal.text, 'B1')


        measure = part.measures[4]
        self.assertEqual(measure.number, 5)

        self.assertTrue(measure.left_barline is not None)
        self.assertTrue(measure.right_barline is None)

        self.assertEqual(measure.left_barline.location, Barline.LEFT)
        self.assertFalse(measure.left_barline.isRepeat)
        self.assertEqual(measure.left_barline.style, Barline.LIGHT_LIGHT)

        rehearsal = measure.notes(staff=1)[0].rehearsal
        self.assertTrue(rehearsal)
        self.assertEqual(rehearsal.text, 'B2')


        measure = part.measures[5]
        self.assertEqual(measure.number, 6)

        self.assertTrue(measure.left_barline is not None)
        self.assertTrue(measure.right_barline is not None)

        self.assertEqual(measure.left_barline.location, Barline.LEFT)
        self.assertFalse(measure.left_barline.isRepeat)
        self.assertEqual(measure.left_barline.style, Barline.LIGHT_LIGHT)

        self.assertEqual(measure.right_barline.location, Barline.RIGHT)
        self.assertFalse(measure.right_barline.isRepeat)
        self.assertEqual(measure.right_barline.style, Barline.LIGHT_HEAVY)

        rehearsal = measure.notes(staff=1)[0].rehearsal
        self.assertTrue(rehearsal)
        self.assertEqual(rehearsal.text, 'C')


    def test_expandRepeats_n1_r2_n1_voltas(self):
        filename = os.path.join(data_dir, 'one_part', 'repeat_n1_r2_n1_voltas.xml')

        score = Score()
        self.assertTrue(score.load(filename))

        score.expandRepeats()

        part = score.parts[0]
        self.assertEqual(part.id, 'P1')
        self.assertEqual(len(part.measures), 6)


        measure = part.measures[0]
        self.assertEqual(measure.number, 1)

        self.assertTrue(measure.left_barline is None)
        self.assertTrue(measure.right_barline is None)


        measure = part.measures[1]
        self.assertEqual(measure.number, 2)

        self.assertTrue(measure.left_barline is not None)
        self.assertTrue(measure.right_barline is None)

        self.assertEqual(measure.left_barline.location, Barline.LEFT)
        self.assertFalse(measure.left_barline.isRepeat)
        self.assertEqual(measure.left_barline.style, Barline.LIGHT_LIGHT)

        rehearsal = measure.notes(staff=1)[0].rehearsal
        self.assertTrue(rehearsal)
        self.assertEqual(rehearsal.text, 'A1')


        measure = part.measures[2]
        self.assertEqual(measure.number, 3)

        self.assertTrue(measure.left_barline is None)
        self.assertTrue(measure.right_barline is None)
        self.assertTrue(measure.volta is None)


        measure = part.measures[3]
        self.assertEqual(measure.number, 4)

        self.assertTrue(measure.left_barline is not None)
        self.assertTrue(measure.right_barline is None)

        self.assertEqual(measure.left_barline.location, Barline.LEFT)
        self.assertFalse(measure.left_barline.isRepeat)
        self.assertEqual(measure.left_barline.style, Barline.LIGHT_LIGHT)

        rehearsal = measure.notes(staff=1)[0].rehearsal
        self.assertTrue(rehearsal)
        self.assertEqual(rehearsal.text, 'A2')


        measure = part.measures[4]
        self.assertEqual(measure.number, 5)

        self.assertTrue(measure.left_barline is None)
        self.assertTrue(measure.right_barline is not None)
        self.assertTrue(measure.volta is None)

        self.assertEqual(measure.right_barline.location, Barline.RIGHT)
        self.assertFalse(measure.right_barline.isRepeat)
        self.assertEqual(measure.right_barline.style, Barline.LIGHT_LIGHT)


        measure = part.measures[5]
        self.assertEqual(measure.number, 6)

        self.assertTrue(measure.left_barline is None)
        self.assertTrue(measure.right_barline is not None)

        self.assertEqual(measure.right_barline.location, Barline.RIGHT)
        self.assertFalse(measure.right_barline.isRepeat)
        self.assertEqual(measure.right_barline.style, Barline.LIGHT_HEAVY)


    def test_addEmptyMeasures(self):
        filename = os.path.join(data_dir, 'one_part', 'repeat_n1_r2.xml')

        score = Score()
        self.assertTrue(score.load(filename))

        score.addEmptyMeasures(2)

        part = score.parts[0]
        self.assertEqual(part.id, 'P1')
        self.assertEqual(len(part.measures), 5)


        measure = part.measures[0]
        self.assertEqual(measure.number, 1)

        self.assertTrue(measure.left_barline is None)
        self.assertTrue(measure.right_barline is None)

        notes = measure.notes(staff=1)
        self.assertEqual(len(notes), 1)
        self.assertTrue(isinstance(notes[0], Rest))

        rehearsal = notes[0].rehearsal
        self.assertTrue(rehearsal)
        self.assertEqual(rehearsal.text, 'A')


        measure = part.measures[1]
        self.assertEqual(measure.number, 2)

        self.assertTrue(measure.left_barline is None)
        self.assertTrue(measure.right_barline is None)

        notes = measure.notes(staff=1)
        self.assertEqual(len(notes), 1)
        self.assertTrue(isinstance(notes[0], Rest))
        self.assertFalse(notes[0].rehearsal)


        measure = part.measures[2]
        self.assertEqual(measure.number, 3)

        self.assertTrue(measure.left_barline is None)
        self.assertTrue(measure.right_barline is None)

        notes = measure.notes(staff=1)
        self.assertEqual(len(notes), 1)
        self.assertTrue(isinstance(notes[0], Note))
        self.assertFalse(notes[0].rehearsal)


        measure = part.measures[3]
        self.assertEqual(measure.number, 4)

        self.assertTrue(measure.left_barline is not None)
        self.assertTrue(measure.right_barline is None)

        self.assertEqual(measure.left_barline.location, Barline.LEFT)
        self.assertTrue(measure.left_barline.isRepeat)

        rehearsal = measure.notes(staff=1)[0].rehearsal
        self.assertTrue(rehearsal)
        self.assertEqual(rehearsal.text, 'B')


        measure = part.measures[4]
        self.assertEqual(measure.number, 5)

        self.assertTrue(measure.left_barline is None)
        self.assertTrue(measure.right_barline is not None)

        self.assertEqual(measure.right_barline.location, Barline.RIGHT)
        self.assertTrue(measure.right_barline.isRepeat)
