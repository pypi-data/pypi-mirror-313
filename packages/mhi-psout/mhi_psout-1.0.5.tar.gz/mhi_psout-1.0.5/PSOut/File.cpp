#include "PSOut.h"

//=============================================================================
// Python Type Definition
//=============================================================================


PyMemberDef File::members[] = {
    { "path", T_OBJECT_EX, offsetof(File, path), READONLY, "Path of the file" },
    { NULL }
};

PyGetSetDef File::getsetters[] = {
    GETSET("created",   getCreated,     NULL, "The 'created on' datetime", NULL),
    GETSET("modified",  getModified,    NULL, "The 'modified on' datetime", NULL),
    GETSET("num_runs",  getRunCount,    NULL, "The number of runs in file", NULL),
    GETSET("root",      getRoot,        NULL, "The root call for the file", NULL),
    GETSET("_vars",     getVarList,     NULL, "Return the file's VarList", NULL),
    { NULL }
};

PyMethodDef File::methods[] = {
    METHOD("close",     close,      METH_NOARGS, "Closes the record file"),
    METHOD("_variables",variables,  METH_NOARGS, "Retrieve the file's variables"),
    METHOD("_get_run",  getRun,     METH_O, "Get a run handle by index"),
    METHOD("_fetch_run",fetchRun,   METH_O, "Fetch a run handle by id"),
    METHOD("_var",      getVar,     METH_O, "Get a variable"),
    { NULL }
};

PyType_Slot File::slots[] = {
    { Py_tp_doc,      (void*)
        "File(file_path, /, open_type=OPEN_EXISTING, section_size=DEFAULT,\n"
        "     reserve_count=DEFAULT, growth_rate=DEFAULT)\n"
        "\n"
        "Opens or creates a file at the provided file path"
        },
    { Py_tp_base,       &Closable::type },
    { Py_tp_init,       init },
    { Py_tp_finalize,   finalize },
    { Py_tp_repr,       repr },
    { Py_tp_methods,    methods },
    { Py_tp_members,    members },
    { Py_tp_getset,     getsetters },
    { 0, 0 }
};

PyType_Spec File::type_spec = {
    MODULE "." "File",                          // name
    sizeof(File),                               // basicsize
    0,                                          // itemsize
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,   // flags
    File::slots                                 // slots
};

PyTypeObject * File::type = NULL;



//=============================================================================
// Timestamp to DateTime
//=============================================================================

static PyObject * timestamp_to_date(long long timestamp) {
   PyObject *datetime_module = PyImport_ImportModule("datetime");
   PyObject *datetime_class = PyObject_GetAttrString(datetime_module, "datetime");
   PyObject *result = PyObject_CallMethod(datetime_class, "fromtimestamp",
                                          "(L)", timestamp);
   Py_XDECREF(datetime_class);
   Py_XDECREF(datetime_module);

   return result;
   }


//=============================================================================
// Python Type Methods
//=============================================================================

//-----------------------------------------------------------------------------
// Open (Constructor)
//-----------------------------------------------------------------------------

int File::init(File *self, PyObject *args, PyObject *kwargs) {
// printf("File::init(%p)\n", self);

   static const char *kwlist[] = { "open_type", "section_size",
                                   "reserve_count", "growth_rate", NULL };
   PyObject *path;
   unsigned int open_type = RFOT_OPENEXISTING;
   uint result;

   self->path = NULL;
   self->root = NULL;

   memset(&self->handle, 0, sizeof(self->handle));
   memset(&self->stats, 0, sizeof(self->stats));

   RecordFileCreationStats& stats = self->stats;
   stats.iSectionSize = RFPS_DEFAULT;
   stats.iReserveCount = RFRS_DEFAULT;
   stats.iGrowthRate = RFGS_DEFAULT;

   if (Closable::init(self, NULL, NULL) < 0)
      return -1;

   if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O|$iiii", (char **)kwlist,
       &path, &open_type, &stats.iSectionSize, &stats.iReserveCount,
       &stats.iGrowthRate))
      return NULL;

   PyObject *fspath = PyOS_FSPath(path);
   if (!fspath)
      return NULL;
   const wchar_t *sPath = PyUnicode_AsWideCharString(fspath, NULL);
   Py_DECREF(fspath);
   if (!sPath)
      return NULL;

   Py_BEGIN_ALLOW_THREADS
   result = OpenRecordFileHandleW(sPath, open_type, &stats, &self->handle);
   Py_END_ALLOW_THREADS

   if (result != RFR_SUCCESS)
      return PyErr_Format(PyExc_FileNotFoundError, "Open failed: %d", result), -1;

   Py_XINCREF(path);
   self->path = path;
   self->open = true;

   return 0;
}


