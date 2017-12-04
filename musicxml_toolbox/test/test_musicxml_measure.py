from unittest import TestCase
import os
import xml.etree.ElementTree as ET

from ..musicxml import Score
from ..musicxml import Measure
from ..musicxml import Chord
from ..musicxml import Note
from . import data_dir


class TestMeasure(TestCase):

    def test_replaceChords(self):
        filename = os.path.join(data_dir, 'one_part', 'four_chords.xml')

        score = Score()
        self.assertTrue(score.load(filename))

        part = score.parts[0]

        measure = part.measures[0]
        measure.replaceChords(staff=1)

        notes = measure.notes(staff=1)
        self.assertEqual(len(notes), 4)

        note = notes[0]
        self.assertTrue(isinstance(note, Note))
        self.assertEqual(note.name, 'C4')
        self.assertEqual(note.duration, 1)
        self.assertEqual(note.staff, 1)

        note = notes[1]
        self.assertTrue(isinstance(note, Note))
        self.assertEqual(note.name, 'F4')
        self.assertEqual(note.duration, 1)
        self.assertEqual(note.staff, 1)

        note = notes[2]
        self.assertTrue(isinstance(note, Note))
        self.assertEqual(note.name, 'C5')
        self.assertEqual(note.duration, 1)
        self.assertEqual(note.staff, 1)

        note = notes[3]
        self.assertTrue(isinstance(note, Note))
        self.assertEqual(note.name, 'E4')
        self.assertEqual(note.duration, 1)
        self.assertEqual(note.staff, 1)


    def test_annotateChords(self):
        filename = os.path.join(data_dir, 'one_part', 'four_chords.xml')

        score = Score()
        self.assertTrue(score.load(filename))

        part = score.parts[0]

        measure = part.measures[0]
        measure.annotateChords(staff=1)

        notes = measure.notes(staff=1)
        self.assertEqual(len(notes), 4)

        chord = notes[0]
        self.assertTrue(isinstance(chord, Chord))
        self.assertTrue(chord.harmony)
        self.assertEqual(chord.harmony.text, 'C')

        chord = notes[1]
        self.assertTrue(isinstance(chord, Chord))
        self.assertTrue(chord.harmony)
        self.assertEqual(chord.harmony.text, 'F')

        chord = notes[2]
        self.assertTrue(isinstance(chord, Chord))
        self.assertTrue(chord.harmony)
        self.assertEqual(chord.harmony.text, 'C')

        chord = notes[3]
        self.assertTrue(isinstance(chord, Chord))
        self.assertTrue(chord.harmony)
        self.assertEqual(chord.harmony.text, 'Em')


    def test_removeKeySignature(self):
        filename = os.path.join(data_dir, 'one_part', 'key_signature.xml')

        score = Score()
        self.assertTrue(score.load(filename))

        part = score.parts[0]

        measure = part.measures[0]
        measure.removeKeySignature()

        notes = measure.notes(staff=1)
        self.assertEqual(len(notes), 4)

        note = notes[0]
        self.assertEqual(note.name, 'C#5')
        self.assertEqual(note.accidental, Note.SHARP)

        note = notes[1]
        self.assertEqual(note.name, 'C5')
        self.assertEqual(note.accidental, Note.NONE)

        note = notes[2]
        self.assertEqual(note.name, 'C#5')
        self.assertEqual(note.accidental, Note.NONE)

        note = notes[3]
        self.assertEqual(note.name, 'D#5')
        self.assertEqual(note.accidental, Note.SHARP)
