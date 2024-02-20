"""Main module."""

import os
from argparse import Action, ArgumentParser

from elftools.elf.elffile import ELFFile
from elftools.elf.sections import SymbolTableSection


def enum_all_funcs(filename, verbose=False):
    funcs = []
    with open(filename, 'rb') as file:
        elffile = ELFFile(file)
        symbol_tables = [
            (idx, s)
            for idx, s in enumerate(elffile.iter_sections())
            if isinstance(s, SymbolTableSection)
        ]
        for idx, s in symbol_tables:
            for nsym, symbol in enumerate(s.iter_symbols()):
                if symbol['st_info']['type'] != 'STT_FUNC':
                    continue
                if verbose:
                    print('Found a function symbol', symbol.name)
                funcs.append(symbol.name)
    return funcs


def extract_func(filename, func, verbose=False):
    base, ext = os.path.splitext(filename)
    with open(filename, 'rb') as file:
        elffile = ELFFile(file)
        symbol_tables = [
            (idx, s)
            for idx, s in enumerate(elffile.iter_sections())
            if isinstance(s, SymbolTableSection)
        ]
        for idx, s in symbol_tables:
            syms = s.get_symbol_by_name(func)
            if not syms:
                continue
            symbol = syms[0]
            shndx = symbol['st_shndx']
            offset = symbol['st_value']
            size = symbol['st_size']
            text = elffile.get_section(shndx)
            if verbose:
                print('Extracting', func)
            with open(base + '.' + func + '.bin', 'wb') as f:
                f.write(text.data()[offset : offset + size])
            return
        print(func, 'is not found')


class ListAction(Action):
    """A list of argument"""

    def __call__(self, parser, namespace, values, option_string=None):
        if isinstance(values, list):
            values = values.split(',')
        v = getattr(namespace, self.dest)
        if v is not None:
            v.extend(values)
        else:
            v = values
        setattr(namespace, self.dest, v)


def main():
    parser = ArgumentParser(description='')
    parser.add_argument(
        '-f',
        '--func',
        dest='funcs',
        action=ListAction,
        help='Functions to be extracted, separated by comma',
    )
    parser.add_argument(
        '-v',
        '--verbose',
        dest='verbose',
        action='store_true',
        help='Enable verbose output',
    )
    parser.add_argument('file', nargs='+', help='ELF file to extract')

    args = parser.parse_args()

    for f in args.file:
        funcs = args.funcs
        if not funcs:
            funcs = enum_all_funcs(f, args.verbose)
        for fn in funcs:
            extract_func(f, fn, args.verbose)


if __name__ == '__main__':
    main()
