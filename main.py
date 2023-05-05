from random import choices
import matplotlib.pyplot as plt
import argparse


file_name = 'names.txt'
name_start = dict()
name_mid = dict()
full_names = dict()


def get_pairs(text):
    pairs = []
    for i in range(len(text) - 1):
        pairs.append(text[i:i+2])
    return pairs


def insert_into_dict(text):
    global name_start, name_mid
    for pair in text:
        if pair[0] == '^':
            name_start[pair] = name_start.get(pair, 0) + 1
        else:
            name_mid[pair] = name_mid.get(pair, 0) + 1


def get_next_letter(letter):
    global name_mid
    possible = dict()
    for pair, count in name_mid.items():
        if letter == pair[0]:
            possible[pair] = count
    next_letter = choices(list(possible.keys()), weights=list(possible.values()))
    return next_letter[0][1]


def create_name():
    first_letter = choices(list(name_start.keys()), weights=list(name_start.values()))
    name = first_letter[0][1]
    next_letter = get_next_letter(name[-1])
    while next_letter != '$':
        name = name + next_letter
        next_letter = get_next_letter(name[-1])
    return name


def count_entries(dictionary):
    return sum(list(dictionary.values()))


def count_probabilities(dictionary):
    global bigrams_count
    x = []
    y = []
    for item, value in dictionary.items():
        x.append(item)
        y.append(value)
    return x, y


if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument('--plot', help='show graph of probabilities', action='store_true')
    args = parser.parse_args()

    with open(file=file_name, mode='r') as file:
        lines = file.readlines()
        for line in lines:
            line = '^' + line.strip() + '$'
            insert_into_dict(get_pairs(line))
    full_names.update(name_start)
    full_names.update(name_mid)
    bigrams_count = count_entries(full_names)
    print(create_name())
    x, y = count_probabilities(full_names)

    if args.plot:
        plt.plot(x, y)
        plt.show()
