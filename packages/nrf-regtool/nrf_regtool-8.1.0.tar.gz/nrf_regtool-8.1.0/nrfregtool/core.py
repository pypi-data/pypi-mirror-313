#
# Copyright (c) 2022 Nordic Semiconductor ASA
#
# SPDX-License-Identifier: Apache-2.0
#

from __future__ import annotations

from collections import ChainMap, Counter
from functools import cached_property
from itertools import chain
from pathlib import Path
from pprint import pformat
from typing import Callable, Dict, List, Mapping, Optional, Sequence, Tuple, Union

import svd
import tomli
from intelhex import IntelHex
from svd import Device, EPath, Field, Peripheral, Register

from . import bicr, uicr
from .common import Record, log_dbg, log_vrb, log_dev
from .parsed_dt import PeripheralResult

# TOML format constants
TOML_FIELD_AS_HEX_WHEN_LARGER_THAN = 32
TOML_FIELD_COMMENT_START_AT_COLUMN = 30
TOML_FIELD_DEFAULT_VALUE_START_AT = 56


# Registers from supported peripherals that must be set as unconstrained
# regardless of commandline options.
REQUIRED_UNCONSTRAINED = {
    "BICR": bicr.BICR_UNCONSTRAINED,
}

# A map of values for a given field that are conflicting between different versions of the device
CONFLICTING_FIELD_VALUES = {
    "BICR": {
        "MODE": {
            # 'Pierce' and 'Crystal' are both used for '0' for this field
            "Pierce": 0,
            "Crystal": 0,
        }
    }
}

# Peripherals that reside in NVM
NVM_PERIPHERALS = ["UICR", "BICR"]
NVM_FILL_BYTE = 0xFF
NVM_RESET_VALUE = 0xFFFF_FFFF


