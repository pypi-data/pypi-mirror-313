/*
 * Copyright © 2024 Contrast Security, Inc.
 * See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
 */
/* Python requires its own header to always be included first */
#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <opcode.h>

#include <contrast/assess/propagate.h>
#include <contrast/assess/scope.h>

/* XXX: for proof of concept purposes just ignore versions < 3.10 */
#if PY_MINOR_VERSION > 9
#if PY_MINOR_VERSION < 13 /* XXX: build breaks in 3.13 */

#if PY_MINOR_VERSION < 11

#define Py_CPYTHON_FRAMEOBJECT_H
#include <cpython/frameobject.h>
#undef Py_CPYTHON_FRAMEOBJECT_H

#define CO_CODE(frame) (frame)->f_code->co_code
#define LASTI(frame) (frame)->f_lasti
#define CHECK_BINARY_ADD(opcode, oparg) ((opcode) == BINARY_ADD)
#define CHECK_BINARY_IADD(opcode, oparg) ((opcode) == INPLACE_ADD)
#define CHECK_MODULO(opcode, oparg) ((opcode) == BINARY_MODULO)

// XXX: this probably won't work for PY_MINOR_VERSION < 10
#define PEEK_STACK(frame, pos) (frame)->f_valuestack[(frame)->f_stackdepth - (pos)-1]

#else

#include <internal/pycore_frame.h>

#define CO_CODE(frame) PyCode_GetCode((frame)->f_frame->f_code)
#define LASTI(frame) _PyInterpreterFrame_LASTI((frame)->f_frame)
#define CHECK_BINARY_ADD(opcode, oparg) ((opcode) == BINARY_OP && (oparg) == NB_ADD)
#define CHECK_BINARY_IADD(opcode, oparg) \
    ((opcode) == BINARY_OP && (oparg) == NB_INPLACE_ADD)
#define CHECK_MODULO(opcode, oparg) ((opcode) == BINARY_OP && (oparg) == NB_REMAINDER)

#define PEEK_STACK(frame, pos) \
    (frame)->f_frame->localsplus[(frame)->f_frame->stacktop - 1 - (pos)]

#endif /* #if PY_MINOR_VERSION < 11 */

/* XXX: this is not thread-safe or correct. It's just to enable the proof of concept */
// XXX: eventually we should implement this in C for speed
PyObject *stack = NULL;

#define DO_CFORMAT 0x80
#define DO_BINADD 0x40

#define POP(result, list)                    \
    result = PySequence_GetItem((list), -1); \
    PySequence_DelItem((list), -1);

static inline PyObject *pop(void) {
    PyObject *result = PySequence_GetItem(stack, -1);
    PySequence_DelItem(stack, -1);
    return result;
}

static int trace_trampoline(
    PyObject *self, PyFrameObject *frame, int what, PyObject *arg) {
    _Py_CODEUNIT *code_stream = NULL;
    PyObject *result = NULL;
    PyObject *left = NULL;
    PyObject *right = NULL;

    int opcode = 0;
#if PY_MINOR_VERSION > 10
    int oparg = 0;
#endif

    if (!(frame->f_trace_opcodes |= (char)should_propagate())) {
        return 0;
    }

    if (what == PyTrace_OPCODE) {
        if (frame->f_trace_opcodes & DO_BINADD) {
            right = pop();
            left = pop();

            // XXX PyUnicode_Check is too restrictive
            if (NULL != (result = PEEK_STACK(frame, 0)) && PyUnicode_Check(result)) {

                Py_INCREF(result);
                propagate_concat(left, right, result, "propagate_unicode_concat");
                Py_DECREF(result);
            }

            frame->f_trace_opcodes &= ~DO_BINADD;
            left = right = NULL;
        }

        if (frame->f_trace_opcodes & DO_CFORMAT) {
            right = pop();
            left = pop();

            // XXX PyUnicode_Check is too restrictive
            if (NULL != (result = PEEK_STACK(frame, 0)) && PyUnicode_Check(result)) {
                Py_INCREF(result);
                call_string_propagator(
                    "propagate_unicode_cformat", left, result, right, NULL);
                Py_DECREF(result);
            }

            frame->f_trace_opcodes &= ~DO_CFORMAT;
            left = right = NULL;
        }

        enter_contrast_scope();
        code_stream = (_Py_CODEUNIT *)PyBytes_AS_STRING(CO_CODE(frame));
        exit_contrast_scope();

        if (NULL == code_stream) {
            /* XXX: log here */
            PyErr_Clear();
            return 0;
        }

        opcode = _Py_OPCODE(code_stream[LASTI(frame)]);
#if PY_MINOR_VERSION > 10
        oparg = _Py_OPARG(code_stream[LASTI(frame)]);
#endif

        /* XXX: should be a switch instead */
        if (CHECK_BINARY_ADD(opcode, oparg) || CHECK_BINARY_IADD(opcode, oparg)) {
            left = PEEK_STACK(frame, 1);
            right = PEEK_STACK(frame, 0);

            PyList_Append(stack, left);
            PyList_Append(stack, right);

            // The frame struct uses 8 bits for a boolean value, which allows us to
            // stash some extra bits We use this mask to indicate which operation needs
            // to be done on the next opcode dispatched within this frame
            frame->f_trace_opcodes |= DO_BINADD;
        }
        if (CHECK_MODULO(opcode, oparg)) {
            left = PEEK_STACK(frame, 1);
            right = PEEK_STACK(frame, 0);

            PyList_Append(stack, left);
            PyList_Append(stack, right);

            frame->f_trace_opcodes |= DO_CFORMAT;
        }
    }

    return 0;
}

static void _initialize_trace() {
    PyThreadState *tstate = PyThreadState_Get();
    _PyEval_SetTrace(tstate, trace_trampoline, NULL);

    stack = PyList_New(0);
}
#endif /* if PY_MINOR_VERSION < 13 */
#endif /* if PY_MINOR_VERSION > 9 */

PyObject *initialize_trace(PyObject *self, PyObject *arg) {
#if PY_MINOR_VERSION > 9
#if PY_MINOR_VERSION < 13
    _initialize_trace();
#endif
#endif

    Py_RETURN_NONE;
}
