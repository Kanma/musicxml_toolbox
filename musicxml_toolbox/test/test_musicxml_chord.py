from unittest import TestCase
import xml.etree.ElementTree as ET

from ..musicxml import Chord
from ..musicxml import Note


#----------------------------------------------------------


class TestChordBase(TestCase):

    def createChord(self, note_names):
        notes = []

        for note in note_names:
            pitch = note[0]

            if note[1] == '#':
                alter = 1
                octave = int(note[2:])
            elif note[1] == 'b':
                alter = -1
                octave = int(note[2:])
            else:
                alter = 0
                octave = int(note[1:])

            notes.append(Note(ET.fromstring("""<note>
                  <pitch>
                    <step>%s</step>
                    <alter>%d</alter>
                    <octave>%d</octave>
                  </pitch>
                  <duration>1</duration>
                  <voice>1</voice>
                  <type>quarter</type>
               </note>""" % (pitch, alter, octave)
            )))

        chord = Chord(notes[0])
        for note in notes[1:]:
            chord.addNote(note)

        return chord


#----------------------------------------------------------


class TestTriadChord(TestChordBase):

    def process(self, name, notes, root, third, fifth, major):
        chord = self.createChord(notes)

        self.assertTrue(chord.isTriad)
        self.assertFalse(chord.isSeventh)
        self.assertFalse(chord.isDominantSeventh)

        self.assertEqual(chord.isMajor, major)

        self.assertEqual(chord.root, root)
        self.assertEqual(chord.third, third)
        self.assertEqual(chord.fifth, fifth)

        self.assertEqual(chord.note_names, notes)
        self.assertEqual(chord.name, name)


    def process_inversions(self, name, notes, root, third, fifth, major):
        for i in range(3):
            self.process(
                name = name,
                notes = notes,
                root = root,
                third = third,
                fifth = fifth,
                major = major
            )

            notes = notes[1:] + [notes[0]]


    def test_C(self):
        self.process_inversions(
            name = 'C',
            notes = ['C4', 'E4', 'G4'],
            root = 'C',
            third = 'E',
            fifth = 'G',
            major = True
        )


    def test_Cm(self):
        self.process_inversions(
            name = 'Cm',
            notes = ['C4', 'Eb4', 'G4'],
            root = 'C',
            third = 'Eb',
            fifth = 'G',
            major = False
        )


    def test_D(self):
        self.process_inversions(
            name = 'D',
            notes = ['D4', 'F#4', 'A4'],
            root = 'D',
            third = 'F#',
            fifth = 'A',
            major = True
        )


    def test_Dm(self):
        self.process_inversions(
            name = 'Dm',
            notes = ['D4', 'F4', 'A4'],
            root = 'D',
            third = 'F',
            fifth = 'A',
            major = False
        )


    def test_E(self):
        self.process_inversions(
            name = 'E',
            notes = ['E4', 'G#4', 'B4'],
            root = 'E',
            third = 'G#',
            fifth = 'B',
            major = True
        )


    def test_Em(self):
        self.process_inversions(
            name = 'Em',
            notes = ['E4', 'G4', 'B4'],
            root = 'E',
            third = 'G',
            fifth = 'B',
            major = False
        )


    def test_F(self):
        self.process_inversions(
            name = 'F',
            notes = ['F4', 'A4', 'C5'],
            root = 'F',
            third = 'A',
            fifth = 'C',
            major = True
        )


    def test_Fm(self):
        self.process_inversions(
            name = 'Fm',
            notes = ['F4', 'Ab4', 'C5'],
            root = 'F',
            third = 'Ab',
            fifth = 'C',
            major = False
        )


    def test_G(self):
        self.process_inversions(
            name = 'G',
            notes = ['G4', 'B4', 'D5'],
            root = 'G',
            third = 'B',
            fifth = 'D',
            major = True
        )


    def test_Gm(self):
        self.process_inversions(
            name = 'Gm',
            notes = ['G4', 'Bb4', 'D5'],
            root = 'G',
            third = 'Bb',
            fifth = 'D',
            major = False
        )


    def test_A(self):
        self.process_inversions(
            name = 'A',
            notes = ['A4', 'C#5', 'E5'],
            root = 'A',
            third = 'C#',
            fifth = 'E',
            major = True
        )


    def test_Am(self):
        self.process_inversions(
            name = 'Am',
            notes = ['A4', 'C5', 'E5'],
            root = 'A',
            third = 'C',
            fifth = 'E',
            major = False
        )


    def test_B(self):
        self.process_inversions(
            name = 'B',
            notes = ['B3', 'D#4', 'F#4'],
            root = 'B',
            third = 'D#',
            fifth = 'F#',
            major = True
        )


    def test_Bm(self):
        self.process_inversions(
            name = 'Bm',
            notes = ['B3', 'D4', 'F#4'],
            root = 'B',
            third = 'D',
            fifth = 'F#',
            major = False
        )


