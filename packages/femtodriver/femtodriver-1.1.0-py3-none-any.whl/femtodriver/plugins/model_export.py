#  Copyright Femtosense 2024
#
#  By using this software package, you agree to abide by the terms and conditions
#  in the license agreement found at https://femtosense.ai/legal/eula/
#

from enum import IntEnum, unique
from os import path
import numpy as np
from dataclasses import dataclass
from typing import Any
from typing_extensions import Self

SPU001_MAX_FREQ: int = 300
SPU001_NUM_CORES: int = 2
MODEL_EXTENSION: str = ".femto"
FILE_MAGIC: str = "femtosense_model"
FILE_FORMAT_VERSION: int = 0x100
FILE_ENDIANNESS: str = "little"
FEMTODRIVER_VERSION: int = 0x100

FILE_HEADER_SIZE: int = 48
MODEL_CONFIG_SIZE: int = 128
MODEL_NAME_MAX_LENGTH: int = 16
SPU_CONFIG_SIZE: int = 80


@unique
class ModelType(IntEnum):
    """Status supported for SPU memory banks"""

    UNKNOWN = 0
    WWD = 10
    GSC = 20
    SLU = 30
    AINR = 40

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_

    @classmethod
    def _missing_(cls, value):
        return cls.UNKNOWN

    def __str__(self) -> str:
        match self.value:
            case self.WWD:
                return "Wakeword Detection"
            case self.GSC:
                return "Google Speech Commands"
            case self.SLU:
                return "Spoken Language Understanding"
            case self.AINR:
                return "AI Noise Reduction"
            case _:
                return "Unknown"

    @classmethod
    def str_to_type(cls, type: str):
        match type.upper():
            case "WWD":
                return cls.WWD
            case "GSC":
                return cls.GSC
            case "SLU":
                return cls.SLU
            case "AINR":
                return cls.AINR
            case _:
                return cls.UNKNOWN


@unique
class SpuPartNumber(IntEnum):
    """Supported SPU part numbers"""

    SPU001 = 1
    UNKNOWN = 255

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_

    @classmethod
    def _missing_(cls, value):
        return cls.UNKNOWN

    def __str__(self) -> str:
        if not self.has_value(self.value):
            return "SPU part number unknown"
        return self.name

    @classmethod
    def str_to_pn(cls, pn: str):
        match pn.upper():
            case "SPU001":
                return cls.SPU001
            case _:
                return cls.UNKNOWN


@unique
class CoreStatus(IntEnum):
    """SPU core status"""

    OFF = 0
    ON = 1
    SLEEPING = 2
    INVALID = 255

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_

    @classmethod
    def _missing_(cls, value):
        return cls.INVALID

    def __str__(self) -> str:
        if not self.has_value(self.value):
            return "SPU core status invalid"
        return self.name


@unique
class SpuVectorType(IntEnum):
    """Vector types supported by SPU"""

    INPUT = 0
    OUTPUT = 1
    COMMAND = 2
    INVALID = 255

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_

    @classmethod
    def _missing_(cls, value):
        return cls.INVALID

    def __str__(self) -> str:
        if not self.has_value(self.value):
            return "Vector type invalid"
        return self.name

    @classmethod
    def to_vector_type(cls, vec_type: Any):
        if isinstance(vec_type, str):
            match vec_type.lower():
                case "input":
                    return cls.INPUT
                case "output":
                    return cls.OUTPUT
                case "command":
                    return cls.COMMAND
                case _:
                    return cls.INVALID
        elif isinstance(vec_type, int):
            return cls(vec_type)
        else:
            return cls.INVALID


@unique
class MemoryState(IntEnum):
    """Model types supported by SPU"""

    OFF = 0
    DISABLED = 1
    SLEEPING = 2
    TRANSITIONING = 3
    ON = 4
    FSM = 5
    INVALID = 255

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_

    @classmethod
    def _missing_(cls, value):
        return cls.INVALID

    @classmethod
    def inactive_states(cls) -> list:
        return [MemoryState.DISABLED, MemoryState.INVALID, MemoryState.OFF]

    def __str__(self) -> str:
        if not self.has_value(self.value):
            return "Memory status invalid"
        return self.name


@unique
class MemoryType(IntEnum):
    """SPU001 memory bank types"""

    DM = 0
    TM = 0x20
    SB = 0x40
    RQ = 0x50
    PB = 0x60
    IM = 0x30
    INVALID = 255

    @classmethod
    def has_value(cls, value) -> bool:
        return value in cls._value2member_map_

    @classmethod
    def _missing_(cls, value):
        return cls.INVALID

    @classmethod
    def str_to_type(cls, type: str):
        match type.upper():
            case "DM":
                return cls.DM
            case "TM":
                return cls.TM
            case "SB":
                return cls.SB
            case "RQ":
                return cls.RQ
            case "PB":
                return cls.PB
            case "IM":
                return cls.IM
            case _:
                return cls.INVALID

    def __str__(self) -> str:
        if not self.has_value(self.value):
            return "SPU memory type invalid"
        return self.name

    @classmethod
    def static_memories(cls) -> list:
        return [MemoryType.SB, MemoryType.RQ, MemoryType.PB]


@dataclass
class SpuVector:
    """
    Class representing a data vector to exchange with SPU

    Attributes:
        id (int): vector identifier
        type (SpuVectorType): type of the vector
        size (int): number of words in int16
        target_core_id (int): target core when writing/reading the vector to/from SPU
        parameter (int): parameter to provide to SPU when writing the vector, or expected mailbox_id when reading from SPU
    """

    def __init__(
        self,
        id: int,
        vector_type: str,
        size: int,
        target_core_id: int,
        parameter: int,
    ) -> None:
        """
        Initializes a SpuVector object

        Args:
            id (int): vector identifier
            type (SpuVectorType): type of the vector
            size (int): number of words in int16
            target_core_id (int): target core when writing/reading the vector to/from SPU
            parameter (int): parameter to provide to SPU when writing the vector, or expected mailbox_id when reading from SPU
        Returns:
            None
        """
        self.id: int = id
        self.type: SpuVectorType = (
            SpuVectorType.to_vector_type(vector_type)
            if isinstance(vector_type, str)
            else vector_type
        )
        self.size: int = size
        self.target_core_id: int = target_core_id
        self.parameter: int = parameter

    def serialize(self) -> bytearray:
        """
        Serializes the SpuVector

        Args:
            None
        Returns:
            bytearray: object serialized into bytes
        """
        byte_buffer = bytearray()

        byte_buffer.extend(
            int.to_bytes(self.id, 1, byteorder=FILE_ENDIANNESS, signed=False)
        )
        byte_buffer.extend(
            int.to_bytes(self.type, 1, byteorder=FILE_ENDIANNESS, signed=False)
        )
        byte_buffer.extend(
            int.to_bytes(
                self.target_core_id, 1, byteorder=FILE_ENDIANNESS, signed=False
            )
        )
        byte_buffer.extend(
            int.to_bytes(self.size, 2, byteorder=FILE_ENDIANNESS, signed=False)
        )
        byte_buffer.extend(
            int.to_bytes(self.parameter, 4, byteorder=FILE_ENDIANNESS, signed=False)
        )
        return byte_buffer

    @classmethod
    def deserialize(cls, vector_bytes: bytearray, endianness: str):
        """
        Deserializes a byte array into a SpuVector object

        Args:
            vector_bytes (bytearray): byte array containing the vector serialized data
            endianness (str): byte order of the serialized data ("big" or "little")
        Return:
            SpuVector: deserialized vector object
        """
        id = int(vector_bytes[0])
        type = SpuVectorType(int(vector_bytes[1]))
        size = int(vector_bytes[2])
        target_core_id = int.from_bytes(
            vector_bytes[3:5],
            byteorder=endianness,
            signed=False,
        )

        parameter = int.from_bytes(
            vector_bytes[5:9], byteorder=endianness, signed=False
        )
        return cls(
            id=id,
            vector_type=type,
            size=size,
            target_core_id=target_core_id,
            parameter=parameter,
        )


