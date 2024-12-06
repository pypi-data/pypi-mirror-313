#include "PSOut.h"

//=============================================================================
// Python Type Definition
//=============================================================================

PyMemberDef Run::members[] = {
    { "file", T_OBJECT_EX, offsetof(Run, file), READONLY, "File run is from" },
    { NULL }
   };

PyGetSetDef Run::getsetters[] = {
    GETSET("id",        getId,          NULL, "Returns run handle id", NULL),
    GETSET("num_traces",getTraceCount,  NULL, "Returns number of traces", NULL),
    GETSET("_vars",     getVarList,     NULL, "Return the node's VarList", NULL),
    { NULL }
   };

PyMethodDef Run::methods[] = {
    METHOD("close",     close,      METH_NOARGS, "Close the run handle"),
    METHOD("_variables",variables,  METH_NOARGS, "Retrieve the run's variables"),
    METHOD("trace",     getTrace,   METH_O, "Get a trace handle"),
    METHOD("__eq__",    equal,      METH_O,     "Compare run objects"),

    { NULL }
};

PyType_Slot Run::slots[] = {
    { Py_tp_doc,      (void*)
        "Run()\n"
        "\n"
        "Blah de blah"
        },
    { Py_tp_base,       &Closable::type },
    { Py_tp_init,       init },
    { Py_tp_finalize,   finalize },
    { Py_tp_hash,       hash },
    { Py_tp_repr,       repr },
    { Py_tp_methods,    methods },
    { Py_tp_members,    members },
    { Py_tp_getset,     getsetters },
    { Py_mp_subscript,  getKey },
    { 0, 0 }
};

PyType_Spec Run::type_spec = {
    MODULE "." "Run",                           // name
    sizeof(Run),                                // basicsize
    0,                                          // itemsize
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,   // flags
    Run::slots                                  // slots
};

PyTypeObject * Run::type = NULL;



//=============================================================================
// Debugging via printf()
//=============================================================================

//#define TRACE_RUN
#ifdef TRACE_RUN
#define TRACE(...) printf(__VA_ARGS__)
#else
#define TRACE(...)
#endif


//=============================================================================
// Python Type Methods
//=============================================================================

//-----------------------------------------------------------------------------
// Open (Constructor)
//-----------------------------------------------------------------------------

int Run::init(Run *self, PyObject *args, PyObject *kwargs) {
// TRACE("Run::init(%p)\n", self);

   self->file = nullptr;

   if (Closable::init(self, NULL, NULL) < 0)
      return -1;

   PyObject *file;
   if (!PyArg_ParseTuple(args, "O", &file))
      return -1;

   if (!PyObject_IsInstance(file, (PyObject*)File::type))
      return PyErr_Format(PyExc_TypeError, "File expected, got %R", file), -1;

   Py_IncRef(file);
   self->file = file;

   memset(&self->handle, 0, sizeof(self->handle));

   return 0;
}


//-----------------------------------------------------------------------------
// Destructor
//----------------------------------------------------------------------------

void Run::finalize(Run *self) {
// TRACE("Run::finalize(%p)\n", self);
   Py_CLEAR(self->file);
   Closable::finalize(self);
}


//-----------------------------------------------------------------------------
// Hash
//-----------------------------------------------------------------------------

Py_hash_t Run::hash(Run *self) {
   if (!self->open)
      return closedHandleError("Run"), -1;

   RecordFileRunHandle* THIS = &self->handle;
   long long hash_val;
   uint result = THIS->hash(THIS, hash_val);
   if (result != RFR_SUCCESS)
      return resultError("Run", "hash", result), -1;

   Py_hash_t value = (Py_hash_t)(hash_val >> 4);
   if (value == -1)
      value = -2;
   return value;
}


//-----------------------------------------------------------------------------
// Equal
//-----------------------------------------------------------------------------

PyObject * Run::equal(Run *self, PyObject *arg0) {
   if (!self->open)
      return closedHandleError("Run");

   int equal = 0;
   if (PyObject_IsInstance(arg0, (PyObject *)Run::type)) {
      Run *that = (Run *)arg0;
      if (!that->open)
         return closedHandleError("Run");

      RecordFileRunHandle* THIS = &self->handle;
      RecordFileRunHandle* THAT = &that->handle;
      uint result = THIS->equal(THIS, THAT, equal);
      if (result != RFR_SUCCESS)
         return resultError("Run", "equal", result);
   }

   return PyBool_FromLong(equal);
}


//-----------------------------------------------------------------------------
// getId
//-----------------------------------------------------------------------------

PyObject * Run::getId(Run *self, void *closure) {
   if (!self->open)
      return closedHandleError("Run");

   RecordFileRunHandle* THIS = &self->handle;
   uint id;
   uint result = THIS->getId(THIS, id);
   if (result != RFR_SUCCESS)
      return resultError("Run", "getId", result);

   return PyLong_FromUnsignedLong(id);
}


//-----------------------------------------------------------------------------
// getTraceCount
//-----------------------------------------------------------------------------

PyObject * Run::getTraceCount(Run *self, void *closure) {
   if (!self->open)
      return closedHandleError("Run");

   RecordFileRunHandle* THIS = &self->handle;
   uint count;
   uint result = THIS->getTraceCount(THIS, count);
   if (result != RFR_SUCCESS)
      return resultError("Run", "getTraceCount", result);

   return PyLong_FromUnsignedLong(count);
}


