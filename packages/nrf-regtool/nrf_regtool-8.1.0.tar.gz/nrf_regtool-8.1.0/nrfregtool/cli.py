#
# Copyright (c) 2023 Nordic Semiconductor ASA
#
# SPDX-License-Identifier: Apache-2.0
#

import enum
import importlib.resources
import pickle
from pathlib import Path
from pprint import pformat
from typing import NamedTuple, Optional

import click
import svd
import tomli
from devicetree import edtlib

from . import __version__, bicr, core, uicr
from .common import Product, Record, config_log, log_dbg, log_dev, log_vrb

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])
_VERBOSITY = 0


class FormatExtension(enum.Enum):
    """Enumeration of supported formats and their file extension."""

    TOML = ".toml"
    HEX = ".hex"


class Output(NamedTuple):
    start_address: int
    end_address: int
    path: Path


class HexIntParamType(click.ParamType):
    """
    Custom parameter type for hexadecimal integers. This allows click to automatically verify
    hexadecimal parameters when given from the commandline.
    """

    name = "hex_integer"

    def convert(self, value, param, ctx):
        """Overridden method."""

        if isinstance(value, int):
            return value

        try:
            return int(value, 16)
        except ValueError:
            self.fail(f"{value!r} must be in hexadecimal format", param, ctx)


HEX_INT = HexIntParamType()


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version=__version__)
@click.option(
    "-v",
    "--verbose",
    count=True,
    help="Print verbose output such as debug information.",
)
@click.option(
    "-c",
    "--config-file",
    type=click.File("rb", encoding="utf-8"),
    help=(
        "A TOML file containing command options. "
        "The file should follow the schema: <param_n> = <value_of_param_n>. "
        "Options given at the command line take precedence over the values contained in the "
        "configuration file."
    ),
)
@click.pass_context
def cli(ctx={}, verbose=False, config_file=None):
    """
    Generate memory-mapped binary files of peripheral register content, based on
    System View Description (SVD) files and configuration files.

    Use the -h or --help option with each command to see more information about
    them and their individual options/arguments.
    \f
    """
    ctx.ensure_object(dict)
    ctx.obj["VERBOSE"] = verbose

    config_log(verbosity=verbose)

    if config_file is not None:
        try:
            command = ctx.invoked_subcommand
            command_parameters = tomli.load(config_file)
            ctx.default_map = {command: command_parameters}
        except tomli.TOMLDecodeError as exc:
            raise click.BadOptionUsage(
                "config_file",
                f"Failed to parse the '{config_file.name}' as toml.",
                ctx=ctx,
            ) from exc


