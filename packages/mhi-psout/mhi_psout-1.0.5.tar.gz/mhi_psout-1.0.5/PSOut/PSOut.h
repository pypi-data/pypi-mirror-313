#pragma once

#define PY_SSIZE_T_CLEAN

//=============================================================================
// Includes
//=============================================================================


#include <Python.h>
#include "structmember.h"
#include "../CurveFile/Interface.h"

//=============================================================================
// Types
//=============================================================================

typedef unsigned int uint;


//=============================================================================
// Python Type Definition Macros
//=============================================================================

#define MODULE "_psout"

#define MEMBER(NAME, TYPE, FIELD, FLAG, DESCR) { NAME, TYPE, offsetof(Proxy, FIELD), FLAG, DESCR }

#define GETSET(NAME, GET, SET, DESCR, CLOSURE) \
               { NAME, (getter)GET, (setter)SET, DESCR, (void*)(CLOSURE) }

#define METHOD(NAME, FUNC, ARGS, DESCR) { NAME, (PyCFunction)FUNC, ARGS, DESCR }



//=============================================================================
// Helper Functions
//=============================================================================

PyObject * getVariables(RecordFileVariableListHandle& varlist);
PyObject * getVariable(RecordFileVariableListHandle& varlist, PyObject *key);

PyObject * closedHandleError(const char *type);
PyObject * resultError(const char *type, const char *call, uint result);


//=============================================================================
// Python PSOUT Module
//=============================================================================

extern PyObject *psout_module;


//=============================================================================
// Python Type Classes
//=============================================================================

//-----------------------------------------------------------------------------
// All PSOut Handles are Closable objects
//-----------------------------------------------------------------------------

struct Closable {
private:
   PyObject_HEAD

public:
            bool                    open;

private:
   static   PyMemberDef             members[];
   static   PyGetSetDef             getsetters[];
   static   PyMethodDef             methods[];

   static   PyType_Slot             slots[];
   static   PyType_Spec             type_spec;

protected:
   static   void                    typeFromSpec(PyTypeObject* &type, PyType_Spec &spec);

public:
   static   PyTypeObject *          type;
   static   void                    makeType() { typeFromSpec(type, type_spec); }

protected:
   static   int                     init(Closable *self, PyObject *args, PyObject *kwds);
   static   void                    finalize(Closable *self);
   static   PyObject *              enter(Closable *self, PyObject *args);
   static   PyObject *              exit(Closable *self, PyObject *args);
   static   PyObject *              close(Closable *self, PyObject *args);
};


//-----------------------------------------------------------------------------
// Call Handle
//-----------------------------------------------------------------------------

struct Call : Closable {
public:
            RecordFileCallHandle    handle;

private:
   static   PyMemberDef             members[];
   static   PyGetSetDef             getsetters[];
   static   PyMethodDef             methods[];

   static   PyType_Slot             slots[];
   static   PyType_Spec             type_spec;

public:
   static   PyTypeObject *          type;
   static   void                    makeType() { typeFromSpec(type, type_spec); }

private:
   static   PyObject *              getVarList(Call *self, void *closure);

   static   PyObject *              getId(Call *self, void *closure);
   static   PyObject *              getCallCount(Call *self, void *closure);
   static   PyObject *              getParent(Call *self, void *closure);

private:
   static   int                     init(Call *self, PyObject *args, PyObject *kwargs);
   static   Py_hash_t               hash(Call *self);
   static   PyObject *              equal(Call *self, PyObject *that);
// static   void                    finalize(Call *self);
   static   PyObject *              repr(Call *self);
   static   PyObject *              close(Call *self, PyObject *args);
   static   PyObject *              variables(Call *self, PyObject *Py_UNUSED(args));
   static   PyObject *              getCall(Call *self, PyObject *index);
   static   PyObject *              fetchCall(Call *self, PyObject *id);
   static   PyObject *              getVar(Call *self, PyObject *key);
};



//-----------------------------------------------------------------------------
// Trace Handle
//-----------------------------------------------------------------------------

struct Trace : Closable {
private:
            PyObject *              run;
public:
            RecordFileTraceHandle   handle;
            PyObject *              data;

private:
   static   PyMemberDef             members[];
   static   PyGetSetDef             getsetters[];
   static   PyMethodDef             methods[];

   static   PyType_Slot             slots[];
   static   PyType_Spec             type_spec;

public:
   static   PyTypeObject *          type;
   static   void                    makeType() { typeFromSpec(type, type_spec); }

private:
   static   PyObject *              getKey(Trace *self, PyObject *key);
   static   PyObject *              getVarList(Trace *self, void *closure);