class LogicalPeripheral:
    """Abstraction for a set of peripherals that are logically grouped together."""

    def __init__(
        self,
        name: str,
        device: Device,
        record: Record,
        unconstrained: Optional[List[str]] = None,
        base_address: Optional[int] = None,
        mem_map: Optional[MemoryMap] = None,
    ):
        """
        :param name: Name of the peripheral.
        :param device: SVD device element
        :param record: Peripheral register record containing register values
        :param unconstrained: List of register paths that should not be constrained
        :param base_address: Base address of the peripheral
        :param mem_map: The memory map containing register values
        """

        self._name: str = name
        self._device: Device = device

        main_peripheral = _find_peripheral(self._device, self._name)
        if base_address is not None:
            main_peripheral = main_peripheral.copy_to(base_address)

        self._peripherals: List[Peripheral] = [main_peripheral]

        if unconstrained is not None:
            self._unconstrain(unconstrained)

        if mem_map is not None:
            self._fill_from_mem_map(mem_map)

        self._fill_from_record(record)

    def _unconstrain(self, unconstrained: List[str]):
        """
        Remove restrictions put on a value held by the register.

        :param unconstrained: List of register paths that should not be constrained
        :raises ValueError: If a register is not found in the peripheral set
        """
        for register_path in unconstrained:
            record_name, field_name = split_register_path(register_path)
            try:
                register = self.record_name_to_register[record_name]
                if field_name is None:
                    register.unconstrain()
                else:
                    register[field_name].unconstrain()
            except KeyError as e:
                raise ValueError(
                    f"Unconstrained register path {register_path} not found in peripheral set "
                    f"{[p.name for p in self._peripherals]}"
                ) from e

    def _fill_from_record(self, record: Record):
        """
        Fill the values of the peripheral set based on the contents of an instance of Record.

        :param record: The record that register values are filled from
        :raises ValueError: If the register cannot be found in the peripheral set
        """
        for record_name, record_fields in record.items():
            try:
                register = self.record_name_to_register[record_name]
            except KeyError as e:
                if self._name == "UICR" and "_instance" in record_name:
                    log_dbg(f"Skipping register {record_name}")
                    continue
                else:
                    raise ValueError(
                        f"Register with record name '{record_name}' not found in peripheral set "
                        f"{[p.name for p in self._peripherals]}"
                    ) from e

            for field, value in record_fields.items():
                try:
                    register[field] = value
                except ValueError as e:
                    # The value is not found in the SVD. This could be the result of a register
                    # value enumeration having different names in different versions of the
                    # product. Check if the field in question is one of those fields, and load
                    # the raw value associated with that enumeration.
                    if (
                        self._name in CONFLICTING_FIELD_VALUES
                        and field in CONFLICTING_FIELD_VALUES[self._name]
                        and value in CONFLICTING_FIELD_VALUES[self._name][field]
                    ):
                        new_value = CONFLICTING_FIELD_VALUES[self._name][field][value]
                        log_dbg(
                            f"Setting {record_name}.{field} to {new_value} as the value '{value}'"
                            f" it is an aliased enumeration: {CONFLICTING_FIELD_VALUES}"
                        )
                        register[field] = new_value
                    else:
                        raise e

    def _fill_from_mem_map(self, mem_map: MemoryMap):
        """
        Fill the values of the peripheral set based on the contents of an instance of MemoryMap.

        :param mem_map: The memory map that register values are filled from
        :raises ValueError: If the register cannot be found in the peripheral set
        """
        mem_map_remainder: Set[int] = set(mem_map)

        for register in self.address_to_register.values():
            value, mask = mem_map[register.address_range]
            if register.content & mask != value:
                register.set_content(value, mask)

            mem_map_remainder.difference_update(register.address_range)

        if mem_map_remainder:
            raise ValueError(
                f"Address {hex(min(mem_map_remainder))} not found in peripheral set "
                f"{[p.name for p in self._peripherals]}"
            )

    @property
    def name(self) -> str:
        """Name of the peripheral set."""
        return self._name

    @cached_property
    def address_to_register(self) -> Mapping[int, Register]:
        """Map of all registers in the peripheral set, keyed by address."""
        return ChainMap(
            *(
                {
                    register.address: register
                    for register in peripheral.register_iter(leaf_only=True)
                }
                for peripheral in self._peripherals
            )
        )

    @cached_property
    def record_name_to_register(self) -> Mapping[str, Register]:
        """Map from record name to register instance."""
        return ChainMap(
            *(
                _make_record_to_register_map(peripheral)
                for peripheral in self._peripherals
            )
        )

    @cached_property
    def path_to_record_name(self) -> Mapping[EPath, str]:
        """Map of register path to record name."""
        return {
            register.path: record_name
            for record_name, register in self.record_name_to_register.items()
        }

    @cached_property
    def memory_map(self) -> Mapping[int, int]:
        """
        Return a combined memory map of the peripherals in the set.
        The returned map has a granularity of 1 byte.
        """
        return ChainMap(
            *(dict(p.memory_iter(absolute_addresses=True)) for p in self._peripherals)
        )

    @cached_property
    def written_memory_map(self) -> Mapping[int, int]:
        """
        Return a combined memory map of the peripherals in the set, but only containing those
        entries that were explicitly written to.
        The returned map has a granularity of 1 byte.
        """
        return ChainMap(
            *(
                dict(p.memory_iter(absolute_addresses=True, written_only=True))
                for p in self._peripherals
            )
        )

    @property
    def address_ranges(self) -> List[range]:
        """Return a list of address ranges covered by each peripheral in the peripheral set."""
        return [range(*peripheral.address_bounds) for peripheral in self._peripherals]

    def __repr__(self) -> str:
        return f"{self.__class__.__name__} {self._peripherals}"

    def __str__(self):
        return self.to_str(lambda reg: reg.modified)

    def to_str(self, reg_filter: Optional[Callable[[Register], bool]] = None):
        lines = []

        lines.append("{")

        for peripheral in self._peripherals:
            lines.append(f"  {peripheral.name} @ 0x{peripheral.base_address:08x}")

            for reg in peripheral.register_iter(leaf_only=True):
                if reg_filter is None or reg_filter(reg):
                    lines.append(f"    {reg}")

        lines.append("}")

        return "\n".join(lines)


def split_register_path(register_path: str) -> Tuple[str, Optional[str]]:
    """Split a register path such as 'register_name.field_name' into its components"""
    path_components = register_path.strip(".").rsplit(".", maxsplit=1)
    register_name = path_components[0]
    field_name = path_components[1] if len(path_components) > 1 else None
    return register_name, field_name


