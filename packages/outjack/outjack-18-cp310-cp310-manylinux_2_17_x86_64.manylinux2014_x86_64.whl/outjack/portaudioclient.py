# Copyright 2017, 2020 Andrzej Cichocki

# This file is part of outjack.
#
# outjack is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# outjack is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with outjack.  If not, see <http://www.gnu.org/licenses/>.

from . import cportaudio

class PortAudioClient:

    def __init__(self, chancount, outputrate, buffersize, ringsize, coupling):
        self.chancount = chancount
        self.outputrate = outputrate
        self.buffersize = buffersize
        self.ringsize = ringsize
        self.coupling = coupling

    def start(self):
        self.portaudio = cportaudio.Client(self.chancount, self.outputrate, self.buffersize, self.ringsize, self.coupling)

    def activate(self):
        self.portaudio.activate()

    def current_output_buffer(self):
        return self.portaudio.current_output_buffer()

    def send_and_get_output_buffer(self):
        return self.portaudio.send_and_get_output_buffer()

    def deactivate(self):
        self.portaudio.deactivate()

    def stop(self):
        self.portaudio.dispose()
