#
# Copyright (c) 2024 Nordic Semiconductor ASA
#
# SPDX-License-Identifier: Apache-2.0
#
import dataclasses as dc
import enum
from typing import List, Optional, Tuple, Union

from devicetree import edtlib

from nrfregtool.common import AddressOffset, NrfPsel, Product, log_dbg


@dc.dataclass(frozen=True)
class GpiosProp:
    """CTRLSEL lookup table entry for *-gpios properties"""

    name: str
    port: int
    pin: int


@enum.unique
class Ctrlsel(enum.IntEnum):
    """
    Enumeration of GPIO.PIN_CNF[n].CTRLSEL values.
    The list here may not be exhaustive.
    """

    GPIO = 0
    VPR_GRC = 1
    CAN_PWM_I3C = 2
    SERIAL0 = 3
    EXMIF_RADIO_SERIAL1 = 4
    CAN_TDM_SERIAL2 = 5
    CAN = 6
    TND = 7


# Default CTRLSEL value indicating that CTRLSEL should not be used
CTRLSEL_DEFAULT = Ctrlsel.GPIO

# Pin functions used with pinctrl, see include/zephyr/dt-bindings/pinctrl/nrf-pinctrl.h
# Only the functions relevant for CTRLSEL deduction have been included.
NRF_FUN_UART_TX = 0
NRF_FUN_UART_RX = 1
NRF_FUN_UART_RTS = 2
NRF_FUN_UART_CTS = 3
NRF_FUN_SPIM_SCK = 4
NRF_FUN_SPIM_MOSI = 5
NRF_FUN_SPIM_MISO = 6
NRF_FUN_SPIS_SCK = 7
NRF_FUN_SPIS_MOSI = 8
NRF_FUN_SPIS_MISO = 9
NRF_FUN_SPIS_CSN = 10
NRF_FUN_TWIM_SCL = 11
NRF_FUN_TWIM_SDA = 12
NRF_FUN_PWM_OUT0 = 22
NRF_FUN_PWM_OUT1 = 23
NRF_FUN_PWM_OUT2 = 24
NRF_FUN_PWM_OUT3 = 25
NRF_FUN_EXMIF_CK = 35
NRF_FUN_EXMIF_DQ0 = 36
NRF_FUN_EXMIF_DQ1 = 37
NRF_FUN_EXMIF_DQ2 = 38
NRF_FUN_EXMIF_DQ3 = 39
NRF_FUN_EXMIF_DQ4 = 40
NRF_FUN_EXMIF_DQ5 = 41
NRF_FUN_EXMIF_DQ6 = 42
NRF_FUN_EXMIF_DQ7 = 43
NRF_FUN_EXMIF_CS0 = 44
NRF_FUN_EXMIF_CS1 = 45
NRF_FUN_CAN_TX = 46
NRF_FUN_CAN_RX = 47

NRF_FUN_TDM_SCK_M = 48
NRF_FUN_TDM_SCK_S = 49
NRF_FUN_TDM_FSYNC_M = 50
NRF_FUN_TDM_FSYNC_S = 51
NRF_FUN_TDM_SDIN = 52
NRF_FUN_TDM_SDOUT = 53
NRF_FUN_TDM_MCK = 54

# Deliberately defined as placeholders
NRF_FUN_EXMIF_RWDS = 0xFF - 2
NRF_FUN_I3C_SDA = 0xFF - 1
NRF_FUN_I3C_SCL = 0xFF