@dataclass
class SpuSequence:
    """
    Class describing an exchange of SpuVectors sequence with SPU

    Attributes:
        id (int): SpuSequence identifier
        input_ids (list(int)): list of the input vector IDs in chronological order
        output_ids (list(int)): list of the outputs vectors IDs in chronological order
    """

    def __init__(
        self, id: int, input_ids: list[int] = None, output_ids: list[int] = None
    ) -> None:
        """
        Initializes a new SpuSequence object

        Args:
            id (int): SpuSequence identifier
            input_ids (list(int)): list of the input vector IDs in chronological order
            output_ids (list(int)): list of the outputs vectors IDs in chronological order
        Returns:
            None
        """
        self.id: int = id
        self.input_ids: list[int] = input_ids if input_ids is not None else []
        self.output_ids: list[int] = output_ids if output_ids is not None else []

    def serialize(self) -> bytearray:
        """
        Serializes the SpuSequence

        Args:
            None
        Returns:
            bytearray: object serialized into bytes
        """
        byte_buffer = bytearray()
        byte_buffer.extend(
            int.to_bytes(self.id, 1, byteorder=FILE_ENDIANNESS, signed=False)
        )
        for input in self.input_ids:
            byte_buffer.extend(
                int.to_bytes(input, 1, byteorder=FILE_ENDIANNESS, signed=False)
            )
        for output in self.output_ids:
            byte_buffer.extend(
                int.to_bytes(output, 1, byteorder=FILE_ENDIANNESS, signed=False)
            )
        return byte_buffer

    @classmethod
    def deserialize(cls, sequence_bytes: bytearray, endianness: str):
        """
        Deserializes a byte array into a SpuSequence object

        Args:
            sequence_bytes (bytearray): byte array containing the sequence serialized data
            endianness (str): byte order of the serialized data ("big" or "little")
        Return:
            SpuSequence: deserialized sequence object
        """
        id = int(sequence_bytes[0])
        input_ids = np.frombuffer(
            sequence_bytes[1:3],
            dtype=np.dtype(np.uint8).newbyteorder(
                "<" if endianness == "little" else ">"
            ),
        ).tolist()
        output_ids = np.frombuffer(
            sequence_bytes[3:5],
            dtype=np.dtype(np.uint8).newbyteorder(
                "<" if endianness == "little" else ">"
            ),
        ).tolist()
        return cls(id=id, input_ids=input_ids, output_ids=output_ids)


@dataclass
class ModelPage:
    """
    Class describing a page of the model. A page contains a subsection of the data store in one of SPU's memory bank

    Attributes:
        id (int): ModelPage identifier
        length (int): number of words (uint32) stored in the ModelPage
        address (int): start address to write the ModelPage in SPU memory
        data (list(int)): list of words (uint32) to be written in SPU memory
    """

    def __init__(
        self,
        id: int = -1,
        length: int = 0,
        address: int = 0,
        data: list[int] = None,
    ) -> None:
        """
        Initializes a new ModelPage object

        Args:
            id (int): ModelPage identifier
            length (int): number of words (uint32) stored in the ModelPage
            address (int): start address to write the ModelPage in SPU memory
            data (list(int)): list of words (uint32) to be written in SPU memory
        Returns:
            None
        """
        self.id: int = id
        self.length: int = length
        self.address: int = address
        self.data: list[int] = data if data is not None else []
        pass

    def serialize(self, chunk_size: int) -> bytearray:
        """
        Serializes the ModelPage

        Args:
            chunk_size (int): size to align the final serialize array
        Returns:
            bytearray: object serialized into bytes
        """
        assert chunk_size > 0
        byte_buffer = bytearray()
        byte_buffer.extend(
            int.to_bytes(self.id, 2, byteorder=FILE_ENDIANNESS, signed=False)
        )
        byte_buffer.extend(
            int.to_bytes(self.length, 2, byteorder=FILE_ENDIANNESS, signed=False)
        )
        byte_buffer.extend(
            int.to_bytes(self.address, 4, byteorder=FILE_ENDIANNESS, signed=False)
        )
        for d in self.data:
            byte_buffer.extend(
                int.to_bytes(int(d), 4, byteorder=FILE_ENDIANNESS, signed=False)
            )
        # Adding padding to reach a multiple of chunk_size
        while len(byte_buffer) % chunk_size != 0:
            byte_buffer.append(0xFF)
        return byte_buffer

    @classmethod
    def deserialize(cls, page_bytes: bytearray, endianness: str):
        """
        Deserializes a byte array into a ModelPage object

        Args:
            page_bytes (bytearray): byte array containing the model page serialized data
            endianness (str): byte order of the serialized data ("big" or "little")
        Return:
            ModelPage: object containing all page data
        """
        id = int.from_bytes(
            page_bytes[0:2],
            byteorder=endianness,
            signed=False,
        )
        length = int.from_bytes(
            page_bytes[2:4],
            byteorder=endianness,
            signed=False,
        )
        address = int.from_bytes(
            page_bytes[4:8],
            byteorder=endianness,
            signed=False,
        )
        data = np.frombuffer(
            page_bytes[8 : 8 + length * 4],
            dtype=np.dtype(np.uint32).newbyteorder(
                "<" if endianness == "little" else ">"
            ),
        ).tolist()
        return cls(id=id, length=length, address=address, data=data)