@cli.command(short_help="Generate hex from a TOML and SVD")
@click.option(
    "-i",
    "--input-config",
    multiple=True,
    type=click.Path(dir_okay=False, exists=True, path_type=Path),
    help=(
        "Input TOML configuration. This can be repeated multiple times to combine "
        "multiple configuration files into a single output."
    ),
)
@click.option(
    "-d",
    "--dts-file",
    type=click.Path(dir_okay=False, exists=True, path_type=Path),
    help=(
        "Compiled DTS configuration. If given, the script will parse the file for nodes that it "
        "recognizes that are relevant to the given peripheral. If given alongside a "
        "TOML configuration, the TOML contents will be applied after parsing this DTS file."
    ),
)
@click.option(
    "-H",
    "--hex-file",
    type=click.Path(dir_okay=False, exists=True, path_type=Path),
    multiple=True,
    help=(
        "HEX file. If given, the script will use it to initialize the values of "
        "the peripheral. Multiple HEX files can be given, and they will be applied in "
        "the order as they are given. Files passed as an input for this option are applied before"
        "any other inputs."
    ),
)
@click.option(
    "-o",
    "--output-file",
    required=True,
    multiple=True,
    type=click.Path(dir_okay=False, exists=False, path_type=Path),
    help=(
        "Generated output file. This can be repeated multiple times to specify "
        "multiple outputs of different formats. Supported formats are: "
        f"{[x.value for x in FormatExtension]}"
    ),
)
@click.option(
    "-p",
    "--peripheral",
    required=True,
    help="Name of the peripheral to be configured.",
)
@click.option(
    "-s",
    "--svd-file",
    required=True,
    type=click.Path(dir_okay=False, exists=True, path_type=Path),
    help=("Path to the device SVD file."),
)
@click.option(
    "-D",
    "--bindings-dir",
    multiple=True,
    type=click.Path(dir_okay=True, exists=True, path_type=Path),
    help="Path to a directory to search for devicetree bindings",
)
@click.option(
    "-b",
    "--base-address",
    type=HEX_INT,
    help="Specific base address to use for the peripheral, given in hexadecimal.",
)
@click.option(
    "-f",
    "--fill-byte",
    type=HEX_INT,
    help=(
        "Fill unconfigured memory space within the peripheral memory boundary with this "
        "byte value. This value may or may not be applied based on other options; see --fill for "
        "more information about how this is applied."
    ),
)
@click.option(
    "-F",
    "--fill",
    type=click.Choice(["unmodified", "all"], case_sensitive=False),
    default="unmodified",
    help=(
        "Apply the fill byte given from --fill to unmodified registers within the peripheral "
        "space, or to all unmodified bytes within the entire memory region of the peripheral "
        "boundary. CAUTION: Applying to the entire memory region could cause unintentional "
        "overwriting of other peripheral register values that exist within that space. "
        "Use 'all' only when certain that the peripheral memory space is not shared. "
        "This option is ignored if no --fill-byte is given, or if paired with --reset-values. "
        "TOML outputs will not reflect filled memory from this strategy."
    ),
)
@click.option(
    "-u",
    "--unconstrained",
    multiple=True,
    help=(
        "A register that should be unconstrained, in which it will accept any value "
        "that can fit inside of its fields. An optional field specifier may be added "
        "by appending a dot '.' and the name of the field to unconstrain, which will "
        "leave all other fields in that register untouched. Can be given multiple "
        "times for multiple unconstrained registers."
    ),
)
@click.option(
    "-m",
    "--modified-only",
    is_flag=True,
    help=(
        "Only output values for the registers that have been modified. "
        "With this flag, only registers that have been assigned a different value than their "
        "reset value are written to the output files. This is useful for updating only specific "
        "registers in a peripheral."
    ),
)
@click.option(
    "--comments",
    is_flag=True,
    help=("Print register field comments in generated TOML configurations."),
)
@click.pass_context
def generate(
    ctx,
    input_config,
    dts_file,
    hex_file,
    output_file,
    peripheral,
    svd_file,
    bindings_dir,
    base_address,
    fill_byte,
    fill,
    unconstrained,
    modified_only,
    comments,
):
    """
    Generate binary and/or TOML file(s) for the given peripheral from an SVD and mix of TOML or
    devicetree (DTS) configurations.

    The SVD file provides the foundational definition of what the peripheral looks like.
    Based on this definition, the registers from the configuration will be mapped accordingly into
    their relevant position in memory.
    By default this peripheral contains register contents that with reset values, which are then
    modified by register records contained within the given configurations.

    Passing a compiled DTS file into the tool, such as the zephyr.dts build artifact from Zephyr
    compilations, maps property information from devicetree for nodes to their relevant register
    and bitfield in the associated peripheral.

    TOML configurations are a definition of explicit registers and bitfields that contain
    specific values.
    Specifying more than one TOML configuration will combine the various register configurations
    into a single map to be applied together.
    When paired with a DTS configuration, the TOML configurations will be applied after the parsed
    devicetree contents are interpreted into UICR representation.

    For example, on nRF54H20:

        \b
        nrf-regtool generate -p UICR \\
        -d _build/zephyr/zephyr.dts \\
        -D nrf/dts/bindings \\
        -D modules/lib/nrf-regtool/dts/bindings \\
        -D modules/ic-next/dts/bindings \\
        -D zephyr/dts/bindings \\
        -s modules/hal/nordic_haltium/nrfx/mdk/nrf54h20_application.svd \\
        -o uicr.hex

    Or for a TOML configuration:

        \b
        nrf-regtool generate -p UICR \\
        -i uicr.toml \\
        -s modules/hal/nordic_haltium/nrfx/mdk/nrf54h20_application.svd \\
        -o uicr.hex

    This command accepts multiple input and output files by repeating the related option with a
    different path. This can be useful for combining multiple configuration files together into
    a single output unit, which can be in the form of a hex file or TOML configuration of the
    combined inputs.

    For example:

        \b
        nrf-regtool generate -p UICR \\
        -d _build/zephyr/zephyr.dts \\
        -D nrf/dts/bindings \\
        -D modules/lib/nrf-regtool/dts/bindings \\
        -D modules/ic-next/dts/bindings \\
        -D zephyr/dts/bindings \\
        -s modules/hal/nordic_haltium/nrfx/mdk/nrf54h20_application.svd \\
        -i register_overrides.toml \\
        -o uicr.hex -o uicr_records.toml
    \f
    """

    log_dev(
        pformat(
            {
                "input_config": input_config,
                "dts_file": dts_file,
                "hex_file": hex_file,
                "output_file": output_file,
                "peripheral_name": peripheral,
                "svd_file": svd_file,
                "fill": fill,
                "fill_byte": fill_byte,
                "comments": comments,
                "base_address": base_address,
                "unconstrained": unconstrained,
                "modified_only": modified_only,
            }
        )
    )

    periph_upper = peripheral.upper()

    if dts_file:
        if periph_upper != "BICR":
            raise click.BadParameter(
                f"Generating from DTS is only supported for peripheral BICR",
                ctx=ctx,
            )
        if not bindings_dir:
            raise click.BadParameter(
                f"DTS parsing requires one or more devicetree bindings directories to be specified",
                ctx=ctx,
            )

    if (
        periph_upper in core.NVM_PERIPHERALS
        and fill_byte is not None
        and fill_byte != core.NVM_FILL_BYTE
    ):
        raise click.BadParameter(
            f"Unused UICR memory should only be filled by {hex(core.NVM_FILL_BYTE)!r}; got {hex(fill_byte)!r}",
            ctx=ctx,
        )
    elif base_address is not None and base_address >= 0xFFFFFFFF:
        raise click.BadParameter(
            f"Invalid base address for peripheral {peripheral!r}: {hex(base_address)}",
            ctx=ctx,
        )

    unconstrained_registers = list(
        set(unconstrained) | set(core.REQUIRED_UNCONSTRAINED.get(periph_upper, []))
    )
    if unconstrained_registers:
        log_dbg(f"Unconstrained registers: {pformat(unconstrained_registers)}\n")

    base_address_dts: Optional[int] = None
    peripheral_records = Record()

    log_vrb(f"\n############### Generate {periph_upper} ###############\n")

    if dts_file:
        # Only BICR is supported as checked above
        devicetree = edtlib.EDT(dts_file, bindings_dir)
        base_address_dts, record = bicr.from_dts(devicetree)
        peripheral_records.update(record)

    if input_config:
        peripheral_records.update(core.parse_toml(*input_config))

    if not peripheral_records:
        log_vrb(f"No records compiled for {periph_upper}")
    else:
        log_dbg("")
        log_dbg(
            f"Compiled {periph_upper} records from all inputs:\n{pformat(peripheral_records.as_hex())}\n\n"
        )

    peripheral_base_address: Optional[int]
    if base_address is not None:
        peripheral_base_address = base_address
    elif base_address_dts is not None:
        peripheral_base_address = base_address_dts
    else:
        # Take the base address from the SVD file
        peripheral_base_address = None

    mem_map = core.MemoryMap(hex_file) if hex_file else None

    device = svd.parse(
        svd_file,
        options=svd.Options(
            parent_relative_cluster_address=True,
        ),
    )
    peripheral = core.LogicalPeripheral(
        name=periph_upper,
        device=device,
        record=peripheral_records,
        unconstrained=unconstrained_registers,
        base_address=peripheral_base_address,
        mem_map=mem_map,
    )

    # If DTS was provided, we have a much nicer debug print before this.
    # Otherwise, the raw registers is the best we can show.
    raw_log_fn = log_dbg if dts_file else log_vrb
    raw_log_fn(f"\nRegisters changed from the reset value:\n{peripheral!s}\n\n")

    log_dev(
        f"Registers to be output:\n{peripheral.to_str(lambda r: r.written or not modified_only)}"
    )

    for out_file in [x for x in output_file]:
        if out_file.suffix == FormatExtension.TOML.value:
            core.generate_toml(
                out_file, peripheral, reset_values=not modified_only, comments=comments
            )
        elif out_file.suffix == FormatExtension.HEX.value:
            core.generate_hex(
                out_file,
                peripheral,
                reset_values=not modified_only,
                fill_byte=fill_byte,
                fill=fill,
            )
        else:
            raise click.BadOptionUsage(
                "output_file",
                f"File extension {out_file.suffix!r} is not a supported format; "
                f"must be one of {[x.value for x in FormatExtension]}",
                ctx=ctx,
            )

    log_vrb(f"\n############### End {periph_upper} ###############\n")


