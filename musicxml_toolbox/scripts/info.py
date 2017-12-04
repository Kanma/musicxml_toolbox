import argparse
from ..musicxml import Score


def main(args=None):
    parser = argparse.ArgumentParser(description='Display informations about a MusicXML file')
    parser.add_argument('file', type=str, help='Path to the MusicXML file')

    args = parser.parse_args(args)

    score = Score()
    score.load(args.file)

    print('Nb measures: %d' % score.parts[0].nb_measures)
    print()

    print('Parts:')
    for index, score_part in enumerate(score.part_list.score_parts):
        part = score.parts[index]
        if part.nb_staves == 1:
            print('  - %s: %d staff' % (score_part.part_name, part.nb_staves))
        else:
            print('  - %s: %d staves' % (score_part.part_name, part.nb_staves))

    return 0



if __name__ == '__main__':
    main()
