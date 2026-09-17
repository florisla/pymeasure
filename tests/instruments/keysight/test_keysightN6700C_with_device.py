#
# This file is part of the PyMeasure package.
#
# Copyright (c) 2013-2026 PyMeasure Developers
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#

import pytest

from pymeasure.instruments.keysight.keysightN6700C import KeysightN6700C


@pytest.fixture(scope="module")
def power_supply(connected_device_address):
    instr = KeysightN6700C(connected_device_address)
    instr.reset()
    return instr


@pytest.fixture(scope="module")
def power_supply_channel(power_supply):
    return power_supply.ch_1


class TestKeysightN6700C:
    """
    Unit tests for KeysightN6700C class.

    This test suite, needs the following setup to work properly:
        - A KeysightN6700C device should be connected.
        - The N6700C should have a power supply module fitted in slot 1.
          Tested with a N6731B.
        - The device's address must be passed to pytest with --device-address="".
    """

    #########################
    # PARAMETRIZATION CASES #
    #########################

    BOOLEANS = [False, True]

    #########
    # TESTS #
    #########

    @pytest.mark.parametrize("case", BOOLEANS)
    def test_output_enabled(self, power_supply_channel, case):
        assert not power_supply_channel.output_enabled
        power_supply_channel.output_enabled = case
        assert power_supply_channel.output_enabled == case

    def test_current_limit_out_of_range(self, power_supply_channel):
        with pytest.raises(ValueError, match=f"Value of 21 is not in range"):
            power_supply_channel.current_limit = 21

    @pytest.mark.parametrize("voltage", (0.050, 1.0, 2.0))
    def test_voltage_setpoint(self, power_supply_channel, voltage):
        # Note: N67* power modules (not SMUs) do not support 0.000 V setpoint.
        # Setpoint will be clipped at lowest value (e.g. 15 mV for N6731B).
        power_supply_channel.voltage_setpoint = voltage
        assert power_supply_channel.voltage_setpoint == voltage

    def test_voltage_setpoint_out_of_range(self, power_supply_channel):
        with pytest.raises(ValueError, match=f"Value of 151 is not in range"):
            power_supply_channel.voltage_setpoint = 151.0

    def test_measure_voltage(self, power_supply_channel):
        assert isinstance(power_supply_channel.voltage, float)

    def test_measure_current(self, power_supply_channel):
        assert isinstance(power_supply_channel.current, float)