def _make_record_to_register_map(peripheral: Peripheral) -> Dict[str, Register]:
    """
    Make a map from record name to register based on the registers in the given peripheral.
    It is assumed that each register name maps to a unique record name in the peripheral.
    """

    register_counts: Counter = Counter()
    record_to_register_map = {}

    for register in peripheral.register_iter(leaf_only=True):
        non_indexed_path = register.path.to_flat()
        index = register_counts[non_indexed_path]
        register_counts[non_indexed_path] += 1
        record_name = f"{'_'.join(non_indexed_path).lower()}_{index}"
        record_to_register_map[record_name] = register

    return record_to_register_map


def _find_peripheral(device: Device, name: str) -> Peripheral:
    """
    Find a peripheral with the given name in the device.
    Certain common prefixes and suffixes used for peripheral names can be omitted from the name.
    """

    matches = [
        periph
        for n, periph in device.items()
        if name in (n, _strip_prefixes_suffixes(n, ["GLOBAL_"], ["_NS", "_S"]))
    ]

    if not matches:
        raise LookupError(
            f"No peripheral with name containing '{name}' found in the SVD file"
        )

    elif len(matches) > 1:
        raise ValueError(
            f"More than one peripheral with name containing '{name}' found in the "
            f"SVD file: {matches}"
        )

    return matches[0]


def _strip_prefixes_suffixes(
    word: str, prefixes: List[str], suffixes: List[str]
) -> str:
    """
    Remove a prefix and suffix from the given string.
    Up to one prefix and/or suffix is removed - if multiple of the provided strings match then
    the first found is removed.

    :param word: String to strip prefixes and suffixes from.
    :param prefixes: List of prefixes to strip.
    :param suffixes: List of suffixes to strip.

    :return: String where prefixes and suffixes have been removed.
    """

    for prefix in prefixes:
        if word.startswith(prefix):
            word = word[len(prefix) :]
            break

    for suffix in suffixes:
        if word.endswith(suffix):
            word = word[: -len(suffix)]
            break

    return word


class MemoryMap:
    """The representation of a memory."""

    def __init__(self, hex_files: Sequence[Path], byteorder: str = "little"):
        """
        :param hex_files: An iterable of hex files paths used to fill the memory map.
        :param byteorder: Byte order to use when retrieving a value from an address range.
        :raises ValueError: If the 'byteorder' is unsupported.
        """
        self._intelhex = IntelHex()
        self._intelhex.padding = None
        for file in hex_files:
            self._intelhex.loadhex(file)

        # Test for supported byteorder
        int.from_bytes((0,), byteorder)
        self._byteorder = byteorder

    def __iter__(self):
        yield from self._intelhex.addresses()

    def __getitem__(self, key: Union[int, range]):
        if isinstance(key, int):
            return self._intelhex[key]

        raw = [self._intelhex[x] for x in key]
        mask = int.from_bytes((0 if x is None else 0xFF for x in raw), self._byteorder)
        value = int.from_bytes((0 if x is None else x for x in raw), self._byteorder)

        return value, mask


def parse_toml(*tomls: Sequence[Union[str, Path]]) -> Record:
    """
    Parse register records extracted from one or more TOML configurations.
    Later configurations override earlier ones.

    :param tomls: Sequence of TOML configuration files with records to load

    :return: Records of register content from TOML configuration files.
    """

    toml_record = Record()

    for config in tomls:
        with Path(config).open("rb") as f_toml:
            toml_record.update(tomli.load(f_toml))

    log_vrb("")
    log_vrb(f"========= TOML Configurations =========\n")
    log_vrb(pformat(toml_record.as_hex()))
    log_vrb("")

    return toml_record


def field_as_toml(field: Field, **kwargs) -> str:
    """
    TOML representation of a register bitfield.

    :kwarg comments: Append comment strings to the field assignment output

    :return: TOML string representation of the field contents.
    """
    comments = kwargs.get("comments")

    reverse_enums: Dict[int, str] = {value: name for name, value in field.enums.items()}

    if field.content in reverse_enums:
        value = f'"{reverse_enums[field.content]}"'
        comment = ", ".join([enum for _value, enum in sorted(reverse_enums.items())])
        default = reverse_enums[field.reset_content]

    elif field.content > TOML_FIELD_AS_HEX_WHEN_LARGER_THAN:
        value = hex(field.content)
        if isinstance(field.allowed_values, range):
            comment = f"0..0x{field.allowed_values.stop - 1:x}"
        else:
            comment = ", ".join([f"{v} (0x{v:x})" for v in field.allowed_values])
        default = hex(field.reset_content)

    else:
        value = str(field.content)
        if isinstance(field.allowed_values, range):
            comment = f"0..{field.allowed_values.stop - 1}"
        else:
            comment = ", ".join([str(v) for v in field.allowed_values])
        default = str(field.reset_content)

    assignment = f"{field.name} = {value}"

    if comments:
        assignment_with_comment = (
            f"{assignment:<{TOML_FIELD_COMMENT_START_AT_COLUMN}}# {comment}"
        )

        return (
            f"{assignment_with_comment:<{TOML_FIELD_DEFAULT_VALUE_START_AT}}"
            f" Reset: {default}"
        )

    return assignment