   static   PyObject *              getId(Trace *self, void *closure);
   static   PyObject *              getDataType(Trace *self, void *closure);
   static   PyObject *              getDomain(Trace *self, void *closure);
   static   PyObject *              getSize(Trace *self, void *closure);
   static   PyObject *              getCall(Trace *self, void *closure);
   static   PyObject *              getData(Trace *self, void *closure);

private:
   static   int                     init(Trace *self, PyObject *args, PyObject *kwargs);
   static   void                    finalize(Trace *self);
   static   Py_hash_t               hash(Trace *self);
   static   PyObject *              equal(Trace *self, PyObject *that);
   static   PyObject *              repr(Trace *self);
   static   PyObject *              close(Trace *self, PyObject *args);
// static   PyObject *              isRun(Trace *self, PyObject *args);
   static   PyObject *              variables(Trace *self, PyObject *Py_UNUSED(args));
   };


//-----------------------------------------------------------------------------
// Run Handle
//-----------------------------------------------------------------------------

struct Run : Closable {
private:
   PyObject *              file;
public:
   RecordFileRunHandle     handle;

private:
   static  PyMemberDef             members[];
   static  PyGetSetDef             getsetters[];
   static  PyMethodDef             methods[];

   static  PyType_Slot             slots[];
   static  PyType_Spec             type_spec;

public:
   static  PyTypeObject *          type;
   static  void                    makeType() { typeFromSpec(type, type_spec); }

private:
   static  PyObject *              getKey(Run *self, PyObject *key);
   static  PyObject *              getVarList(Run *self, void *closure);

   static  PyObject *              getId(Run *self, void *closure);
   static  PyObject *              getTraceCount(Run *self, void *closure);

private:
   static  int                     init(Run *self, PyObject *args, PyObject *kwargs);
   static  void                    finalize(Run *self);
   static  Py_hash_t               hash(Run *self);
   static  PyObject *              equal(Run *self, PyObject *that);
   static  PyObject *              repr(Run *self);
   static  PyObject *              close(Run *self, PyObject *args);
// static  PyObject *              getTrace(Run *self, PyObject *args, PyObject *kwargs);
   static  PyObject *              getTrace(Run *self, PyObject *arg0);
   static  PyObject *              variables(Run *self, PyObject *Py_UNUSED(args));
};


//-----------------------------------------------------------------------------
// VarList Handle
//-----------------------------------------------------------------------------

struct VarList : Closable {
public:
            RecordFileVariableListHandle  handle;

private:
   static   PyMemberDef             members[];
   static   PyGetSetDef             getsetters[];
   static   PyMethodDef             methods[];

   static   PyType_Slot             slots[];
   static   PyType_Spec             type_spec;

public:
   static   PyTypeObject *          type;  
   static   void                    makeType() { typeFromSpec(type, type_spec); }

private:
   static   PyObject *              getKey(VarList *self, PyObject *key);

private:
   static   int                     init(VarList *self, PyObject *args, PyObject *kwargs);
// static   void                    finalize(VarList *self);
   static   Py_hash_t               hash(VarList *self);
   static   PyObject *              equal(VarList *self, PyObject *that);
   static   PyObject *              close(VarList *self, PyObject *args);
   static   PyObject *              as_dict(VarList *self, PyObject *args);
};


//-----------------------------------------------------------------------------
// File Handle
//-----------------------------------------------------------------------------

struct File : Closable {
private:
            PyObject *              path;
            PyObject *              root;
            RecordFileHandle        handle;
            RecordFileCreationStats stats;

private:
   static   PyMemberDef             members[];
   static   PyGetSetDef             getsetters[];
   static   PyMethodDef             methods[];

   static   PyType_Slot             slots[];
   static   PyType_Spec             type_spec;

public:
   static   PyTypeObject *          type;
   static   void                    makeType() { typeFromSpec(type, type_spec); }

private:
   static   PyObject *              getCreated(File *self, void *closure);
   static   PyObject *              getModified(File *self, void *closure);
   static   PyObject *              getRunCount(File *self, void *closure);
   static   PyObject *              getRoot(File *self, void *closure);
   static   PyObject *              getVarList(File *self, void *closure);

private:
   static   int                     init(File *self, PyObject *args, PyObject *kwargs);
   static   void                    finalize(File *self);
   static   PyObject *              repr(File *self);
   static   PyObject *              close(File *self, PyObject *args);
   static   PyObject *              variables(File *self, PyObject *Py_UNUSED(args));
   static   PyObject *              getRun(File *self, PyObject *index);
   static   PyObject *              fetchRun(File *self, PyObject *id);
   static   PyObject *              getVar(File *self, PyObject *key);
   };

