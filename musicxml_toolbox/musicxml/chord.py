import music21

from .fingering import Fingering


class Chord(object):

    def __init__(self, first_note):
        self.notes = [first_note]
        self.rehearsal = None
        self.harmony = None
        self.m21_chord = None


    def addNote(self, note):
        self.notes.append(note)


    def saveTo(self, xml_parent):
        if self.rehearsal is not None:
            self.rehearsal.saveTo(xml_parent)

        if self.harmony is not None:
            self.harmony.saveTo(xml_parent)

        for note in self.notes:
            note.saveTo(xml_parent)


    @property
    def name(self):
        if self.isTriad:
            if self.isMajor:
                return self.root
            else:
                return self.root + 'm'

        elif self.isDominantSeventh:
            return self.root + '7'

        elif self.isSeventh:
            if self.isMajor:
                return self.root + 'M7'
            else:
                return self.root + 'm7'

        return None


    @property
    def note_names(self):
        return [ x.name for x in self.notes ]


    @property
    def fingering(self):
        if self.notes[0].fingering is not None:
            return [ x.fingering.finger for x in self.notes ]
        else:
            return None


    @fingering.setter
    def fingering(self, value):
        for index, finger in enumerate(value):
            self.notes[index].fingering = Fingering(finger=finger)


    @property
    def duration(self):
        return self.notes[0].duration


    @property
    def type(self):
        return self.notes[0].type


    @property
    def staff(self):
        return self.notes[0].staff


    @property
    def voice(self):
        return self.notes[0].voice


    @property
    def isTriad(self):
        return self._chord.isTriad()


    @property
    def isSeventh(self):
        return self._chord.isSeventh()


    @property
    def isDominantSeventh(self):
        return self._chord.isDominantSeventh()


    @property
    def isMajor(self):
        return (self._chord.quality == 'major')


    @property
    def root(self):
        return Chord._fromMusic21(self._chord.root().name)


    @property
    def third(self):
        return Chord._fromMusic21(self._chord.third.name)


    @property
    def fifth(self):
        return Chord._fromMusic21(self._chord.fifth.name)


    @property
    def seventh(self):
        return Chord._fromMusic21(self._chord.seventh.name)


    @property
    def _chord(self):
        if self.m21_chord is None:
            self.m21_chord = music21.chord.Chord(Chord._toMusic21(' '.join(self.note_names)))

        return self.m21_chord


    @staticmethod
    def _toMusic21(name):
        return name.replace('b', '-')


    @staticmethod
    def _fromMusic21(name):
        return name.replace('-', 'b')
