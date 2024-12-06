# ruff: noqa
# SPDX-FileCopyrightText: 2024 EasyCrystallography contributors
# SPDX-License-Identifier: BSD-3-Clause
# © 2022-2024 Contributors to the EasyCrystallography project <https://github.com/EasyScience/EasyCrystallography>

from typing import List
from typing import Optional
from typing import Union

from gemmi import cif

from .cif import *
from .template import AbstractStructureParser
from .template import AbstractStructureReader
from .template import AbstractStructureWriter


class CifFileReader(AbstractStructureReader):
    """
    Reads a structure from a CIF file.
    """

    def __init__(self, filename: str) -> None:
        """
        Initializes the CIF structure reader.

        :param filename: The filename of the CIF file.
        """
        self.file_path = filename
        self._handle = None
        self._document = cif.read(filename)

    def __exit__(self, *args, **kwargs):
        self._document = None

    def _block_finder(self, block_name):
        if block_name is None:
            block = self._document.sole_block()
        elif block_name == -1:
            block = self._document
        else:
            block = self._document.find_block(block_name)
        if block is None:
            raise AttributeError(f"Block '{block_name}' not found in {self.file_path}")
        return block

    def lattice(self, data_name: Optional[str] = None):
        block = self._block_finder(data_name)
        return self.read(block, Lattice().CLASS_READER)

    def atom_sites(self, data_name: Optional[str] = None):
        block = self._block_finder(data_name)
        return self.read(block, Atoms().CLASS_READER)

    def atom_site_aniso(self, data_name: Optional[str] = None):
        pass

    def atom_site_sus(self, data_name: Optional[str] = None):
        pass

    def symmetry(self, data_name: Optional[str] = None):
        block = self._block_finder(data_name)
        return self.read(block, SpaceGroup().CLASS_READER)

    def structure(self, data_name: Optional[str] = None, phase_class: Optional = None):
        block = self._block_finder(data_name)
        if phase_class is None:
            from easycrystallography.Structures.Phase import Phase as phase_class
        components = {'cell': Lattice, 'spacegroup': SpaceGroup, 'atoms': Atoms}
        kwargs = {'name': block.name}
        for key, value in components.items():
            kwargs[key] = self.read(block, value().CLASS_READER)
        return phase_class(**kwargs)

    def structures(self, phases_class: Optional = None, phase_class: Optional = None):
        if phase_class is None:
            from easycrystallography.Structures.Phase import Phase as phase_class
        if phases_class is None:
            from easycrystallography.Structures.Phase import Phases as phases_class
        components = {'cell': Lattice, 'spacegroup': SpaceGroup, 'atoms': Atoms}
        phases = []
        document = self._block_finder(-1)
        for block in document:
            kwargs = {'name': block.name}
            for key, value in components.items():
                kwargs[key] = self.read(block, value().CLASS_READER)
            phases.append(phase_class(**kwargs))
        return phases_class('from_cif', *phases)

    def read(self, in_str: str, reader_class):
        """
        Reads the CIF structure.

        :return: The CIF structure.
        """
        return reader_class(in_str)


class CifFileWriter(AbstractStructureWriter):
    """
    Writes a structure to a CIF file.
    """

    def __init__(self, filename: str, data_name: Optional[Union[str, List[str]]] = None, raw='w') -> None:
        """
        Initializes the CIF structure writer.

        :param filename: The filename of the CIF file.
        """
        self.filename = filename
        self.file = open(filename, raw)
        self.document = cif.Document()
        if isinstance(data_name, str):
            data_name = [data_name]
        self.data_name = data_name
        if self.data_name is None:
            self.data_name = []
        self.blocks = [self.document.add_new_block(name) for name in self.data_name]

    def __exit__(self, exc_type, exc_val, exc_tb):
        with self.file as w:
            w.write(self.document.as_string(cif.Style.Simple))

    def write(self, structure, writer_class, *args, **kwargs):
        """
        Writes the CIF structure.

        :param structure: The CIF structure.
        """
        return writer_class(structure, *args, **kwargs)

    def get_data_block(self, data_name: Optional[str] = None):
        if data_name is None:
            if len(self.document) == 0:
                data_name = 'data'
            else:
                data_name = self.document[0].name
        if data_name not in self.data_name:
            self.data_name.append(data_name)
            self.blocks.append(self.document.add_new_block(data_name))
        return self.document[self.data_name.index(data_name)]

    def lattice(self, obj, data_name: Optional[str] = None):
        block = self.get_data_block(data_name)
        return self.write(obj, Lattice().CLASS_WRITER, block)

    def atom_sites(self, obj, data_name: Optional[str] = None):
        block = self.get_data_block(data_name)
        return self.write(obj, Atoms().CLASS_WRITER, block)

    def atom_site_aniso(self, obj):
        pass

    def atom_site_sus(self, obj):
        pass

    def symmetry(self, obj, data_name: Optional[str] = None):
        block = self.get_data_block(data_name)
        return self.write(obj, SpaceGroup().CLASS_WRITER, block)

    def structure(self, obj, data_name: Optional[str] = None):
        if data_name is None:
            data_name = obj.name
        block = self.get_data_block(data_name)
        components = {'cell': Lattice, 'spacegroup': SpaceGroup, 'atoms': Atoms}
        for key, value in components.items():
            self.write(getattr(obj, key), value().CLASS_WRITER, block)

    def structures(self, objs):
        components = {'cell': Lattice, 'spacegroup': SpaceGroup, 'atoms': Atoms}
        for obj in objs:
            data_name = obj.name
            block = self.get_data_block(data_name)
            for key, value in components.items():
                self.write(getattr(obj, key), value().CLASS_WRITER, block)


