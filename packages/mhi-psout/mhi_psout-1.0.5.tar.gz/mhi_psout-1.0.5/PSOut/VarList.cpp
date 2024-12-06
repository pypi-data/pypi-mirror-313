#include "PSOut.h"

//=============================================================================
// Python Type Definition
//=============================================================================

PyMemberDef VarList::members[] = {
    { NULL }
};

PyGetSetDef VarList::getsetters[] = {
    { NULL }
};

PyMethodDef VarList::methods[] = {
    METHOD("close",     close, METH_NOARGS, "Closes the var list handle"),
    METHOD("asdict",    as_dict, METH_NOARGS, "Convert var list to dict"),
    METHOD("__eq__",    equal,      METH_O,     "Compare trace objects"),
    { NULL }
};

PyType_Slot VarList::slots[] = {
    { Py_tp_doc,      (void*)
        "VarList()\n"
        "\n"
        "Blah de blah"
        },
    { Py_tp_base,       &Closable::type },
    { Py_tp_init,       init },
//  { Py_tp_finalize,   finalize },
    { Py_tp_hash,       hash },
    { Py_tp_methods,    methods },
    { Py_tp_members,    members },
    { Py_tp_getset,     getsetters },
    { Py_mp_subscript,  getKey },
    { 0, 0 }
};

PyType_Spec VarList::type_spec = {
    MODULE "." "VarList",           // name
    sizeof(VarList),                // basicsize
    0,                              // itemsize
    Py_TPFLAGS_DEFAULT,             // flags
    VarList::slots                  // slots
   };

PyTypeObject * VarList::type = NULL;


//=============================================================================
// Debugging via printf()
//=============================================================================

//#define TRACE_VARLIST
#ifdef TRACE_VARLIST
#define TRACE(...) printf(__VA_ARGS__)
#else
#define TRACE(...)
#endif


//=============================================================================
// Helpers
//=============================================================================

#define GETVAR_BUF_SIZE 1
PyObject * _getVariable(RecordFileVariableListHandle& varlist, PyObject *key) {
   uint result;
   uint type;
   long long size;
   const wchar_t *szKey = PyUnicode_AsWideCharString(key, NULL);
   if (!szKey)
      return nullptr;

   result = varlist.getVariableTypeW(&varlist, szKey, type);
   TRACE("      getVariableTypeW(  %p, '%ls', type <- %d) -> %d\n",
         &varlist, szKey, type, result);
   if (result != RFR_SUCCESS)
      return resultError("VarList", "getVariableTypeW", result);

   if (type == RFVT_Invalid)
      return PyErr_Format(PyExc_KeyError, "No variable named %R exists.", key);

   result = varlist.getVariableLengthW(&varlist, szKey, size);
   TRACE("      getVariableLengthW(%p, '%ls', size <- %lld) -> %d\n",
         &varlist, szKey, size, result);
   if (result != RFR_SUCCESS)
      return resultError("VarList", "getVariableLengthW", result);

   if (size < 0)
      return PyErr_Format(PyExc_TypeError, "Bad size: %d", size);

   if (size == 0 && (type == RFVT_StringAscii || type == RFVT_StringUnicode)) {
      fprintf(stderr, "Zero length string! - no null terminator\n");
      return PyUnicode_FromStringAndSize("", 0);
   }

   PyObject *object = NULL;
   char buffer[GETVAR_BUF_SIZE], *p = &buffer[0];
   if (size > GETVAR_BUF_SIZE) {
      p = (char *)malloc(size);
      if (p == nullptr)
         return PyErr_Format(PyExc_MemoryError, "Allocate failed (%lld bytes)", size);
   }

   result = varlist.getVariableW(&varlist, szKey, p, size, type);
   if (result == RFR_SUCCESS) {
      //TRACE("   Data:");
      //for (int j = 0; j < size; j++)
      //   TRACE(" %02x", p[j] & 0xFF);
      //TRACE("\n");

      switch (type) {
         case RFVT_Bit:
         case RFVT_Byte:
            object = PyLong_FromUnsignedLong((unsigned)p[0]);
            break;
         case RFVT_Int16: object = PyLong_FromLong(*(signed short *)p); break;
         case RFVT_UInt16: object = PyLong_FromUnsignedLong(*(unsigned short *)p);  break;
         case RFVT_Int32: object = PyLong_FromLong(*(signed int *)p);   break;
         case RFVT_UInt32: object = PyLong_FromUnsignedLong(*(unsigned int *)p);    break;
         case RFVT_Int64: object = PyLong_FromLongLong(*(signed long long *) p); break;
         case RFVT_UInt64: object = PyLong_FromUnsignedLongLong(*(unsigned long long *) p);  break;
         case RFVT_Real32: object = PyFloat_FromDouble(*(float *)p);    break;
         case RFVT_Real64: object = PyFloat_FromDouble(*(double *)p);  break;
         case RFVT_Charater: object = PyUnicode_FromStringAndSize(p, 1); break;
         case RFVT_WideChar: object = PyUnicode_FromWideChar((wchar_t*)p, 1); break;
         case RFVT_StringAscii: object = PyUnicode_DecodeUTF8(p, size - 1, "replace"); break;
         case RFVT_StringUnicode: object = PyUnicode_FromWideChar((wchar_t*)p, size / 2 - 1); break;
         case RFVT_Blob: object = PyBytes_FromStringAndSize(p, size); break;
         case RFVT_Complex64: object = PyComplex_FromDoubles(((float*)p)[0], ((float*)p)[1]); break;
         case RFVT_Complex128: object = PyComplex_FromDoubles(((double*)p)[0], ((double*)p)[1]); break;
         default:
            PyErr_Format(PyExc_NotImplementedError, "Variable Type not supported: type=%d size=%lld", type, size);
      }
   }

//#ifdef TRACE_VARLIST
//   if (type == RFVT_StringAscii) {
//      TRACE("      \"%s\"\n", p);
//   }
//#endif

   if (size > GETVAR_BUF_SIZE)
      free(p);

   if (result != RFR_SUCCESS)
      return resultError("VarList", "getVariableW", result);

   return object;
}