@cli.command(short_help="Compile UICR from a DTS")
@click.option(
    "-e",
    "--edt-pickle-file",
    required=True,
    type=click.Path(dir_okay=False, exists=True, path_type=Path),
    help=(
        "Pickled edtlib.EDT object with parsed devicetree contents, "
        "containing information that is relevant for a domain's UICR."
    ),
)
@click.option(
    "-o",
    "--output-file",
    required=True,
    multiple=True,
    type=click.Path(dir_okay=False, exists=False, path_type=Path),
    help=(
        "Generated output file in HEX format. "
        "Multiple output paths can be given by repeating this option."
    ),
)
@click.option(
    "-P",
    "--product-name",
    required=True,
    help=(
        "Name of the Nordic SoC or SiP for which to compile the UICR. "
        f"Supported values are: {', '.join(x.name for x in Product)}"
    ),
)
@click.pass_context
def uicr_compile(
    ctx,
    edt_pickle_file,
    output_file,
    product_name,
):
    """
    User Information Configuration Registers (UICR), in the context of certain
    Nordic SoCs, are used by Secure Domain Firmware (SDFW) to configure system
    resources, like memory and peripherals. When used in singular, a UICR refers
    to a complete set of registers for one domain.

    This command compiles a UICR binary blob from devicetree input, which should
    indicate the system resource configuration required for a single domain.

    For example, on nRF54H20:

        \b
        PYTHONPATH=zephyr/scripts/dts/python-devicetree/src \\
        nrf-regtool uicr-compile \\
        -e _build/zephyr/edt.pickle \\
        -o uicr.hex \\
        -P NRF54H20

    This command is intended for use as part of the Zephyr RTOS application
    development workflow. nrf-regtool depends on edtlib, a devicetree parsing
    library provided by the Zephyr Project, and the input file would usually be
    the edt.pickle artifact from a Zephyr build system. Using the pickle input
    requires a matching revision of edtlib from the Zephyr repository.
    \f
    """

    try:
        product = Product(product_name)
    except ValueError:
        raise click.BadOptionUsage(
            "product_name",
            f"Unknown product name {product_name}; must be one of {[x.name for x in Product]}",
            ctx=ctx,
        )

    log_vrb(f"\n############### Compile UICR ###############\n")

    with edt_pickle_file.open("rb") as file:
        devicetree = pickle.load(file)

    base_address, record = uicr.from_dts(devicetree, product)

    if not record:
        log_vrb(f"No records compiled for UICR")
    else:
        log_dbg(
            f"\nCompiled UICR records from all inputs:\n{pformat(record.as_hex())}\n\n"
        )

    with importlib.resources.path("nrfregtool.resources", "uicr.svd") as svd_file:
        device = svd.parse(
            svd_file,
            options=svd.Options(
                parent_relative_cluster_address=True,
            ),
        )

    peripheral = core.LogicalPeripheral(
        name="UICR",
        device=device,
        record=record,
        base_address=base_address,
    )

    log_dbg(f"\nRegisters changed from the reset value:\n{peripheral!s}\n\n")
    log_dev(f"Registers to be output:\n{peripheral.to_str()}")

    for out_file in output_file:
        core.generate_hex(out_file, peripheral, reset_values=True)

    log_vrb(f"\n############### End UICR ###############\n")
