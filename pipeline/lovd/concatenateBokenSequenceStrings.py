#!/usr/bin/env python

"""
Description:
    This file removes newlines if its mid sequence
"""

import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', help='Input LOVD file for ammendment.')
    parser.add_argument('-o', '--output', help='Ouput txt file result.')
    options = parser.parse_args()
    return options


def main():
    options = parse_args()
    f_in = open(options.input, 'r')
    f_out = open(options.output, 'w')

    appended = False
    line_out = ''
    for line in f_in:
        line = line.rstrip()
        c = line[-1]
        if c != '"':
            if line_out == '':
                line_out = line
            else:
                line_out += line
            appended = True
        else:
            if appended == True:
                line_out += line
            if line_out == '':
                f_out.write(line + '\n')
            else:
                f_out.write(line_out + '\n')
            appended = False
            line_out = ''

    f_in.close()
    f_out.close()


if __name__ == "__main__":
    main()
