/*
 * Copyright © 2024 Contrast Security, Inc.
 * See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
 */
/* Python requires its own header to always be included first */
#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include <string.h>

#define STRING_CHECK(X) PyUnicode_Check(X)
#define COMPARE_NAME(X, Y) PyUnicode_CompareWithASCIIString(X, Y)

static PyObject *find_method_body(PyTypeObject *type, PyObject *args) {
    PyObject *name;
    PyMethodDef *method;

    if (!PyArg_ParseTuple(args, "O", &name))
        return NULL;

    if (!STRING_CHECK(name)) {
        PyErr_SetString(PyExc_TypeError, "string argument expected");
        return NULL;
    }

    for (int i = 0;; i++) {
        method = &(type->tp_methods[i]);
        if (method->ml_name == NULL)
            break;

        if (COMPARE_NAME(name, method->ml_name) != 0)
            continue;

        /* We found a matching name */
        return Py_BuildValue("ii", i, method->ml_flags);
    }

    Py_RETURN_NONE;
}

static PyObject *get_type_method_body(
    const char *modulename, const char *typename, PyObject *args) {
    PyObject *module = NULL;
    PyTypeObject *type = NULL;
    PyObject *result = NULL;

    if ((module = PyImport_ImportModule(modulename)) == NULL)
        goto cleanup_and_exit;

    if ((type = (PyTypeObject *)PyObject_GetAttrString(module, typename)) == NULL)
        goto cleanup_and_exit;

    result = find_method_body(type, args);

cleanup_and_exit:
    Py_XDECREF(module);
    Py_XDECREF(type);
    return result;
}

static PyObject *find_stringio_hook(PyObject *self, PyObject *args) {
    return get_type_method_body("io", "StringIO", args);
}

static PyObject *find_bytesio_hook(PyObject *self, PyObject *args) {
    return get_type_method_body("io", "BytesIO", args);
}

static PyObject *find_iobase_hook(PyObject *self, PyObject *args) {
    return get_type_method_body("_io", "_IOBase", args);
}

static void add_int_constants(PyObject *module) {
    PyModule_AddIntConstant(module, "METH_O", METH_O);
    PyModule_AddIntConstant(module, "METH_NOARGS", METH_NOARGS);
    PyModule_AddIntConstant(module, "METH_VARARGS", METH_VARARGS);
    PyModule_AddIntConstant(module, "METH_KEYWORDS", METH_KEYWORDS);
    PyModule_AddIntConstant(module, "METH_FASTCALL", METH_FASTCALL);
}

static PyMethodDef methods[] = {
    {"find_stringio_hook", find_stringio_hook, METH_VARARGS, "find stringio hook"},
    {"find_bytesio_hook", find_bytesio_hook, METH_VARARGS, "find bytesio hook"},
    {"find_iobase_hook", find_iobase_hook, METH_VARARGS, "find iobase hook"},
    {NULL, NULL, 0, NULL}};

static struct PyModuleDef hookspy_definition = {
    PyModuleDef_HEAD_INIT,
    "hookspy",
    "find method hooks for python string objects",
    -1,
    methods,
    NULL,
    NULL,
    NULL,
    NULL};

PyMODINIT_FUNC PyInit_hookspy(void) {
    PyObject *module;

    Py_Initialize();

    module = PyModule_Create(&hookspy_definition);
    add_int_constants(module);

    return module;
}
