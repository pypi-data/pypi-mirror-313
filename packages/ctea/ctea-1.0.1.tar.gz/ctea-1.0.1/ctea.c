/*
 * Copyright (c) 2014-2024, Wood
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without modification,
 * are permitted provided that the following conditions are met:
 *
 *     * Redistributions of source code must retain the above copyright notice,
 *       this list of conditions and the following disclaimer.
 *     * Redistributions in binary form must reproduce the above copyright notice,
 *       this list of conditions and the following disclaimer in the documentation
 *       and/or other materials provided with the distribution.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
 * ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
 * WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
 * DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
 * FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
 * DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
 * SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
 * CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
 * OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
 * OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 *
 */

#include <Python.h>
#include <stdint.h>

typedef uint8_t  byte;
typedef uint32_t uint;
static const uint const1 = 0x61C88647;

static uint bswap32(uint x) {
    return ((x & 0xFF) << 24) | ((x & 0xFF00) << 8) | ((x >> 8) & 0xFF00) | ((x >> 24) & 0xFF);
}

static void dectea(byte *result, int v2, int v3) {
    uint v4, v5, v6;
    v4 = bswap32(*(uint *)(result + v2));
    v5 = bswap32(*(uint *)(result + v3));
    v6 = 3337565984;

    for (int i = 32; i > 0; i--) {
        v5 = v5 - (((v4 >> 5) - 1580959241) ^ (16 * v4 + 1901764813) ^ (v4 + v6));
        v4 = v4 - ((16 * v5 - 1784187092) ^ (v6 + v5) ^ ((v5 >> 5) - 1658011373));
        v6 = v6 + const1;
    }

    *(uint *)(result + v2) = bswap32(v4);
    *(uint *)(result + v3) = bswap32(v5);
}

static void decdata(byte *data, int dlen) {
    int i, count;
    count = (dlen / 8) * 8;
    if (count > 0) {
        for (i = 0; i < count; i+= 8)
            dectea(data, i, i+4);
    }
}

static PyObject* decrypt(PyObject* self, PyObject* args) {
    Py_buffer data;
    if (!PyArg_ParseTuple(args, "y*", &data)) {
        return NULL;
    }
    int length = (int)data.len;
    decdata((byte *)data.buf, length);
    
    PyBuffer_Release(&data);
    Py_RETURN_NONE;
}

static PyMethodDef TeaMethods[] = {
    {"decrypt", (PyCFunction)decrypt, METH_VARARGS, "Decrypt TEA"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef cteamoudule = {
    PyModuleDef_HEAD_INIT,
    "ctea",
    NULL,
    -1,
    TeaMethods
};

PyMODINIT_FUNC PyInit_ctea(void) {
    return PyModule_Create(&cteamoudule);
}
