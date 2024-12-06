# SPDX-FileCopyrightText: 2024 EasyCrystallography contributors
# SPDX-License-Identifier: BSD-3-Clause
# © 2022-2024 Contributors to the EasyCrystallography project <https://github.com/EasyScience/EasyCrystallography>

from __future__ import annotations

import textwrap
from collections.abc import MutableMapping
from math import floor
from math import log10
from numbers import Number
from typing import TYPE_CHECKING
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

import numpy as np
from easyscience.Utils.io.dict import DataDictSerializer
from easyscience.Utils.io.dict import DictSerializer
from easyscience.Utils.io.template import BaseEncoderDecoder
from gemmi import cif

if TYPE_CHECKING:
    from easyscience.Utils.typing import BV

_MAX_LEN = 160
_SEP = '.'


def _flatten_dict_gen(d, parent_key, sep):
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, MutableMapping):
            yield from flatten_dict(v, new_key, sep=sep).items()
        elif isinstance(v, list):
            yield (
                new_key,
                [value if not isinstance(value, MutableMapping) else flatten_dict(value, '', sep) for value in v],
            )
        else:
            yield new_key, v


def flatten_dict(d: MutableMapping, parent_key: str = '', sep: str = '.') -> dict:
    return dict(_flatten_dict_gen(d, parent_key, sep))


def _unflatten_dict(key, value, out, sep) -> dict:
    key, *rest = key.split(sep, 1)
    if rest:
        _unflatten_dict(rest[0], value, out.setdefault(key, {}), sep)
    else:
        v, e, f = CifSerializer.string_to_variable(value)
        out[key] = v
        if e is not None:
            out['error'] = e
        if f is not None and not f:
            out['fixed'] = f


def _unflatten_loop(loop: cif.Loop, out: dict, sep: str):
    loop_name = ''.join(p for p, *r in zip(*loop.tags) if all(p == c for c in r))
    labels = [lab[len(loop_name) :] for lab in loop.tags]
    out[loop_name] = []
    width = loop.width()
    length = loop.length()
    for idx in range(length):
        this_dict = {}
        for idx2 in range(width):
            _unflatten_dict(labels[idx2], loop.val(idx, idx2), this_dict, sep)
        out[loop_name].append(this_dict)
    return out


def unflatten_bock(block: cif.Block, sep: str) -> dict:
    # Note that all names start with "_", so start at index 1!
    inter_dict = {item.pair[0][1:]: item.pair[1] for item in block if item.loop is None}
    loops = [loop.loop for loop in block if loop.loop is not None]
    out_dict = {}
    for k, v in inter_dict.items():
        _unflatten_dict(k, v, out_dict, sep)
    for loop in loops:
        _unflatten_loop(loop, out_dict, sep)
    return out_dict


class CifSerializer(BaseEncoderDecoder):
    def encode(self, obj: BV, skip: Optional[List[str]] = None, data_only: bool = False) -> str:
        if skip is None:
            skip = []
        doc = cif.Document()
        encoder = DictSerializer
        if data_only:
            encoder = DataDictSerializer
        obj_dict = obj.encode(encoder=encoder, skip=skip, include_id=False)
        flattened_obj = flatten_dict(obj_dict, sep=_SEP)
        block = doc.add_new_block(str(obj._borg.map.convert_id_to_key(obj)))
        for k, v in flattened_obj.items():
            self._check_class(doc, block, k, v)
        return doc.as_string()

    @classmethod
    def decode(cls, data_str) -> Union[BV, Dict[str, BV]]:
        document = cif.read_string(data_str)
        out_dict = {}
        for i, block in enumerate(document):
            out_dict[block.name] = DictSerializer.decode(unflatten_bock(block, sep=_SEP))
        if len(document) == 1:
            out_dict = list(out_dict.values())[0]
        return out_dict

    def _check_class(self, document: cif.Document, block: cif.Block, key: str, value: Any):
        T_ = type(value)
        if issubclass(T_, bool):
            new_obj = '@bool.' + str(value)
            self._str_encoder(block, key, new_obj)
        elif issubclass(T_, list):
            if len(value) > 0:
                test_item = value[0]
                if not issubclass(type(test_item), dict):
                    raise NotImplementedError
                else:
                    names = list(test_item.keys())
                    self._list_encoder(block, key, value, names)
        elif issubclass(T_, (str, Number)):
            self._str_encoder(block, key, value)

    def _str_encoder(self, block: cif.Block, key: str, in_str: str):
        in_str = self.variable_to_string(in_str)
        if key[0] != '_':
            key = '_' + key
        block.set_pair(key, in_str)

    def _list_encoder(self, block: cif.Block, name: str, items: List, keys: List[str]):
        if name[0] != '_':
            name = '_' + name
        loop: cif.Loop = block.init_loop(name, keys)
        for item in items:
            if len(keys) == 1:
                loop.add_row([self.variable_to_string(item)])
            else:
                loop.add_row([self.variable_to_string(item.get(key)) for key in keys])

    def variable_to_string(self, value, fixed: Optional[bool] = None, error: Optional[float] = None) -> str:
        decimal_places = 8
        if isinstance(value, Number):
            try:
                if np.isinf(value):
                    return self.variable_to_string(str(value))
            except TypeError:
                print(type(value))
            if abs(value - int(value)) > 0.0:
                decimal_places = len(str(value).split('.')[1]) - 1
            initial_str = '{:.' + str(decimal_places) + 'f}'
            s = initial_str.format(round(value, decimal_places))
            if error is not None and not np.isclose(error, 0.0):
                xe_exp = int(floor(log10(error)))

                # uncertainty
                un_exp = xe_exp - decimal_places + 1
                un_int = round(error * 10 ** (-un_exp))

                # nominal value
                no_exp = un_exp
                no_int = round(value * 10 ** (-no_exp))

                # format - nom(unc)
                fmt = '%%.%df' % max(0, -no_exp)
                s = (fmt + '(%.0f)') % (
                    no_int * 10**no_exp,
                    un_int * 10 ** max(0, un_exp),
                )
        elif isinstance(value, str):
            s = '{:s}'.format(value)
        else:
            s = '{:s}'.format(str(value))
        if fixed is not None and not fixed and error is None:
            s += '()'
        return self._format_field(s)

    @staticmethod
    def string_to_variable(in_string: str):
        in_string = in_string.strip()
        if "'" in in_string:
            in_string = in_string.replace("'", '')
        if '"' in in_string:
            in_string = in_string.replace('"', '')
        fixed = None
        error = None
        tokens = in_string.split('(')
        try:
            value = float(tokens[0])
        except ValueError:
            value = tokens[0]
            if value[0] == '@':
                tokens = value[1:].split('.')
                cls = tokens[0]
                val = tokens[1]
                value = eval(cls)(val)  # noqa S307
            elif value == 'None':
                value = None
            return value, error, fixed
        if len(tokens) > 1:
            fixed = False
            if tokens[1][0] != ')':
                error = (10 ** -(len(f'{tokens[0]}'.split('.')[1]) - 1)) * int(tokens[1][:-1])
        return value, error, fixed

    @staticmethod
    def _format_field(v):
        v = v.__str__().strip()
        if len(v) > _MAX_LEN:
            return ';\n' + textwrap.fill(v, _MAX_LEN) + '\n;'
        # add quotes if necessary
        if v == '':
            return '""'
        if (' ' in v or v[0] == '_') and not (v[0] == "'" and v[-1] == "'") and not (v[0] == '"' and v[-1] == '"'):
            if "'" in v:
                q = '"'
            else:
                q = "'"
            v = q + v + q
        return v