#----------------------------------------------------------


class TestSeventhChord(TestChordBase):

    def process(self, name, notes, root, third, fifth, seventh, dominant, major):
        chord = self.createChord(notes)

        self.assertFalse(chord.isTriad)
        self.assertTrue(chord.isSeventh)

        self.assertEqual(chord.isDominantSeventh, dominant)
        self.assertEqual(chord.isMajor, major)

        self.assertEqual(chord.root, root)
        self.assertEqual(chord.third, third)
        self.assertEqual(chord.fifth, fifth)
        self.assertEqual(chord.seventh, seventh)

        self.assertEqual(chord.note_names, notes)
        self.assertEqual(chord.name, name)


    def process_inversions(self, name, notes, root, third, fifth, seventh, dominant, major):
        for i in range(3):
            self.process(
                name = name,
                notes = notes,
                root = root,
                third = third,
                fifth = fifth,
                seventh = seventh,
                dominant = dominant,
                major = major
            )

            notes = notes[1:] + [notes[0]]


    def test_C7(self):
        self.process_inversions(
            name = 'C7',
            notes = ['C4', 'E4', 'G4', 'Bb4'],
            root = 'C',
            third = 'E',
            fifth = 'G',
            seventh = 'Bb',
            dominant = True,
            major = True
        )


    def test_CM7(self):
        self.process_inversions(
            name = 'CM7',
            notes = ['C4', 'E4', 'G4', 'B4'],
            root = 'C',
            third = 'E',
            fifth = 'G',
            seventh = 'B',
            dominant = False,
            major = True
        )


    def test_Cm7(self):
        self.process_inversions(
            name = 'Cm7',
            notes = ['C4', 'Eb4', 'G4', 'Bb4'],
            root = 'C',
            third = 'Eb',
            fifth = 'G',
            seventh = 'Bb',
            dominant = False,
            major = False
        )


    def test_D(self):
        self.process_inversions(
            name = 'D7',
            notes = ['D4', 'F#4', 'A4', 'C5'],
            root = 'D',
            third = 'F#',
            fifth = 'A',
            seventh = 'C',
            dominant = True,
            major = True
        )


    def test_DM7(self):
        self.process_inversions(
            name = 'DM7',
            notes = ['D4', 'F#4', 'A4', 'C#5'],
            root = 'D',
            third = 'F#',
            fifth = 'A',
            seventh = 'C#',
            dominant = False,
            major = True
        )


    def test_Dm7(self):
        self.process_inversions(
            name = 'Dm7',
            notes = ['D4', 'F4', 'A4', 'C5'],
            root = 'D',
            third = 'F',
            fifth = 'A',
            seventh = 'C',
            dominant = False,
            major = False
        )


    def test_E7(self):
        self.process_inversions(
            name = 'E7',
            notes = ['E4', 'G#4', 'B4', 'D5'],
            root = 'E',
            third = 'G#',
            fifth = 'B',
            seventh = 'D',
            dominant = True,
            major = True
        )


    def test_EM7(self):
        self.process_inversions(
            name = 'EM7',
            notes = ['E4', 'G#4', 'B4', 'D#5'],
            root = 'E',
            third = 'G#',
            fifth = 'B',
            seventh = 'D#',
            dominant = False,
            major = True
        )


    def test_Em7(self):
        self.process_inversions(
            name = 'Em7',
            notes = ['E4', 'G4', 'B4', 'D5'],
            root = 'E',
            third = 'G',
            fifth = 'B',
            seventh = 'D',
            dominant = False,
            major = False
        )


    def test_F7(self):
        self.process_inversions(
            name = 'F7',
            notes = ['F4', 'A4', 'C5', 'Eb5'],
            root = 'F',
            third = 'A',
            fifth = 'C',
            seventh = 'Eb',
            dominant = True,
            major = True
        )


    def test_FM7(self):
        self.process_inversions(
            name = 'FM7',
            notes = ['F4', 'A4', 'C5', 'E5'],
            root = 'F',
            third = 'A',
            fifth = 'C',
            seventh = 'E',
            dominant = False,
            major = True
        )


    def test_Fm7(self):
        self.process_inversions(
            name = 'Fm7',
            notes = ['F4', 'Ab4', 'C5', 'Eb5'],
            root = 'F',
            third = 'Ab',
            fifth = 'C',
            seventh = 'Eb',
            dominant = False,
            major = False
        )


    def test_G7(self):
        self.process_inversions(
            name = 'G7',
            notes = ['G4', 'B4', 'D5', 'F5'],
            root = 'G',
            third = 'B',
            fifth = 'D',
            seventh = 'F',
            dominant = True,
            major = True
        )


    def test_GM7(self):
        self.process_inversions(
            name = 'GM7',
            notes = ['G4', 'B4', 'D5', 'F#5'],
            root = 'G',
            third = 'B',
            fifth = 'D',
            seventh = 'F#',
            dominant = False,
            major = True
        )


    def test_Gm7(self):
        self.process_inversions(
            name = 'Gm7',
            notes = ['G4', 'Bb4', 'D5', 'F5'],
            root = 'G',
            third = 'Bb',
            fifth = 'D',
            seventh = 'F',
            dominant = False,
            major = False
        )


    def test_A7(self):
        self.process_inversions(
            name = 'A7',
            notes = ['A4', 'C#5', 'E5', 'G5'],
            root = 'A',
            third = 'C#',
            fifth = 'E',
            seventh = 'G',
            dominant = True,
            major = True
        )


    def test_AM7(self):
        self.process_inversions(
            name = 'AM7',
            notes = ['A4', 'C#5', 'E5', 'G#5'],
            root = 'A',
            third = 'C#',
            fifth = 'E',
            seventh = 'G#',
            dominant = False,
            major = True
        )


    def test_Am7(self):
        self.process_inversions(
            name = 'Am7',
            notes = ['A4', 'C5', 'E5', 'G5'],
            root = 'A',
            third = 'C',
            fifth = 'E',
            seventh = 'G',
            dominant = False,
            major = False
        )


    def test_B7(self):
        self.process_inversions(
            name = 'B7',
            notes = ['B3', 'D#4', 'F#4', 'A4'],
            root = 'B',
            third = 'D#',
            fifth = 'F#',
            seventh = 'A',
            dominant = True,
            major = True
        )


    def test_BM7(self):
        self.process_inversions(
            name = 'BM7',
            notes = ['B3', 'D#4', 'F#4', 'A#4'],
            root = 'B',
            third = 'D#',
            fifth = 'F#',
            seventh = 'A#',
            dominant = False,
            major = True
        )


    def test_Bm7(self):
        self.process_inversions(
            name = 'Bm7',
            notes = ['B3', 'D4', 'F#4', 'A4'],
            root = 'B',
            third = 'D',
            fifth = 'F#',
            seventh = 'A',
            dominant = False,
            major = False
        )