_PINCTRL_CTRLSEL_LOOKUP_NRF54H20 = {
    # I3C120
    0x5F8D_3000: {
        # P2
        NrfPsel(fun=NRF_FUN_I3C_SDA, port=2, pin=1): Ctrlsel.CAN_PWM_I3C,
        NrfPsel(fun=NRF_FUN_I3C_SCL, port=2, pin=0): Ctrlsel.CAN_PWM_I3C,
        # P6
        NrfPsel(fun=NRF_FUN_I3C_SDA, port=6, pin=2): Ctrlsel.CAN_PWM_I3C,
        NrfPsel(fun=NRF_FUN_I3C_SCL, port=6, pin=1): Ctrlsel.CAN_PWM_I3C,
    },
    # CAN120
    0x5F8D_8000: {
        # P2
        NrfPsel(fun=NRF_FUN_CAN_TX, port=2, pin=9): Ctrlsel.CAN_PWM_I3C,
        NrfPsel(fun=NRF_FUN_CAN_RX, port=2, pin=8): Ctrlsel.CAN_PWM_I3C,
        # P9
        NrfPsel(fun=NRF_FUN_CAN_TX, port=9, pin=5): Ctrlsel.CAN,
        NrfPsel(fun=NRF_FUN_CAN_RX, port=9, pin=4): Ctrlsel.CAN,
    },
    # I3C121
    0x5F8D_E000: {
        # P2
        NrfPsel(fun=NRF_FUN_I3C_SDA, port=2, pin=3): Ctrlsel.CAN_PWM_I3C,
        NrfPsel(fun=NRF_FUN_I3C_SCL, port=2, pin=2): Ctrlsel.CAN_PWM_I3C,
        # P7
        NrfPsel(fun=NRF_FUN_I3C_SDA, port=7, pin=3): Ctrlsel.CAN_PWM_I3C,
        NrfPsel(fun=NRF_FUN_I3C_SCL, port=7, pin=2): Ctrlsel.CAN_PWM_I3C,
    },
    # PWM120
    0x5F8E_4000: {
        # P2
        NrfPsel(fun=NRF_FUN_PWM_OUT0, port=2, pin=4): Ctrlsel.CAN_PWM_I3C,
        NrfPsel(fun=NRF_FUN_PWM_OUT1, port=2, pin=5): Ctrlsel.CAN_PWM_I3C,
        NrfPsel(fun=NRF_FUN_PWM_OUT2, port=2, pin=6): Ctrlsel.CAN_PWM_I3C,
        NrfPsel(fun=NRF_FUN_PWM_OUT3, port=2, pin=7): Ctrlsel.CAN_PWM_I3C,
        # P6
        NrfPsel(fun=NRF_FUN_PWM_OUT0, port=6, pin=6): Ctrlsel.CAN_PWM_I3C,
        NrfPsel(fun=NRF_FUN_PWM_OUT1, port=6, pin=7): Ctrlsel.CAN_PWM_I3C,
        NrfPsel(fun=NRF_FUN_PWM_OUT2, port=6, pin=8): Ctrlsel.CAN_PWM_I3C,
        NrfPsel(fun=NRF_FUN_PWM_OUT3, port=6, pin=9): Ctrlsel.CAN_PWM_I3C,
        # P7
        NrfPsel(fun=NRF_FUN_PWM_OUT0, port=7, pin=0): Ctrlsel.CAN_PWM_I3C,
        NrfPsel(fun=NRF_FUN_PWM_OUT1, port=7, pin=1): Ctrlsel.CAN_PWM_I3C,
        NrfPsel(fun=NRF_FUN_PWM_OUT2, port=7, pin=6): Ctrlsel.CAN_PWM_I3C,
        NrfPsel(fun=NRF_FUN_PWM_OUT3, port=7, pin=7): Ctrlsel.CAN_PWM_I3C,
    },
    # PWM130
    0x5F9A_4000: {
        # P9
        NrfPsel(fun=NRF_FUN_PWM_OUT0, port=9, pin=2): Ctrlsel.CAN_PWM_I3C,
        NrfPsel(fun=NRF_FUN_PWM_OUT1, port=9, pin=3): Ctrlsel.CAN_PWM_I3C,
        NrfPsel(fun=NRF_FUN_PWM_OUT2, port=9, pin=4): Ctrlsel.CAN_PWM_I3C,
        NrfPsel(fun=NRF_FUN_PWM_OUT3, port=9, pin=5): Ctrlsel.CAN_PWM_I3C,
    },
    # SPIM130/SPIS130/TWIM130/TWIS130/UARTE130
    0x5F9A_5000: {
        # SPIM mappings
        NrfPsel(fun=NRF_FUN_SPIM_MOSI, port=9, pin=5): Ctrlsel.SERIAL0,
        NrfPsel(fun=NRF_FUN_SPIM_MISO, port=9, pin=2): Ctrlsel.SERIAL0,
        GpiosProp(name="cs-gpios", port=9, pin=3): Ctrlsel.SERIAL0,
        NrfPsel(fun=NRF_FUN_SPIM_SCK, port=9, pin=4): Ctrlsel.SERIAL0,
        # SPIS mappings
        NrfPsel(fun=NRF_FUN_SPIS_MISO, port=9, pin=5): Ctrlsel.SERIAL0,
        NrfPsel(fun=NRF_FUN_SPIS_MOSI, port=9, pin=2): Ctrlsel.SERIAL0,
        NrfPsel(fun=NRF_FUN_SPIS_CSN, port=9, pin=3): Ctrlsel.SERIAL0,
        NrfPsel(fun=NRF_FUN_SPIS_SCK, port=9, pin=4): Ctrlsel.SERIAL0,
        # TWIM mappings
        NrfPsel(fun=NRF_FUN_TWIM_SDA, port=9, pin=5): Ctrlsel.SERIAL0,
        NrfPsel(fun=NRF_FUN_TWIM_SCL, port=9, pin=4): Ctrlsel.SERIAL0,
        # UARTÈ mappings
        NrfPsel(fun=NRF_FUN_UART_TX, port=9, pin=5): Ctrlsel.SERIAL0,
        NrfPsel(fun=NRF_FUN_UART_RX, port=9, pin=4): Ctrlsel.CAN_TDM_SERIAL2,
        NrfPsel(fun=NRF_FUN_UART_CTS, port=9, pin=2): Ctrlsel.SERIAL0,
        NrfPsel(fun=NRF_FUN_UART_RTS, port=9, pin=3): Ctrlsel.SERIAL0,
    },
    # SPIM131/SPIS131/TWIM131/TWIS131/UARTE131
    0x5F9A_6000: {
        # SPIM mappings
        NrfPsel(fun=NRF_FUN_SPIM_MOSI, port=9, pin=0): Ctrlsel.CAN_TDM_SERIAL2,
        NrfPsel(fun=NRF_FUN_SPIM_MISO, port=9, pin=2): Ctrlsel.CAN_TDM_SERIAL2,
        GpiosProp(name="cs-gpios", port=9, pin=3): Ctrlsel.CAN_TDM_SERIAL2,
        NrfPsel(fun=NRF_FUN_SPIM_SCK, port=9, pin=1): Ctrlsel.CAN_TDM_SERIAL2,
        # SPIS mappings
        NrfPsel(fun=NRF_FUN_SPIS_MISO, port=9, pin=0): Ctrlsel.CAN_TDM_SERIAL2,
        NrfPsel(fun=NRF_FUN_SPIS_MOSI, port=9, pin=2): Ctrlsel.CAN_TDM_SERIAL2,
        NrfPsel(fun=NRF_FUN_SPIS_CSN, port=9, pin=3): Ctrlsel.CAN_TDM_SERIAL2,
        NrfPsel(fun=NRF_FUN_SPIS_SCK, port=9, pin=1): Ctrlsel.CAN_TDM_SERIAL2,
        # TWIM mappings
        NrfPsel(fun=NRF_FUN_TWIM_SDA, port=9, pin=0): Ctrlsel.CAN_TDM_SERIAL2,
        NrfPsel(fun=NRF_FUN_TWIM_SCL, port=9, pin=1): Ctrlsel.CAN_TDM_SERIAL2,
        # UARTÈ mappings
        NrfPsel(fun=NRF_FUN_UART_TX, port=9, pin=0): Ctrlsel.CAN_TDM_SERIAL2,
        NrfPsel(fun=NRF_FUN_UART_RX, port=9, pin=1): Ctrlsel.SERIAL0,
        NrfPsel(fun=NRF_FUN_UART_CTS, port=9, pin=2): Ctrlsel.CAN_TDM_SERIAL2,
        NrfPsel(fun=NRF_FUN_UART_RTS, port=9, pin=3): Ctrlsel.CAN_TDM_SERIAL2,
    },
    # SPIS120
    0x5F8E_5000: {
        NrfPsel(fun=NRF_FUN_SPIS_MISO, port=6, pin=3): Ctrlsel.SERIAL0,
        NrfPsel(fun=NRF_FUN_SPIS_MOSI, port=6, pin=4): Ctrlsel.SERIAL0,
        NrfPsel(fun=NRF_FUN_SPIS_CSN, port=6, pin=9): Ctrlsel.SERIAL0,
        NrfPsel(fun=NRF_FUN_SPIS_SCK, port=6, pin=0): Ctrlsel.SERIAL0,
    },
    # SPIM120/UARTE120
    0x5F8E_6000: {
        # SPIM P6 mappings
        NrfPsel(fun=NRF_FUN_SPIM_MOSI, port=6, pin=8): Ctrlsel.SERIAL0,
        NrfPsel(fun=NRF_FUN_SPIM_MISO, port=6, pin=7): Ctrlsel.SERIAL0,
        GpiosProp(name="cs-gpios", port=6, pin=5): Ctrlsel.SERIAL0,
        NrfPsel(fun=NRF_FUN_SPIM_SCK, port=6, pin=1): Ctrlsel.SERIAL0,
        # SPIM P7 mappings
        NrfPsel(fun=NRF_FUN_SPIM_MOSI, port=7, pin=7): Ctrlsel.SERIAL0,
        NrfPsel(fun=NRF_FUN_SPIM_MISO, port=7, pin=6): Ctrlsel.SERIAL0,
        GpiosProp(name="cs-gpios", port=7, pin=5): Ctrlsel.SERIAL0,
        NrfPsel(fun=NRF_FUN_SPIM_SCK, port=7, pin=3): Ctrlsel.SERIAL0,
        # SPIM P2 mappings
        NrfPsel(fun=NRF_FUN_SPIM_MOSI, port=2, pin=6): Ctrlsel.SERIAL0,
        NrfPsel(fun=NRF_FUN_SPIM_MISO, port=2, pin=5): Ctrlsel.SERIAL0,
        GpiosProp(name="cs-gpios", port=2, pin=7): Ctrlsel.SERIAL0,
        NrfPsel(fun=NRF_FUN_SPIM_SCK, port=2, pin=3): Ctrlsel.SERIAL0,
        # UARTÈ P6 mappings
        NrfPsel(fun=NRF_FUN_UART_TX, port=6, pin=8): Ctrlsel.SERIAL0,
        NrfPsel(fun=NRF_FUN_UART_CTS, port=6, pin=7): Ctrlsel.SERIAL0,
        NrfPsel(fun=NRF_FUN_UART_RX, port=6, pin=6): Ctrlsel.SERIAL0,
        NrfPsel(fun=NRF_FUN_UART_RTS, port=6, pin=5): Ctrlsel.SERIAL0,
        # UARTÈ P7 mappings
        NrfPsel(fun=NRF_FUN_UART_TX, port=7, pin=7): Ctrlsel.SERIAL0,
        NrfPsel(fun=NRF_FUN_UART_CTS, port=7, pin=6): Ctrlsel.SERIAL0,
        NrfPsel(fun=NRF_FUN_UART_RX, port=7, pin=4): Ctrlsel.SERIAL0,
        NrfPsel(fun=NRF_FUN_UART_RTS, port=7, pin=5): Ctrlsel.SERIAL0,
        # UARTÈ P2 mappings
        NrfPsel(fun=NRF_FUN_UART_TX, port=2, pin=6): Ctrlsel.SERIAL0,
        NrfPsel(fun=NRF_FUN_UART_CTS, port=2, pin=5): Ctrlsel.SERIAL0,
        NrfPsel(fun=NRF_FUN_UART_RX, port=2, pin=4): Ctrlsel.SERIAL0,
        NrfPsel(fun=NRF_FUN_UART_RTS, port=2, pin=7): Ctrlsel.SERIAL0,
    },
    # SPIM121
    0x5F8E_7000: {
        # SPIM P6 mappings
        NrfPsel(fun=NRF_FUN_SPIM_MOSI, port=6, pin=13): Ctrlsel.SERIAL0,
        NrfPsel(fun=NRF_FUN_SPIM_MISO, port=6, pin=12): Ctrlsel.SERIAL0,
        GpiosProp(name="cs-gpios", port=6, pin=10): Ctrlsel.SERIAL0,
        NrfPsel(fun=NRF_FUN_SPIM_SCK, port=6, pin=2): Ctrlsel.SERIAL0,
        # SPIM P7 mappings
        NrfPsel(fun=NRF_FUN_SPIM_MOSI, port=7, pin=1): Ctrlsel.EXMIF_RADIO_SERIAL1,
        NrfPsel(fun=NRF_FUN_SPIM_MISO, port=7, pin=0): Ctrlsel.EXMIF_RADIO_SERIAL1,
        GpiosProp(name="cs-gpios", port=7, pin=4): Ctrlsel.EXMIF_RADIO_SERIAL1,
        NrfPsel(fun=NRF_FUN_SPIM_SCK, port=7, pin=2): Ctrlsel.EXMIF_RADIO_SERIAL1,
        # SPIM P2 mappings
        NrfPsel(fun=NRF_FUN_SPIM_MOSI, port=2, pin=11): Ctrlsel.SERIAL0,
        NrfPsel(fun=NRF_FUN_SPIM_MISO, port=2, pin=10): Ctrlsel.SERIAL0,
        GpiosProp(name="cs-gpios", port=2, pin=8): Ctrlsel.SERIAL0,
        NrfPsel(fun=NRF_FUN_SPIM_SCK, port=2, pin=2): Ctrlsel.SERIAL0,
    },
    # EXMIF
    0x5F09_5000: {
        NrfPsel(fun=NRF_FUN_EXMIF_CK, port=6, pin=0): Ctrlsel.EXMIF_RADIO_SERIAL1,
        NrfPsel(fun=NRF_FUN_EXMIF_RWDS, port=6, pin=2): Ctrlsel.EXMIF_RADIO_SERIAL1,
        NrfPsel(fun=NRF_FUN_EXMIF_CS0, port=6, pin=3): Ctrlsel.EXMIF_RADIO_SERIAL1,
        NrfPsel(fun=NRF_FUN_EXMIF_DQ7, port=6, pin=4): Ctrlsel.EXMIF_RADIO_SERIAL1,
        NrfPsel(fun=NRF_FUN_EXMIF_DQ1, port=6, pin=5): Ctrlsel.EXMIF_RADIO_SERIAL1,
        NrfPsel(fun=NRF_FUN_EXMIF_DQ6, port=6, pin=6): Ctrlsel.EXMIF_RADIO_SERIAL1,
        NrfPsel(fun=NRF_FUN_EXMIF_DQ0, port=6, pin=7): Ctrlsel.EXMIF_RADIO_SERIAL1,
        NrfPsel(fun=NRF_FUN_EXMIF_DQ5, port=6, pin=8): Ctrlsel.EXMIF_RADIO_SERIAL1,
        NrfPsel(fun=NRF_FUN_EXMIF_DQ3, port=6, pin=9): Ctrlsel.EXMIF_RADIO_SERIAL1,
        NrfPsel(fun=NRF_FUN_EXMIF_DQ2, port=6, pin=10): Ctrlsel.EXMIF_RADIO_SERIAL1,
        NrfPsel(fun=NRF_FUN_EXMIF_DQ4, port=6, pin=11): Ctrlsel.EXMIF_RADIO_SERIAL1,
        NrfPsel(fun=NRF_FUN_EXMIF_CS1, port=6, pin=13): Ctrlsel.EXMIF_RADIO_SERIAL1,
    },
    # TDM130
    0x5F99_2000: {
        # TDM P1 mappings
        NrfPsel(fun=NRF_FUN_TDM_MCK, port=1, pin=2): Ctrlsel.CAN_TDM_SERIAL2,
        NrfPsel(fun=NRF_FUN_TDM_SCK_M, port=1, pin=3): Ctrlsel.CAN_TDM_SERIAL2,
        NrfPsel(fun=NRF_FUN_TDM_SCK_S, port=1, pin=3): Ctrlsel.CAN_TDM_SERIAL2,
        NrfPsel(fun=NRF_FUN_TDM_SDOUT, port=1, pin=4): Ctrlsel.CAN_TDM_SERIAL2,
        NrfPsel(fun=NRF_FUN_TDM_SDIN, port=1, pin=5): Ctrlsel.CAN_TDM_SERIAL2,
        NrfPsel(fun=NRF_FUN_TDM_FSYNC_M, port=1, pin=6): Ctrlsel.CAN_TDM_SERIAL2,
        NrfPsel(fun=NRF_FUN_TDM_FSYNC_S, port=1, pin=6): Ctrlsel.CAN_TDM_SERIAL2,
        # TDM P2 mappings
        NrfPsel(fun=NRF_FUN_TDM_MCK, port=2, pin=0): Ctrlsel.CAN_TDM_SERIAL2,
        NrfPsel(fun=NRF_FUN_TDM_SCK_M, port=2, pin=1): Ctrlsel.CAN_TDM_SERIAL2,
        NrfPsel(fun=NRF_FUN_TDM_SCK_S, port=2, pin=1): Ctrlsel.CAN_TDM_SERIAL2,
        NrfPsel(fun=NRF_FUN_TDM_SDOUT, port=2, pin=9): Ctrlsel.CAN_TDM_SERIAL2,
        NrfPsel(fun=NRF_FUN_TDM_SDIN, port=2, pin=10): Ctrlsel.CAN_TDM_SERIAL2,
        NrfPsel(fun=NRF_FUN_TDM_FSYNC_M, port=2, pin=11): Ctrlsel.CAN_TDM_SERIAL2,
        NrfPsel(fun=NRF_FUN_TDM_FSYNC_S, port=2, pin=11): Ctrlsel.CAN_TDM_SERIAL2,
    },
    # TDM131
    0x5F99_7000: {
        # TDM P1 mappings
        NrfPsel(fun=NRF_FUN_TDM_MCK, port=1, pin=0): Ctrlsel.CAN_TDM_SERIAL2,
        NrfPsel(fun=NRF_FUN_TDM_SCK_M, port=1, pin=1): Ctrlsel.CAN_TDM_SERIAL2,
        NrfPsel(fun=NRF_FUN_TDM_SCK_S, port=1, pin=1): Ctrlsel.CAN_TDM_SERIAL2,
        NrfPsel(fun=NRF_FUN_TDM_SDOUT, port=1, pin=9): Ctrlsel.CAN_TDM_SERIAL2,
        NrfPsel(fun=NRF_FUN_TDM_SDIN, port=1, pin=10): Ctrlsel.CAN_TDM_SERIAL2,
        NrfPsel(fun=NRF_FUN_TDM_FSYNC_M, port=1, pin=11): Ctrlsel.CAN_TDM_SERIAL2,
        NrfPsel(fun=NRF_FUN_TDM_FSYNC_S, port=1, pin=11): Ctrlsel.CAN_TDM_SERIAL2,
        # TDM P2 mappings
        NrfPsel(fun=NRF_FUN_TDM_MCK, port=2, pin=2): Ctrlsel.CAN_TDM_SERIAL2,
        NrfPsel(fun=NRF_FUN_TDM_SCK_M, port=2, pin=3): Ctrlsel.CAN_TDM_SERIAL2,
        NrfPsel(fun=NRF_FUN_TDM_SCK_S, port=2, pin=3): Ctrlsel.CAN_TDM_SERIAL2,
        NrfPsel(fun=NRF_FUN_TDM_SDOUT, port=2, pin=4): Ctrlsel.CAN_TDM_SERIAL2,
        NrfPsel(fun=NRF_FUN_TDM_SDIN, port=2, pin=6): Ctrlsel.CAN_TDM_SERIAL2,
        NrfPsel(fun=NRF_FUN_TDM_FSYNC_M, port=2, pin=7): Ctrlsel.CAN_TDM_SERIAL2,
        NrfPsel(fun=NRF_FUN_TDM_FSYNC_S, port=2, pin=7): Ctrlsel.CAN_TDM_SERIAL2,
    },
}