//-----------------------------------------------------------------------------
// Destructor
//----------------------------------------------------------------------------

void File::finalize(File *self) {
// printf("File::finalize(%p)\n", self);
   Py_CLEAR(self->root);
   Py_CLEAR(self->path);

   Closable::finalize(self);
}


//-----------------------------------------------------------------------------
// Repr
//-----------------------------------------------------------------------------

PyObject * File::repr(File *self) {
   return PyUnicode_FromFormat("File(%R)", self->path);
}


//-----------------------------------------------------------------------------
// getVar
//-----------------------------------------------------------------------------

PyObject * File::getVar(File *self, PyObject *key) {
   if (!self->open)
      return closedHandleError("File");

   if (PyUnicode_Check(key)) {
      RecordFileHandle* THIS = &self->handle;
      RecordFileVariableListHandle varlist;
      memset(&varlist, 0, sizeof(varlist));
      uint result = THIS->getVariableList(THIS, &varlist);
      if (result != RFR_SUCCESS)
         return resultError("File", "getVariableList", result);

      return getVariable(varlist, key);
   } else {
      return PyErr_Format(PyExc_TypeError, "Key must be a string");
   }
}


//-----------------------------------------------------------------------------
// variables
//-----------------------------------------------------------------------------

PyObject * File::variables(File *self, PyObject *Py_UNUSED(args)) {
   if (!self->open)
      return closedHandleError("File");

   RecordFileHandle* THIS = &self->handle;
   RecordFileVariableListHandle varlist;
   memset(&varlist, 0, sizeof(varlist));
   uint result = THIS->getVariableList(THIS, &varlist);
   if (result != RFR_SUCCESS)
      return resultError("File", "getVariableList", result);

   return getVariables(varlist);
}


//-----------------------------------------------------------------------------
// getVarList
//-----------------------------------------------------------------------------

PyObject * File::getVarList(File *self, void *closure) {
   if (!self->open)
      return closedHandleError("File");

   PyObject *object = PyObject_CallMethod(psout_module, "VarList", NULL);
   if (!object)
      return object;

   RecordFileHandle* THIS = &self->handle;
   VarList *var_list = (VarList*)object;
   RecordFileVariableListHandle *varlist = &var_list->handle;

   uint result = THIS->getVariableList(THIS, varlist);
   if (result != RFR_SUCCESS) {
      Py_DECREF(object);
      return resultError("File", "getVariableList", result);
   }

   var_list->open = true;
   return object;
}


//-----------------------------------------------------------------------------
// Get Created/Modified On
//-----------------------------------------------------------------------------

PyObject * File::getCreated(File *self, void *closure) {
   if (!self->open)
      return closedHandleError("File");

   RecordFileHandle* THIS = &self->handle;
   long long timestamp = 0;
   uint result = THIS->getCreatedOn(THIS, timestamp);
   if (result != RFR_SUCCESS)
      return resultError("File", "getCreatedOn", result);

   return timestamp_to_date(timestamp);
   }

PyObject * File::getModified(File *self, void *closure) {
   if (!self->open)
      return closedHandleError("File");

   RecordFileHandle* THIS = &self->handle;
   long long timestamp = 0;
   uint result = THIS->getLastModifiedOn(THIS, timestamp);
   if (result != RFR_SUCCESS)
      return resultError("File", "getLastModifiedOn", result);

   return timestamp_to_date(timestamp);
}