PyObject * getVariable(RecordFileVariableListHandle& varlist, PyObject *key) {
   PyObject *object = _getVariable(varlist, key);
   uint result = varlist.close(&varlist);
   TRACE("      VarList::close(%p) -> %d\n", &varlist, result);

   if (object != nullptr && result != RFR_SUCCESS) {
      Py_DECREF(object);
      return resultError("VarList", "close", result);
   }

   return object;
}

PyObject * _getVariables(RecordFileVariableListHandle& varlist) {
   long long i, count;
   uint result = varlist.getCount(&varlist, count);
   TRACE("  VarList::getCount(     %p, count <- %lld) -> %d\n", &varlist, count, result);
   if (result != RFR_SUCCESS)
      return resultError("VariableList", "getCount", result);

   PyObject *dict = PyDict_New();
   if (dict)
      {
      bool failed = false;
      for (i = 0; i < count && !failed; i++) {
         long long length;
         result = varlist.getNameSize(&varlist, i, length);
         TRACE("    VarList::getNameSize(%p, %d, length <- %lld) -> %d\n", &varlist, i, length, result);
         if (result != RFR_SUCCESS) {
            PyErr_Format(PyExc_ValueError, "VariableList: getNameSize failed (%d)",
                         result);
            failed = true;
            break;
            }
         wchar_t *name = (wchar_t*)calloc(length, 2);
         if (name) {
            result = varlist.getNameW(&varlist, i, name, 2 * length);
            TRACE("    VarList::getNameW(   %p, %d, name <- '%ls', %lld) -> %d\n", &varlist, i, name, length, result);
            if (result != RFR_SUCCESS) {
               PyErr_Format(PyExc_ValueError, "VariableList: getNameW failed (%d)",
                            result);
               free(name);
               failed = true;
               break;
               }
            PyObject *key = PyUnicode_FromWideChar(name, length - 1); // Exclude NUL
            if (key) {
               PyObject *value = _getVariable(varlist, key);
               if (value)
                  PyDict_SetItem(dict, key, value);
               else
                  failed = true;
               Py_XDECREF(value);
               Py_DECREF(key);
               }
            else {
               failed = true;
               }
            free(name);
            }
         else {
            PyErr_Format(PyExc_ValueError, "VariableList: calloc failed");
            failed = true;
            }
         }
      if (failed)
         Py_CLEAR(dict);
      }

   return dict;
   }

