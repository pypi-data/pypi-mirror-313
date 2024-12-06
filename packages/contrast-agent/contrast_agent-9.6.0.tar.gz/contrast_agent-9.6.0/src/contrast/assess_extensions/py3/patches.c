/*
 * Copyright © 2024 Contrast Security, Inc.
 * See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
 */
/* Python requires its own header to always be included first */
#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include <contrast/assess/patches.h>
#include <contrast/assess/scope.h>
#include <contrast/assess/intern.h>
#include <contrast/assess/logging.h>
#include <contrast/assess/trace.h>

static PyMethodDef methods[] = {
    {"initialize_logger",
     (PyCFunction)initialize_logger,
     METH_VARARGS | METH_KEYWORDS,
     "Initialize C extension logger"},
    {"initialize",
     (PyCFunction)initialize,
     METH_NOARGS,
     "Initialize C extension patcher"},
    {"enable_required_hooks",
     enable_required_hooks,
     METH_NOARGS,
     "Hook relevant non-method functions"},
    {"initialize_trace",
     initialize_trace,
     METH_NOARGS,
     "Initialize trace for string propagation"},
    {"disable", disable, METH_NOARGS, "Remove all hooks"},
    {"get_tp_version_tag", get_tp_version_tag, METH_O, "Get tp_version_tag for a type"},
    {"set_attr_on_type", set_attr_on_type, METH_VARARGS, "Set attribute on type"},
    {"is_string_interned", is_string_interned, METH_O, "Checks if string is interned"},
    {NULL, NULL, 0, NULL}};

static struct PyModuleDef cs_str_definition = {
    PyModuleDef_HEAD_INIT,
    "cs_str",
    "description here",
    -1,
    methods,
    NULL,
    NULL,
    NULL,
    NULL};

PyMODINIT_FUNC PyInit_cs_str(void) {
    PyObject *module;

    Py_Initialize();

    module = PyModule_Create(&cs_str_definition);

    if (PyModule_AddIntConstant(
            module,
            "DEBUG",
#ifdef ASSESS_DEBUG
            1
#else
            0
#endif
            ) != 0) {
        PyErr_Print();
        PyErr_SetString(PyExc_RuntimeError, "Failed to add debug constant");
    }

    PyModule_AddIntMacro(module, Py_TPFLAGS_HEAPTYPE);
#if PY_MINOR_VERSION > 9
    PyModule_AddIntMacro(module, Py_TPFLAGS_IMMUTABLETYPE);
#endif

    PyObject *py_scope = PyImport_ImportModule("contrast.agent.scope");
    if (py_scope == NULL) {
        PyErr_Print();
        PyErr_SetString(PyExc_RuntimeError, "Failed to import contrast.agent.scope");
        return NULL;
    }

    PyObject *contrast_scope = PyObject_GetAttrString(py_scope, "CONTRAST_SCOPE");
    PyObject *propagation_scope = PyObject_GetAttrString(py_scope, "PROPAGATION_SCOPE");
    PyObject *trigger_scope = PyObject_GetAttrString(py_scope, "TRIGGER_SCOPE");

    if (contrast_scope == NULL || propagation_scope == NULL || trigger_scope == NULL) {
        PyErr_Print();
        PyErr_SetString(
            PyExc_RuntimeError, "Failed to get scope vars from contrast.agent.scope");
        return NULL;
    }

    init_contrast_scope_cvars(contrast_scope, propagation_scope, trigger_scope);

    return module;
}
