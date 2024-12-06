# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Child DCpsu Module of Keysightn6705c."""

from py_lab_hal.cominterface import cominterface
from py_lab_hal.instrument import instrument
from py_lab_hal.instrument.common.keysight import keysight_n6705c
from py_lab_hal.instrument.dcpsu import dcpsu


class KeysightN6705c(keysight_n6705c.KeysightN6705c, dcpsu.DCpsu):
  """Child DCpsu Class of Keysightn6705c."""

  def __init__(
      self,
      com: cominterface.ComInterfaceClass,
      inst_config: instrument.InstrumentConfig,
  ) -> None:
    keysight_n6705c.KeysightN6705c.__init__(self, com, inst_config)

  def open_instrument(self):
    super().open_instrument()
    super().select_mode(
        self.inst_config.channel, instrument.SmuEmulationMode.PS1Q
    )

  def set_OVP_value(self, channel, ovp_voltage):
    if ovp_voltage < 0:
      raise RuntimeError('Voltage can not be less than 0')
    super().set_OVP_value(channel, ovp_voltage)

  def set_NPLC(self, channel, power_line_freq, nplc):
    pass

  def set_sequence(self, channel, voltage, current, delay):
    pass

  def set_output_current(self, channel, current):
    self.set_level(channel, instrument.ChannelMode.CURRENT_DC, current)

  def set_output_voltage(self, channel, voltage):
    self.set_level(channel, instrument.ChannelMode.VOLTAGE_DC, voltage)
