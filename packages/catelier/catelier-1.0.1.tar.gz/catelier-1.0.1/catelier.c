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
#include <stdlib.h>
#include <string.h>

typedef uint8_t  byte;
typedef uint32_t uint;
typedef uint64_t uint64;
typedef int32_t int32;

static inline uint Unpack(byte *barray, int index) {
    return (barray[index] | (barray[index + 1] << 8) | (barray[index + 2] << 16) | (barray[index + 3] << 24));
}

static inline uint RotateRight(uint value, int32 shift) {
    return (value >> shift) | (value << (32 - shift));
}

static void QuarterRound(uint *x, int a, int b, int c, int d) {
    x[a] += x[b];
    x[d] ^= x[a];
    x[d] = (x[d] << 16) | (x[d] >> 16);
    x[c] += x[d];
    x[b] ^= x[c];
    x[b] = (x[b] << 12) | (x[b] >> 20);
    x[a] += x[b];
    x[d] ^= x[a];
    x[d] = (x[d] << 8) | (x[d] >> 24);
    x[c] += x[d];
    x[b] ^= x[c];
    x[b] = (x[b] << 7) | (x[b] >> 25);
}

static void DoRound(byte *output, byte *iv, int rounds, uint *state) {
    uint x[16];
    uint y[16];
    int i;

    for (i = 0; i < 16; i++) {
        x[i] = state[i] ^ ((uint)iv[i * 4] |
                           ((uint)iv[i * 4 + 1] << 8) |
                           ((uint)iv[i * 4 + 2] << 16) |
                           ((uint)iv[i * 4 + 3] << 24));
        y[i] = x[i];
    }

    for (i = rounds; i > 0; i -= 2) {
        QuarterRound(x, 0, 4, 8, 12);
        QuarterRound(x, 1, 5, 9, 13);
        QuarterRound(x, 2, 6, 10, 14);
        QuarterRound(x, 3, 7, 11, 15);
        QuarterRound(x, 0, 5, 10, 15);
        QuarterRound(x, 1, 6, 11, 12);
        QuarterRound(x, 2, 7, 8, 13);
        QuarterRound(x, 3, 4, 9, 14);
    }

    for (i = 0; i < 16; i++) {
        uint sum = x[i] + y[i];
        output[i * 4] = (byte)sum;
        output[i * 4 + 1] = (byte)(sum >> 8);
        output[i * 4 + 2] = (byte)(sum >> 16);
        output[i * 4 + 3] = (byte)(sum >> 24);
    }

    state[12] += 1;
    if (state[12] == 0) {
        state[13] += 1;
    }
}

static void generate_key(byte *context, uint *key, byte *nonce_seed_bytes, int counter) {
    uint nonceSeedPart0High, nonceSeedPart0Low, nonceSeedPart1, nonceSeedPart2, nonceSeed;
    uint state[16];
    byte iv[64];
    int i;
    int rounds[8] = {12, 8, 8, 8, 4, 4, 4, 4};

    nonceSeedPart0High = Unpack(nonce_seed_bytes, (counter % 0xD) | 0x30);
    nonceSeedPart0Low = Unpack(nonce_seed_bytes, (counter / 0xD) % 0xD);
    nonceSeedPart1 = Unpack(nonce_seed_bytes, ((counter / 0xA9) % 0xD) | 0x10);
    nonceSeedPart2 = Unpack(nonce_seed_bytes, ((counter / 0x895) % 0xD) | 0x20);

    nonceSeed = RotateRight(nonceSeedPart0High, 0x1C * (int32)((0x24924925 * (uint64)((counter / 0x152) & 0x3FFFFFFF)) >> 32) - 2 * (counter / 0xA9)) ^
                RotateRight(nonceSeedPart0Low, -(3 * (counter / 0x93E) % 0x1B));

    state[0] = 1634760805;
    state[1] = 857760878;
    state[2] = 2036477234;
    state[3] = 1797285236;
    for (i = 0; i < 8; i++) {
        state[4 + i] = key[i];
    }
    state[12] = counter + 1;
    state[13] = nonceSeed;
    state[14] = nonceSeed ^ nonceSeedPart1;
    state[15] = state[14] ^ nonceSeedPart2;

    for (i = 0; i < 8; i++) {
        if (i == 0) {
            memset(iv, 0, 64);
        } else {
            memcpy(iv, &context[(i - 1) * 64], 64);
        }
        DoRound(&context[i * 64], iv, rounds[i], state);
    }
}

static void decrypt(byte *data, int dlen, uint *key, byte *nonce_seed_bytes) {
    int blocklen = 0x200;
    int count, count2, counter, dataIndex;
    byte *array = (byte*)malloc(blocklen * sizeof(byte));
    int i, j;

    count = dlen / blocklen;
    count2 = dlen % blocklen;
    counter = 0;
    dataIndex = 0;

    if (count > 0) {
        for (i = 0; i < count; i++) {
            generate_key(array, key, nonce_seed_bytes, counter++);
            for (j = 0; j < blocklen; j++) {
                data[dataIndex++] ^= array[j];
            }
        }
    }
    if (count2 > 0) {
        generate_key(array, key, nonce_seed_bytes, counter++);
        for (i = 0; i < count2; i++) {
            data[dataIndex++] ^= array[i];
        }
    }

    free(array);
}

static PyObject* py_decrypt(PyObject* self, PyObject* args) {
    Py_buffer data;
    Py_buffer keyBytes;
    Py_buffer nonceSeed;
    PyObject *result;
    byte *darr, *narr;
    uint *karr;

    result = data.buf = keyBytes.buf = nonceSeed.buf = NULL;

    if (!PyArg_ParseTuple(args, "s*s*s*", &data, &keyBytes, &nonceSeed)) {
        return NULL;
    }

    darr = (byte*)data.buf;
    karr = (uint*)keyBytes.buf;
    narr = (byte*)nonceSeed.buf;

    decrypt(darr, (int)data.len, karr, narr);

    result = PyBytes_FromStringAndSize((const char *)darr, data.len);

    PyBuffer_Release(&data);
    PyBuffer_Release(&keyBytes);
    PyBuffer_Release(&nonceSeed);

    return result;
}

static PyMethodDef CAtelierMethods[] = {
    {"decrypt", (PyCFunction)py_decrypt, METH_VARARGS, "Decrypt data"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef cateliermodule = {
    PyModuleDef_HEAD_INIT,
    "catelier",
    NULL,
    -1,
    CAtelierMethods
};

PyMODINIT_FUNC PyInit_catelier(void) {
    return PyModule_Create(&cateliermodule);
}