@dataclass
class MemoryBank:
    """
    Class describing an SPU internal memory bank

    Attributes:
        id (int): memory bank identifier
        type (MemoryType): type of memory bank
        state (MemoryState): state of the memory bank
        capacity (int): capacity of the memory bank in bytes
        page_count (int): number of ModelPages constituting the MemoryBank
        start_address (int): address of the first word of the MemoryBank
        data (list[int]): data stored in the memory bank
        pages (list(ModelPage)): list of ModelPages containing the MemoryBank data
    """

    def __init__(
        self,
        id: int,
        type: str,
        core_id: int,
        spu_pn: SpuPartNumber,
    ) -> None:
        """
        Initializes a new MemoryBank object

        Args:
                id (int): memory bank identifier
                type (MemoryType): type of memory bank
                core_id (int): identifier of the SpuCore in which the MemoryBank resides
                spu_pn (SpuPartNumber): part number of the SPU in which the MemoryBank resides
        Returns:
            None
        """
        self.id: int = id
        self.type: MemoryType = MemoryType.str_to_type(type)
        self.state: MemoryState = MemoryState.OFF
        self.capacity: int = self.get_memory_capacity(memory_type=type, spu_pn=spu_pn)
        self.page_count = 0
        self.start_address: int = self.get_memory_start_address(
            core_id=core_id, spu_pn=spu_pn
        )
        self.data: list[int] = []
        self.pages: list[ModelPage] = []

    def add_data(self, data: list[int]) -> None:
        """
        Adds data to the MemoryBank

        Args:
            data (list[int]): list of words (uint32) divided in arrays setting the page length
        Returns:
            None
        Raises:
            Exception: if the data added exceeds the capacity of the memory bank
        """
        if len(data) == 0:
            return

        self.state = MemoryState.FSM
        self.data.extend(data)

        # Make sure the data stored in the bank actually fits
        content_size = len(self.data) * 4
        if content_size > self.capacity:
            raise Exception(
                f"Trying to store more data than the bank can contain:"
                f"{content_size} bytes in {str(self.type)}{self.id} (capacity: {self.capacity})"
            )

    def is_unused(self) -> bool:
        """
        Indicates whether the MemoryBank is in an inactive state

        Args:
            None
        Returns:
            bool: true if the MemoryBank is inactive, false otherwise
        """
        return self.state in MemoryState.inactive_states()

    @staticmethod
    def get_memory_capacity(
        memory_type: str, spu_pn: SpuPartNumber = SpuPartNumber.SPU001
    ) -> int:
        """
        Provides the capacity of a memory bank based on the type of MemoryBank and the SPU part number

        Args:
            memory_type (str): type of the memory
            spu_pn (SpuPartNumber): part number of the SPU in which the MemoryBank resides
        Returns:
            int: capacity of the MemoryBank in bytes
        """
        if spu_pn is not SpuPartNumber.SPU001:
            return 0
        match MemoryType.str_to_type(memory_type):
            case MemoryType.DM:
                return 0x10000
            case MemoryType.TM:
                return 0x4000
            case MemoryType.SB | MemoryType.RQ | MemoryType.PB:
                return 0x0200
            case MemoryType.IM:
                return 0x8000
            case _:
                return 0

    def get_memory_start_address(self, spu_pn: SpuPartNumber, core_id: int) -> int:
        """
        Prodides the start address of the MemoryBank according to the SPU part number and the core ID

        Args:
            spu_pn (SpuPartNumber): part number of the SPU in which the MemoryBank resides
            core_id (int): identifier of the SpuCore in which the MemoryBank resides
        Returns:
            int: first address of the MemoryBank
        Raises:
            Exception: if the part number is not supported
            ValueError: if the memory type is invalid
        """
        if spu_pn is not SpuPartNumber.SPU001:
            raise Exception(f"SPU part number not supported: {str(spu_pn)}")

        if core_id >= SPU001_NUM_CORES:
            return 0xFFFFFF

        core_offset = 0x00100000 * (core_id + 1)
        match self.type:
            case MemoryType.DM:
                return core_offset + 0x10000 * self.id
            case MemoryType.TM:
                return core_offset + 0x80000 + self.id * 0x10000
            case MemoryType.SB:
                return core_offset + 0xC0000
            case MemoryType.RQ:
                return core_offset + 0xD0000
            case MemoryType.PB:
                return core_offset + 0xE0000
            case MemoryType.IM:
                return core_offset + 0xF0000
            case _:
                raise ValueError(f"Memory type invalid: {str(self.type)}")

    @classmethod
    def get_info_from_address(
        cls, spu_pn: SpuPartNumber, address: int
    ) -> tuple[MemoryType, int]:
        """
        Prodides the type of memory and bank ID from the address provided

        Args:
            spu_pn (SpuPartNumber): part number of the SPU in which the MemoryBank resides
            address (int): address in SPU memory
        Returns:
            tuple[MemoryType, int]: (memory_type, bank_id) corresponding to the address provided
        Raises:
            Exception: if the part number is not supported
        """
        if spu_pn is not SpuPartNumber.SPU001:
            raise Exception(f"SPU part number not supported: {str(spu_pn)}")

        mem_base = address & 0xFFFFF
        match mem_base:
            case addr if 0x0 <= addr <= 0x7FFFF:
                mem_type = MemoryType.DM
                bank_id = int(mem_base / 0x10000)
            case addr if 0x80000 <= addr <= 0xB3FFF:
                mem_type = MemoryType.TM
                bank_id = int((mem_base - 0x80000) / 0x10000)
            case addr if 0xC0000 <= addr <= 0xC01FF:
                mem_type = MemoryType.SB
                bank_id = 0
            case addr if 0xD0000 <= addr <= 0xD01FF:
                mem_type = MemoryType.RQ
                bank_id = 0
            case addr if 0xE0000 <= addr <= 0xE01FF:
                mem_type = MemoryType.PB
                bank_id = 0
            case addr if 0xF0000 <= addr <= 0xF7FFF:
                mem_type = MemoryType.IM
                bank_id = 0
            case _:
                mem_type = MemoryType.INVALID
                bank_id = 0xFF

        return (mem_type, bank_id)

    def _id_to_int(self) -> int:
        """
        Converts the MemoryBank (type, id) into a unique ID

        Args:
            None
        Returns:
            int: unique MemoryBank identifier
        """
        return self.type.value + self.id * 4

    def add_pages(self, start_page_id: int, data: list[np.ndarray[np.uint32]]) -> int:
        """
        Adds pages to the MemoryBank

        Args:
            start_page_id (int): identifier of the first ModelPage of the MemoryBank
            data (list(np.ndarrary[np.uint32])): list of words (uint32) divided in arrays setting the page length
        Returns:
            int: the number of pages added to the MemoryBank
        """
        if len(data) == 0:
            return 0

        self.state = MemoryState.FSM
        batch_page_count = 0
        page_address = (
            self.start_address if self.page_count == 0 else self.pages[-1].address + 4
        )
        self.page_count += len(data)
        for page in data:
            model_page = ModelPage(
                id=batch_page_count + start_page_id,
                length=len(page),
                address=page_address,
                data=page,
            )
            batch_page_count += 1
            page_address += len(page) * 4
            self.pages.append(model_page)

        # Make sure the data stored in the bank actually fits
        content_size = sum([page.length * 4 for page in self.pages])
        if content_size > self.capacity:
            raise Exception(
                f"Trying to store more data than the bank can contain:"
                f"{content_size} bytes in {str(self.type)}{self.id} (capacity: {self.capacity})"
            )
        return batch_page_count

    def generate_pages(self, page_size: int, start_page_id: int) -> int:
        """
        Generates pages from the data stored in the memory banks

        Args:
            page_size (int): number of uint32 words per page
            start_page_id (int): identifier of the first page
        Returns:
            int: number of pages created
        """
        return self.add_pages(
            start_page_id=start_page_id,
            data=[
                self.data[x : x + page_size]
                for x in range(0, len(self.data), page_size)
            ],
        )

    def serialize_data(self, chunk_size: int) -> bytearray:
        """
        Serializes the ModelPage data

        Args:
            chunk_size (int): size to align the final serialize array
        Returns:
            bytearray: data serialized into bytes
        """
        byte_buffer = bytearray()
        if self.page_count == 0:
            return bytearray()
        for page in self.pages:
            byte_buffer.extend(page.serialize(chunk_size=chunk_size))
        return byte_buffer

    def serialize_configuration(self) -> bytearray:
        """
        Serializes the MemoryBank configuration

        Args:
            None
        Returns:
            bytearray: configuration serialized into bytes
        """
        byte_buffer = bytearray()

        if self.type in MemoryType.static_memories():
            return byte_buffer

        byte_buffer.extend(
            int.to_bytes(self._id_to_int(), 1, byteorder=FILE_ENDIANNESS, signed=False)
        )
        byte_buffer.extend(
            int.to_bytes(self.state, 1, byteorder=FILE_ENDIANNESS, signed=False)
        )
        return byte_buffer


