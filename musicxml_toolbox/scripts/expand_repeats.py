import argparse
from ..musicxml import Score


def main(args=None):

    # Command-line parsing
    parser = argparse.ArgumentParser(
        description='Expand the repeats of a MusicXML file'
    )

    parser.add_argument('src_file', type=str, help='Path to the input MusicXML file')
    parser.add_argument('dst_file', type=str, help='Path to the output MusicXML file')

    args = parser.parse_args(args)


    # Processing of the file
    score = Score()
    score.load(args.src_file)

    score.expandRepeats()

    score.save(args.dst_file)

    return 0



if __name__ == '__main__':
    main()
