from sys import version_info

from . import hookspy


py_version = version_info[:2]


fastcall_name = "fastcall_func"
fastcall_typedef = (
    f"typedef PyObject *(*{fastcall_name})(PyObject *, PyObject *const *, Py_ssize_t)"
)

fastcall_kwargs_name = "fastcall_kwargs_func"
fastcall_kwargs_typedef = f"typedef PyObject *(*{fastcall_kwargs_name})(PyObject *, PyObject *const *, Py_ssize_t, PyObject *)"


unaryfunc_signature = "PyObject *{}(PyObject *self)"
binaryfunc_signature = "PyObject *{}(PyObject *self, PyObject *args)"
ternaryfunc_signature = "PyObject *{}(PyObject *self, PyObject *args, PyObject *kwargs)"
fastcall_signature = (
    "PyObject *{}(PyObject *self, PyObject *const *args, Py_ssize_t nargs)"
)
fastcall_kwargs_signature = "PyObject *{}(PyObject *self, PyObject *const *args, Py_ssize_t nargs, PyObject *kwnames)"

newfunc_signature = "PyObject *{}(PyTypeObject *type, PyObject *args, PyObject *kwds)"
initproc_signature = "int {}(PyObject *self, PyObject *args, PyObject *kwds)"

unaryfunc_call = "(self)"
binaryfunc_call = "(self, args)"
ternaryfunc_call = "(self, args, kwargs)"
fastcall_call = "(self, args, nargs)"
fastcall_kwargs_call = "(self, args, nargs, kwargs)"
newfunc_call = "(type, args, kwds)"
initproc_call = "(self, args, kwds)"


propagate_args_by_name = {
    "unaryfunc": "NULL, NULL",
    "binaryfunc": "args, NULL",
    "ternaryfunc": "args, kwargs",
}


method_signatures_map = {
    hookspy.METH_O: "binaryfunc",
    hookspy.METH_NOARGS: "unaryfunc",
    hookspy.METH_VARARGS: "binaryfunc",
    hookspy.METH_KEYWORDS: "ternaryfunc",
    hookspy.METH_FASTCALL: fastcall_name,
    hookspy.METH_VARARGS | hookspy.METH_KEYWORDS: "ternaryfunc",
    hookspy.METH_FASTCALL | hookspy.METH_KEYWORDS: fastcall_kwargs_name,
}


def get_method_signature(argtype):
    return method_signatures_map[argtype]