@dataclass
class SpuCore:
    """
    Class describing a SpuCore including its configuration and memory content

    Attributes:
        id (int): SpuCore identifier
        status (CoreStatus): status of the SpuCore
        memory_banks (dict[str, MemoryBank]): dictionary containing the MemoryBanks
                                              in a SpuCore given the Spu part number
    """

    def __init__(
        self, id: int, spu_pn: SpuPartNumber, status: CoreStatus = CoreStatus.OFF
    ) -> None:
        """
        Creates a new SpuCore object

        Args:
            id (int): SpuCore identifier
            spu_pn (SpuPartNumber): Spu part number
            status (CoreStatus): status of the SpuCore
        Returns:
            None
        """
        self.id: int = id
        self.status: CoreStatus = status
        self.memory_banks: dict[str, MemoryBank] = {}

        available_banks = self.get_available_memory_banks(spu_pn)
        for memory_type in available_banks:
            for bank_id in range(0, available_banks[memory_type]):
                self._add_memory(
                    memory_type=memory_type,
                    bank_id=bank_id,
                    spu_pn=spu_pn,
                )

    def _add_memory(
        self,
        memory_type: str,
        bank_id: int = 0,
        spu_pn: SpuPartNumber = SpuPartNumber.SPU001,
    ) -> None:
        """
        Adds a new MemoryBank to the SpuCore

        Args:
            memory_type (str): type of memory bank to add
            bank_id (int): memory bank identifier
            spu_pn (SpuPartNumber): SPU part number
        Returns:
            None
        """
        bank_key: str = (
            f"{memory_type}{bank_id}".upper()
            if memory_type in ["DM", "TM"]
            else f"{memory_type}".upper()
        )
        self.memory_banks[bank_key] = MemoryBank(
            id=bank_id,
            type=memory_type,
            core_id=self.id,
            spu_pn=spu_pn,
        )

    def populate_bank(self, bank_key: str, data: list[int]) -> int:
        """
        Populates the SpuCore's memory bank with the data provided

        Args:
            bank_key (str): key identifying the MemoryBank to store the data in
            start_page_id (int): identifier of the first page
            data (list[int]): list of words to store
        Returns:
            int: the number of pages added to the MemoryBank
        """
        self.memory_banks.get(bank_key).add_data(data)

    def generate_pages(self, page_size: int, start_page_id: int) -> int:
        """
        Generates pages from the data stored in the memory banks

        Args:
            page_size (int): number of uint32 words per page
            start_page_id (int): identifier of the first page
        Returns:
            int: number of pages created
        """
        page_count = start_page_id
        for bank in self.memory_banks:
            page_count += self.memory_banks.get(bank).generate_pages(
                page_size=page_size, start_page_id=page_count
            )

        return page_count

    def serialize_banks(self, chunk_size: int) -> bytearray:
        """
        Serializes all SpuCore's memory banks used

        Args:
            chunk_size (int): size to align the final serialize array
        Returns:
            bytearray:  serialized into bytes
        """
        byte_buffer = bytearray()
        for bank in self.memory_banks:
            byte_buffer.extend(
                self.memory_banks.get(bank).serialize_data(chunk_size=chunk_size)
            )

        return byte_buffer

    def serialize_configuration(self) -> bytearray:
        """
        Serializes the SpuCore's configuration

        Args:
            None
        Returns:
            bytearray: configuration serialized into bytes
        """
        byte_buffer = bytearray()

        byte_buffer.extend(
            int.to_bytes(self.id, 1, byteorder=FILE_ENDIANNESS, signed=False)
        )
        byte_buffer.extend(
            int.to_bytes(self.status, 1, byteorder=FILE_ENDIANNESS, signed=False)
        )
        for bank in self.memory_banks:
            byte_buffer.extend(self.memory_banks.get(bank).serialize_configuration())

        return byte_buffer

    @staticmethod
    def get_available_memory_banks(spu_pn: SpuPartNumber) -> dict[str, int]:
        """
        Provides the number of banks available for a given SPU part number

        Args:
            spu_pn (SpuPartNumber): SPU part number
        Returns:
            dict[str,int]: dictionary containing the number of banks available (value)
                           for each type of MemoryBank (key)
        """
        banks: dict[str, int] = {}
        match spu_pn:
            case SpuPartNumber.SPU001:
                # DM
                banks["DM"] = 8
                # TM
                banks["TM"] = 4
                # SB
                banks["SB"] = 1
                # RQ
                banks["RQ"] = 1
                # PB
                banks["PB"] = 1
                # IM
                banks["IM"] = 1

        return banks

    @classmethod
    def deserialize(cls, spu_pn: SpuPartNumber, core_bytes: bytearray):
        """
        Deserializes a byte array into a SpuCore object

        Args:
            spu_pn (SpuPartNumber): part number of the SPU this SpuCore belongs to
            core_bytes (bytearray): byte array containing the SPU configuration serialized data
        Return:
            SpuCore: object describing a SpuCore configuration
        """
        id = core_bytes[0]
        status = CoreStatus(core_bytes[1])
        return cls(id=id, spu_pn=spu_pn, status=status)


