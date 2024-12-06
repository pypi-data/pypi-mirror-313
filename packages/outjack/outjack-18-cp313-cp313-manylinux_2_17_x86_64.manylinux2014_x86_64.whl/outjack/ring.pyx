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

from libc.stdint cimport uintptr_t
from libc.stdio cimport fprintf, stderr
from libc.stdlib cimport malloc
from libc.string cimport memcpy
cimport numpy as np

cdef np.float32_t* getaddress(np.ndarray[np.float32_t, ndim=1] samples):
    return &samples[0]

cdef class Payload:

    def __init__(self, portcount, buffersize, ringsize, coupling):
        self.ports = <uintptr_t*> malloc(portcount * sizeof (uintptr_t))
        for portindex in xrange(portcount):
            self.ports[portindex] = <uintptr_t> NULL
        pthread_mutex_init(&(self.mutex), NULL)
        pthread_cond_init(&(self.cond), NULL)
        self.ringsize = ringsize
        self.chunks = <ring_sample_t**> malloc(self.ringsize * sizeof (ring_sample_t*))
        for i in xrange(self.ringsize):
            self.chunks[i] = NULL
        self.writecursor = 0
        self.readcursor = 0
        self.bufferbytes = buffersize * sizeof (ring_sample_t)
        self.portcount = portcount
        self.buffersize = buffersize
        self.coupling = coupling

    cdef unsigned send(self, ring_sample_t* samples):
        pthread_mutex_lock(&(self.mutex))
        self.chunks[self.writecursor] = samples # It was NULL.
        self.writecursor = (self.writecursor + 1) % self.ringsize
        # Allow callback to see the data before releasing slot to the producer:
        if self.chunks[self.writecursor] != NULL:
            if not self.coupling:
                fprintf(stderr, "%s\n", <char*> 'Overrun!') # The producer is too fast.
            # There is only one consumer, but we use while to catch spurious wakeups:
            while self.chunks[self.writecursor] != NULL:
                with nogil:
                    pthread_cond_wait(&(self.cond), &(self.mutex))
        pthread_mutex_unlock(&(self.mutex))
        return self.writecursor

    cdef void callback(self, ring_nframes_t nframes, void* callbackinfo) noexcept nogil:
        # This is a Python-free zone!
        pthread_mutex_lock(&(self.mutex)) # Worst case is a tiny delay while we wait for send to finish.
        cdef ring_sample_t* samples = self.chunks[self.readcursor]
        if samples != NULL:
            for portindex in xrange(self.portcount):
                memcpy(self.get_buffer(self.ports[portindex], nframes, callbackinfo), samples, self.bufferbytes)
                samples = &samples[self.buffersize]
            self.chunks[self.readcursor] = NULL
            self.readcursor = (self.readcursor + 1) % self.ringsize
            pthread_cond_signal(&(self.cond))
        else:
            # Unknown when send will run, so give up:
            fprintf(stderr, "%s\n", <char*> 'Underrun!')
        pthread_mutex_unlock(&(self.mutex))
