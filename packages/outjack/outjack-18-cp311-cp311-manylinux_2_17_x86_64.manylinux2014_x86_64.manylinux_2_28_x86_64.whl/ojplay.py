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

'Usage example.'
__import__('pyrbo.jit')
from argparse import ArgumentParser
from outjack.jackclient import JackClient
from outjack.portaudioclient import PortAudioClient
import logging, numpy as np

log = logging.getLogger(__name__)
amplitude = .5
ringsize = 2

class Client:

    class jack(JackClient):

        def __init__(self):
            super().__init__('ojplay', 1, ringsize, True)

        def start(self):
            super().start()
            self.port_register_output('tone')

        def activate(self):
            super().activate()
            for sink in 'playback_1', 'playback_2': # TODO: Deduce these.
                self.connect(0, f"system:{sink}")

    class portaudio(PortAudioClient):

        def __init__(self):
            super().__init__(1, 44100, 1024, ringsize, True)

def main(): # FIXME: Do not play garbage at first.
    logging.basicConfig(format = "%(levelname)s %(message)s", level = logging.DEBUG)
    parser = ArgumentParser()
    parser.add_argument('--client', choices = [name for name in dir(Client) if '_' != name[0]], default = Client.portaudio.__name__)
    parser.add_argument('--frequency', type = float, default = 440)
    args = parser.parse_args()
    client = getattr(Client, args.client)()
    frequency = args.frequency
    client.start()
    try:
        buffersize = client.buffersize
        outputrate = client.outputrate
        log.debug(dict(buffersize = buffersize, outputrate = outputrate))
        client.activate()
        try:
            k = 0
            buffer = client.current_output_buffer()
            while True:
                buffer[:] = np.sin(np.arange(k, k + buffersize) * (2 * np.pi * frequency / outputrate)) * amplitude
                k += buffersize
                buffer = client.send_and_get_output_buffer()
        finally:
            client.deactivate()
    finally:
        client.stop()

if '__main__' == __name__:
    main()
