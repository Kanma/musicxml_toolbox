import argparse
from ..musicxml import Score


def main(args=None):

    # Command-line parsing
    parser = argparse.ArgumentParser(
        description='Simplify a MusicXML file, by replacing chords by their root note'
    )

    parser.add_argument('--staff', type=str,
                        help='''The staff to simplify, in the form: "part:staff" (by
                                default, all parts are processed)'''
    )

    parser.add_argument('src_file', type=str, help='Path to the input MusicXML file')
    parser.add_argument('dst_file', type=str, help='Path to the output MusicXML file')

    args = parser.parse_args(args)


    # Processing of the file
    score = Score()
    score.load(args.src_file)

    (parts, errors) = score.getPartsAndStaves(args.staff)
    if errors:
        for error in errors:
            print(error)
        return 1

    for part, staff in parts:
        part.replaceChords(staff=staff)

    score.save(args.dst_file)

    return 0



if __name__ == '__main__':
    main()