@dataclass
class Spu:
    """
    Class describing the Spu configuration and content

    Attributes:
        part_number (SpuPartNumber): Spu part number
        core_clock_frequency_mhz (int): recommended core clock frequency in MHz
        encryption_key_index (int): index of the encrytion key to use
        cores (list[SpuCore]): list of the cores present in the SPU
    """

    def __init__(
        self,
        part_number: SpuPartNumber,
        core_clock_frequency_mhz: int,
        encryption_key_index: int,
        num_used_cores: int = 0,
        cores: list[SpuCore] = None,
    ) -> None:
        """
        Creates a new Spu object

        Args:
            part_number (SpuPartNumber): Spu part number
            num_used_cores (int): number of SpuCores in use
            core_clock_frequency_mhz (int): recommended core clock frequency in MHz
            encryption_key_index (int): index of the encrytion key to use
            cores (list[SpuCore]): list of cores in the SPU
        Returns:
            None
        """
        self.part_number: SpuPartNumber = part_number
        self.core_clock_frequency_mhz: int = core_clock_frequency_mhz
        self.encryption_key_index: int = encryption_key_index
        if cores is not None:
            self.cores: list[SpuCore] = cores
        else:
            self.cores: list[SpuCore] = []
            for core_id in range(num_used_cores):
                self.cores.append(
                    SpuCore(id=core_id, spu_pn=part_number, status=CoreStatus.ON)
                )
        # variable to help keep track of pages' consecutiveness when calling populate_from_page
        self.last_page_id: int = 0

    def validate_configuration(self) -> bool:
        """
        Checks the validity of the Spu against its physical capabitilites

        Args:
            None
        Returns:
            bool: true if the Spu configuration is valid, false otherwise
        """
        match self.part_number:
            case SpuPartNumber.SPU001:
                if self.encryption_key_index < 0 or self.encryption_key_index > 32:
                    return False
                if len(self.cores) > SPU001_NUM_CORES:
                    return False
                if self.core_clock_frequency_mhz > SPU001_MAX_FREQ:
                    raise Exception(
                        f"{self.core_clock_frequency_mhz} - {SPU001_MAX_FREQ}"
                    )
                    return False
                # TODO: add tests on number of memory banks
            case _:
                return False
        return True

    def populate_memory(
        self,
        core_id: int,
        bank_key: str,
        data: list[int],
    ) -> None:
        """
        Populate the Spu memory bank with the data provided

        Args:
            core_id (int): identifier of the core
            bank_key (str): key identifying the MemoryBank to store the data in
            data (list[int]): list of words to store
        Returns:
            None
        """
        assert (
            core_id >= 0
            and core_id < len(self.cores)
            and bank_key in self.cores[core_id].memory_banks.keys()
        )
        self.cores[core_id].populate_bank(bank_key=bank_key, data=data)

    def populate_from_page(self, page: ModelPage) -> None:
        """
        Appends the data stored in the page provided to the coresponding SPU memory.

        Args:
            page (ModelPage): model page to be added to the SPU
        Returns:
            None
        Raises:
            ValueError: the page ID is invalid
            Exception: the SPU part number is not supported
            ValueError: the core ID is invalid
            ValueError: the address of the page provided doesn't exist
        """
        # TODO: replace the class variable with something more appropriate (look at generators)
        if page.id - self.last_page_id > 1:
            raise ValueError(
                f"Page ID invalid: {str(page.id)} (previous page ID: {str(self.last_page_id)})"
                f"Pages must be provided consecutively to ensure the data is correctly order in the memory bank"
            )

        core_id = (page.address >> 20) - 1
        if self.part_number != SpuPartNumber.SPU001:
            raise Exception(f"SPU part number not supported: {str(self.part_number)}")
        elif core_id >= SPU001_NUM_CORES:
            raise ValueError(f"Core ID invalid: {str(core_id)}")

        memory_type, bank_id = MemoryBank.get_info_from_address(
            spu_pn=self.part_number, address=page.address
        )
        if memory_type == MemoryType.INVALID:
            raise ValueError(
                f"Address {hex(page.address)} does not exist in {str(self.part_number)}'s  memory"
            )

        bank_key: str = (
            f"{memory_type}{bank_id}".upper()
            if str(memory_type) in ["DM", "TM"]
            else f"{memory_type}".upper()
        )

        self.cores[core_id].memory_banks[bank_key].add_data(page.data[: page.length])
        self.last_page_id = page.id
        return (core_id, memory_type, bank_id)

    def generate_pages(self, page_size: int) -> int:
        """
        Generates pages from the data stored in the memory banks

        Args:
            page_size (int): number of uint32 words per page
        Returns:
            int: number of pages created
        """
        page_count = 0
        for core in self.cores:
            page_count = core.generate_pages(
                page_size=page_size, start_page_id=page_count
            )
        return page_count

    def serialize_memory(self, chunk_size: int) -> bytearray:
        """
        Serializes the content of all Spu memory banks used

        Args:
            chunk_size (int): size to align the final serialize array
        Returns:
            bytearray: memory serialized into bytes
        """
        byte_buffer = bytearray()
        for core in self.cores:
            byte_buffer.extend(core.serialize_banks(chunk_size=chunk_size))
        return byte_buffer

    def serialize_configuration(self) -> bytearray:
        """
        Serializes the Spu configuration

        Args:
            chunk_size (int): size to align the final serialize array
        Returns:
            bytearray: configuration serialized into bytes
        """
        byte_buffer = bytearray()
        byte_buffer.extend(
            int.to_bytes(self.part_number, 1, byteorder=FILE_ENDIANNESS, signed=False)
        )
        byte_buffer.extend(
            int.to_bytes(
                self.encryption_key_index,
                1,
                byteorder=FILE_ENDIANNESS,
                signed=False,
            )
        )
        byte_buffer.extend(
            int.to_bytes(
                self.core_clock_frequency_mhz,
                2,
                byteorder=FILE_ENDIANNESS,
                signed=False,
            )
        )

        for core in self.cores:
            byte_buffer.extend(core.serialize_configuration())

        while len(byte_buffer) % SPU_CONFIG_SIZE != 0:
            byte_buffer.append(0xFF)

        return byte_buffer

    @classmethod
    def deserialize(cls, spu_bytes: bytearray, endianness: str):
        """
        Deserializes a byte array into a Spu object

        Args:
            spu_bytes (bytearray): byte array containing the SPU configuration serialized data
            endianness (str): byte order of the serialized data ("big" or "little")
        Return:
            Spu: object containing all information describing the SPU configuration
        """
        part_number = SpuPartNumber(spu_bytes[0])
        encryption_key_index = int(spu_bytes[1])
        core_clock_frequency_mhz = int.from_bytes(
            spu_bytes[2:4],
            byteorder=endianness,
            signed=False,
        )
        cores: list[SpuCore] = []
        for core_id in range(SPU001_NUM_CORES):
            core_base_index = 4 + core_id * 28
            core = SpuCore.deserialize(
                spu_pn=part_number,
                core_bytes=spu_bytes[core_base_index : core_base_index + 28],
            )
            if core.id != 0xFF:
                cores.append(core)

        return cls(
            part_number=part_number,
            core_clock_frequency_mhz=core_clock_frequency_mhz,
            encryption_key_index=encryption_key_index,
            cores=cores,
        )


