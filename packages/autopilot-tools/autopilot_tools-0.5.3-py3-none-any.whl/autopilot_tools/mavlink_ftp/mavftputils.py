#!/usr/bin/env python3
from __future__ import annotations

import os
import struct
from dataclasses import dataclass, field
from datetime import datetime
from enum import auto, IntEnum
from itertools import chain
from typing import Type, TypeVar, Sequence, NamedTuple, cast, List, Callable

from pymavlink.dialects.v20.ardupilotmega import MAVLink_file_transfer_protocol_message
from pymavlink.mavutil import mavfile

from ..mavlink_ftp.ftp_filesystem import DataChunk, File, Folder
from ..exceptions import MavlinkTimeoutError, NoSessionsAvailable, UnknownError
from ..utils import retry_command

T = TypeVar('T')


DATA_SIZE = 239
HEADER_SIZE = 12
STRUCT_SIZE = DATA_SIZE + HEADER_SIZE
MAX_FAILS = 5


class MavFtpMessage(NamedTuple):
    seq_number: int
    session: int
    opcode: OpCodes
    size: int
    req_opcode: int
    burst_complete: int
    padding: int
    offset: int
    data: bytes

    @classmethod
    def pack(cls: Type[MavFtpMessage], data: Sequence[int, ...]) -> MavFtpMessage:
        return cls(*(
            struct.unpack('<HBBBBBBI', struct.pack(f'<{HEADER_SIZE}B', *data[:HEADER_SIZE])) +
            (struct.pack(f'<{DATA_SIZE}B', *data[HEADER_SIZE:]),)
        ))

    def unpack(self) -> Sequence[int, ...]:
        header = self[:-1]  # pylint: disable=unsubscriptable-object
        # self being a subclass of NamedTuple is VERY much subscriptable
        return (
            struct.unpack(f'<{HEADER_SIZE}B', struct.pack('<HBBBBBBI', *map(int, header))) +
            struct.unpack(f'<{DATA_SIZE}B', self.data)
        )


class OpCodes(IntEnum):
    None_ = 0
    TerminateSession = auto()
    ResetSessions = auto()
    ListDirectory = auto()
    OpenFileRO = auto()
    ReadFile = auto()
    CreateFile = auto()
    WriteFile = auto()
    RemoveFile = auto()
    CreateDirectory = auto()
    RemoveDirectory = auto()
    OpenFileWO = auto()
    TruncateFile = auto()
    Rename = auto()
    CalcFileCRC32 = auto()
    BurstReadFile = auto()
    ACK = 128
    NAK = 129


class Errors(IntEnum):
    None_ = 0
    Fail = auto()
    FailErrno = auto()
    InvalidDataSize = auto()
    InvalidSession = auto()
    NoSessionsAvailable = auto()
    EOF = auto()
    UnknownCommand = auto()
    FileExists = auto()
    FileProtected = auto()
    FileNotFound = auto()


