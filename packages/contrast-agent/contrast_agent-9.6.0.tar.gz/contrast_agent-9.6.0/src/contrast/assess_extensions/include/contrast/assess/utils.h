/*
 * Copyright © 2024 Contrast Security, Inc.
 * See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
 */
#ifndef _ASSESS_UTILS_H_
#define _ASSESS_UTILS_H_
/* Python requires its own header to always be included first */
#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include <contrast/assess/logging.h>
#include <contrast/assess/patches.h>

typedef PyObject *(*fastcall_method)(PyObject *, PyObject *const *, Py_ssize_t);
typedef PyObject *(*ternary_fastcall_method)(
    PyObject *, PyObject *const *, Py_ssize_t, PyObject *);

static inline PyObject *pack_args_tuple(PyObject *const *args, Py_ssize_t nargs) {
    PyObject *hook_args = PyList_New(0);
    Py_ssize_t i;

    for (i = 0; i < nargs; i++) {
        PyList_Append(hook_args, args[i]);
    }

    return hook_args;
}

static inline PyObject *pack_kwargs_dict(
    PyObject *const *args, Py_ssize_t nargs, PyObject *kwnames) {
    PyObject *kwargs = PyDict_New();
    PyObject *name;
    Py_ssize_t i;

    if (kwnames == NULL)
        goto cleanup_and_exit;

    for (i = 0; i < PySequence_Size(kwnames); i++) {
        name = PySequence_GetItem(kwnames, i);
        PyDict_SetItem(kwargs, name, args[i + nargs]);
        Py_DECREF(name);
    }

cleanup_and_exit:
    return kwargs;
}

#define HOOK_UNARYFUNC(NAME)                                                  \
    static PyObject *NAME##_new(PyObject *self) {                             \
        PyObject *result = NAME##_orig(self);                                 \
                                                                              \
        if (result == NULL)                                                   \
            return result;                                                    \
                                                                              \
        call_string_propagator("propagate_" #NAME, self, result, NULL, NULL); \
                                                                              \
        return result;                                                        \
    }

#define HOOK_BINARYFUNC(NAME)                                                 \
    static PyObject *NAME##_new(PyObject *self, PyObject *args) {             \
        PyObject *result = NAME##_orig(self, args);                           \
                                                                              \
        if (result == NULL)                                                   \
            return result;                                                    \
                                                                              \
        call_string_propagator("propagate_" #NAME, self, result, args, NULL); \
                                                                              \
        return result;                                                        \
    }

#define HOOK_STREAM_UNARYFUNC(NAME, EVENT)                 \
    static PyObject *NAME##_new(PyObject *self) {          \
        PyObject *result = NAME##_orig(self);              \
                                                           \
        if (result == NULL)                                \
            return result;                                 \
                                                           \
        propagate_stream(EVENT, self, result, NULL, NULL); \
                                                           \
        return result;                                     \
    }

#define HOOK_STREAM_BINARYFUNC(NAME, EVENT)                       \
    static PyObject *NAME##_new(PyObject *self, PyObject *args) { \
        PyObject *result = NAME##_orig(self, args);               \
                                                                  \
        if (result == NULL)                                       \
            return result;                                        \
                                                                  \
        propagate_stream(EVENT, self, result, args, NULL);        \
                                                                  \
        return result;                                            \
    }

#define HOOK_STREAM_FASTCALL(NAME, EVENT)                                           \
    PyObject *NAME##_new(PyObject *self, PyObject *const *args, Py_ssize_t nargs) { \
        PyObject *hook_args = pack_args_tuple(args, nargs);                         \
        if (hook_args == NULL)                                                      \
            PyErr_Clear();                                                          \
                                                                                    \
        PyObject *result = NAME##_orig(self, args, nargs);                          \
                                                                                    \
        if (result == NULL || hook_args == NULL)                                    \
            goto cleanup_and_exit;                                                  \
                                                                                    \
        propagate_stream(EVENT, self, result, hook_args, NULL);                     \
                                                                                    \
    cleanup_and_exit:                                                               \
        Py_XDECREF(hook_args);                                                      \
        return result;                                                              \
    }

#define ADD_STREAM_HOOK(TYPE, NAME, OFFSET)                 \
    NAME##_orig = (void *)TYPE->tp_methods[OFFSET].ml_meth; \
    TYPE->tp_methods[OFFSET].ml_meth = (void *)NAME##_new;

#define REVERSE_STREAM_HOOK(TYPE, NAME, OFFSET) \
    TYPE->tp_methods[OFFSET].ml_meth = (void *)NAME##_orig;

#endif /* _ASSESS_UTILS_H_ */