_PINCTRL_CTRLSEL_LOOKUP_NRF9280 = {
    # I3C120
    0x5F8D_3000: {
        NrfPsel(fun=NRF_FUN_I3C_SCL, port=2, pin=8): Ctrlsel.CAN_PWM_I3C,
        NrfPsel(fun=NRF_FUN_I3C_SDA, port=2, pin=9): Ctrlsel.CAN_PWM_I3C,
    },
    # CAN120
    0x5F8D_8000: {
        # P2
        NrfPsel(fun=NRF_FUN_CAN_RX, port=2, pin=10): Ctrlsel.CAN_TDM_SERIAL2,
        NrfPsel(fun=NRF_FUN_CAN_TX, port=2, pin=11): Ctrlsel.CAN_TDM_SERIAL2,
        # P9
        NrfPsel(fun=NRF_FUN_CAN_RX, port=9, pin=4): Ctrlsel.CAN_TDM_SERIAL2,
        NrfPsel(fun=NRF_FUN_CAN_TX, port=9, pin=5): Ctrlsel.CAN_TDM_SERIAL2,
    },
    # CAN121
    0x5F8D_B000: {
        # P2
        NrfPsel(fun=NRF_FUN_CAN_RX, port=2, pin=8): Ctrlsel.CAN_TDM_SERIAL2,
        NrfPsel(fun=NRF_FUN_CAN_TX, port=2, pin=9): Ctrlsel.CAN_TDM_SERIAL2,
        # P9
        NrfPsel(fun=NRF_FUN_CAN_RX, port=9, pin=2): Ctrlsel.CAN_TDM_SERIAL2,
        NrfPsel(fun=NRF_FUN_CAN_TX, port=9, pin=3): Ctrlsel.CAN_TDM_SERIAL2,
    },
    # I3C121
    0x5F8D_E000: {
        NrfPsel(fun=NRF_FUN_I3C_SCL, port=2, pin=10): Ctrlsel.CAN_PWM_I3C,
        NrfPsel(fun=NRF_FUN_I3C_SDA, port=2, pin=11): Ctrlsel.CAN_PWM_I3C,
    },
    # PWM120
    0x5F8E_4000: {
        # P2
        NrfPsel(fun=NRF_FUN_PWM_OUT0, port=2, pin=0): Ctrlsel.CAN_PWM_I3C,
        NrfPsel(fun=NRF_FUN_PWM_OUT1, port=2, pin=1): Ctrlsel.CAN_PWM_I3C,
        NrfPsel(fun=NRF_FUN_PWM_OUT2, port=2, pin=2): Ctrlsel.CAN_PWM_I3C,
        NrfPsel(fun=NRF_FUN_PWM_OUT3, port=2, pin=3): Ctrlsel.CAN_PWM_I3C,
        # P6
        NrfPsel(fun=NRF_FUN_PWM_OUT0, port=6, pin=0): Ctrlsel.CAN_PWM_I3C,
        NrfPsel(fun=NRF_FUN_PWM_OUT0, port=6, pin=6): Ctrlsel.CAN_PWM_I3C,
        NrfPsel(fun=NRF_FUN_PWM_OUT1, port=6, pin=1): Ctrlsel.CAN_PWM_I3C,
        NrfPsel(fun=NRF_FUN_PWM_OUT1, port=6, pin=7): Ctrlsel.CAN_PWM_I3C,
        NrfPsel(fun=NRF_FUN_PWM_OUT2, port=6, pin=2): Ctrlsel.CAN_PWM_I3C,
        NrfPsel(fun=NRF_FUN_PWM_OUT2, port=6, pin=8): Ctrlsel.CAN_PWM_I3C,
        NrfPsel(fun=NRF_FUN_PWM_OUT3, port=6, pin=3): Ctrlsel.CAN_PWM_I3C,
        NrfPsel(fun=NRF_FUN_PWM_OUT3, port=6, pin=9): Ctrlsel.CAN_PWM_I3C,
    },
    # SPIS120
    0x5F8E_5000: {
        NrfPsel(fun=NRF_FUN_SPIS_CSN, port=6, pin=9): Ctrlsel.SERIAL0,
        NrfPsel(fun=NRF_FUN_SPIS_MISO, port=6, pin=3): Ctrlsel.SERIAL0,
        NrfPsel(fun=NRF_FUN_SPIS_MOSI, port=6, pin=4): Ctrlsel.SERIAL0,
        NrfPsel(fun=NRF_FUN_SPIS_SCK, port=6, pin=0): Ctrlsel.SERIAL0,
    },
    # SPIM120/UARTE120
    0x5F8E_6000: {
        # SPIM P2 mappings
        GpiosProp(name="cs-gpios", port=2, pin=5): Ctrlsel.SERIAL0,
        NrfPsel(fun=NRF_FUN_SPIM_MISO, port=2, pin=3): Ctrlsel.SERIAL0,
        NrfPsel(fun=NRF_FUN_SPIM_MOSI, port=2, pin=4): Ctrlsel.SERIAL0,
        NrfPsel(fun=NRF_FUN_SPIM_SCK, port=2, pin=0): Ctrlsel.SERIAL0,
        # SPIM P6 mappings
        GpiosProp(name="cs-gpios", port=6, pin=5): Ctrlsel.SERIAL0,
        NrfPsel(fun=NRF_FUN_SPIM_MISO, port=6, pin=7): Ctrlsel.SERIAL0,
        NrfPsel(fun=NRF_FUN_SPIM_MOSI, port=6, pin=8): Ctrlsel.SERIAL0,
        NrfPsel(fun=NRF_FUN_SPIM_SCK, port=6, pin=1): Ctrlsel.SERIAL0,
        # UARTE P2 mappings
        NrfPsel(fun=NRF_FUN_UART_CTS, port=2, pin=3): Ctrlsel.SERIAL0,
        NrfPsel(fun=NRF_FUN_UART_RTS, port=2, pin=5): Ctrlsel.SERIAL0,
        NrfPsel(fun=NRF_FUN_UART_RX, port=2, pin=2): Ctrlsel.SERIAL0,
        NrfPsel(fun=NRF_FUN_UART_TX, port=2, pin=4): Ctrlsel.SERIAL0,
        # UARTE P6 mappings
        NrfPsel(fun=NRF_FUN_UART_CTS, port=6, pin=7): Ctrlsel.SERIAL0,
        NrfPsel(fun=NRF_FUN_UART_RTS, port=6, pin=5): Ctrlsel.SERIAL0,
        NrfPsel(fun=NRF_FUN_UART_RX, port=6, pin=6): Ctrlsel.SERIAL0,
        NrfPsel(fun=NRF_FUN_UART_TX, port=6, pin=8): Ctrlsel.SERIAL0,
    },
    # SPIM121
    0x5F8E_7000: {
        # P2
        GpiosProp(name="cs-gpios", port=2, pin=6): Ctrlsel.SERIAL0,
        NrfPsel(fun=NRF_FUN_SPIM_MISO, port=2, pin=8): Ctrlsel.SERIAL0,
        NrfPsel(fun=NRF_FUN_SPIM_MOSI, port=2, pin=9): Ctrlsel.SERIAL0,
        NrfPsel(fun=NRF_FUN_SPIM_SCK, port=2, pin=1): Ctrlsel.SERIAL0,
        # P6
        GpiosProp(name="cs-gpios", port=6, pin=10): Ctrlsel.SERIAL0,
        NrfPsel(fun=NRF_FUN_SPIM_MISO, port=6, pin=12): Ctrlsel.SERIAL0,
        NrfPsel(fun=NRF_FUN_SPIM_MOSI, port=6, pin=13): Ctrlsel.SERIAL0,
        NrfPsel(fun=NRF_FUN_SPIM_SCK, port=6, pin=2): Ctrlsel.SERIAL0,
    },
    # PWM130
    0x5F9A_4000: {
        NrfPsel(fun=NRF_FUN_PWM_OUT0, port=9, pin=2): Ctrlsel.CAN_PWM_I3C,
        NrfPsel(fun=NRF_FUN_PWM_OUT1, port=9, pin=3): Ctrlsel.CAN_PWM_I3C,
        NrfPsel(fun=NRF_FUN_PWM_OUT2, port=9, pin=4): Ctrlsel.CAN_PWM_I3C,
        NrfPsel(fun=NRF_FUN_PWM_OUT3, port=9, pin=5): Ctrlsel.CAN_PWM_I3C,
    },
    # SPIM130/SPIS130/TWIM130/TWIS130/UARTE130
    0x5F9A_5000: {
        # SPIM mappings
        GpiosProp(name="cs-gpios", port=9, pin=1): Ctrlsel.SERIAL0,
        NrfPsel(fun=NRF_FUN_SPIM_MISO, port=9, pin=2): Ctrlsel.SERIAL0,
        NrfPsel(fun=NRF_FUN_SPIM_MOSI, port=9, pin=3): Ctrlsel.SERIAL0,
        NrfPsel(fun=NRF_FUN_SPIM_SCK, port=9, pin=0): Ctrlsel.SERIAL0,
        # SPIS mappings
        NrfPsel(fun=NRF_FUN_SPIS_CSN, port=9, pin=1): Ctrlsel.SERIAL0,
        NrfPsel(fun=NRF_FUN_SPIS_MISO, port=9, pin=3): Ctrlsel.SERIAL0,
        NrfPsel(fun=NRF_FUN_SPIS_MOSI, port=9, pin=2): Ctrlsel.SERIAL0,
        NrfPsel(fun=NRF_FUN_SPIS_SCK, port=9, pin=0): Ctrlsel.SERIAL0,
        # TWIM mappings
        NrfPsel(fun=NRF_FUN_TWIM_SCL, port=9, pin=0): Ctrlsel.SERIAL0,
        NrfPsel(fun=NRF_FUN_TWIM_SDA, port=9, pin=3): Ctrlsel.SERIAL0,
        # UARTE mappings
        NrfPsel(fun=NRF_FUN_UART_CTS, port=9, pin=2): Ctrlsel.SERIAL0,
        NrfPsel(fun=NRF_FUN_UART_RTS, port=9, pin=1): Ctrlsel.SERIAL0,
        NrfPsel(fun=NRF_FUN_UART_RX, port=9, pin=4): Ctrlsel.SERIAL0,
        NrfPsel(fun=NRF_FUN_UART_TX, port=9, pin=3): Ctrlsel.SERIAL0,
    },
}