@dataclass
class Model:
    """
    Class describing a SPU Model

    Attributes:
        type (ModelType): type of the Model
        version (int): version of the Model
        audio_num_input_channel (int): number of audio input channels expected by the Model,
        audio_sampling_frequency_khz (int): audio sampling frequency in kHz expected by the Model
        name (str): name of the model
        vectors (list[SpuVector]): list of the SpuVectors that can be used to interact with the Model
        io_sequences (list[SpuSequence]): list of the SpuSequences that can be used to interact with the Model
        page_count (int): numbers of pages constituting the model
        spu (Spu): object describing the Spu configuration and content
    """

    def __init__(
        self,
        type: ModelType,
        version: int,
        audio_num_input_channel: int,
        audio_sampling_frequency_khz: int,
        target_spu: SpuPartNumber = SpuPartNumber.UNKNOWN,
        num_used_cores: int = 0,
        spu_core_clock_frequency_mhz: int = 0,
        encryption_key_index: int = -1,
        model_name: str = "generic_model",
        page_count: int = 0,
        spu: Spu = None,
        vectors: list[SpuVector] = None,
        io_sequences: list[SpuSequence] = None,
    ) -> None:
        """
        Creates a new Model object

        Args:
            type (ModelType): type of the Model
            version (int): version of the Model
            audio_num_input_channel (int): number of audio input channels expected by the Model
            audio_sampling_frequency_khz (int): audio sampling frequency in kHz expected by the Model
            target_spu (SpuPartNumber): SPU part number for which the Model is intended to run on
            num_used_cores (int): number of SpuCores used by the Model
            spu_core_clock_frequency_mhz (int): recommended SpuCore clock frequency to run the Model
            encryption_key_index (int): index of the key used to encrypt the Model
            model_name (str): name of the model (Default value: "generic_model")
            page_count (int): number of pages in the model
            spu (Spu): object describing the Spu configuration and content
            vectors (list[SpuVector]): list of the SpuVectors that can be used to interact with the Model
            io_sequences (list[SpuSequence]): list of the SpuSequences that can be used to interact with the Model
        Returns:
            None
        """
        self.type: ModelType = type
        self.version: int = version
        # TODO: find a way to a space for generic parameters, these two audio paarameters are too specific
        self.audio_num_input_channel: int = audio_num_input_channel
        self.audio_sampling_frequency_khz: int = audio_sampling_frequency_khz
        self.name: str = model_name
        self.vectors: list[SpuVector] = vectors if vectors is not None else []
        self.io_sequences: list[SpuSequence] = (
            io_sequences if io_sequences is not None else []
        )
        self.page_count: int = page_count
        self.spu = (
            Spu(
                part_number=target_spu,
                num_used_cores=num_used_cores,
                core_clock_frequency_mhz=spu_core_clock_frequency_mhz,
                encryption_key_index=encryption_key_index,
            )
            if not spu
            else spu
        )

    def populate_memory(self, core_id: int, bank_key: str, data: list[int]) -> None:
        """
        Populate the SPU memory bank with the data provided

        Args:
            core_id (int): identifier of the SpuCore where the data should be stored
            bank_key (str): key (concatenation of MemoryBank.type and MemoryBank.id)
                            describing the MemoryBank where the data should be stored
            data (list[int]): list of words to be stored in memory
        Returns:
            None
        """
        self.spu.populate_memory(
            core_id=core_id,
            bank_key=bank_key,
            data=data,
        )

    def serialize_data(self, chunk_size: int) -> bytearray:
        """
        Serializes the Model data

        Args:
            chunk_size (int): size to align the final serialize array
        Returns:
            bytearray: data serialized into bytes
        """
        self.page_count = self.spu.generate_pages(page_size=int((chunk_size - 8) / 4))
        return self.spu.serialize_memory(chunk_size=chunk_size)

    def serialize_header(self) -> bytearray:
        """
        Serializes the Model header

        Args:
            None
        Returns:
            bytearray: header serialized into bytes
        """
        byte_buffer = bytearray()

        byte_buffer.extend(
            int.to_bytes(self.type, 2, byteorder=FILE_ENDIANNESS, signed=False)
        )
        byte_buffer.extend(
            int.to_bytes(self.version, 2, byteorder=FILE_ENDIANNESS, signed=False)
        )
        byte_buffer.extend(
            int.to_bytes(self.page_count, 2, byteorder=FILE_ENDIANNESS, signed=False)
        )
        byte_buffer.extend(
            int.to_bytes(
                self.audio_num_input_channel,
                1,
                byteorder=FILE_ENDIANNESS,
                signed=False,
            )
        )
        byte_buffer.extend(
            int.to_bytes(
                self.audio_sampling_frequency_khz,
                1,
                byteorder=FILE_ENDIANNESS,
                signed=False,
            )
        )
        name_in_header = (
            self.name[:MODEL_NAME_MAX_LENGTH]
            if len(self.name) > MODEL_NAME_MAX_LENGTH
            else self.name.ljust(MODEL_NAME_MAX_LENGTH, "\0")
        )
        byte_buffer.extend(name_in_header.encode("utf-8"))
        for vector in self.vectors:
            byte_buffer.extend(vector.serialize())
        for io_sequence in self.io_sequences:
            byte_buffer.extend(io_sequence.serialize())
        while len(byte_buffer) % MODEL_CONFIG_SIZE != 0:
            byte_buffer.append(0xFF)

        return byte_buffer

    @classmethod
    def deserialize(
        cls,
        model_config_bytes: bytearray,
        spu_config_bytes: bytearray,
        model_data_bytes: bytearray,
        chunk_size: int,
        page_size: int,
        endianness: str,
    ):
        """
        Deserializes a byte array into a Model object

        Args:
            model_config_bytes (bytearray): byte array containing the model configuration serialized data
            model_config_bytes (bytearray): byte array containing the model configuration serialized data
            model_config_bytes (bytearray): byte array containing the model configuration serialized data
            chunk_size (int): size of the chunk (amount of data that can be processed at once) in bytes
            page_size (int): size of the model pages in uint32
            endianness (str): byte order of the serialized data ("big" or "little")
        Return:
            Model: object containing all information describing the model
        """
        type = ModelType(
            int.from_bytes(model_config_bytes[:2], byteorder=endianness, signed=False)
        )
        version = int.from_bytes(
            model_config_bytes[2:4], byteorder=endianness, signed=False
        )
        page_count = int.from_bytes(
            model_config_bytes[4:6], byteorder=endianness, signed=False
        )
        audio_num_input_channel = int(model_config_bytes[6])

        audio_sampling_frequency_khz = int(model_config_bytes[7])
        name = model_config_bytes[8:24].decode("utf-8").strip("\x00")
        vectors: list[SpuVector] = []
        for vector_id in range(8):
            vector_base_index = 24 + vector_id * 9
            vectors.append(
                SpuVector.deserialize(
                    vector_bytes=model_config_bytes[
                        vector_base_index : vector_base_index + 9
                    ],
                    endianness=endianness,
                )
            )

        io_sequences: list[SpuSequence] = []
        for sequence_id in range(4):
            sequence_base_index = 96 + sequence_id * 5
            io_sequences.append(
                SpuSequence.deserialize(
                    sequence_bytes=model_config_bytes[
                        sequence_base_index : sequence_base_index + 5
                    ],
                    endianness=endianness,
                )
            )

        spu = Spu.deserialize(spu_bytes=spu_config_bytes, endianness=endianness)

        # Break down the model data into chunk_size long arrays to be parse as ModelPages
        raw_model_pages: list[np.ndarray[np.uint32]] = [
            model_data_bytes[x : x + chunk_size]
            for x in range(0, len(model_data_bytes), chunk_size)
        ]

        for page_bytes in raw_model_pages:
            spu.populate_from_page(
                page=ModelPage.deserialize(page_bytes=page_bytes, endianness=endianness)
            )
        page_count = spu.generate_pages(page_size=page_size)

        return cls(
            model_name=name,
            type=type,
            version=version,
            audio_num_input_channel=audio_num_input_channel,
            audio_sampling_frequency_khz=audio_sampling_frequency_khz,
            vectors=vectors,
            io_sequences=io_sequences,
            spu=spu,
            page_count=page_count,
        )


