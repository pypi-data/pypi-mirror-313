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

# cython: language_level=3

from .portaudio cimport *
from .ring cimport getaddress, Payload, ring_nframes_t
from cpython.ref cimport PyObject
from libc.stdint cimport uintptr_t
cimport numpy as np
import numpy as pynp

cdef int callback(const void* input, void* output, unsigned long frameCount, const PaStreamCallbackTimeInfo* timeInfo, PaStreamCallbackFlags statusFlags, void* userData) noexcept:
    cdef Payload payload = <Payload> userData
    payload.callback(frameCount, output)
    return paContinue

cdef void* _get_buffer(uintptr_t port, ring_nframes_t nframes, void* callbackinfo) noexcept nogil:
    return (<void**> callbackinfo)[port]

cdef class Client:

    cdef PaStream* stream
    cdef object outbufs
    cdef Payload payload
    cdef unsigned writecursorproxy
    cdef int chancount
    cdef double outputrate
    cdef unsigned long buffersize

    def __init__(self, chancount, outputrate, buffersize, ringsize, coupling):
        Pa_Initialize()
        self.outbufs = [pynp.empty(chancount * buffersize, dtype = pynp.float32) for _ in xrange(ringsize)]
        self.payload = Payload(chancount, buffersize, ringsize, coupling)
        self.payload.get_buffer = &_get_buffer
        for portindex in xrange(chancount):
            self.payload.ports[portindex] = portindex
        self.writecursorproxy = self.payload.writecursor
        self.chancount = chancount
        self.outputrate = outputrate
        self.buffersize = buffersize

    def activate(self):
        Pa_OpenDefaultStream(&self.stream, 0, self.chancount, paFloat32 | paNonInterleaved, self.outputrate, self.buffersize, &callback, <PyObject*> self.payload)
        Pa_StartStream(self.stream)

    def current_output_buffer(self):
        return self.outbufs[self.writecursorproxy]

    def send_and_get_output_buffer(self):
        cdef np.float32_t* samples = getaddress(self.current_output_buffer())
        self.writecursorproxy = self.payload.send(samples) # May block until there is a free buffer.
        return self.current_output_buffer()

    def deactivate(self):
        Pa_StopStream(self.stream)
        Pa_CloseStream(self.stream)

    def dispose(self):
        Pa_Terminate()
