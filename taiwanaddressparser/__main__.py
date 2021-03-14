import argparse

import taiwanaddressparser


def parse(addresses, cut=False):
    result = []
    df = taiwanaddressparser.transform(addresses, cut=cut)

    for map_key in zip(df["省"], df["市"], df["区"], df["地址"]):
        place = map_key[3]
        if not isinstance(place, str):
            place = ''
        result.append('\t'.join([map_key[0], map_key[1], map_key[2], place]))
    return result


def main(**kwargs):
    lines = []
    with open(kwargs['input'], 'r', encoding='utf-8') as f:
        for line in f:
            lines.append(line.strip())

    print('{} lines in input'.format(len(lines)))
    cut = kwargs['cut'] if 'cut' in kwargs else False
    parsed = parse(lines, cut=cut)
    count = 0
    with open(kwargs['output'], 'w', encoding='utf-8') as f:
        for i, o in zip(lines, parsed):
            count += 1
            f.write(i + '\t' + o + '\n')
    print('{} lines in output'.format(count))


def run():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=str,
                        help='the input file path, file encode need utf-8.')
    parser.add_argument('-o', '--output', type=str, required=True,
                        help='the output file path.')
    parser.add_argument('-c', '--cut', action="store_true", help='use cut mode.')
    args = parser.parse_args()
    main(**vars(args))


if __name__ == '__main__':
    run()