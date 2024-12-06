#include "PSOut.h"

//=============================================================================
// Python Type Definition
//=============================================================================


PyMemberDef Call::members[] = {
    { NULL }
};

PyGetSetDef Call::getsetters[] = {
    GETSET("id",        getId,         NULL, "Returns call handle id", NULL),
    GETSET("num_calls", getCallCount,  NULL, "Returns number of sub call handles", NULL),
    GETSET("parent",    getParent,     NULL, "Return the parent call handle", NULL),
    GETSET("_vars",     getVarList,    NULL, "Return the node's VarList", NULL),
    { NULL }
};

PyMethodDef Call::methods[] = {
    METHOD("close",     close,      METH_NOARGS, "Closes the call handle"),
    METHOD("_variables",variables,  METH_NOARGS, "Retrieve the call's variables"),
    METHOD("_fetch",    fetchCall,  METH_O, "Fetch a call handle by id"),
    METHOD("_get",      getCall,    METH_O, "Get a call handle by index"),
    METHOD("_var",      getVar,     METH_O, "Get a variable"),
    METHOD("__eq__",    equal,      METH_O, "Compare call objects"),
    { NULL }
};

PyType_Slot Call::slots[] = {
    { Py_tp_doc,      (void*)
        "Call()\n"
        "\n"
        "Blah de blah"
        },
    { Py_tp_base,       &Closable::type },
    { Py_tp_init,       init },
//  { Py_tp_finalize,   finalize },
    { Py_tp_hash,       hash },
    { Py_tp_repr,       repr },
    { Py_tp_methods,    methods },
    { Py_tp_members,    members },
    { Py_tp_getset,     getsetters },
    { 0, 0 }
};

PyType_Spec Call::type_spec = {
    MODULE "." "Call",                          // name
    sizeof(Call),                               // basicsize
    0,                                          // itemsize
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,   // flags
    Call::slots                                 // slots
};

PyTypeObject * Call::type = NULL;


//=============================================================================
// Debugging via printf()
//=============================================================================

//#define TRACE_CALL
#ifdef TRACE_CALL
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

int Call::init(Call *self, PyObject *args, PyObject *kwargs) {
//   printf("Call::init(%p)\n", self);

   if (Closable::init(self, NULL, NULL) < 0)
      return -1;

   memset(&self->handle, 0, sizeof(self->handle));

   return 0;
}


//-----------------------------------------------------------------------------
// Destructor
//----------------------------------------------------------------------------

//void Call::finalize(Call *self) {
//// printf("Call::finalize(%p)\n", self);
//   Closable::finalize(self);
//}


//-----------------------------------------------------------------------------
// Hash
//-----------------------------------------------------------------------------
Py_hash_t Call::hash(Call *self) {
   if (!self->open)
      return closedHandleError("Call"), -1;

   RecordFileCallHandle* THIS = &self->handle;
   long long hash_val;
   uint result = THIS->hash(THIS, hash_val);
   if (result != RFR_SUCCESS)
      return resultError("Call", "hash", result), -1;

   Py_hash_t value = (Py_hash_t)(hash_val >> 4);
   if (value == -1)
      value = -2;
   return value;
}


//-----------------------------------------------------------------------------
// Equal
//-----------------------------------------------------------------------------

PyObject * Call::equal(Call *self, PyObject *arg0) {
   if (!self->open)
      return closedHandleError("Call");

   int equal = 0;
   if (PyObject_IsInstance(arg0, (PyObject *)Call::type)) {
      Call *that = (Call *)arg0;
      if (!that->open)
         return closedHandleError("Call");

      RecordFileCallHandle* THIS = &self->handle;
      RecordFileCallHandle* THAT = &that->handle;
      uint result = THIS->equal(THIS, THAT, equal);
      if (result != RFR_SUCCESS)
         return resultError("Call", "hash", result);
   }

   return PyBool_FromLong(equal);
}


//-----------------------------------------------------------------------------
// getId
//-----------------------------------------------------------------------------

PyObject * Call::getId(Call *self, void *closure) {
   if (!self->open)
      return closedHandleError("Call");

   RecordFileCallHandle* THIS = &self->handle;
   uint id;
   uint result = THIS->getId(THIS, id);
   if (result != RFR_SUCCESS)
      return resultError("Call", "getId", result);

   return PyLong_FromUnsignedLong(id);
}


//-----------------------------------------------------------------------------
// getCallCount
//-----------------------------------------------------------------------------

PyObject * Call::getCallCount(Call *self, void *closure) {
   if (!self->open)
      return closedHandleError("Call");

   RecordFileCallHandle* THIS = &self->handle;
   uint count;
   uint result = THIS->getCallCount(THIS, count);
   if (result != RFR_SUCCESS)
      return resultError("Call", "getCallCount", result);

   return PyLong_FromUnsignedLong(count);
}


//-----------------------------------------------------------------------------
// getKey
//-----------------------------------------------------------------------------

PyObject * Call::getVar(Call *self, PyObject *key) {
   if (!self->open)
      return closedHandleError("Call");

   RecordFileCallHandle* THIS = &self->handle;

   if (PyUnicode_Check(key)) {
      RecordFileVariableListHandle varlist;
      memset(&varlist, 0, sizeof(varlist));
      uint result = THIS->getVariableList(THIS, &varlist);
      if (result != RFR_SUCCESS)
         return resultError("Call", "getVariableList", result);

      return getVariable(varlist, key);
   }
   else {
      return PyErr_Format(PyExc_TypeError, "Key must be a string");
   }
}