_PINCTRL_CTRLSEL_LOOKUP = {
    Product.NRF54H20: _PINCTRL_CTRLSEL_LOOKUP_NRF54H20,
    Product.NRF9280: _PINCTRL_CTRLSEL_LOOKUP_NRF9280,
}


def dt_lookup_ctrlsel(
    product: Product,
    src: Union[edtlib.PinCtrl, edtlib.Property],
    psel: Union[NrfPsel, Tuple[int, int]],
) -> Optional[int]:
    """Get the CTRLSEL value to use for a given pin selection."""

    lut = _PINCTRL_CTRLSEL_LOOKUP[product]

    if isinstance(src, edtlib.PinCtrl):
        identifier = src.node.regs[0].addr
        sub_entry = psel
    elif isinstance(src, edtlib.Property):
        try:
            identifier = src.node.regs[0].addr
        except IndexError:
            identifier = src.node.label
        sub_entry = GpiosProp(name=src.name, port=psel[0], pin=psel[1])
    else:
        raise ValueError(f"Unsupported GPIO pin source: {src}")

    if identifier in lut:
        ctrlsel = lut[identifier].get(sub_entry, CTRLSEL_DEFAULT)
    else:
        ctrlsel = None

    log_dbg(
        f"identifier={hex(identifier) if isinstance(identifier, int) else identifier}, "
        f"{sub_entry=} -> {ctrlsel=}"
    )

    return ctrlsel


