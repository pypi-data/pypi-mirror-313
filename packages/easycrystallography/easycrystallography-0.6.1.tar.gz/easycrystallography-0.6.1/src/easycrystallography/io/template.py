# SPDX-FileCopyrightText: 2024 EasyCrystallography contributors
# SPDX-License-Identifier: BSD-3-Clause
# © 2022-2024 Contributors to the EasyCrystallography project <https://github.com/EasyScience/EasyCrystallography>

from abc import abstractmethod
from contextlib import AbstractContextManager
from typing import List


class AbstractBase(AbstractContextManager):
    @abstractmethod
    def __init__(self, *args, **kwargs):
        pass

    @abstractmethod
    def __exit__(self, *args, **kwargs):
        pass

    @abstractmethod
    def lattice(self, obj):
        pass

    @abstractmethod
    def atom_sites(self, obj):
        pass

    @abstractmethod
    def atom_site_aniso(self, obj):
        pass

    @abstractmethod
    def atom_site_sus(self, obj):
        pass

    @abstractmethod
    def symmetry(self, obj):
        pass

    @abstractmethod
    def structure(self, obj):
        pass

    @abstractmethod
    def structures(self, obj):
        pass


class AbstractStructureReader(AbstractBase):
    """
    Abstract class for reading structures.
    """

    @abstractmethod
    def read(self, input, *args, **kwargs) -> List[str]:
        """
        Reads a structure from a file.

        :param filename: The filename to read from.
        :return: The structure.
        """
        pass


class AbstractStructureWriter(AbstractBase):
    """
    Abstract class for writing structures.
    """

    @abstractmethod
    def write(self, structure, *args, **kwargs) -> None:
        """
        Writes a structure to a file.

        :param structure: The structure to write.
        :param filename: The filename to write to.
        """
        pass


class AbstractStructureParser:
    def __init__(self, reading_context_class, writing_context_class):
        self._reading_context_class = reading_context_class
        self._writing_context_class = writing_context_class

    def writer(self, *args, **kwargs):
        return self._writing_context_class(*args, **kwargs)

    def reader(self, *args, **kwargs):
        return self._reading_context_class(*args, **kwargs)

    def open(self, *args, rw: str = 'r', **kwargs):
        if rw == 'r':
            return self.reader(*args, **kwargs)
        elif rw == 'w':
            return self.writer(*args, **kwargs)
        else:
            raise ValueError('rw must be either "r" or "w"')

    def __call__(self, *args, rw: str = 'r', **kwargs):
        return self.open(*args, rw=rw, **kwargs)