@dataclass
class FileHeader:
    """
    Class describing the information contained in the header starting the ModelFile

    Attributes:
        magic (str): signature indicating that the file is a Femto File
        endianness (str): endianness of the data used to encode this file
        chunk_size (int): size of the data chunk to read this file
        file_format_version (int): version of the file format
        femtodriver_version (int): version of Femtodriver used to generate this file
        checksum (int): value of checksum for validity verification
        model_config_offset (int): offset in bytes of the model configuration section from the beginning of the file
        model_config_size (int): size of the model header section in bytes
        spu_config_offset (int): offset in bytes of the spu configuration section from the beginning of the file
        spu_config_size (int): size of the SPU configuration section in bytes
        model_data_offset (int): offset in bytes of the model data section from the beginning of the file
        model_data_size (int): size of the model data section in bytes
    """

    def __init__(
        self,
        chunk_size: int,
        model_config_size: int,
        spu_config_size: int,
        model_data_size: int,
        checksum: int,
        magic: str = FILE_MAGIC,
        endianness: str = FILE_ENDIANNESS,
        file_format_version: int = FILE_FORMAT_VERSION,
        femtodriver_version: int = FEMTODRIVER_VERSION,
    ) -> None:
        """
        Creates a FileHeader object

        Args:
            chunk_size (int): size of the data chunk to read this file
            model_config_size (int): size of the model header section in bytes
            spu_config_size (int): size of the SPU configuration section in bytes
            model_data_size (int): size of the model data section in bytes
            checksum (int): value of checksum for validity verification
            magic (str): signature indicating that the file is a Femto File
            endianness (str): byte order of the serialized data ("big" or "little")
            file_format_version (int): version of the file format used
            femtodriver_version (int): version of Femtodriver used to generate the file
        Return:
            None
        """
        self.magic: str = magic
        self.endianness: str = endianness
        self.chunk_size: int = chunk_size
        self.file_format_version: int = file_format_version
        self.femtodriver_version: int = femtodriver_version
        self.checksum: int = checksum
        self.model_config_offset: int = FILE_HEADER_SIZE
        self.model_config_size: int = model_config_size
        self.spu_config_offset: int = self.model_config_offset + self.model_config_size
        self.spu_config_size: int = spu_config_size
        self.model_data_offset: int = self.spu_config_offset + self.spu_config_size
        self.model_data_size: int = model_data_size

    def serialize(self) -> bytearray:
        """
        Serializes the FileHeader

        Args:
            None
        Returns:
            bytearray: object serialized into bytes
        """

        byte_buffer = bytearray()
        byte_buffer.extend(FILE_MAGIC.encode("utf-8"))
        byte_buffer.extend(
            int.to_bytes(
                1 if self.endianness == "little" else 2,
                1,
                byteorder=FILE_ENDIANNESS,
                signed=False,
            )
        )
        byte_buffer.extend(
            int.to_bytes(self.chunk_size, 2, byteorder=FILE_ENDIANNESS, signed=False)
        )
        byte_buffer.extend(
            int.to_bytes(
                self.file_format_version, 2, byteorder=FILE_ENDIANNESS, signed=False
            )
        )
        byte_buffer.extend(
            int.to_bytes(
                self.femtodriver_version, 2, byteorder=FILE_ENDIANNESS, signed=False
            )
        )
        byte_buffer.extend(
            int.to_bytes(self.checksum, 4, byteorder=FILE_ENDIANNESS, signed=False)
        )

        byte_buffer.extend(
            int.to_bytes(
                self.model_config_offset, 2, byteorder=FILE_ENDIANNESS, signed=False
            )
        )
        byte_buffer.extend(
            int.to_bytes(
                self.model_config_size, 2, byteorder=FILE_ENDIANNESS, signed=False
            )
        )
        byte_buffer.extend(
            int.to_bytes(
                self.spu_config_offset,
                2,
                byteorder=FILE_ENDIANNESS,
                signed=False,
            )
        )
        byte_buffer.extend(
            int.to_bytes(
                self.spu_config_size,
                2,
                byteorder=FILE_ENDIANNESS,
                signed=False,
            )
        )
        byte_buffer.extend(
            int.to_bytes(
                self.model_data_offset, 2, byteorder=FILE_ENDIANNESS, signed=False
            )
        )
        byte_buffer.extend(
            int.to_bytes(
                self.model_data_size, 4, byteorder=FILE_ENDIANNESS, signed=False
            )
        )
        while len(byte_buffer) % FILE_HEADER_SIZE != 0:
            byte_buffer.append(0xFF)
        return byte_buffer

    @classmethod
    def deserialize(cls, file_header_bytes: bytearray) -> Self:
        """
        Deserializes a byte array into a FileHeader object

        Args:
            file_header_bytes (bytearray): byte array containing the file header serialized data
        Return:
            FileHeader: object containing information necessary to read the file
        Raises:
            ValueError: the file was not recognized
        """
        magic = file_header_bytes[:16].decode("utf-8").strip()
        if magic != FILE_MAGIC:
            raise ValueError("File not recognized! Magic={magic}")

        endianness = "little" if file_header_bytes[16] == 1 else "big"

        chunk_size = int.from_bytes(
            file_header_bytes[17:19], byteorder=endianness, signed=False
        )
        file_format_version = int.from_bytes(
            file_header_bytes[19:21], byteorder=endianness, signed=False
        )
        femtodriver_version = int.from_bytes(
            file_header_bytes[21:23], byteorder=endianness, signed=False
        )
        checksum = int.from_bytes(
            file_header_bytes[23:27], byteorder=endianness, signed=False
        )
        model_config_offset = int.from_bytes(
            file_header_bytes[27:29], byteorder=endianness, signed=False
        )
        model_config_size = int.from_bytes(
            file_header_bytes[29:31], byteorder=endianness, signed=False
        )
        spu_config_offset = int.from_bytes(
            file_header_bytes[31:33], byteorder=endianness, signed=False
        )
        spu_config_size = int.from_bytes(
            file_header_bytes[33:35], byteorder=endianness, signed=False
        )
        model_data_offset = int.from_bytes(
            file_header_bytes[35:37], byteorder=endianness, signed=False
        )
        model_data_size = int.from_bytes(
            file_header_bytes[37:41], byteorder=endianness, signed=False
        )

        assert model_config_offset == FILE_HEADER_SIZE
        assert spu_config_offset == model_config_offset + model_config_size
        assert model_data_offset == spu_config_offset + spu_config_size

        return cls(
            chunk_size=chunk_size,
            model_config_size=model_config_size,
            spu_config_size=spu_config_size,
            model_data_size=model_data_size,
            checksum=checksum,
            magic=magic,
            endianness=endianness,
            file_format_version=file_format_version,
            femtodriver_version=femtodriver_version,
        )


