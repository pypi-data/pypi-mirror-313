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

#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

typedef uint8_t byte;

void decrypt(byte* buffer, int size, int key0, int key1, int key2) {
    for (int i = 0; i < size; i++) {
        buffer[i] ^= (byte)((key0 ^ key1 ^ key2) >> 24);
        key0 = key0 * 214013 + 2531011;
        key1 = key1 * 214013 + 2531011;
        key2 = key2 * 214013 + 2531011;
    }
}

static PyObject* py_decrypt(PyObject* self, PyObject* args, PyObject* kwargs) {
    const char *data;
    Py_ssize_t dlen;

    int key0 = 698;
    int key1 = 927;
    int key2 = 2174;

    static char *kwlist[] = {"data", "key0", "key1", "key2", NULL};

    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "y#|iii", kwlist, &data, &dlen, &key0, &key1, &key2)) {
        return NULL;
    }

    byte* darr = (byte*)malloc(dlen);
    if (darr == NULL) {
        PyErr_NoMemory();
        return NULL;
    }

    memcpy(darr, data, dlen);
    decrypt(darr, (int)dlen, key0, key1, key2);

    PyObject* result = PyBytes_FromStringAndSize((const char*)darr, dlen);
    free(darr);

    return result;
}

static PyMethodDef CBBSMethods[] = {
    {"decrypt", (PyCFunction)py_decrypt, METH_VARARGS | METH_KEYWORDS, "Decrypt data"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef cbbsmodule = {
    PyModuleDef_HEAD_INIT,
    "cbbs",
    NULL,
    -1,
    CBBSMethods
};

PyMODINIT_FUNC PyInit_cbbs(void) {
    return PyModule_Create(&cbbsmodule);
}
