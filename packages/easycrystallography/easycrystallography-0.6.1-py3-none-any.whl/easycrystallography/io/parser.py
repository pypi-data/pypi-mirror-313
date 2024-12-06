# SPDX-FileCopyrightText: 2024 EasyCrystallography contributors
# SPDX-License-Identifier: BSD-3-Clause
# © 2022-2024 Contributors to the EasyCrystallography project <https://github.com/EasyScience/EasyCrystallography>

from .cif_parser import CifFileParser
from .cif_parser import CifStringParser


class Parsers:
    _parsers = {'cif_str': CifStringParser, 'cif': CifFileParser}

    def __init__(self, parser_choice: str, *args, **kwargs):
        self._setup_parser(parser_choice, *args, **kwargs)

    def _setup_parser(self, parser_choice, *args, **kwargs):
        try:
            p = self._parsers.get(parser_choice)
        except KeyError:
            raise KeyError(f"The parser '{parser_choice}' is not a known parser")
        self._parser = p(*args, **kwargs)

    def writer(self, *args, **kwargs):
        return self._parser.writer(*args, **kwargs)

    def reader(self, *args, **kwargs):
        return self._parser.reader(*args, **kwargs)

    @property
    def parsers(self):
        return list(self._parsers.keys())

    @property
    def parser(self):
        return self._parser

    def set_parser(self, new_parser, *args, **kwargs):
        self._setup_parser(new_parser, *args, **kwargs)