//-----------------------------------------------------------------------------
// variables
//-----------------------------------------------------------------------------

PyObject * Call::variables(Call *self, PyObject *Py_UNUSED(args)) {
   TRACE("Call::variables(%p)\n", self);
   if (!self->open)
      return closedHandleError("Call");

   RecordFileCallHandle* THIS = &self->handle;
   RecordFileVariableListHandle varlist;
   memset(&varlist, 0, sizeof(varlist));
   uint result = THIS->getVariableList(THIS, &varlist);
   if (result != RFR_SUCCESS)
      return resultError("Call", "getVariableList", result);

   TRACE("  getVariableList(%p, varlist <- %p) -> %d\n", THIS, &varlist, result);

   return getVariables(varlist);
}


//-----------------------------------------------------------------------------
// getVarList
//-----------------------------------------------------------------------------

PyObject * Call::getVarList(Call *self, void *closure) {
   if (!self->open)
      return closedHandleError("Call");

   PyObject *object = PyObject_CallMethod(psout_module, "VarList", NULL);
   if (!object)
      return object;

   RecordFileCallHandle* THIS = &self->handle;
   VarList *var_list = (VarList*)object;
   RecordFileVariableListHandle *varlist = &var_list->handle;

   uint result = THIS->getVariableList(THIS, varlist);
   if (result != RFR_SUCCESS) {
      Py_DECREF(object);
      if (result != RFR_SUCCESS)
         return resultError("Call", "getVariableList", result);
      }

   var_list->open = true;
   return object;
}


//-----------------------------------------------------------------------------
// Repr
//-----------------------------------------------------------------------------

PyObject * Call::repr(Call *self) {
   if (!self->open)
      return closedHandleError("Call");

   RecordFileCallHandle* THIS = &self->handle;
   uint id;
   uint result = THIS->getId(THIS, id);
   if (result != RFR_SUCCESS)
      return resultError("Call", "getId", result);

   return PyUnicode_FromFormat("<Call(%u)>", id);
}


//-----------------------------------------------------------------------------
// Close
//-----------------------------------------------------------------------------

PyObject * Call::close(Call *self, PyObject *args) {

   if (!self->open)
      return closedHandleError("Call");

   RecordFileCallHandle* THIS = &self->handle;
   uint result = THIS->close(THIS);
   if (result != RFR_SUCCESS)
      return resultError("Call", "close", result);

   self->open = false;

   Py_RETURN_NONE;
}



//-----------------------------------------------------------------------------
// getParent
//-----------------------------------------------------------------------------

PyObject * Call::getParent(Call *self, void *closure) {
   if (!self->open)
      return closedHandleError("Call");

   PyObject *obj = PyObject_CallMethod(psout_module, "Call", NULL);
   if (!obj)
      return obj;
   Call *ch = (Call *)obj;

   RecordFileCallHandle* THIS = &self->handle;
   uint result = THIS->getParent(THIS, &ch->handle);
   if (result != RFR_SUCCESS) {
      Py_DECREF(obj);
      return resultError("Call", "getParent", result);
   }

   TRACE("  Marking %p open\n", obj);
   ch->open = true;

   return obj;
}


//-----------------------------------------------------------------------------
// Get Call Handle
//-----------------------------------------------------------------------------

PyObject * Call::getCall(Call *self, PyObject *arg0) {
   if (!self->open)
      return closedHandleError("Call");

   long _index = PyLong_AsLong(arg0);
   if (PyErr_Occurred())
      return nullptr;

   RecordFileCallHandle* THIS = &self->handle;
   uint count;
   uint result = THIS->getCallCount(THIS, count);
   if (result != RFR_SUCCESS)
      return resultError("Call", "getCallCount", result);

   if (_index >= (long)count || _index < -(long)count)
      return PyErr_Format(PyExc_IndexError, "Index out of range");

   unsigned int index = _index >= 0 ? _index : _index + count;

   PyObject *obj = PyObject_CallMethod(psout_module, "Call", NULL);
   if (!obj)
      return obj;
   Call *ch = (Call *)obj;

   TRACE("  Call() -> %p\n", obj);

   result = THIS->getCall(THIS, index, &ch->handle);

   TRACE("  Call::getCall(%d) = %d\n", index, result);

   if (result != RFR_SUCCESS) {
      Py_DECREF(obj);
      return resultError("Call", "getCall", result);
   }

   TRACE("  Marking %p open\n", obj);
   ch->open = true;

   return obj;
}


//-----------------------------------------------------------------------------
// Fetch a Call Handle by id
//-----------------------------------------------------------------------------

PyObject * Call::fetchCall(Call *self, PyObject *arg0) {
   if (!self->open)
      return closedHandleError("Call");

   long _id = PyLong_AsLong(arg0);
   if (PyErr_Occurred())
      return nullptr;
   if (_id < 0 || _id > UINT_MAX)
      return PyErr_Format(PyExc_ValueError, "Invalid Id");

   uint id = _id;

   PyObject *obj = PyObject_CallMethod(psout_module, "Call", NULL);
   if (!obj)
      return obj;
   Call *ch = (Call *)obj;

   TRACE("  Call() -> %p\n", obj);

   RecordFileCallHandle* THIS = &self->handle;
   uint result = THIS->fetchCall(THIS, id, &ch->handle);
   TRACE("  Call::fetchCall(%d) = %d\n", index, result);
   if (result != RFR_SUCCESS) {
      Py_DECREF(obj);
      return resultError("Call", "fetchCall", result);
      }

   TRACE("  Marking %p open\n", obj);
   ch->open = true;

   return obj;
   }