NRF_SAADC_AIN0 = 1
NRF_SAADC_AIN1 = 2
NRF_SAADC_AIN2 = 3
NRF_SAADC_AIN3 = 4
NRF_SAADC_AIN4 = 5
NRF_SAADC_AIN5 = 6
NRF_SAADC_AIN6 = 7
NRF_SAADC_AIN7 = 8

_CHANNEL_LOOKUP = {
    # SAADC
    0x5F98_2000: {
        NRF_SAADC_AIN0: (1, 0),
        NRF_SAADC_AIN1: (1, 1),
        NRF_SAADC_AIN2: (1, 2),
        NRF_SAADC_AIN3: (1, 3),
        NRF_SAADC_AIN4: (1, 4),
        NRF_SAADC_AIN5: (1, 5),
        NRF_SAADC_AIN6: (1, 6),
        NRF_SAADC_AIN7: (1, 7),
    }
}


def dt_lookup_adc_channel_pins(channel: edtlib.Node) -> List[Tuple[int, int]]:
    lut = _CHANNEL_LOOKUP

    address = channel.parent.regs[0].addr | (1 << AddressOffset.SECURITY)
    if address not in lut:
        return []

    pins = []

    if "zephyr,input-positive" in channel.props:
        positive_pin = lut[address].get(channel.props["zephyr,input-positive"].val)
        if positive_pin is not None:
            log_dbg(
                f"{address=:08x}, {channel.props['zephyr,input-positive']=} -> {positive_pin=}"
            )

            pins.append(positive_pin)

    if "zephyr,input-negative" in channel.props:
        negative_pin = lut[address].get(channel.props["zephyr,input-negative"].val)
        if negative_pin is not None:
            log_dbg(
                f"{address=:08x}, {channel.props['zephyr,input-negative']=} -> {negative_pin=}"
            )

            pins.append(negative_pin)

    return pins


