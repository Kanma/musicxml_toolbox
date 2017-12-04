import argparse
from ..musicxml import Score


def main(args=None):

    # Command-line parsing
    parser = argparse.ArgumentParser(
        description='Convert a MusicXML file in a Yousician-friendly format (for Piano)'
    )

    parser.add_argument('src_file', type=str, help='Path to the input MusicXML file')
    parser.add_argument('dst_file', type=str, help='Path to the output MusicXML file')

    args = parser.parse_args(args)


    # Processing of the file
    score = Score()
    score.load(args.src_file)

    piano_part = score.partByName('Piano')
    if piano_part is None:
        print('No piano part found')
        return -1

    piano_part.removeKeySignature()
    piano_part.annotateChords(staff=1)

    piano_part.addFingering(staff=1)
    if piano_part.nb_staves > 1:
        piano_part.addFingering(staff=2)

    score.expandRepeats()
    score.addEmptyMeasures(2)

    voice_score_part = score.part_list.find(name='Voice')
    if voice_score_part is not None:
        voice_score_part.midi_instrument = 25

    score.moveRehearsalsTo(piano_part)

    score.save(args.dst_file)

    return 0



if __name__ == '__main__':
    main()
