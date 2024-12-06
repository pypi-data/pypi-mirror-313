#!/usr/bin/env python3
# This program is free software under the GNU General Public License v3.
# See <https://www.gnu.org/licenses/> for details.
# Author: Yuriy <1budsmoker1@gmail.com>
from __future__ import annotations

import logging
import os
from dataclasses import dataclass, field
from functools import partial

from typing import TYPE_CHECKING
from tqdm import tqdm
from ..utils import retry_command

if TYPE_CHECKING:
    from mavftputils import MavFTP

logger = logging.getLogger(__name__)

@dataclass
class Chunk:
    offset: int
    length: int

    @property
    def end(self):
        return self.length + self.offset


@dataclass
class DataChunk(Chunk):
    data: bytes


@dataclass
class FSNode:
    name: str
    path: str = field(default='')

    _ftp_connection: MavFTP = field(init=False, default=None, repr=False)

    @property
    def full_path(self):
        return os.path.join(self.path, self.name)

    def materialize(self):
        pass

    def connect(self, connection: MavFTP):
        self._ftp_connection = connection


@dataclass
class Folder(FSNode):
    _children: dict[str, FSNode] = field(init=False, default=None)

    @property
    def children(self):
        if self._children is None:
            self._children = {}
            self.materialize()
            return self._children
        return self._children

    def add_child_node(self, node: FSNode):
        self.children[node.name] = node
        node.path = self.full_path
        node.connect(self._ftp_connection)

    def materialize(self):
        ls = self._ftp_connection.list_directory(self.full_path)
        for item in ls:
            if item['type'] == 'dir':
                self.add_child_node(Folder(name=item['name']))
            elif item['type'] == 'file':
                self.add_child_node(File(name=item['name'], size=item['size']))

    def mkdir(self, name):
        self.children[name] = Folder(
            path=self.full_path,
            name=name
        )

        self._ftp_connection.mkdir(self.full_path, name)

    def touch(self, name):
        self.children[name] = File(
            path=self.full_path,
            name=name
        )
        self._ftp_connection.touch(self.full_path, name)

    def rm(self, name):
        self.children.pop(name)
        self._ftp_connection.rm(self.full_path, name)


@dataclass
class File(FSNode):
    size: int = field(default=-1)
    data: bytes = field(default=b'')

    def materialize(self):
        self._ftp_connection.open_file_ro(self.full_path)
        chunk_list: list[DataChunk] = []
        missing = File._find_missing_chunks(chunk_list, 0, self.size)

        pbar = None
        if logger.level < logging.INFO:
            pbar = tqdm(total=self.size)

        while missing:
            missing_chunk = missing.pop()
            data = retry_command(partial(
                self._ftp_connection.burst_read_file,
                missing_chunk.offset, missing_chunk.end)
            )
            if data is None:
                raise OSError(f"Unable to read file {self.name} at {self.path}")
            chunk_list += data

            missing += File._find_missing_chunks(
                data, missing_chunk.offset, missing_chunk.end
            )

            if logger.level < logging.INFO:
                pbar.update(sum(x.length for x in data))

        self._ftp_connection.terminate_session()
        self.data = b''.join([x.data for x in chunk_list])

        if logger.level < logging.INFO:
            pbar.close()

    def save_locally(self, path: str):
        with open(path, 'wb') as f:
            f.write(self.data)

    @staticmethod
    def _find_missing_chunks(chunk_list: list[DataChunk], start: int, end: int) -> list[Chunk]:
        missing: list[Chunk] = []
        last_chunk = Chunk(offset=start, length=0)
        missing_detected = True
        for chunk in chunk_list:
            if missing_detected:
                missing_detected = False
            elif last_chunk.offset + last_chunk.length != chunk.offset:
                missing.append(Chunk(
                    offset=last_chunk.end,
                    length=chunk.offset - last_chunk.end
                ))
                missing_detected = True
            last_chunk = chunk

        if last_chunk.offset + last_chunk.length < end:
            missing.append(Chunk(
                offset=last_chunk.end,
                length=end-last_chunk.end
            ))
        return missing
