/*
 * Copyright © 2024 Contrast Security, Inc.
 * See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
 */
#ifndef _ASSESS_TRACE_H_
#define _ASSESS_TRACE_H_

/* Python requires its own header to always be included first */
#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <opcode.h>

PyObject *initialize_trace(PyObject *self, PyObject *arg);

#endif /* _ASSESS_TRACE_H_ */