@dataclass
class MavFTP:
    master: mavfile
    _seq_n: int = field(default=0, init=False)

    def get_file(self, path: str) -> File:
        pass

    def get_folder(self, path: str) -> Folder:
        base_path, name = os.path.split(path)
        folder = Folder(path=base_path, name=name)
        folder.connect(self)
        folder.materialize()
        return folder

    def get_last_log(self, log_folder: str, criterion: Callable[[File], int] =
                     lambda x: datetime.strptime(
                        f'{os.path.split(x.path)[1]} {os.path.splitext(x.name)[0]}',
                        '%Y-%m-%d %H_%M_%S')) -> File:

        f = self.get_folder(log_folder)
        files = [
            x.children.values() if isinstance(x, Folder) else [x] for x in f.children.values()
        ]
        files: List[File] = list(chain(*files))
        files = sorted(files, key=criterion)
        return files[-1]

    def burst_read_file(self, start: int = 0, end: int = -1) -> list[DataChunk] | None:
        there_is_more = True

        self.master.mav.file_transfer_protocol_send(
            0, self.master.target_system, self.master.target_component,
            MavFtpMessage(
                seq_number=self._seq_n,
                session=0,
                offset=start,
                opcode=OpCodes.BurstReadFile,
                size=4,
                req_opcode=0,
                burst_complete=0,
                padding=0,
                data=struct.pack('<I', end-start).ljust(DATA_SIZE, b'\0')
            ).unpack()
        )
        files = []
        fail_count = 0

        while there_is_more:
            chunk = self.master.recv_match(
                type='FILE_TRANSFER_PROTOCOL', blocking=True, timeout=1)
            if fail_count == MAX_FAILS:
                raise MavlinkTimeoutError

            if chunk is None:
                fail_count += 1
                continue
            fail_count = 0

            chunk = MavFtpMessage.pack(chunk.payload)
            if chunk.req_opcode != OpCodes.BurstReadFile:
                continue

            if not((chunk.opcode == OpCodes.NAK and chunk.size == 1
                    and chunk.data[0] == Errors.EOF)):
                files.append(DataChunk(
                    offset=chunk.offset,
                    length=chunk.size,
                    data=chunk.data[:chunk.size],
                ))
            else:
                there_is_more = False
            if chunk.burst_complete == 1:
                there_is_more = False

        self._seq_n += 1
        return files

    def list_directory(self, path: str) -> list:
        there_is_more = True
        offset = 0
        self._seq_n = 0

        result = []

        while there_is_more:

            def get_chunk() -> MAVLink_file_transfer_protocol_message:
                self.master.mav.file_transfer_protocol_send(
                    0, self.master.target_system, self.master.target_component,
                    MavFtpMessage(
                        seq_number=self._seq_n,
                        session=0,
                        offset=offset,
                        opcode=OpCodes.ListDirectory,
                        size=len(path),
                        req_opcode=0,
                        burst_complete=0,
                        padding=0,
                        data=path.encode('ASCII').ljust(DATA_SIZE, b'\0')
                    ).unpack()
                )
                return self.master.recv_match(
                    type='FILE_TRANSFER_PROTOCOL', blocking=True, timeout=0.5)

            self._seq_n += 1
            res = retry_command(get_chunk)
            if res is None:
                raise MavlinkTimeoutError

            payload = MavFtpMessage.pack(res.payload)

            if payload.opcode == OpCodes.ACK:
                result += [payload.data[:payload.size].decode('ASCII').strip('\0').split('\0')]

            if payload.opcode == OpCodes.NAK:
                MavFTP._check_for_common_mavlink_errors(payload)
                if payload.data[0] == Errors.EOF:
                    there_is_more = False
                else:
                    raise UnknownError(payload)

            offset += len(result[-1])

        root = []

        for line in chain(*result):
            if line.startswith('F'):
                name, size = line[1:].split('\t')
                root.append({'type': 'file', 'name': name, 'size': int(size)})
            elif line.startswith('D'):
                root.append({'type': 'dir', 'name': line[1:]})

        self._seq_n = 0

        return root

    def terminate_session(self):
        self.master.mav.file_transfer_protocol_send(
            0, self.master.target_system, self.master.target_component,
            MavFtpMessage(
                seq_number=self._seq_n,
                session=0,
                offset=0,
                opcode=OpCodes.TerminateSession,
                size=0,
                req_opcode=0,
                burst_complete=0,
                padding=0,
                data=bytes(DATA_SIZE)
            ).unpack()
        )

    def open_file_ro(self, path: str) -> int:
        """
        Opens file at path
        Returns size of file
        """
        def read_file() -> MAVLink_file_transfer_protocol_message:
            self.master.mav.file_transfer_protocol_send(
                0, self.master.target_system, self.master.target_component,
                MavFtpMessage(
                    seq_number=0,
                    session=0,
                    offset=0,
                    opcode=OpCodes.OpenFileRO,
                    size=len(path),
                    req_opcode=0,
                    burst_complete=0,
                    padding=0,
                    data=path.encode('ASCII').ljust(DATA_SIZE, b'\0')
                ).unpack()
            )

            return self.master.recv_match(type='FILE_TRANSFER_PROTOCOL', blocking=True, timeout=0.5)
        # maybe even make this a decorator, should be fun
        res = retry_command(read_file)
        self._seq_n = 2
        if res is None:
            raise MavlinkTimeoutError
        payload = MavFtpMessage.pack(res.payload)
        MavFTP._check_for_common_mavlink_errors(payload)
        return struct.unpack('<I', payload.data[:4])[0]

    def mkdir(self, path, name):
        pass

    def touch(self, path, name):
        pass

    def rm(self, path, name):
        pass

    @staticmethod
    def _check_for_common_mavlink_errors(payload: MavFtpMessage):
        exc = {
            Errors.FileNotFound: FileNotFoundError,
            Errors.FileProtected: PermissionError,
            Errors.NoSessionsAvailable: NoSessionsAvailable,
        }.get(cast(Errors, payload.data[0]))
        if exc is None:
            return
        raise exc
