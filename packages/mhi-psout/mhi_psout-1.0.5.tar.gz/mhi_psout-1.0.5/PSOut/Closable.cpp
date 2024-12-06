#include "PSOut.h"

//=============================================================================
// Python Type Definition
//=============================================================================

PyMemberDef Closable::members[] = {
    { NULL }
};

PyGetSetDef Closable::getsetters[] = {
    { NULL }
};

PyMethodDef Closable::methods[] = {
    METHOD("__enter__", enter, METH_NOARGS, "Enter a runtime context"),
    METHOD("__exit__",  exit, METH_VARARGS, "Exit the runtime context & close the handle"),
    METHOD("close",     close, METH_NOARGS, "Close the handle"),
    { NULL }
};

PyType_Slot Closable::slots[] = {
    { Py_tp_init,       init },
    { Py_tp_finalize,   finalize },
    { Py_tp_methods,    methods },
    { Py_tp_members,    members },
    { Py_tp_getset,     getsetters },
    { 0, 0 }
};

PyType_Spec Closable::type_spec = {
    MODULE "." "Closable",                      // name
    sizeof(Closable),                           // basicsize
    0,                                          // itemsize
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,   // flags
    Closable::slots                             // slots
};

PyTypeObject * Closable::type = NULL;


//=============================================================================
// Python Type Methods
//=============================================================================

//-----------------------------------------------------------------------------
// Type Creation Helper
//-----------------------------------------------------------------------------

void Closable::typeFromSpec(PyTypeObject* &type, PyType_Spec &spec) {
   for (PyType_Slot* slot = spec.slots; slot->slot != 0; slot++)
      if (slot->slot == Py_tp_base)
         slot->pfunc = *(PyObject **)slot->pfunc;

   type = (PyTypeObject *)PyType_FromSpec(&spec);
}


//-----------------------------------------------------------------------------
// Open (Constructor)
//-----------------------------------------------------------------------------

int Closable::init(Closable *self, PyObject *args, PyObject *kwargs) {
// printf("Closable::init(%p)\n", self);
   self->open = false;
   return 0;
}


//-----------------------------------------------------------------------------
// Destructor
//----------------------------------------------------------------------------

void Closable::finalize(Closable *self) {
// printf("Closable::finalize(%p)\n", self);
   if (self->open)
      PyObject_CallMethod((PyObject *)self, "close", NULL);
}


//-----------------------------------------------------------------------------
// Enter
//-----------------------------------------------------------------------------

PyObject * Closable::enter(Closable *self, PyObject *args) {
   Py_INCREF(self);
   return (PyObject *)self;
}


//-----------------------------------------------------------------------------
// Exit
//-----------------------------------------------------------------------------

PyObject * Closable::exit(Closable *self, PyObject *args) {
   PyObject_CallMethod((PyObject *)self, "close", NULL);
   Py_RETURN_NONE;
}

//-----------------------------------------------------------------------------
// Close
//-----------------------------------------------------------------------------

PyObject * Closable::close(Closable *self, PyObject *args) {
   if (!self->open)
      return PyErr_Format(PyExc_ValueError, "Handle is already closed");

   self->open = false;

   Py_RETURN_NONE;
}

