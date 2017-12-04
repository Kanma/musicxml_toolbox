from unittest import TestCase
import os
import xml.etree.ElementTree as ET

from ..musicxml import Score
from ..musicxml import Measure
from ..musicxml import Chord
from ..musicxml import Note
from . import data_dir


class TestMeasure(TestCase):

    def test_addFingering(self):
        filename = os.path.join(data_dir, 'one_part', 'fingering.xml')

        score = Score()
        self.assertTrue(score.load(filename))

        part = score.parts[0]

        part.addFingering(staff=1)
        part.addFingering(staff=2)

        measure = part.measures[0]


        notes = measure.notes(staff=1)
        self.assertEqual(len(notes), 4)

        note = notes[0]
        self.assertTrue(isinstance(note, Note))
        self.assertEqual(note.fingering.finger, 2)

        note = notes[1]
        self.assertTrue(isinstance(note, Note))
        self.assertEqual(note.fingering.finger, 3)

        note = notes[2]
        self.assertTrue(isinstance(note, Note))
        self.assertEqual(note.fingering.finger, 4)

        note = notes[3]
        self.assertTrue(isinstance(note, Note))
        self.assertEqual(note.fingering.finger, 5)


        notes = measure.notes(staff=2)
        self.assertEqual(len(notes), 4)

        note = notes[0]
        self.assertTrue(isinstance(note, Note))
        self.assertEqual(note.fingering.finger, 4)

        note = notes[1]
        self.assertTrue(isinstance(note, Note))
        self.assertEqual(note.fingering.finger, 3)

        note = notes[2]
        self.assertTrue(isinstance(note, Note))
        self.assertEqual(note.fingering.finger, 2)

        note = notes[3]
        self.assertTrue(isinstance(note, Note))
        self.assertEqual(note.fingering.finger, 1)
