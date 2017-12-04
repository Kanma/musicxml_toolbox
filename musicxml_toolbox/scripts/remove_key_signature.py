import argparse
from ..musicxml import Score


def main(args=None):

    # Command-line parsing
    parser = argparse.ArgumentParser(
        description='''Remove the key signatures found in a MusicXML file, and ensure
                       that all accidentals are correctly displayed'''
    )

    parser.add_argument('--part', type=str,
                        help='''The name of the part to process (by default, all parts
                                are processed)'''
    )

    parser.add_argument('src_file', type=str, help='Path to the input MusicXML file')
    parser.add_argument('dst_file', type=str, help='Path to the output MusicXML file')

    args = parser.parse_args(args)


    # Processing of the file
    score = Score()
    score.load(args.src_file)

    if args.part is not None:
        part = score.partByName(args.part)
        if part is None:
            print('Part not found: %s' % args.part)
            return 1

        part.removeKeySignature()

    else:
        for part in score.parts:
            part.removeKeySignature()

    score.save(args.dst_file)

    return 0



if __name__ == '__main__':
    main()
