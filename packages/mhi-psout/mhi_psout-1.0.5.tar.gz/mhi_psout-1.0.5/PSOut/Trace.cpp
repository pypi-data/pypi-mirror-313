#include "PSOut.h"
#include <limits>

//=============================================================================
// Python Type Definition
//=============================================================================

PyMemberDef Trace::members[] = {
    { "run", T_OBJECT_EX, offsetof(Trace, run), READONLY, "Run trace is from" },
    { NULL }
};

PyGetSetDef Trace::getsetters[] = {
    GETSET("id",        getId,          NULL, "Returns run handle id", NULL),
    GETSET("datatype",  getDataType,    NULL, "Returns the trace datatype", NULL),
    GETSET("_domain",   getDomain,      NULL, "Returns the domain", NULL),
    GETSET("size",      getSize,        NULL, "Returns the size", NULL),
    GETSET("call",      getCall,        NULL, "Returns the associated call", NULL),
    GETSET("data",      getData,        NULL, "Returns the sample values", NULL),
    GETSET("_vars",     getVarList,     NULL, "Return the node's VarList", NULL),
    { NULL }
};

PyMethodDef Trace::methods[] = {
    METHOD("close",     close,      METH_NOARGS, "Close the trace"),
    METHOD("_variables",variables,  METH_NOARGS, "Retrieve the trace's variables"),
//  METHOD("is_run",    isRun,      METH_VARARGS, "Tests if the trace is from a run"),
    METHOD("__eq__",    equal,      METH_O,     "Compare trace objects"),
    { NULL }
};

