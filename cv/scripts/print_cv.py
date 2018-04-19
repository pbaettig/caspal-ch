#!/usr/bin/python

import sys
from time import sleep
from prettytable import PrettyTable
from collections import OrderedDict
from cv import cv_english
from sys import exit, argv
 
def stdout_write(s):
    sys.stdout.write(s)
    sys.stdout.flush()

def type_out(s, sleep_time=0.01):
    for c in s:
        stdout_write(c)
        if c.isalnum():
            sleep(sleep_time)
            sys.stdout.flush()
    sys.stdout.write('\n')
    

def main():
    tables = OrderedDict()


    for section, details in cv_english.items():
        table = PrettyTable(field_names=['key', 'value'])
        table.align['key'] = 'l'
        table.align['value'] = 'l'
        table.header = False
        table.border = False
        table.vrule = True
        table.print_empty = True
        table.left_padding_width = 0
        table.right_padding_width = 10
        for title, value in details.items():
            if not title.isspace():
                t = '\033[4m{}\033[0m'.format(title)
            else:
                t = title
            table.add_row([t, value])

        tables[section] = table

    tables['Personal Information'].right_padding_width = 16

    for section, table in tables.items():
        #if not section == 'Work Experience':
        #    continue
        rows = table.get_string().split('\n')
        rows.insert(0, '\n\033[1m*** {} ***\033[0m'.format(section))
        for row in rows:
            type_out(row)


if __name__ == '__main__':
    if len(argv) > 1:
        type_out('Nice try :-)')
        exit(1)

    try:
        main()
    except KeyboardInterrupt:
        sys.stdout.write('\033[0m')
        type_out('\nThank you for your consideration and have a nice day!', sleep_time=0.02)
        exit(0)
    except:
        exit(1)
    else:
        exit(0)
