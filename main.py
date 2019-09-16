#!/usr/bin/env python3

import argparse
import random


class Crypto(object):
    ACTIONS = [
        'enc',  # encrypt
        'dec',  # decrypt
    ]
    ALGORITHMS = [
        'sub',  # substitution
        'per',  # permutation
        'sca',  # scaling
    ]

    FIRST_CHAR = ' '
    LAST_CHAR = '~'

    def __init__(self):
        print('__init__(self)')
        parser = argparse.ArgumentParser()
        parser.add_argument('--input', '-i', default='sample.txt',
                            help='path to source file')
        parser.add_argument('--output', '-o', default='encrypted.txt',
                            help='path to resulting file(s)')
        parser.add_argument('--action', '-a', default=Crypto.ACTIONS[0],
                            help='action to perform', choices=Crypto.ACTIONS)
        parser.add_argument('--algorithm', '-l', default=Crypto.ALGORITHMS[0],
                            help='available encryption algorithms',
                            choices=Crypto.ALGORITHMS)
        parser.add_argument('--seed', '-s', default=0, type=int,
                            help='used for random generators')
        parser.add_argument('--key', '-k', default='',
                            help='used for scaling algorithm')
        args = parser.parse_args()

        self.input_file_name = args.input
        self.output_file_name = args.output
        self.key_file_name = args.key
        self.__input = ''
        self.__output = ''
        self.__key = ''
        self.__action = args.action
        self.__algorithm = args.algorithm
        self.__seed = args.seed

        with open(self.input_file_name) as f:
            self.__input = f.read()

        print(5)

    def run(self):
        print('run(self)')
        if self.__algorithm == Crypto.ALGORITHMS[0]:
            self.substitution()
        elif self.__algorithm == Crypto.ALGORITHMS[1]:
            self.permutation()
        elif self.__algorithm == Crypto.ALGORITHMS[2]:
            self.scaling()

        self.save_to_file()

    @staticmethod
    def get_alphabet():
        print('get_alphabet()')
        return [
            [chr(x)
                for x
                in range(ord(Crypto.FIRST_CHAR), ord(Crypto.LAST_CHAR) + 1)],
            {chr(x): x
                for x
                in range(ord(Crypto.FIRST_CHAR), ord(Crypto.LAST_CHAR) + 1)},
        ]

    def get_substitution_alphabet(self):
        print('get_substitution_alphabet(self)')
        [alpha, alpha_rev] = Crypto.get_alphabet()
        shuffled = alpha[:]

        self.reset_generator()
        random.shuffle(shuffled)

        return [
            {key: value for key, value in zip(alpha, shuffled)},
            {key: value for value, key in zip(alpha, shuffled)}
        ]

    def substitution(self):
        print('substitution(self)')
        alpha, alpha_rev = self.get_substitution_alphabet()
        if self.__action == Crypto.ACTIONS[0]:
            self.__output = ''.join([alpha[x] for x in self.__input])
        elif self.__action == Crypto.ACTIONS[1]:
            self.__output = ''.join([alpha_rev[x] for x in self.__input])
        else:
            self.__output = ''

    def permutation(self):
        print('permutation(self)')
        reference = list(range(len(self.__input)))
        self.reset_generator()
        random.shuffle(reference)

        if self.__action == Crypto.ACTIONS[0]:
            self.__output = ''.join([self.__input[x] for x in reference])
        elif self.__action == Crypto.ACTIONS[1]:
            self.__output = list(range(len(self.__input)))
            for x, char in zip(reference, self.__input):
                self.__output[x] = char
            self.__output = ''.join(self.__output)
        else:
            self.__output = ''

    def scaling(self):
        [alpha, alpha_rev] = Crypto.get_alphabet()
        self.__get_key()
        self.__output = []

        _min = ord(Crypto.FIRST_CHAR)
        _max = ord(Crypto.LAST_CHAR)
        _range = _max - _min + 1

        if self.__action == Crypto.ACTIONS[0]:
            for index, char in enumerate(self.__input):
                key_index = index % len(self.__key)
                char_code = ord(char) + alpha_rev[self.__key[key_index]] - _min
                char_code %= _range
                char_code += _min
                self.__output.append(chr(char_code))
            self.__output = ''.join(self.__output)
        elif self.__action == Crypto.ACTIONS[1]:
            for index, char in enumerate(self.__input):
                key_index = index % len(self.__key)
                char_code = ord(char) - alpha_rev[self.__key[key_index]] - _min
                char_code %= _range
                char_code += _min
                self.__output.append(chr(char_code))
            self.__output = ''.join(self.__output)
        else:
            self.__output = ''

    def __get_key(self):
        try:
            with open(self.key_file_name, 'r') as f:
                self.__key = f.read()
            if len(self.__key) == 0:
                raise FileNotFoundError
        except FileNotFoundError:
            raise argparse.ArgumentTypeError(
                    'key "{}" not found'.format(self.key_file_name))

    def save_to_file(self):
        print('save_to_file(self)')
        with open(self.output_file_name, 'w') as f:
            f.write(self.__output)

    def reset_generator(self):
        print('reset_generator(self)')
        random.seed(self.__seed)


if __name__ == "__main__":
    Crypto().run()
