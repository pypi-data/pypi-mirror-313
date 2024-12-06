# SPDX-FileCopyrightText: 2024 EasyCrystallography contributors
# SPDX-License-Identifier: BSD-3-Clause
# © 2022-2024 Contributors to the EasyCrystallography project <https://github.com/EasyScience/EasyCrystallography>

# from __future__ import annotations
#
# from typing import List, NoReturn, TYPE_CHECKING, ClassVar, Tuple, Dict
#
# from easyscience.Objects.ObjectClasses import B
# from easycrystallography.Structures.Phase import Phase as _Phase, Phases as _Phases
# from .template import CIF_Template, gemmi
# from . import *
#
#
# class Phase(CIF_Template):
#
#     def __init__(self, reference_class=_Phase):
#         super().__init__()
#         self._CIF_CLASS = reference_class
#
#     def from_cif_block(self, block: gemmi.cif.Block) -> B:
#         pass
#
#     def add_to_cif_block(self, obj: B, block: gemmi.cif.Block) -> NoReturn:
#         pass
#
#     def from_cif_string(self, cif_string: str) -> List[B]:
#         pass
#