PyType_Slot Trace::slots[] = {
    { Py_tp_doc,      (void*)
        "Trace()\n"
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

PyType_Spec Trace::type_spec = {
    MODULE "." "Trace",                         // name
    sizeof(Trace),                              // basicsize
    0,                                          // itemsize
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,   // flags
    Trace::slots                                // slots
};

PyTypeObject * Trace::type = NULL;



//=============================================================================
// Debugging via printf()
//=============================================================================

//#define TRACE_TRACE
#ifdef TRACE_TRACE
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

int Trace::init(Trace *self, PyObject *args, PyObject *kwargs) {
// printf("Trace::init(%p)\n", self);

   if (Closable::init(self, NULL, NULL) < 0)
      return -1;

   self->data = NULL;
   memset(&self->handle, 0, sizeof(self->handle));

   PyObject *run;
   if (!PyArg_ParseTuple(args, "O", &run))
      return -1;

   if (!PyObject_IsInstance(run, (PyObject*)Run::type))
      return PyErr_Format(PyExc_TypeError, "Run expected, got %R", run), -1;

   Py_IncRef(run);
   self->run = run;

   return 0;
}


//-----------------------------------------------------------------------------
// Destructor
//----------------------------------------------------------------------------

void Trace::finalize(Trace *self) {
// printf("Trace::finalize(%p)\n", self);
   Py_CLEAR(self->run);
   Py_CLEAR(self->data);
   Closable::finalize(self);
}


//-----------------------------------------------------------------------------
// Hash
//-----------------------------------------------------------------------------

Py_hash_t Trace::hash(Trace *self) {
   if (!self->open)
      return closedHandleError("Trace"), -1;

   RecordFileTraceHandle* THIS = &self->handle;
   long long hash_val;
   uint result = THIS->hash(THIS, hash_val);
   if (result != RFR_SUCCESS)
      return resultError("Trace", "hash", result), -1;

   Py_hash_t value = (Py_hash_t)(hash_val >> 4);
   if (value == -1)
      value = -2;
   return value;
}


//-----------------------------------------------------------------------------
// Equal
//-----------------------------------------------------------------------------

PyObject * Trace::equal(Trace *self, PyObject *arg0) {
   if (!self->open)
      return closedHandleError("Trace");

   int equal = 0;
   if (PyObject_IsInstance(arg0, (PyObject *)Trace::type)) {
      Trace *that = (Trace *)arg0;
      if (!that->open)
         return closedHandleError("Trace");

      RecordFileTraceHandle* THIS = &self->handle;
      RecordFileTraceHandle* THAT = &that->handle;
      uint result = THIS->equal(THIS, THAT, equal);
      if (result != RFR_SUCCESS)
         return resultError("Trace", "hash", result);
   }

   return PyBool_FromLong(equal);
}


//-----------------------------------------------------------------------------
// getId
//-----------------------------------------------------------------------------

PyObject * Trace::getId(Trace *self, void *closure) {
   if (!self->open)
      return closedHandleError("Trace");

   RecordFileTraceHandle* THIS = &self->handle;
   uint id;
   uint result = THIS->getId(THIS, id);
   if (result != RFR_SUCCESS)
      return resultError("Trace", "getId", result);

   return PyLong_FromUnsignedLong(id);
}


//-----------------------------------------------------------------------------
// getDataType
//-----------------------------------------------------------------------------

PyObject * Trace::getDataType(Trace *self, void *closure) {
   if (!self->open)
      return closedHandleError("Trace");

   RecordFileTraceHandle* THIS = &self->handle;
   uint type_id;
   uint result = THIS->getDataType(THIS, type_id);
   if (result != RFR_SUCCESS)
      return resultError("Trace", "getDataType", result);

   PyTypeObject *type = NULL;
   switch (type_id) {
      case RFVT_Invalid:
         return PyObject_Type(Py_None);
      case RFVT_Bit:
         type = &PyBool_Type;
         break;
      case RFVT_Byte:
      case RFVT_Int16:
      case RFVT_UInt16:
      case RFVT_Int32:
      case RFVT_UInt32:
      case RFVT_Int64:
      case RFVT_UInt64:
         type = &PyLong_Type;
         break;
      case RFVT_Real32:
      case RFVT_Real64:
         type = &PyFloat_Type;
         break;
      case RFVT_Charater:
      case RFVT_WideChar:
      case RFVT_StringAscii:
      case RFVT_StringUnicode:
         type = &PyUnicode_Type;
         break;
      case RFVT_Blob:
         type = &PyBytes_Type;
         break;
      case RFVT_Complex64:
      case RFVT_Complex128:
         type = &PyComplex_Type;
         break;
      default:
         return PyErr_Format(PyExc_TypeError, "Unsupported Type: %d", type_id);
      }

   PyObject *obj = (PyObject *)type;
   Py_INCREF(obj);

   return obj;
}


//-----------------------------------------------------------------------------
// getSize
//-----------------------------------------------------------------------------

PyObject * Trace::getSize(Trace *self, void *closure) {
   if (!self->open)
      return closedHandleError("Trace");

   RecordFileTraceHandle* THIS = &self->handle;
   unsigned long long size;
   uint result = THIS->getSize(THIS, size);
   if (result != RFR_SUCCESS)
      return resultError("Trace", "getId", result);

   return PyLong_FromUnsignedLongLong(size);
}


//-----------------------------------------------------------------------------
// getDomain
//-----------------------------------------------------------------------------

PyObject * Trace::getDomain(Trace *self, void *closure) {
   if (!self->open)
      return closedHandleError("Trace");

   RecordFileTraceHandle* THIS = &self->handle;

   PyObject *obj = PyObject_CallMethod(psout_module, "Trace",
                                       "O", self->run);
   if (!obj)
      return obj;

   Trace *domain = (Trace *)obj;
   uint result = THIS->getDomain(THIS, &domain->handle);

   if (result != RFR_SUCCESS) {
      Py_DECREF(obj);
      return resultError("Trace", "getDomain", result);
   }

   domain->open = true;

   return obj;
}


//-----------------------------------------------------------------------------
// getData
//-----------------------------------------------------------------------------

const unsigned int MAX_READ = std::numeric_limits<int>::max();

PyObject * Trace::getData(Trace *self, void *closure) {
   if (!self->open)
      return closedHandleError("Trace");

   RecordFileTraceHandle* THIS = &self->handle;

   if (self->data == NULL) {
      uint result;
      uint type_id;
      char type;
      int data_size = 0;
      unsigned long long size;

      result = THIS->getDataType(THIS, type_id);
      if (result != RFR_SUCCESS)
         return resultError("Trace", "getDataType", result);

      switch (type_id) {
         case RFVT_Bit:
         case RFVT_Byte:      type = 'B'; data_size = 1; type_id = RFVT_Byte; break;
         case RFVT_Int16:     type = 'h'; data_size = 2;  break;
         case RFVT_UInt16:    type = 'H'; data_size = 2;  break;
         case RFVT_Int32:     type = 'l'; data_size = 4;  break;
         case RFVT_UInt32:    type = 'L'; data_size = 4;  break;
         case RFVT_Int64:     type = 'q'; data_size = 8;  break;
         case RFVT_UInt64:    type = 'Q'; data_size = 8;  break;
         case RFVT_Real32:    type = 'f'; data_size = 4;  break;
         case RFVT_Real64:    type = 'd'; data_size = 8;  break;
         case RFVT_Charater:  type = 'B'; data_size = 1;  break;
         case RFVT_WideChar:  type = 'u'; data_size = 2;  break;
         case RFVT_Blob:      type = 'B'; data_size = 1;  break;
         default:
            return PyErr_Format(PyExc_TypeError, "Unsupported Type: %d", type_id);
      }

      result = THIS->getSize(THIS, size);
      if (result != RFR_SUCCESS)
         return resultError("Trace", "getSize", result);

      unsigned long long buffer_size = size * data_size;
      char *buffer = (char *) malloc(buffer_size);
      if (buffer == NULL)
         return PyErr_Format(PyExc_MemoryError, "Unable to allocate %llu bytes",
                             buffer_size);

      if (size > 0) {
         result = THIS->seek(THIS, 0, RFSD_ForwardFromBeginning);
         if (result != RFR_SUCCESS) {
            free(buffer);
            return resultError("Trace", "seek", result);
         }

         char *ptr = buffer;
         while (size > 0) {
            unsigned int count = size > MAX_READ ? MAX_READ : (unsigned int) size;
            int read;
            result = THIS->readValues(THIS, ptr, data_size, type_id, count, read);
            if (result != RFR_SUCCESS) {
               free(buffer);
               return resultError("Trace", "readValues", result);
            }
            ptr += data_size * read;
            size -= read;
         }
      }

      PyObject *bytes = PyBytes_FromStringAndSize(buffer, buffer_size);
      free(buffer);
      if (!bytes)
         return bytes;

      PyObject *array_module = PyImport_ImportModule("array");
      PyObject *array_class = PyObject_GetAttrString(array_module, "array");
      self->data = PyObject_CallFunction(array_class, "(s#O)", &type, 1, bytes);
      Py_XDECREF(array_class);
      Py_XDECREF(array_module);
      Py_XDECREF(bytes);
   }

   Py_XINCREF(self->data);
   return self->data;
}


//-----------------------------------------------------------------------------
// getCall
//-----------------------------------------------------------------------------

PyObject * Trace::getCall(Trace *self, void *closure) {
   if (!self->open)
      return closedHandleError("Trace");

   RecordFileTraceHandle* THIS = &self->handle;

   PyObject *obj = PyObject_CallMethod(psout_module, "Call", NULL);
   if (!obj)
      return obj;
   Call *ch = (Call *)obj;

   uint result = THIS->getCall(THIS, &ch->handle);
   if (result != RFR_SUCCESS) {
      Py_XDECREF(obj);
      return resultError("Trace", "getCall", result);
      }

   ch->open = true;
   return obj;
}


//-----------------------------------------------------------------------------
// getVarList
//-----------------------------------------------------------------------------

PyObject * Trace::getVarList(Trace *self, void *closure) {
   if (!self->open)
      return closedHandleError("Trace");

   PyObject *object = PyObject_CallMethod(psout_module, "VarList", NULL);
   if (!object)
      return object;

   RecordFileTraceHandle* THIS = &self->handle;
   VarList *var_list = (VarList*)object;
   RecordFileVariableListHandle *varlist = &var_list->handle;

   uint result = THIS->getVariableList(THIS, varlist);

   if (result != RFR_SUCCESS) {
      Py_DECREF(object);
      return resultError("Trace", "getVariableList", result);
   }

   var_list->open = true;
   return object;
}


//-----------------------------------------------------------------------------
// variables
//-----------------------------------------------------------------------------

PyObject * Trace::variables(Trace *self, PyObject *Py_UNUSED(args)) {
   TRACE("Trace::variables(%p)\n", self);
   if (!self->open)
      return closedHandleError("Trace");
   
   RecordFileTraceHandle* THIS = &self->handle;
   RecordFileVariableListHandle varlist;
   memset(&varlist, 0, sizeof(varlist));
   uint result = THIS->getVariableList(THIS, &varlist);
   if (result != RFR_SUCCESS)
      return resultError("Trace", "getVariableList", result);

   TRACE("  getVariableList(%p, varlist <- %p) -> %d\n", THIS, &varlist, result);

   return getVariables(varlist);
}


//-----------------------------------------------------------------------------
// getKey
//-----------------------------------------------------------------------------

PyObject * Trace::getKey(Trace *self, PyObject *key) {
   if (!self->open)
      return closedHandleError("Trace");

   if (PyUnicode_Check(key)) {
      RecordFileTraceHandle* THIS = &self->handle;
      RecordFileVariableListHandle varlist;
      memset(&varlist, 0, sizeof(varlist));
      uint result = THIS->getVariableList(THIS, &varlist);
      if (result != RFR_SUCCESS)
         return resultError("Trace", "getVariableList", result);

      return getVariable(varlist, key);
   } else {
      return PyErr_Format(PyExc_TypeError, "Key must be a string");
   }
}


//-----------------------------------------------------------------------------
// Repr
//-----------------------------------------------------------------------------

PyObject * Trace::repr(Trace *self) {
   TRACE("Trace::repr()\n");
   if (!self->open)
      return closedHandleError("Trace");

   RecordFileTraceHandle* THIS = &self->handle;
   uint id;
   uint result = THIS->getId(THIS, id);
   TRACE("Trace::getId() = %d\n", result);
   if (result != RFR_SUCCESS)
      return resultError("Trace", "getId", result);

   return PyUnicode_FromFormat("<Trace(%u)>", id);
}


//-----------------------------------------------------------------------------
// Close
//-----------------------------------------------------------------------------

PyObject * Trace::close(Trace *self, PyObject *args) {

   if (!self->open)
      return closedHandleError("Trace");

   RecordFileTraceHandle* THIS = &self->handle;
   uint result = THIS->close(THIS);
   if (result != RFR_SUCCESS)
      return resultError("Trace", "close", result);

   self->open = false;

   Py_RETURN_NONE;
}



/*
//-----------------------------------------------------------------------------
// Test if trace is from a given run
//  - Not necessary as we can just test ``trace.run == other_run``
//-----------------------------------------------------------------------------

PyObject * Trace::isRun(Trace *self, PyObject *args) {
   if (!self->open)
      return closedHandleError("Trace");

   PyObject *py_run = NULL;
   if (!PyArg_ParseTuple(args, "O", &py_run))
      return NULL;

   if (!PyObject_IsInstance(py_run, (PyObject *) Run::type))
      return PyErr_Format(PyExc_TypeError, "%R in not a Run object", py_run);

   RecordFileTraceHandle* THIS = &self->handle;
   RecordFileRunHandle *rh = &((Run *)py_run)->handle;
   int equal = 0;
   uint result = THIS->isRun(THIS, rh, equal);
   if (result != RFR_SUCCESS)
      return resultError("Trace", "isRun", result);

   return PyBool_FromLong(result);
}
*/
