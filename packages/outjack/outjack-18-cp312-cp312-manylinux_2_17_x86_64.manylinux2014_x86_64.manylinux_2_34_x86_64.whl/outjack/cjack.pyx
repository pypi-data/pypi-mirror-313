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

from .jack cimport *
from .ring cimport getaddress, Payload
from cpython.ref cimport PyObject
from libc.stdint cimport uintptr_t
import numpy as pynp

cdef int callback(jack_nframes_t nframes, void* arg) noexcept:
    cdef Payload payload = <Payload> arg
    payload.callback(nframes, NULL)
    return 0 # Success.

cdef void* _get_buffer(uintptr_t port, jack_nframes_t nframes, void* callbackinfo) noexcept nogil:
    return jack_port_get_buffer(<jack_port_t*> port, nframes)

cdef class Client:

    cdef jack_client_t* client
    cdef size_t buffersize
    cdef object outbufs
    cdef Payload payload # This is a pointer in C.
    cdef unsigned writecursorproxy

    def __init__(self, const char* client_name, chancount, ringsize, coupling):
        self.client = jack_client_open(client_name, JackNullOption, NULL)
        if NULL == self.client:
            raise Exception('Failed to create a JACK client.')
        self.buffersize = jack_get_buffer_size(self.client)
        self.outbufs = [pynp.empty(chancount * self.buffersize, dtype = pynp.float32) for _ in xrange(ringsize)]
        self.payload = Payload(chancount, self.buffersize, ringsize, coupling)
        self.payload.get_buffer = &_get_buffer
        self.writecursorproxy = self.payload.writecursor
        # Note the pointer stays valid until Client is garbage-collected:
        jack_set_process_callback(self.client, &callback, <PyObject*> self.payload)

    def get_sample_rate(self):
        return jack_get_sample_rate(self.client)

    def get_buffer_size(self):
        return self.buffersize

    def port_register_output(self, const char* port_name):
        # Last arg ignored for JACK_DEFAULT_AUDIO_TYPE:
        for portindex in xrange(self.payload.portcount):
            if (<void*> self.payload.ports[portindex]) == NULL:
                self.payload.ports[portindex] = <uintptr_t> jack_port_register(self.client, port_name, JACK_DEFAULT_AUDIO_TYPE, JackPortIsOutput, 0)
                return
        raise Exception('No more ports.')

    def activate(self):
        return jack_activate(self.client)

    def connect_name(self, const char* source_port_name, const char* destination_port_name):
        return jack_connect(self.client, source_port_name, destination_port_name)

    def connect_index(self, source_port_index, const char* destination_port_name):
        return jack_connect(self.client, jack_port_name(<jack_port_t*> self.payload.ports[source_port_index]), destination_port_name)

    def current_output_buffer(self):
        return self.outbufs[self.writecursorproxy]

    def send_and_get_output_buffer(self):
        cdef jack_default_audio_sample_t* samples = getaddress(self.current_output_buffer())
        self.writecursorproxy = self.payload.send(samples) # May block until there is a free buffer.
        return self.current_output_buffer()

    def deactivate(self):
        jack_deactivate(self.client)

    def dispose(self):
        jack_client_close(self.client)