//-----------------------------------------------------------------------------
// Get Run Count
//-----------------------------------------------------------------------------

PyObject * File::getRunCount(File *self, void *closure) {
   if (!self->open)
      return closedHandleError("File");

   RecordFileHandle* THIS = &self->handle;
   uint runs = 0;
   uint result = THIS->getRunCount(THIS, runs);
   if (result != RFR_SUCCESS)
      return resultError("File", "getRunCount", result);

   return PyLong_FromUnsignedLong(runs);
}


//-----------------------------------------------------------------------------
// Get Run
//-----------------------------------------------------------------------------

PyObject * File::getRun(File *self, PyObject *arg0) {
   if (!self->open)
      return closedHandleError("File");

   long _index = PyLong_AsLong(arg0);
   if (PyErr_Occurred())
      return nullptr;

   RecordFileHandle* THIS = &self->handle;
   uint count;
   uint result = THIS->getRunCount(THIS, count);
   if (result != RFR_SUCCESS)
      return resultError("File", "getRunCount", result);

   if (_index >= (long)count || _index < -(long)count)
      return PyErr_Format(PyExc_IndexError, "Index out of range");

   unsigned int index = _index >= 0 ? _index : _index + count;

   PyObject *obj = PyObject_CallMethod(psout_module, "Run",
                                       "O", self);
   Run *rh = (Run *)obj;

   result = THIS->getRun(THIS, index, &rh->handle);
   if (result != RFR_SUCCESS) {
      Py_XDECREF(obj);
      return resultError("File", "getRun", result);
   }
 
   rh->open = true;
   return obj;
}


//-----------------------------------------------------------------------------
// Fetch Run
//-----------------------------------------------------------------------------

PyObject * File::fetchRun(File *self, PyObject *arg0) {
   if (!self->open)
      return closedHandleError("File");

   long _id = PyLong_AsLong(arg0);
   if (PyErr_Occurred())
      return nullptr;
   if (_id < 0 || _id > UINT_MAX)
      return PyErr_Format(PyExc_ValueError, "Invalid Id");
   uint id = _id;

   PyObject *obj = PyObject_CallMethod(psout_module, "Run",
                                       "O", self);
   if (!obj)
      return obj;
   Run *rh = (Run *)obj;

   RecordFileHandle* THIS = &self->handle;
   uint result = THIS->fetchRun(THIS, id, &rh->handle);
   if (result != RFR_SUCCESS) {
      Py_XDECREF(obj);
      return resultError("File", "fetchRun", result);
   }

   rh->open = true;
   return obj;
   }


   //-----------------------------------------------------------------------------
// Get Root
//-----------------------------------------------------------------------------

PyObject * File::getRoot(File *self, void *closure) {
   if (!self->open)
      return closedHandleError("File");

   if (self->root == NULL) {
      self->root = PyObject_CallMethod(psout_module, "Call", NULL);

      if (!self->root)
         return PyErr_Format(PyExc_MemoryError, "Failed to allocate Call Handle");
      }

   Call *root = (Call *)self->root;
   if (!root->open) {
      RecordFileHandle* THIS = &self->handle;
      memset(&root->handle, 0, sizeof(root->handle));
      uint result = THIS->getRoot(THIS, &root->handle);
      if (result != RFR_SUCCESS)
         return resultError("File", "getRoot", result);

      root->open = true;
      }

   Py_INCREF(self->root);
   return self->root;
}


//-----------------------------------------------------------------------------
// Close
//-----------------------------------------------------------------------------

PyObject * File::close(File *self, PyObject *args) {
   if (!self->open)
      return closedHandleError("File");

   RecordFileHandle* THIS = &self->handle;
   uint result = THIS->close(THIS);

   self->open = false;

   if (result != RFR_SUCCESS)
      return resultError("File", "close", result);

   Py_RETURN_NONE;
}


