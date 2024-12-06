#include "PSOut.h"

//=============================================================================
// Module Version
//=============================================================================

#define VERSION "0.9.1a1"
#define VERSION_HEX 0x000901a1


//=============================================================================
// Module Definition
//=============================================================================

static PyMethodDef psout_Methods[] = {
    {NULL, NULL, 0, NULL}
};

static PyModuleDef psout_module_def = {
    PyModuleDef_HEAD_INIT,
    MODULE,
    "PSCAD PSOut module",
    -1,
    psout_Methods,
};

PyObject *psout_module = nullptr;

//=============================================================================
// Module Initialization
//=============================================================================

static bool addType(PyObject *module, PyTypeObject *type, const char *name) {
    Py_INCREF(type);
    if (PyModule_AddObject(module, name, (PyObject *) type) < 0) {
        Py_DECREF(type);
        Py_DECREF(module);
        return false;
    }
    return true;
}

PyMODINIT_FUNC
PyInit__psout(void)
{
    Closable::makeType();
    File::makeType();
    Call::makeType();
    Run::makeType();
    Trace::makeType();
    VarList::makeType();

    if (PyType_Ready(Closable::type) < 0)
        return NULL;

    if (PyType_Ready(File::type) < 0)
        return NULL;

    if (PyType_Ready(Call::type) < 0)
        return NULL;

    if (PyType_Ready(Run::type) < 0)
        return NULL;

    if (PyType_Ready(Trace::type) < 0)
       return NULL;

    if (PyType_Ready(VarList::type) < 0)
       return NULL;

    psout_module = PyModule_Create(&psout_module_def);
    if (psout_module == NULL)
        return NULL;

    PyModule_AddStringConstant(psout_module, "VERSION", VERSION);
    PyModule_AddIntConstant(psout_module, "VERSION_HEX", VERSION_HEX);

    if (!addType(psout_module, Closable::type, "Closable")) return NULL;
    if (!addType(psout_module, File::type, "File")) return NULL;
    if (!addType(psout_module, Call::type, "Call")) return NULL;
    if (!addType(psout_module, Run::type, "Run")) return NULL;
    if (!addType(psout_module, Trace::type, "Trace")) return NULL;
    if (!addType(psout_module, VarList::type, "VarList")) return NULL;

    return psout_module;
}

PyObject * closedHandleError(const char *type) {
   return PyErr_Format(PyExc_ValueError, "%s handle is closed", type);
}


PyObject * resultError(const char *type, const char *call, uint result) {
   if (result == RFR_INVALID_HANDLE)
      return PyErr_Format(PyExc_ReferenceError, "Invalid %s handle", type);
   return PyErr_Format(PyExc_ValueError, "%s: %s failed (%d)", type, call, result);
}