def register_as_toml(register: Register, **kwargs) -> str:
    """
    TOML representation of a peripheral register.

    :kwarg reset_values: Include unmodified Fields as their reset value
    :kwarg comments: Allow field comment strings in the TOML
    :kwarg force_32_bit_fields: List of Fields that should be given as 32-bit integers, regardless
        of bit width (for example, addresses).

    :return: TOML string representation of the register contents.
    """
    comments = kwargs.get("comments")
    reset_values = kwargs.get("reset_values")
    force_32_bit_fields = kwargs.get("force_32_bit_fields")

    return "\n".join(
        [
            field_as_toml(
                field, comments=comments, force_32_bit_fields=force_32_bit_fields
            )
            for field in register.values()
            if (reset_values or field.modified)
        ]
    )


def generate_toml(out_path: Path, peripheral: LogicalPeripheral, **kwargs):
    """
    Write the peripheral representation to a TOML file.

    This is written without the use of 3rd party libraries, for three reasons:
        1) Most TOML libraries focus on reading, rather than writing.
        2) The libraries that do support writing, do not always handle comments.
        3) Writing TOML is simple.

    :param out_path: Path to write TOML file to.
    :param peripheral: Peripheral to map register content into TOML

    :kwarg reset_values: Include register bit reset values along with modified values.
    :kwarg comments: Include register field comments in the output configuration
    """

    reset_values = kwargs.get("reset_values")
    comments = kwargs.get("comments")

    peripheral_toml: List[str] = []

    for _address, register in sorted(peripheral.address_to_register.items()):
        if reset_values or register.modified:
            register_toml = register_as_toml(
                register,
                reset_values=reset_values,
                comments=comments,
            )
            peripheral_toml.append(
                f"[{peripheral.path_to_record_name[register.path]}]\n{register_toml}"
            )

    file_content = "\n\n".join(peripheral_toml)
    trailing_newline = "\n" if len(file_content) != 0 else ""

    with open(out_path, "w", encoding="utf-8") as file:
        file.write(file_content + trailing_newline)


def generate_hex(out_path: Path, peripheral: LogicalPeripheral, **kwargs):
    """
    Write the peripheral representation to a HEX file.

    :param out_path: Path to write HEX file to.
    :param peripheral: Peripheral to map register content into hex

    :kwarg reset_values: Include register bit reset values along with modified values.
    :kwarg fill_byte: Byte value used to fill unused memory in the peripheral space.
    :kwarg fill: Method for writing fill byte to memory.
    """

    reset_values = kwargs.get("reset_values")
    fill_byte = kwargs.get("fill_byte")
    fill_type = kwargs.get("fill")

    raw_memory: Dict[int, int] = dict(
        peripheral.memory_map if reset_values else peripheral.written_memory_map
    )

    if fill_byte is not None:
        if fill_type == "unmodified":
            # Write the fill byte to all addresses that correspond to a register but that hasn't
            # been modified
            unmodified_addresses = (
                peripheral.memory_map.keys() - peripheral.written_memory_map.keys()
            )
            raw_memory.update({address: fill_byte for address in unmodified_addresses})

        elif fill_type == "all":
            # Write the fill byte to every unmodified address in the peripheral's address range,
            # even those that don't correspond to a register
            gap_addresses = (
                set(chain.from_iterable(peripheral.address_ranges)) - raw_memory.keys()
            )
            raw_memory.update({address: fill_byte for address in gap_addresses})

    ih = IntelHex(raw_memory)
    ih.write_hex_file(out_path)