NRF_COMP_LPCOMP_AIN0 = "AIN0"
NRF_COMP_LPCOMP_AIN1 = "AIN1"
NRF_COMP_LPCOMP_AIN2 = "AIN2"
NRF_COMP_LPCOMP_AIN3 = "AIN3"
NRF_COMP_LPCOMP_AIN4 = "AIN4"
NRF_COMP_LPCOMP_AIN5 = "AIN5"
NRF_COMP_LPCOMP_AIN6 = "AIN6"
NRF_COMP_LPCOMP_AIN7 = "AIN7"

_COMP_LPCOMP_LOOKUP = {
    # COMP/LPCOMP
    0x5F98_3000: {
        NRF_COMP_LPCOMP_AIN0: (1, 0),
        NRF_COMP_LPCOMP_AIN1: (1, 1),
        NRF_COMP_LPCOMP_AIN2: (1, 2),
        NRF_COMP_LPCOMP_AIN3: (1, 3),
        NRF_COMP_LPCOMP_AIN4: (1, 4),
        NRF_COMP_LPCOMP_AIN5: (1, 5),
        NRF_COMP_LPCOMP_AIN6: (1, 6),
        NRF_COMP_LPCOMP_AIN7: (1, 7),
    }
}


def dt_lookup_comp_lpcomp_pins(comp_lpcomp: edtlib.Node) -> List[Tuple[int, int]]:
    lut = _COMP_LPCOMP_LOOKUP

    address = comp_lpcomp.regs[0].addr | (1 << AddressOffset.SECURITY)
    if address not in lut:
        return []

    pins = []

    if "psel" in comp_lpcomp.props:
        psel = lut[address].get(comp_lpcomp.props["psel"].val)
        if psel:
            log_dbg(f"{address=:08x}, psel -> {psel=}")
            pins.append(psel)

    if "extrefsel" in comp_lpcomp.props:
        extrefsel = lut[address].get(comp_lpcomp.props["extrefsel"].val)
        if extrefsel:
            log_dbg(f"{address=:08x}, extrefsel -> {extrefsel=}")
            pins.append(extrefsel)

    return pins


@dc.dataclass
class HardwareId:
    part_code: int
    revision: int


_HARDWARE_ID_LOOKUP = {
    Product.NRF54H20: HardwareId(part_code=0x16, revision=0x2),
    Product.NRF9280: HardwareId(part_code=0x12, revision=0x1),
}


def lookup_hardware_id(product: Product) -> HardwareId:
    """
    Look up hardware ID information based on a product.

    :param product: Product.

    :return: Hardware ID information.
    """
    return _HARDWARE_ID_LOOKUP[product]
