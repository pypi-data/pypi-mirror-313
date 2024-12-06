from __future__ import annotations

import logging
from enum import Enum, IntEnum
from typing import Literal, overload

import itksn

from module_qc_database_tools.typing_compat import Annotated, ModuleType

log = logging.getLogger(__name__)


class ComponentType(IntEnum):
    """
    An enum for component types.
    """

    SensorTile: Annotated[int, "SensorTile"] = 0
    FeChip: Annotated[int, "FeChip"] = 1
    BareModule: Annotated[int, "BareModule"] = 2
    TripletModule: Annotated[int, "TripletModule"] = 3
    QuadModule: Annotated[int, "QuadModule"] = 4


class DPPort(str, Enum):
    """
    Enum for DP Port labeling on PCIe cards.
    """

    A = "A"
    B = "B"
    C = "C"
    D = "D"


def get_layer_from_serial_number(serial_number):
    """
    Get the layer from the serial number.
    """
    if len(serial_number) != 14 or not serial_number.startswith("20U"):
        log.exception("Error: Please enter a valid ATLAS SN.")
        raise ValueError()
    YY = serial_number[5:7]
    if "B1" in YY or "FC" in YY:
        return (
            "L2"  ## Doesn't look like there is anything dependent on SCC vs module flex
        )

    if "PIMS" in serial_number or "PIR6" in serial_number:
        return "L0"

    if "PIM0" in serial_number or "PIR7" in serial_number:
        return "R0"

    if "PIM5" in serial_number or "PIR8" in serial_number:
        return "R0.5"

    if "PIM1" in serial_number or "PIRB" in serial_number:
        return "L1"

    if "PG" in serial_number:
        return "L2"

    log.exception("Invalid module SN: %s", serial_number)
    raise ValueError()


def chip_serial_number_to_uid(serial_number):
    """
    Convert chip serial number to hexadecimal UID.
    """
    assert serial_number.startswith(
        "20UPGFC"
    ), "Serial number must be for a valid RD53 chip"
    return hex(int(serial_number[-7:]))


def chip_uid_to_serial_number(uid):
    """
    Convert chip hexadecimal UID to serial number.
    """
    return f"20UPGFC{int(uid, 16):07}"


def get_chip_type_from_serial_number(serial_number):
    """
    Convert module SN or chip SN to chip type
    """
    if "FC" in serial_number.upper():
        serial_number = str(chip_serial_number_to_uid(serial_number))
        if int(serial_number[-5]) == 1:
            return "RD53B"
        if int(serial_number[-5]) >= 2:
            return "ITKPIXV2"
        log.exception("Invalid serial number: %s", serial_number)
        raise ValueError()

    if serial_number[7] in ["1", "2"]:
        return "RD53B"
    if serial_number[7] == "3":
        return "ITKPIXV2"
    log.exception("Invalid serial number: %s", serial_number)
    raise ValueError()


def get_chip_type_from_config(config):
    """
    Get chip type from keyword in chip config
    """
    chiptype = ""
    try:
        chiptype = next(iter(config.keys()))
    except IndexError:
        log.error("One of your chip configuration files is empty")

    if chiptype not in {"RD53B", "ITKPIXV2"}:
        log.warning(
            "Chip name in configuration not one of expected chip names (RD53B or ITKPIXV2)"
        )
    return chiptype


def get_component_type(serial_number: str) -> ComponentType:
    """
    Returns component type for the serial number.
    """
    info = itksn.parse(serial_number.encode("utf-8"))

    assert (
        "pixel" in info.project_code.title().lower()
    ), "This is not a pixel project component."

    if "sensor_tile" in info.component_code.title().lower():
        return ComponentType.SensorTile

    if "fe_chip" in info.component_code.title().lower():
        return ComponentType.FeChip

    if "bare_module" in info.component_code.title().lower():
        return ComponentType.BareModule

    if (
        "triplet" in info.component_code.title().lower()
        and "module" in info.component_code.title().lower()
    ):
        return ComponentType.TripletModule

    if "quad_module" in info.component_code.title().lower():
        return ComponentType.QuadModule

    msg = (
        f"{serial_number} does not correspond to a sensor tile, bare module, or module."
    )
    raise ValueError(msg)


@overload
def get_chip_connectivity(
    dp_port: DPPort,
    chip_index: Literal[0, 1, 2],
    module_type: Literal["triplet"],
    reverse: bool,
):
    ...


@overload
def get_chip_connectivity(
    dp_port: DPPort,
    chip_index: Literal[0, 1, 2, 3],
    module_type: Literal["quad"],
    reverse: bool,
):
    ...


def get_chip_connectivity(
    dp_port: DPPort,
    chip_index: int,
    module_type: ModuleType = "quad",
    reverse: bool = False,
):
    """
    Get chip connectivity information for a chip on a triplet or quad module.

    Triplets use 4x4 firmware:

    - tx = 0 fixed by data adapter card,
    - rx = 0, 1, 2, 3

    Quads use 16x1 firmware:

    - tx = 0, 1, 2, 3
    - rx is one of the following depending on the DP port used

       - `A`: 0, 1, 2, 3
       - `B`: 4, 5, 6, 7
       - `C`: 8, 9, 10, 11
       - `D`: 12, 13, 14, 15

    """
    if module_type == "single":
        ports = [port.value for port in DPPort]
        if dp_port in ports:
            tx = ports.index(dp_port)
            rx = tx * 4
        else:
            msg = "could not determine rx/tx settings"
            raise RuntimeError(msg)
    elif module_type == "triplet":
        tx = 0
        rx = [2, 1, 0][chip_index] if reverse else [0, 1, 2][chip_index]
    else:
        ports = [port.value for port in DPPort]
        if dp_port in ports:
            tx = ports.index(dp_port)
            rx = [2 + tx * 4, 1 + tx * 4, 0 + tx * 4, 3 + tx * 4][chip_index]
        else:
            msg = "could not determine rx/tx settings"
            raise RuntimeError(msg)
    return tx, rx
