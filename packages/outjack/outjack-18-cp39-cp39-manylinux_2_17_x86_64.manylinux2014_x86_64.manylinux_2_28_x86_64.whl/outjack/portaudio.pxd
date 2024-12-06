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

cdef extern from "portaudio.h":

    cdef enum PaStreamCallbackResult:
        paContinue = 0

    ctypedef double PaTime

    ctypedef struct PaStreamCallbackTimeInfo:
        pass

    ctypedef int PaError

    ctypedef void PaStream

    ctypedef unsigned long PaSampleFormat

    ctypedef unsigned long PaStreamCallbackFlags

    ctypedef int PaStreamCallback(const void*, void*, unsigned long, const PaStreamCallbackTimeInfo*, PaStreamCallbackFlags, void*)

    cdef PaSampleFormat paFloat32 = 0x00000001

    cdef PaSampleFormat paNonInterleaved = 0x80000000

    PaError Pa_Initialize()
    PaError Pa_Terminate()
    PaError Pa_OpenDefaultStream(PaStream**, int, int, PaSampleFormat, double, unsigned long, PaStreamCallback*, void*)
    PaError Pa_StartStream(PaStream*)
    PaError Pa_StopStream(PaStream*)
    PaError Pa_CloseStream(PaStream*)
