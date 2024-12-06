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
cimport numpy as np

cdef extern from "pthread.h":

    ctypedef struct pthread_mutex_t:
        pass

    ctypedef struct pthread_cond_t:
        pass

    int pthread_mutex_init(pthread_mutex_t*, void*)
    int pthread_mutex_lock(pthread_mutex_t*) nogil
    int pthread_mutex_unlock(pthread_mutex_t*) nogil
    int pthread_cond_init(pthread_cond_t*, void*)
    int pthread_cond_signal(pthread_cond_t*) nogil
    int pthread_cond_wait(pthread_cond_t*, pthread_mutex_t*) nogil

ctypedef np.float32_t ring_sample_t

ctypedef np.uint32_t ring_nframes_t

cdef np.float32_t* getaddress(np.ndarray[np.float32_t, ndim=1] samples)

cdef class Payload:

    cdef uintptr_t* ports
    cdef pthread_mutex_t mutex
    cdef pthread_cond_t cond
    cdef unsigned ringsize
    cdef ring_sample_t** chunks
    cdef unsigned writecursor # Always points to a free chunk.
    cdef unsigned readcursor
    cdef size_t bufferbytes
    cdef size_t portcount
    cdef size_t buffersize
    cdef bint coupling
    cdef void* (*get_buffer)(uintptr_t, ring_nframes_t, void*) noexcept nogil

    cdef unsigned send(self, ring_sample_t* samples)

    cdef void callback(self, ring_nframes_t nframes, void* callbackinfo) noexcept nogil