class CifStringReader(AbstractStructureReader):
    """
    Reads a structure from a CIF String.
    """

    def __init__(self) -> None:
        """
        Initializes the CIF structure reader.

        """
        self._handle = None

    def __exit__(self, *args, **kwargs):
        pass

    def lattice(self, in_str):
        return self.read(in_str, Lattice().STRING_READER)

    def atom_sites(self, in_str):
        return self.read(in_str, Atoms().STRING_READER)

    def atom_site_aniso(self, in_str):
        pass

    def atom_site_sus(self, in_str):
        pass

    def symmetry(self, in_str):
        return self.read(in_str, SpaceGroup().STRING_READER)

    def structure(
        self,
        in_str: Optional[str] = None,
        block_name: Optional[str] = None,
        phase_class: Optional = None,
    ):
        if phase_class is None:
            from easycrystallography.Structures.Phase import Phase as phase_class
        components = {'cell': Lattice, 'spacegroup': SpaceGroup, 'atoms': Atoms}
        document = cif.read_string(in_str)
        data_names = [block.name for block in document]
        idx = 0
        if block_name is not None:
            if block_name in data_names:
                idx = data_names.index(block_name)
            else:
                raise ValueError('Block name not found')
        block = document[idx]
        kwargs = {'name': block.name}
        for key, value in components.items():
            kwargs[key] = self.read(in_str, value().STRING_READER)[idx]
        return phase_class(**kwargs)

    def structures(self, document, phase_class: Optional = None):
        from easycrystallography.Structures.Phase import Phases

        if phase_class is None:
            from easycrystallography.Structures.Phase import Phase as phase_class
        components = {'cell': Lattice, 'spacegroup': SpaceGroup, 'atoms': Atoms}
        phases = []
        document = cif.read_string(document)
        for block in document:
            kwargs = {'name': block.name}
            for key, value in components.items():
                kwargs[key] = self.read(block, value().CLASS_READER)
            phases.append(phase_class(**kwargs))
        return Phases('from_cif', *phases)

    def read(self, in_str: str, reader_class):
        """
        Reads the CIF structure.

        :return: The CIF structure.
        """
        return reader_class(in_str)


class CifStringWriter(AbstractStructureWriter):
    """
    Writes a structure to a CIF file.
    """

    def __init__(self) -> None:
        """
        Initializes the CIF structure writer.
        """
        self._handle = None

    def __exit__(self, *args, **kwargs):
        pass

    def lattice(self, obj) -> str:
        return self.write(obj, Lattice().STRING_WRITER)

    def atom_sites(self, obj):
        return self.write(obj, Atoms().STRING_WRITER)

    def atom_site_aniso(self, obj):
        pass

    def atom_site_sus(self, obj):
        pass

    def symmetry(self, obj) -> str:
        return self.write(obj, SpaceGroup().STRING_WRITER)

    def structure(self, obj, data_name: Optional[str] = None):
        d = cif.Document()
        if data_name is None:
            data_name = obj.name
        block = d.add_new_block(data_name)
        components = {'cell': Lattice, 'space_group': SpaceGroup, 'atoms': Atoms}
        for key, value in components.items():
            self.write(getattr(obj, key), value().CLASS_WRITER, block)
        return d.as_string(cif.Style.Simple)

    def structures(self, objs):
        components = {'cell': Lattice, 'space_group': SpaceGroup, 'atoms': Atoms}
        d = cif.Document()
        for obj in objs:
            data_name = obj.name
            block = d.add_new_block(data_name)
            for key, value in components.items():
                self.write(getattr(obj, key), value().CLASS_WRITER, block)
        return d.as_string(cif.Style.Simple)

    def write(self, structure, writer_class, *args, **kwargs) -> str:
        """
        Writes the CIF structure.

        :param structure: The CIF structure.
        """
        return writer_class(structure, *args, **kwargs)


class CifStringParser(AbstractStructureParser):
    def __init__(self):
        super(CifStringParser, self).__init__(CifStringReader, CifStringWriter)


class CifFileParser(AbstractStructureParser):
    def __init__(self):
        super(CifFileParser, self).__init__(CifFileReader, CifFileWriter)
