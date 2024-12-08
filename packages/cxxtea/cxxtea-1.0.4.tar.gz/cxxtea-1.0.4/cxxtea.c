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

#define MX (((z >> 5 ^ y << 2) + (y >> 3 ^ z << 4)) ^ ((sum ^ y) + (k[(p & 3) ^ e] ^ z)))

typedef uint8_t byte;
typedef uint32_t uint;

static PyObject* _long2bytes(uint* v, int length, int w) {
    int n = (length - 1) << 2;
    if (w) {
        int m = v[length - 1];
        if ((m < n - 3) || (m > n)) {
            Py_RETURN_NONE;
        }
        n = m;
    }

    PyObject* result = PyBytes_FromStringAndSize(NULL, n);
    if (!result) return NULL;

    byte* s = (byte*)PyBytes_AsString(result);
    if (!s) {
        Py_DECREF(result);
        return NULL;
    }
    memcpy(s, v, n);

    return result;
}

static uint* _bytes2long(const char* s, int len, int* out_len) {
    int m = ((4 - (len & 3)) & 3) + len;
    uint* v = (uint*)malloc(m);
    if (!v) return NULL;
    memcpy(v, s, len);
    memset((char*)v + len, 0, m - len);

    *out_len = m >> 2;
    return v;
}

static PyObject* decrypt(PyObject* self, PyObject* args) {
    const char *data_buf, *sign_buf, *key_buf;
    Py_ssize_t dlen, slen, klen;
    uint _DELTA = 0x9e3779b9;
    int delend = 1;
    uint y, z, sum;
    int p, e, v_len, k_len, n, q;
    uint* v = NULL;
    uint* k = NULL; 

    PyObject *result = NULL;

    if (!PyArg_ParseTuple(args, "y#y#y#|Ip", 
                          &data_buf, &dlen, 
                          &sign_buf, &slen, 
                          &key_buf, &klen, 
                          &_DELTA, &delend))
        return NULL;

    if (dlen == 0) {
        result = PyBytes_FromStringAndSize("", 0);
        goto cleanup;
    }

    if (slen > 0 && (dlen < slen || memcmp(data_buf, sign_buf, slen) != 0)) {
        result = PyBytes_FromStringAndSize("", 0);
        goto cleanup;
    }

    v = _bytes2long(data_buf + slen, dlen - slen, &v_len);
    if (!v) {
        result = PyBytes_FromStringAndSize("", 0);
        goto cleanup;
    }

    k = _bytes2long(key_buf, 16, &k_len);
    if (!k) {
        result = PyBytes_FromStringAndSize("", 0);
        goto cleanup;
    }

    n = v_len - 1;
    y = v[0];
    q = 6 + 52 / (n + 1);
    sum = q * _DELTA;

    do {
        e = (sum >> 2) & 3;
        for (p = n; p > 0; p--) {
            z = v[p - 1];
            v[p] -= MX;
            y = v[p];
        }
        z = v[n];
        v[0] -= MX;
        y = v[0];
        sum -= _DELTA;
    } while (--q);

    result = _long2bytes(v, v_len, delend);

cleanup:
    if (v) free(v);
    if (k) free(k);

    return result;
}

static PyMethodDef CxxteaMethods[] = {
    {"decrypt", (PyCFunction)decrypt, METH_VARARGS, "Decrypt XXTEA"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef cxxteamodule = {
    PyModuleDef_HEAD_INIT,
    "cxxtea",
    NULL,
    -1,
    CxxteaMethods
};

PyMODINIT_FUNC PyInit_cxxtea(void) {
    return PyModule_Create(&cxxteamodule);
}