PyObject * getVariables(RecordFileVariableListHandle& varlist) {
   PyObject *object = _getVariables(varlist);
   uint result = varlist.close(&varlist);
   TRACE("  VarList::close(        %p) -> %d\n", &varlist, result);

   if (object != nullptr && result != RFR_SUCCESS) {
      Py_DECREF(object);
      return resultError("VarList", "close", result);
      }
   return object;
}


//=============================================================================
// Python Type Methods
//=============================================================================

//-----------------------------------------------------------------------------
// Open (Constructor)
//-----------------------------------------------------------------------------

int VarList::init(VarList *self, PyObject *args, PyObject *kwargs) {
// TRACE("VarList::init(%p)\n", self);

   if (Closable::init(self, NULL, NULL) < 0)
      return -1;

   memset(&self->handle, 0, sizeof(self->handle));

   return 0;
}


//-----------------------------------------------------------------------------
// Destructor
//----------------------------------------------------------------------------

//void VarList::finalize(Run *self) {
//   TRACE("VarList::finalize(%p)\n", self);
//   Closable::finalize(self);
//}


//-----------------------------------------------------------------------------
// Hash
//-----------------------------------------------------------------------------

Py_hash_t VarList::hash(VarList *self) {
   if (!self->open)
      return closedHandleError("VarList"), -1;

   RecordFileVariableListHandle* THIS = &self->handle;
   long long hash_val;
   uint result = THIS->hash(THIS, hash_val);
   if (result != RFR_SUCCESS)
      return resultError("VarList", "hash", result), -1;

   Py_hash_t value = (Py_hash_t)(hash_val >> 4);
   if (value == -1)
      value = -2;
   return value;
}


//-----------------------------------------------------------------------------
// Equal
//-----------------------------------------------------------------------------

PyObject * VarList::equal(VarList *self, PyObject *arg0) {
   if (!self->open)
      return closedHandleError("VarList");

   int equal = 0;
   if (PyObject_IsInstance(arg0, (PyObject *)VarList::type)) {
      VarList *that = (VarList *)arg0;
      if (!that->open)
         return closedHandleError("VarList");

      RecordFileVariableListHandle* THIS = &self->handle;
      RecordFileVariableListHandle* THAT = &that->handle;
      uint result = THIS->equal(THIS, THAT, equal);
      if (result != RFR_SUCCESS)
         return resultError("VarList", "equal", result);
   }

   return PyBool_FromLong(equal);
}


//-----------------------------------------------------------------------------
// getKey
//-----------------------------------------------------------------------------

PyObject * VarList::getKey(VarList *self, PyObject *key) {
   if (!self->open)
      return PyErr_Format(PyExc_ValueError, "Variable List handle is closed");

   if (PyUnicode_Check(key)) {
      RecordFileVariableListHandle& varlist = self->handle;
      return _getVariable(varlist, key);
   } else {
      return PyErr_Format(PyExc_TypeError, "Key must be a string");
   }
}


//-----------------------------------------------------------------------------
// asDict
//-----------------------------------------------------------------------------

PyObject * VarList::as_dict(VarList *self, PyObject *args) {
   if (!self->open)
      return PyErr_Format(PyExc_ValueError, "Variable List handle is closed");

   RecordFileVariableListHandle& varlist = self->handle;
   return _getVariables(varlist);
}


//-----------------------------------------------------------------------------
// Close
//-----------------------------------------------------------------------------

PyObject * VarList::close(VarList *self, PyObject *args) {

   if (!self->open)
      return PyErr_Format(PyExc_ValueError, "Variable List handle is closed");

   RecordFileVariableListHandle* THIS = &self->handle;
   uint result = THIS->close(THIS);

   if (result != RFR_SUCCESS)
      return PyErr_Format(PyExc_ValueError, "Close failed: %d", result);

   self->open = false;

   Py_RETURN_NONE;
}