@dataclass
class FemtoFile:
    """
    Class representing the femto file to export

    Attributes:
        file_header (FileHeader): object containing information necessary to read the file
        model (Model): object containing all information describing the model
        page_size (int): size of the model pages in uint32
    """

    def __init__(
        self,
        name: str = "",
        type: str = "",
        version: int = 0,
        metadata: dict = None,
        encryption_key_index: int = 0,
        target_spu: SpuPartNumber = SpuPartNumber.UNKNOWN,
        num_used_cores: int = 0,
        page_size: int = 62,
        spu_core_clock_frequency_mhz: int = 250,
        audio_num_input_channel: int = 1,
        sampling_frequency_khz: int = 16,
        model: Model = None,
        file_header: FileHeader = None,
    ) -> None:
        """
        Initializes a ModelFile object

        Args:
            name (str): name of the model
            type (str): type of the model
            version (int): version of the model
            metadata (dict): metadata generated by Femtodriver containing information to run the model (e.g. input-output specifications)
            encryption_key_index (int): index of the key used encrypt the model
            target_spu (str): intented SPU part number to run this model
            num_used_cores (int): number of cores in use to run the model
            page_size (int): size of the model page in uint32
            spu_core_clock_frequency_mhz (int): recommended SPU core frequency in MHz
            audio_num_input_channel (int): number of input audio channels expected by the model
            sampling_frequency_khz (int): sampling frequency of the audio signal expected by the model
            model (Model): object containing all information describing the model
            file_header (FileHeader): object containing information necessary to read the file
        Returns:
            None
        Raises:
            Exception: the SPU configuration is invalid
        """
        self.file_header = file_header
        self.page_size: int = page_size
        self.model = (
            Model(
                type=ModelType.str_to_type(type),
                version=version,
                target_spu=SpuPartNumber.str_to_pn(target_spu),
                num_used_cores=num_used_cores,
                spu_core_clock_frequency_mhz=spu_core_clock_frequency_mhz,
                encryption_key_index=encryption_key_index,
                audio_num_input_channel=audio_num_input_channel,
                audio_sampling_frequency_khz=sampling_frequency_khz,
                model_name=name,
            )
            if not model
            else model
        )
        print(
            f"FemtoFile: num_used_cores={num_used_cores} SPU cores={len(self.model.spu.cores)}"
        )
        # TODO: source the proper IOSpecs from Femtodriver, the current metadata do not provide sufficient information
        if metadata:
            self._parse_io_specs(metadata=metadata)
            if not self.model.spu.validate_configuration():
                raise Exception("The SPU configuration is not valid!")

    def _parse_io_specs(self, metadata: dict) -> None:
        """
        Extracts necessary information from the metadata dictionary provided by Femtodriver

        Args:
            metadata (dict): metadata generated by Femtodriver containing information to run the model (e.g. input-output specifications)
        Returns:
            Model: model objects with IO specifications attributes populated
        """

        # TODO: handle exceptions
        # TODO: handle proper IOSpecs from Femtodriver
        sequence_id: int = 0
        vector_id: int = 0

        for input in metadata["inputs"]:
            self.model.vectors.append(
                SpuVector(
                    id=vector_id,
                    vector_type="input",
                    size=metadata["inputs"][input]["len_64b_words"] * 4,
                    target_core_id=metadata["inputs"][input]["core"],
                    parameter=metadata["inputs"][input]["pc_val"],
                )
            )
            vector_id += 1
        for output in metadata["outputs"]:
            self.model.vectors.append(
                SpuVector(
                    id=vector_id,
                    vector_type="output",
                    size=metadata["outputs"][output]["len_64b_words"] * 4,
                    target_core_id=metadata["outputs"][output]["core"],
                    parameter=metadata["outputs"][output]["mailbox_id"],
                )
            )
            vector_id += 1

        # TODO: move away from fixed size IO definitions and remove the manual padding
        # Vector list set to 8 objects
        while len(self.model.vectors) < 8:
            self.model.vectors.append(
                SpuVector(
                    id=0xFF,
                    vector_type=" ",
                    target_core_id=0xFF,
                    size=0xFFFF,
                    parameter=0xFFFFFFFF,
                )
            )

        # Simple sequence assumed as 1 input and 1 output
        self.model.io_sequences.append(
            SpuSequence(id=sequence_id, input_ids=[0, 0xFF], output_ids=[1, 0xFF])
        )
        # Sequence list set to 4 objects
        while len(self.model.io_sequences) < 4:
            self.model.io_sequences.append(
                SpuSequence(id=0xFF, input_ids=[0xFF, 0xFF], output_ids=[0xFF, 0xFF])
            )

        sequence_id += 1

    def fill_memory(
        self, core_id: int, bank_id: str, data: np.ndarray[np.uint32]
    ) -> None:
        """
        Fill the SPU memory with the data provided. The data array is broken down into chunks to match the page size

        Args:
            core_id (int): ID of the core where the data should be stored (e.g. 0 or 1 for SPU001)
            bank_id (str): ID of the memory bank where the data should be stored (e.g. "DM2", "TM3")
            data (np.ndarray[np.uint32]): array containing data to be stored in the memory bank
        Return:
            None
        """
        self.model.populate_memory(
            core_id=core_id,
            bank_key=bank_id,
            data=data,
        )

    def _serialize_header(
        self, model_size: int, chunk_size: int, checksum: int
    ) -> bytearray:
        """
        Serializes the header section of the model (file header-model header-spu configuration)

        Args:
            model_size (int): size of the model in bytes
            chunk_size (int): size of the chunk (amount of data that can be processed at once) in bytes
            checksum (int): value of the checksum over the entire model
        Returns:
            bytearray: model header section serialized into bytes
        """
        # Prepare the header data prior to populating the header
        model_config = self.model.serialize_header()
        spu_config = self.model.spu.serialize_configuration()

        self.file_header = FileHeader(
            chunk_size=chunk_size,
            model_config_size=len(model_config),
            spu_config_size=len(spu_config),
            model_data_size=model_size,
            checksum=checksum,
        )

        byte_buffer = bytearray()
        byte_buffer.extend(self.file_header.serialize())

        byte_buffer.extend(model_config)
        byte_buffer.extend(spu_config)

        # Pad the file header to align the chunk size
        while len(byte_buffer) % chunk_size != 0:
            byte_buffer.append(0xFF)
        return byte_buffer

    def serialize(self) -> bytearray:
        """
        Serializes the complete model (including headers)

        Args:
            None
        Returns:
            bytearray: model serialized into bytes
        """

        byte_buffer = bytearray()
        model_data = self.model.serialize_data(chunk_size=256)
        # TODO: compute a valid checksum
        headers = self._serialize_header(
            model_size=len(model_data), chunk_size=256, checksum=0
        )

        byte_buffer.extend(headers)
        byte_buffer.extend(model_data)

        return byte_buffer

    def export_file(self, export_path: str) -> tuple[str, int]:
        """
        Writes the serialized model to file

        Args:
            export_path (str): path to export the femto file
        Return:
            tuple[str, int]: a tuple containing the path to the exported file and its size
        """

        file_size = 0
        file_path = path.join(export_path, f"{self.model.name}{MODEL_EXTENSION}")
        output_file = open(file=file_path, mode="wb")

        file_size += output_file.write(self.serialize())

        output_file.close()

        return (file_path, file_size)

    @classmethod
    def import_file(cls, import_path: str) -> Self:
        """
        Reads the file provided and extract the data it contains into a FemtoFile object

        Args:
            import_path (str): path to the .femto file
        Returns:
            FemtoFile: object identical to the one use to generate the femto file
        """
        input_file = open(file=import_path, mode="rb")

        # Read the header section (always 256 bytes)
        header_bytes = input_file.read(256)
        file_header: FileHeader = FileHeader.deserialize(file_header_bytes=header_bytes)
        page_size = int((file_header.chunk_size - 8) / 4)

        model_config_bytes = header_bytes[
            file_header.model_config_offset : file_header.model_config_offset
            + file_header.model_config_size
        ]
        spu_config_bytes = header_bytes[
            file_header.spu_config_offset : file_header.spu_config_offset
            + file_header.spu_config_size
        ]
        model_data_bytes = input_file.read(file_header.model_data_size)
        model = Model.deserialize(
            model_config_bytes=model_config_bytes,
            spu_config_bytes=spu_config_bytes,
            model_data_bytes=model_data_bytes,
            chunk_size=file_header.chunk_size,
            page_size=page_size,
            endianness=file_header.endianness,
        )
        return cls(file_header=file_header, model=model, page_size=page_size)