//-----------------------------------------------------------------------------
// getKey
//-----------------------------------------------------------------------------

PyObject * Run::getKey(Run *self, PyObject *key) {
   if (!self->open)
      return closedHandleError("Run");

   if (PyUnicode_Check(key)) {
      RecordFileRunHandle* THIS = &self->handle;
      RecordFileVariableListHandle varlist;
      memset(&varlist, 0, sizeof(varlist));
      uint result = THIS->getVariableList(THIS, &varlist);
      if (result != RFR_SUCCESS)
         return resultError("Run", "getVariableList", result);

      return getVariable(varlist, key);
   } else {
      return PyErr_Format(PyExc_TypeError, "Key must be a string");
   }
}


//-----------------------------------------------------------------------------
// variables
//-----------------------------------------------------------------------------

PyObject * Run::variables(Run *self, PyObject *Py_UNUSED(args)) {
   if (!self->open)
      return closedHandleError("Run");

   RecordFileRunHandle* THIS = &self->handle;
   RecordFileVariableListHandle varlist;
   memset(&varlist, 0, sizeof(varlist));
   uint result = THIS->getVariableList(THIS, &varlist);
   if (result != RFR_SUCCESS)
      return resultError("Run", "getVariableList", result);

   return getVariables(varlist);
}


//-----------------------------------------------------------------------------
// getVarList
//-----------------------------------------------------------------------------

PyObject * Run::getVarList(Run *self, void *closure) {
   if (!self->open)
      return closedHandleError("Run");

   PyObject *object = PyObject_CallMethod(psout_module, "VarList", NULL);
   if (!object)
      return object;

   RecordFileRunHandle* THIS = &self->handle;
   VarList *var_list = (VarList*)object;
   RecordFileVariableListHandle *varlist = &var_list->handle;

   uint result = THIS->getVariableList(THIS, varlist);
   if (result != RFR_SUCCESS) {
      Py_DECREF(object);
      return resultError("Run", "getVariableList", result);
      }

   var_list->open = true;
   return object;
}


//-----------------------------------------------------------------------------
// Repr
//-----------------------------------------------------------------------------

PyObject * Run::repr(Run *self) {
   if (!self->open)
      return closedHandleError("Run");

   RecordFileRunHandle* THIS = &self->handle;
   uint id;
   uint result = THIS->getId(THIS, id);
   if (result != RFR_SUCCESS)
      return resultError("Run", "getId", result);

   return PyUnicode_FromFormat("<Run(%u)>", id);
}


//-----------------------------------------------------------------------------
// Close
//-----------------------------------------------------------------------------

PyObject * Run::close(Run *self, PyObject *args) {
   if (!self->open)
      return closedHandleError("Run");

   RecordFileRunHandle* THIS = &self->handle;
   uint result = THIS->close(THIS);
   if (result != RFR_SUCCESS)
      return resultError("Run", "close", result);

   self->open = false;

   Py_RETURN_NONE;
}


//-----------------------------------------------------------------------------
// Get Call Handle
//-----------------------------------------------------------------------------

//PyObject * Run::getTrace(Run *self, PyObject *args, PyObject *kwargs) {
PyObject * Run::getTrace(Run *self, PyObject *arg0) {
   if (!self->open)
      return closedHandleError("Run");

   //static const char *kwlist[] = { "index", "call", NULL };
   uint index = UINT_MAX;
   PyObject *py_call = NULL;

   /*
   if (!PyArg_ParseTupleAndKeywords(args, kwargs, "|I$O", (char **)kwlist,
       &index, &py_call))
      return NULL;

   if (index == UINT_MAX && py_call == NULL)
      return PyErr_Format(PyExc_ValueError, "Index or call must be given");

   if (index != UINT_MAX && py_call != NULL)
      return PyErr_Format(PyExc_ValueError, "Both index and call cannot be given");
   */
   TRACE("Run:getTrace(%p, %s)\n", arg0, arg0->ob_type->tp_name);
   if (PyLong_CheckExact(arg0)) {
      TRACE("   %p is a Long\n", arg0);
      long val = PyLong_AsLong(arg0);
      if (PyErr_Occurred())
         return NULL;
      if (val < 0 || val >= UINT_MAX)
         return PyErr_Format(PyExc_ValueError, "Index out of range");
      index = val;
   }
   else if (PyObject_IsInstance(arg0, (PyObject *)Call::type)) {
      TRACE("   %p is a Call::type\n", arg0);
      py_call = arg0;
   }
   else  {
      TRACE("   Dunno\n");
      return PyErr_Format(PyExc_TypeError, "%R is not an index or Call object", arg0);
   }

   PyObject *obj = PyObject_CallMethod(psout_module, "Trace",
                                       "O", self);
   if (!obj)
      return obj;
   Trace *th = (Trace *)obj;

   uint result;
   RecordFileRunHandle* THIS = &self->handle;
   if (index != UINT_MAX) {
      result = THIS->getTrace(THIS, index, &th->handle);
      if (result != RFR_SUCCESS) {
         Py_DECREF(obj);
         return resultError("Run", "getTrace", result);
      }
   } else {
      Call *call = (Call *)py_call;
      result = THIS->fetchTrace(THIS, &call->handle, &th->handle);
      if (result != RFR_SUCCESS) {
         Py_DECREF(obj);
         return resultError("Run", "fetchTrace", result);
      }
   }

   th->open = true;
   return obj;
}
