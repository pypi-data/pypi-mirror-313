//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// PSOUT File Serialize
//------------------------------------------------------------------------------
// This is a library for reading and writing *.psout file. The file is formatted
// in a way that allows for large amount of data to be written to or read from
// without needing the entire file in memory. This file accomplishes this through
// a design that lends itself to Random Access of the file.
//
// The file separates itself into "Pages" which can be read and operated on
// independently of other "Pages". Any Pages that are not being actively read
// from or written to are offloaded onto the disk.
//
// The file stores information in a direct "Binary" fashion that is not human
// readable. It begins with the same 128 bit identifier at the start of the file.
// It also contains several "Constant Real Numbers" that it compares the binary
// values against to ensure the same binary encoding was used.
//
// There are three main storage section of the file.
//   1. Traces, These are large arrays of double \ real values.
//   2. Call Stack, This stores location information about the traces
//   3. String Table, This is where all string information in the file is
//      stored, This is because strings are of varying sizes.
//
// Created By:
// ~~~~~~~~~~~
//    PSCAD Design Team <pscad@hvdc.ca>
//    Manitoba HVDC Research Centre Inc.
//    Winnipeg, Manitoba. CANADA
//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#pragma once

#pragma pack(push)

//------------------------------------------------------------------------------
// Forward References for structure required to operate with the interface
//------------------------------------------------------------------------------
struct __RecordFileHandle__;
struct __RecordFileCallHandle__;
struct __RecordFileTraceHandle__;
struct __RecordFileRunHandle__;
struct __RecordFileVariableListHandle__;
struct __RecordFileBaseHandle__;
struct __RecordFileCreationStats__;
struct __RecordFileComplex64__;
struct __RecordFileComplex128__;

//------------------------------------------------------------------------------
// Renaming of structure to use common names
//------------------------------------------------------------------------------
typedef struct __RecordFileHandle__                RecordFileHandle;
typedef struct __RecordFileCallHandle__            RecordFileCallHandle;
typedef struct __RecordFileTraceHandle__           RecordFileTraceHandle;
typedef struct __RecordFileRunHandle__             RecordFileRunHandle;
typedef struct __RecordFileVariableListHandle__    RecordFileVariableListHandle;
typedef struct __RecordFileBaseHandle__            RecordFileBaseHandle;
typedef struct __RecordFileCreationStats__         RecordFileCreationStats;
typedef struct __RecordFileComplex64__             RecordFileComplex64;
typedef struct __RecordFileComplex128__            RecordFileComplex128;

//------------------------------------------------------------------------------
// OpenRecordFileHandleA()
//
// Opens / Creates a file at the provided file path
//------------------------------------------------------------------------------
unsigned int _cdecl OpenRecordFileHandleA(const char * file_path, unsigned int open_type, RecordFileCreationStats * file_stats, RecordFileHandle * handle);

//------------------------------------------------------------------------------
// OpenRecordFileHandleW()
//
// Opens / Creates a file at the provided file path
//------------------------------------------------------------------------------
unsigned int _cdecl OpenRecordFileHandleW(const wchar_t * file_path, unsigned int open_type, RecordFileCreationStats * file_stats, RecordFileHandle * handle);

//==============================================================================
// RecordFileBaseHandle
//------------------------------------------------------------------------------
// This structure stores the internal information required to operate on each
// of the other structures.
//------------------------------------------------------------------------------
#pragma pack(1)
struct __RecordFileBaseHandle__
   {
   void * pReserved; // Reserved for internal use
   };

//================================================================================
// RecordFileHandle
//--------------------------------------------------------------------------------
// This is a handle to a file
//--------------------------------------------------------------------------------
#pragma pack(1)
struct __RecordFileHandle__
   {
   RecordFileBaseHandle cObject;
   unsigned int (_cdecl *getCreatedOn)        (RecordFileHandle * _this, long long& create_time);
   unsigned int (_cdecl *getLastModifiedOn)   (RecordFileHandle * _this, long long& mod_time);
   unsigned int (_cdecl *getVariableList)     (RecordFileHandle * _this, RecordFileVariableListHandle * list);
   unsigned int (_cdecl *getRunCount)         (RecordFileHandle * _this, unsigned int& count);
   unsigned int (_cdecl *getRun)              (RecordFileHandle * _this, unsigned int index, RecordFileRunHandle * run);
   unsigned int (_cdecl *fetchRun)            (RecordFileHandle * _this, unsigned int id, RecordFileRunHandle * run);
   unsigned int (_cdecl *addRun)              (RecordFileHandle * _this, unsigned int id, RecordFileRunHandle * run);
   unsigned int (_cdecl *getRoot)             (RecordFileHandle * _this, RecordFileCallHandle* root);
   unsigned int (_cdecl *close)               (RecordFileHandle * _this);
   };

//================================================================================
// RecordFileCallHandle
//--------------------------------------------------------------------------------
// This is a handle to a call in the call tree \ stack of the file.
//--------------------------------------------------------------------------------
#pragma pack(1)
struct __RecordFileCallHandle__
   {
   RecordFileBaseHandle cObject;
   unsigned int (_cdecl *getId)          (RecordFileCallHandle * _this, unsigned int& id);
   unsigned int (_cdecl *getVariableList)(RecordFileCallHandle * _this, RecordFileVariableListHandle * list);
   unsigned int (_cdecl *getCallCount)   (RecordFileCallHandle * _this, unsigned int& count);
   unsigned int (_cdecl *getCall)        (RecordFileCallHandle * _this, unsigned int index, RecordFileCallHandle* call);
   unsigned int (_cdecl *fetchCall)      (RecordFileCallHandle * _this, unsigned int id, RecordFileCallHandle* call);
   unsigned int (_cdecl *addCall)        (RecordFileCallHandle * _this, unsigned int id, RecordFileCallHandle* call);
   unsigned int (_cdecl *addTraceCall)   (RecordFileCallHandle * _this, unsigned int id, RecordFileCallHandle* trace);
   unsigned int (_cdecl *getParent)      (RecordFileCallHandle * _this, RecordFileCallHandle * call);
   unsigned int (_cdecl *hash)           (RecordFileCallHandle * _this, long long &hash);
   unsigned int (_cdecl *equal)          (RecordFileCallHandle * _this, RecordFileCallHandle * _that, int &equal);
   unsigned int (_cdecl *close)          (RecordFileCallHandle * _this);
   };

//================================================================================
// RecordFileTraceHandle
//--------------------------------------------------------------------------------
// This is a handle to a call in the call tree \ stack of the file.
//--------------------------------------------------------------------------------
#pragma pack(1)
struct __RecordFileTraceHandle__
   {
   RecordFileBaseHandle cObject;
   unsigned int (_cdecl *getId)              (RecordFileTraceHandle * _this, unsigned int& id);
   unsigned int (_cdecl *getDataType)        (RecordFileTraceHandle * _this, unsigned int& type);
   unsigned int (_cdecl *getVariableList)    (RecordFileTraceHandle * _this, RecordFileVariableListHandle * list);
   unsigned int (_cdecl *getDomain)          (RecordFileTraceHandle * _this, RecordFileTraceHandle* domain);
   unsigned int (_cdecl *getSize)            (RecordFileTraceHandle * _this, unsigned long long& size);
   unsigned int (_cdecl *getCall)            (RecordFileTraceHandle * _this, RecordFileCallHandle * call);
   unsigned int (_cdecl *isRun)              (RecordFileTraceHandle * _this, RecordFileRunHandle * run, int& equal);
   unsigned int (_cdecl *peek)               (RecordFileTraceHandle * _this, long long& length);
   unsigned int (_cdecl *readValue)          (RecordFileTraceHandle * _this, void * buffer, long long buffer_size, unsigned int type);
   unsigned int (_cdecl *writeValue)         (RecordFileTraceHandle * _this, void * buffer, long long buffer_size, unsigned int type);
   unsigned int (_cdecl *readValues)         (RecordFileTraceHandle * _this, void * buffer, long long buffer_size, unsigned int type, int value_count, int &read);
   unsigned int (_cdecl *writeValues)        (RecordFileTraceHandle * _this, void * buffer, long long buffer_size, unsigned int type, int value_count, int &written);
   unsigned int (_cdecl *seek)               (RecordFileTraceHandle * _this, unsigned long long value_count, int direction);
   unsigned int (_cdecl *reset)              (RecordFileTraceHandle * _this);
   unsigned int (_cdecl *hash)               (RecordFileTraceHandle * _this, long long &hash);
   unsigned int (_cdecl *equal)              (RecordFileTraceHandle * _this, RecordFileTraceHandle * _that, int &equal);
   unsigned int (_cdecl *close)              (RecordFileTraceHandle * _this);
   };

//=================================================================================
// RecordFileRunHandle
//---------------------------------------------------------------------------------
// This is a handle to a run set in the Record File. The run set is a collection of
// traces, that match the set structure defined by the call nodes
//---------------------------------------------------------------------------------
#pragma pack(1)
struct __RecordFileRunHandle__
   {
   RecordFileBaseHandle cObject;
   unsigned int (_cdecl *getId)              (RecordFileRunHandle * _this, unsigned int& id);
   unsigned int (_cdecl *getVariableList)    (RecordFileRunHandle * _this, RecordFileVariableListHandle * list);
   unsigned int (_cdecl *getTraceCount)      (RecordFileRunHandle * _this, unsigned int& count);
   unsigned int (_cdecl *getTrace)           (RecordFileRunHandle * _this, unsigned int index, RecordFileTraceHandle * trace);
   unsigned int (_cdecl *fetchTrace)         (RecordFileRunHandle * _this, RecordFileCallHandle * call, RecordFileTraceHandle * trace);
   unsigned int (_cdecl *addTrace)           (RecordFileRunHandle * _this, RecordFileCallHandle* trace_call, unsigned int data_type, RecordFileTraceHandle* domain, RecordFileTraceHandle* trace);
   unsigned int (_cdecl *hash)               (RecordFileRunHandle * _this, long long &hash);
   unsigned int (_cdecl *equal)              (RecordFileRunHandle * _this, RecordFileRunHandle * _that, int &equal);
   unsigned int (_cdecl *close)              (RecordFileRunHandle * _this);
   };

//=================================================================================
// RecordFileVariableList
//---------------------------------------------------------------------------------
// This is a handle to a variable list of name/values pairs. The names may be
// presented in ASCII or UNICODE (however if names are in UNICODE they will be
// inaccessible to callers using the ASCII set only. Values are defined separate
// and are defined as one of the RecordFileVariableType enumerations
//---------------------------------------------------------------------------------
#pragma pack(1)
struct __RecordFileVariableListHandle__
   {
   RecordFileBaseHandle cObject;
   unsigned int (_cdecl *getVariableTypeA)   (RecordFileVariableListHandle * _this, const char *     name, unsigned int& type);
   unsigned int (_cdecl *getVariableTypeW)   (RecordFileVariableListHandle * _this, const wchar_t *  name, unsigned int& type);
   unsigned int (_cdecl *getVariableLengthA) (RecordFileVariableListHandle * _this, const char *     name, long long& length);
   unsigned int (_cdecl *getVariableLengthW) (RecordFileVariableListHandle * _this, const wchar_t *  name, long long& length);
   unsigned int (_cdecl *getVariableA)       (RecordFileVariableListHandle * _this, const char *     name, void* buffer, long long buffer_size, unsigned int type);
   unsigned int (_cdecl *getVariableW)       (RecordFileVariableListHandle * _this, const wchar_t *  name, void* buffer, long long buffer_size, unsigned int type);
   unsigned int (_cdecl *setVariableA)       (RecordFileVariableListHandle * _this, const char *     name, void* buffer, long long buffer_size, unsigned int type);
   unsigned int (_cdecl *setVariableW)       (RecordFileVariableListHandle * _this, const wchar_t *  name, void* buffer, long long buffer_size, unsigned int type);
   unsigned int (_cdecl *getCount)           (RecordFileVariableListHandle * _this, long long&       length);
   unsigned int (_cdecl *getNameA)           (RecordFileVariableListHandle * _this, long long        index, char* name   , long long buffer_size);
   unsigned int (_cdecl *getNameW)           (RecordFileVariableListHandle * _this, long long        index, wchar_t* name, long long buffer_size);
   unsigned int (_cdecl *getNameSize)        (RecordFileVariableListHandle * _this, long long        index, long long& length);
   unsigned int (_cdecl *hash)               (RecordFileVariableListHandle * _this, long long &hash);
   unsigned int (_cdecl *equal)              (RecordFileVariableListHandle * _this, RecordFileVariableListHandle * _that, int &equal);
   unsigned int (_cdecl *close)              (RecordFileVariableListHandle * _this);
   };

//=================================================================================
// RecordFileCreationStats
//---------------------------------------------------------------------------------
// This is a handle to a call in the call tree \ stack of the file.
//---------------------------------------------------------------------------------
#pragma pack(1)
struct __RecordFileCreationStats__
   {
   unsigned int   iSectionSize;
   unsigned int   iReserveCount;
   unsigned int   iGrowthRate;
   };

//=================================================================================
// RecordFileComplex64
//---------------------------------------------------------------------------------
// A complex number represented by two 32 bit floating pointer numbers. This
// structure corresponds to the RFVT_Complex64 enumeration in the
// RecordFileVariableType enumerable
//---------------------------------------------------------------------------------
#pragma pack(1)
struct __RecordFileComplex64__
   {
   float iReal;
   float iImag;
   };

//=================================================================================
// RecordFileComplex64
//---------------------------------------------------------------------------------
// A complex number represented by two 64 bit floating pointer numbers. This
// structure corresponds to the RFVT_Complex128 enumeration in the
// RecordFileVariableType enumerable
//---------------------------------------------------------------------------------
#pragma pack(1)
struct __RecordFileComplex128__
   {
   double iReal;
   double iImag;
   };

//=================================================================================
// RecordFileResponse
//---------------------------------------------------------------------------------
// This enumerable represents the responses that can occur from a call to the
// library. This indicates success of the function call, or failure, and what
// kind of failure.
//---------------------------------------------------------------------------------
enum RecordFileResponse
   {
      RFR_SUCCESS = 0
   ,  RFR_INVALID_HANDLE = 1
   ,  RFR_INVALID_PARAMETER = 2
   ,  RFR_FAIL = 0xFFFF
   };

//=================================================================================
// RecordFileOpenType
//---------------------------------------------------------------------------------
// This enumerable enumerates the different ways a file can be opened or created.
//---------------------------------------------------------------------------------
enum RecordFileOpenType
   {
      RFOT_CREATENEW = 0
   ,  RFOT_OPENEXISTING = 1
   ,  RFOT_OPEN_CREATE = 2
   ,  RFOT_CREATEOVERWRITE = 3
   ,  RFOT_CREATERENAME = 4
   };

//=================================================================================
// RecordFilePageSize
//---------------------------------------------------------------------------------
// This enumerable enumerates the different page sizes that are supported by
// the file for file creation. Larger page size may require less page swapping,
// which may be faster, but it may provide more wasted unused space. and require
// more memory to operate on.
//---------------------------------------------------------------------------------
enum RecordFilePageSize
   {
      RFPS_DEFAULT = 0
   ,  RFPS_1024 = 1
   ,  RFPS_2048 = 2
   ,  RFPS_4096 = 3
   ,  RFPS_8192 = 4
   ,  RFPS_16384 = 5
   ,  RFPS_32768 = 6
   ,  RFPS_65536 = 7
   };

//=================================================================================
// RecordFileReserverSize
//---------------------------------------------------------------------------------
// This enumerable enumerates the reserve sizes, this is the initial size of
// the file in pages. (To get the size in bytes multiply this value * the page
// size value). The large the initial size is, the longer it has until the first
// resizing operation. The resizing operation are semi-expensive, by allocating more
// at the start, it can postpone any resize operation.
//---------------------------------------------------------------------------------
enum RecordFileReserverSize
   {
      RFRS_DEFAULT = 0
   ,  RFRS_1024 = 1
   ,  RFRS_2048 = 2
   ,  RFRS_4096 = 3
   ,  RFRS_8192 = 4
   ,  RFRS_16384 = 5
   ,  RFRS_32768 = 6
   ,  RFRS_65536 = 7
   ,  RFRS_131072 = 8
   ,  RFRS_262144 = 9
   ,  RFRS_524288 = 10
   ,  RFRS_1048576 = 11
   };

//=================================================================================
// RecordFileGrowthSize
//---------------------------------------------------------------------------------
// This enumerable enumerates the growth sizes, this is the amount the size of
// the file will grow when needing to allocate for file space, in pages. (To get
// the size in bytes multiply this value * the page size value). The large the
// growth size is, the fewer resizing operation it will need but the more
// potential space it may take up (temporary) while writing.  The resizing
// operation are  semi-expensive, by increasing the amount it resize it can
// reduce the number of resize operations.
//---------------------------------------------------------------------------------
enum RecordFileGrowthSize
   {
      RFGS_DEFAULT = 0
   , RFGS_256 = 1
   , RFGS_512 = 2
   , RFGS_1024 = 3
   , RFGS_2048 = 4
   , RFGS_4096 = 5
   , RFGS_8192 = 6
   , RFGS_16384 = 7
   , RFGS_32768 = 8
   , RFGS_65536 = 9
   , RFGS_131072 = 10
   , RFGS_262144 = 11
   , RFGS_524288 = 12
   , RFGS_1048576 = 13
   };

//=================================================================================
// RecordFileVariableType
//---------------------------------------------------------------------------------
// This enumerable enumerates the variable types that can be stored in this file.
// Some of the variable types in here are defined as a buffered type, meaning that
// they have no definitive size, and the size must be provided for each value to be
// set
//
// Note: Values in this enumerable are not continuous, there are spot reserved for
//       new value types and encodings.
//---------------------------------------------------------------------------------
enum RecordFileVariableType
   {
      RFVT_Invalid = 0
   ,  RFVT_Bit  = 1
   ,  RFVT_Byte = 2
   ,  RFVT_Charater = 8
   ,  RFVT_WideChar = 9
   ,  RFVT_Int16   = 16
   ,  RFVT_UInt16  = 17
   ,  RFVT_Int32   = 18
   ,  RFVT_UInt32  = 19
   ,  RFVT_Int64   = 20
   ,  RFVT_UInt64  = 21
   ,  RFVT_Real32  = 32
   ,  RFVT_Real64  = 33
   ,  RFVT_Complex64 = 64
   ,  RFVT_Complex128 = 65
   ,  RFVT_StringAscii  = 128
   ,  RFVT_StringUnicode = 129
   ,  RFVT_Blob    = 255
   };

//=================================================================================
// RecordFileSeekDirection
//---------------------------------------------------------------------------------
// This enumerable enumerates the ways a trace can seek from its current position.
//---------------------------------------------------------------------------------
enum RecordFileSeekDirection
   {
      RFSD_ForwardFromBeginning = 0
   ,  RFSD_ForwardFromCurrent = 1
   ,  RFSD_BackwardFromCurrent = 2
   };

#pragma pack(pop)

//------------------------------------------------------------------------------
// OpenRecordFileHandleA()
//
// Opens / Creates a file at the provided file path
//
// Parameters:
//   file_path   const char*                ANSI file path containing location
//                                          of file to open.
//
//   open_type   unsigned int               The type of open / create that this
//                                          operation should complete as. This
//                                          value should be one of the values in
//                                          the RecordFileOpenType enumerable
//
//   file_stats  RecordFileCreationStats*   The creation state required to create
//                                          a new file.
//
//   handle      RecordFileHandle*          A handle to an initialized (zeroed)
//                                          structure to hold the file that
//                                          is being opened / created.
//
// Returns:
//   integer that corresponds to RecordFileResponse indicating success or
//   failure, see RecordFileResponse for more information on return values
//
//------------------------------------------------------------------------------
// OpenRecordFileHandleW()
//
// Opens / Creates a file at the provided file path
//
// Parameters:
//   file_path   const wchar_t*             UNICODE file path containing location
//                                          of file to open.
//
//   open_type   unsigned int               The type of open / create that this
//                                          operation should complete as. This
//                                          value should be one of the values in
//                                          the RecordFileOpenType enumerable
//
//   file_stats  RecordFileCreationStats*   The creation state required to create
//                                          a new file.
//
//   handle      RecordFileHandle*          A handle to an initialized (zeroed)
//                                          structure to hold the file that
//                                          is being opened / created.
//
// Returns:
//   integer that corresponds to RecordFileResponse indicating success or
//   failure, see RecordFileResponse for more information on return values
//------------------------------------------------------------------------------

//================================================================================
// RecordFileHandle
//--------------------------------------------------------------------------------
// This is a handle to a file
//--------------------------------------------------------------------------------
// RecordFileHandle_getCreatedOn()
//
//    Gets the date \ time seconds from beginning of epoch, in a 64bit number for
//    the creation of this file
//
// Parameters:
//    _this          RecordFileHandle*          The object to operate on
//                                              (the this pointer)
//
//    create_time    long long&                 The value that will contain the
//                                              creation time, in seconds from
//                                              epoch
//
// Returns:
//    integer that corresponds to RecordFileResponse indicating success or
//    failure, see RecordFileResponse for more information on return values
//
//--------------------------------------------------------------------------------
// RecordFileHandle_getLastModifiedOn()
//
//    Gets the date \ time seconds from beginning of epoch, in a 64bit number for
//    the last modification made to this file.
//
// Parameters:
//    _this          RecordFileHandle*          The object to operate on
//                                              (the this pointer)
//
//    mod_time       long long&                 The value that will contain the
//                                              modification time, in seconds from
//                                              epoch
//
// Returns:
//    integer that corresponds to RecordFileResponse indicating success or
//    failure, see RecordFileResponse for more information on return values
//
//--------------------------------------------------------------------------------
// RecordFileHandle_getVariableList()
//
//    Gets the variable list, that contains name/value pairs for this object
//
// Parameters:
//    _this          RecordFileHandle*          The object to operate on
//                                              (the this pointer)
//
//    list           RecordFileVariableListHandle&   A blank handle to a variable list,
//                                                   to set to this variable list
//
// Returns:
//    integer that corresponds to RecordFileResponse indicating success or
//    failure, see RecordFileResponse for more information on return values
//
//--------------------------------------------------------------------------------
// RecordFileHandle_getRunCount()
//
//    Gets the date \ time seconds from beginning of epoch, in a 64bit number for
//    the last modification made to this file.
//
// Parameters:
//    _this          RecordFileHandle*          The object to operate on
//                                              (the this pointer)
//
//    count          unsigned int&              The value that will be filled with
//                                              the number of runs in this file.
//
// Returns:
//    integer that corresponds to RecordFileResponse indicating success or
//    failure, see RecordFileResponse for more information on return values
//
//--------------------------------------------------------------------------------
// RecordFileHandle_getRun()
//
//    Gets the date \ time seconds from beginning of epoch, in a 64bit number for
//    the last modification made to this file.
//
// Parameters:
//    _this          RecordFileHandle*          The object to operate on
//                                              (the this pointer)
//
//    index          unsigned int               The index of the run to retrieve
//
// Returns:
//    integer that corresponds to RecordFileResponse indicating success or
//    failure, see RecordFileResponse for more information on return values
//
//--------------------------------------------------------------------------------
// RecordFileHandle_fetchRun()
//
//    Gets the date \ time seconds from beginning of epoch, in a 64bit number for
//    the last modification made to this file.
//
// Parameters:
//    _this          RecordFileHandle*          The object to operate on
//                                              (the this pointer)
//
//    id             unsigned int               The id of the run to retrieve
//
// Returns:
//    integer that corresponds to RecordFileResponse indicating success or
//    failure, see RecordFileResponse for more information on return values
//
//--------------------------------------------------------------------------------
// RecordFileHandle_addRun()
//
//    Gets the date \ time seconds from beginning of epoch, in a 64bit number for
//    the last modification made to this file.
//
// Parameters:
//    _this          RecordFileHandle*          The object to operate on
//                                              (the this pointer)
//
//    id             unsigned int               The id of the run to add
//
// Returns:
//    integer that corresponds to RecordFileResponse indicating success or
//    failure, see RecordFileResponse for more information on return values
//
//--------------------------------------------------------------------------------
// RecordFileHandle_getRoot()
//
//    Gets the root call for this file
//
// Parameters:
//    _this          RecordFileHandle*          The object to operate on
//                                              (the this pointer)
//
//    root           RecordFileCallHandle*      A handle to an initialized
//                                              (zeroed) structure to hold the
//                                              call that is being retrieved.
//
// Returns:
//    integer that corresponds to RecordFileResponse indicating success or
//    failure, see RecordFileResponse for more information on return values
//
//--------------------------------------------------------------------------------
// RecordFileHandle_close()
//
//    Closes the file, thus invalidating all open Handles that are associated with
//    this file. (other handles should still be closed to prevent memory leaks,
//    however any other operation will fail as there is no file to operate on)
//
// Parameters:
//    _this          RecordFileHandle*          The object to operate on
//                                              (the this pointer)
//
// Returns:
//    integer that corresponds to RecordFileResponse indicating success or
//    failure, see RecordFileResponse for more information on return values
//--------------------------------------------------------------------------------

//================================================================================
// RecordFileCallHandle
//--------------------------------------------------------------------------------
// This is a handle to a call in the call tree \ stack of the file.
//--------------------------------------------------------------------------------
// getId()
//
//    Retrieves the id of the call
//
// Parameters:
//    _this          RecordFileCallHandle*      The object to operate on
//                                              (the this pointer)
//
//    id             unsigned int&              The buffer that will contain the
//                                              ID after this function is
//                                              successful.
//
// Returns:
//    integer that corresponds to RecordFileResponse indicating success or
//    failure, see RecordFileResponse for more information on return values
//
//--------------------------------------------------------------------------------
// getVariableList()
//
//    Gets the variable list, that contains name/value pairs for this object
//
// Parameters:
//    _this          RecordFileCallHandle*      The object to operate on
//                                              (the this pointer)
//
//    list           RecordFileVariableListHandle&   A blank handle to a variable list,
//                                                   to set to this variable list
//
// Returns:
//    integer that corresponds to RecordFileResponse indicating success or
//    failure, see RecordFileResponse for more information on return values
//
//--------------------------------------------------------------------------------
// getCallCount()
//
//    Retrieves the number of child calls that this call has
//
// Parameters:
//    _this          RecordFileCallHandle*      The object to operate on
//                                              (the this pointer)
//
//    count          unsigned int&              The buffer that will contain the
//                                              value, after the function is
//                                              successful
//
// Returns:
//    integer that corresponds to RecordFileResponse indicating success or
//    failure, see RecordFileResponse for more information on return values
//
//--------------------------------------------------------------------------------
// getCall()
//
//    Retrieves a child call of this call via index
//
// Parameters:
//    _this          RecordFileCallHandle*      The object to operate on
//                                              (the this pointer)
//
//    index          unsigned int               The index of the call to retrieve.
//
//    call           RecordFileCallHandle*      A handle to an initialized
//                                              (zeroed) structure to hold the
//                                              call that is being retrieved.
//
// Returns:
//    integer that corresponds to RecordFileResponse indicating success or
//    failure, see RecordFileResponse for more information on return values
//
//--------------------------------------------------------------------------------
// RecordFileCallHandle_fetchCall()
//
//    Retrieves a child call of this call via id
//
// Parameters:
//    _this          RecordFileCallHandle*      The object to operate on
//                                              (the this pointer)
//
//    id             unsigned int               The id of the call to retrieve.
//
//    call           RecordFileCallHandle*      A handle to an initialized
//                                              (zeroed) structure to hold the
//                                              call that is being retrieved.
//
// Returns:
//    integer that corresponds to RecordFileResponse indicating success or
//    failure, see RecordFileResponse for more information on return values
//
//--------------------------------------------------------------------------------
// RecordFileCallHandle_addCall()
//
//    Creates and appends a call to this call with a provided stats, it will
//    return the created call in a structure provided.
//
// Parameters:
//    _this          RecordFileCallHandle*      The object to operate on
//                                              (the this pointer)
//
//    id             unsigned int               The id of the call to add.
//
//    call           RecordFileCallHandle*      A handle to an initialized
//                                              (zeroed)  structure to hold the
//                                              call that is  being retrieved.
//
// Returns:
//    integer that corresponds to RecordFileResponse indicating success or
//    failure, see RecordFileResponse for more information on return values
//
//--------------------------------------------------------------------------------
// RecordFileCallHandle_addTraceCall()
//
//    Creates and appends a call to this call with a provided stats, that call
//    that is created will also correspond to a trace with the states provided.
//
// Parameters:
//    _this          RecordFileCallHandle*      The object to operate on
//                                              (the this pointer)
//
//    id             int                        The id of the call to add.
//
//    call           RecordFileCallHandle*      A handle to an initialized
//                                              (zeroed) structure to hold the
//                                              call that is being retrieved.
//
// Returns:
//    integer that corresponds to RecordFileResponse indicating success or
//    failure, see RecordFileResponse for more information on return values
//
//--------------------------------------------------------------------------------
// RecordFileCallHandle_getParent()
//
//    Retrieves the parent call of this call.
//
// Parameters:
//    _this          RecordFileCallHandle*      The object to operate on
//                                              (the this pointer)
//
//    call           RecordFileCallHandle*      A handle to an initialized (zeroed)
//                                              structure to hold the call that is
//                                              being retrieved.
//
// Returns:
//    integer that corresponds to RecordFileResponse indicating success or
//    failure, see RecordFileResponse for more information on return values
//
//--------------------------------------------------------------------------------
// RecordFileCallHandle_hash()
//
//    Return the hash value of the call object.  They are used to quickly compare
//    handles to see if they refer to the same underlying object.
//
// Parameters:
//    _this          RecordFileCallHandle*      The object to operate on
//                                              (the this pointer)
//
//    hash           long long                  The hash value for the object
//
// Returns:
//    integer that corresponds to RecordFileResponse indicating success or
//    failure, see RecordFileResponse for more information on return values
//
//--------------------------------------------------------------------------------
// RecordFileCallHandle_equal()
//
//    Checks if two call handles refer to the same call object.
//
// Parameters:
//    _this          RecordFileCallHandle*      The object to operate on
//                                              (the this pointer)
//
//    _that          RecordFileCallHandle*      The object to test against
//
//    equal          int&                       This is 1 if the handles refer
//                                              to the same underlying objects.
//
// Returns:
//    integer that corresponds to RecordFileResponse indicating success or
//    failure, see RecordFileResponse for more information on return values
//
//--------------------------------------------------------------------------------
// RecordFileCallHandle_close()
//
// Closes this call, freeing up all resources associated with the call. All calls
// should be closed, to ensure no memory leaks. Note: after the structure is
// closed,  it will be inoperable, but can be reused for other return values.
//
// Parameters:
//    _this          RecordFileCallHandle*      The object to operate on
//                                              (the this pointer)
//
// Returns:
//    integer that corresponds to RecordFileResponse indicating success or
//    failure, see RecordFileResponse for more information on return values
//--------------------------------------------------------------------------------

//================================================================================
// RecordFileTraceHandle
//--------------------------------------------------------------------------------
// This is a handle to a call in the call tree \ stack of the file.
//--------------------------------------------------------------------------------
// getId()
//
//    Retrieves the id of the trace
//
// Parameters:
//    _this          RecordFileTraceHandle*  The object to operate on
//                                           (the this pointer)
//
//    id             unsigned int&           The buffer that will contain the
//                                           ID after this function is successful.
//
// Returns:
//    integer that corresponds to RecordFileResponse indicating success or
//    failure, see RecordFileResponse for more information on return values
//
//--------------------------------------------------------------------------------
// getDataType()
//
//    Retrieves the Data Type of the trace. The data type is defined by the
//    RecordFileVariableType enumerable
//
// Parameters:
//    _this          RecordFileTraceHandle*  The object to operate on
//                                           (the this pointer)
//
//    type           unsigned int&           The buffer that will contain the
//                                           type after this function is
//                                           successful
//
// Returns:
//    integer that corresponds to RecordFileResponse indicating success or
//    failure, see RecordFileResponse for more information on return values
//
//--------------------------------------------------------------------------------
// getVariableList()
//
//    Gets the variable list, that contains name/value pairs for this object
//
// Parameters:
//    _this          RecordFileTraceHandle*     The object to operate on
//                                              (the this pointer)
//
//    list           RecordFileVariableListHandle&   A blank handle to a variable list,
//                                                   to set to this variable list
//
// Returns:
//    integer that corresponds to RecordFileResponse indicating success or
//    failure, see RecordFileResponse for more information on return values
//
//--------------------------------------------------------------------------------
// getDomain()
//
//    Get the domain trace, that contains the domain values associated with this
//    trace.
//
// Parameters:
//    _this          RecordFileTraceHandle*     The object to operate on
//                                              (the this pointer)
//
//    domain         RecordFileTraceHandle*     A handle to an initialized (zeroed)
//                                              structure to hold the trace that is
//                                              being retrieved.
//
// Returns:
//    integer that corresponds to RecordFileResponse indicating success or
//    failure, see RecordFileResponse for more information on return values
//
//--------------------------------------------------------------------------------
// getSize()
//
// Retrieves the count of values in the trace
//
// Parameters:
//    _this          RecordFileTraceHandle*     The object to operate on
//                                              (the this pointer)
//
//    size           unsigned long long&        The value will be placed in this
//                                              parameter if the call is
//                                              successful
//
// Returns:
//    integer that corresponds to RecordFileResponse indicating success or
//    failure, see RecordFileResponse for more information on return values
//
//--------------------------------------------------------------------------------
// getCall()
//
//    Retrieves the parent call of this trace.
//
// Parameters:
//    _this          RecordFileTraceHandle*     The object to operate on
//                                              (the this pointer)
//
//    call           RecordFileCallHandle*      A handle to an initialized
//                                              (zeroed) structure to hold the
//                                              call that is  being retrieved.
//
// Returns:
//    integer that corresponds to RecordFileResponse indicating success or
//    failure, see RecordFileResponse for more information on return values
//
//--------------------------------------------------------------------------------
// isRun()
//
//    Checks if this trace belongs to the run provided.
//
// Parameters:
//    _this          RecordFileTraceHandle*     The object to operate on
//                                              (the this pointer)
//
//    run            RecordFileRunHandle*       The run object, to check if this
//                                              trace is a member of
//
//    equal          int&                       This is 0 if the run trace is not
//                                              a member of the run, and 1 if it
//                                              is part of the run provided.
//
// Returns:
//    integer that corresponds to RecordFileResponse indicating success or
//    failure, see RecordFileResponse for more information on return values
//
//--------------------------------------------------------------------------------
// peek()
//
//    Retrieves the minimum required buffer size to retrieve the next value.
//
// Parameters:
//    _this          RecordFileTraceHandle*  The object to operate on
//                                              (the this pointer)
//
//    run            long long&               The minum next buffer size required.
//
// Returns:
//    integer that corresponds to RecordFileResponse indicating success or
//    failure, see RecordFileResponse for more information on return values
//
//--------------------------------------------------------------------------------
// readValue()
//
//    Retrieves the next value in the read stream for this trace.
//
// Parameters:
//    _this          RecordFileTraceHandle*     The object to operate on
//                                              (the this pointer)
//
//    buffer         void*                      A buffer that the next value
//                                              will be written into
//
//    buffer_size    long long                  The size of the buffer provided.
//
//    type           unsigned int               The data type that the buffer is
//                                              expecting, as defined by the
//                                              RecordFileVariableType enumerable
//
// Returns:
//    integer that corresponds to RecordFileResponse indicating success or
//    failure, see RecordFileResponse for more information on return values
//
//--------------------------------------------------------------------------------
// writeValue()
//
//    Writes the next value into the stream of the trace.
//
// Parameters:
//    _this          RecordFileTraceHandle*     The object to operate on
//                                              (the this pointer)
//
//    buffer         void*                      A buffer that contains the next
//                                              value to write
//
//    buffer_size    long long                  The size of the buffer provided.
//
//    type           unsigned int               The data type that the buffer
//                                              contains, as defined  by the
//                                              RecordFileVariableType enumerable
//
// Returns:
//    integer that corresponds to RecordFileResponse indicating success or
//    failure, see RecordFileResponse for more information on return values
//
//--------------------------------------------------------------------------------
// readValues()
//
//    Retrieves the next several values in the read stream for this trace.
//
// Parameters:
//    _this          RecordFileTraceHandle*     The object to operate on
//                                              (the this pointer)
//
//    buffer         void*                      A buffer that the next value will
//                                              be written into
//
//    data_size      long long                  The size of each value buffer
//
//    type           unsigned int               The data type that the buffer is
//                                              expecting, as defined by the
//                                              RecordFileVariableType enumerable
//
//    value_count    unsigned int               The number of values to read
//
//    read           int&                       Will contain the number of values
//                                              read, if this call is successful
//
// Returns:
//    integer that corresponds to RecordFileResponse indicating success or
//    failure, see RecordFileResponse for more information on return values
//
// Remarks:
//    If the value type that is being written is a buffered type (such as a
//    string, or blob type) then the buffer provided should be an array of
//    pointers to other buffers of equal length to the size provided. If the Data
//    Type is not a buffered type, then the buffer provided should be a single
//    contiguous memory block, containing the values separated by the data_size
//    provided.
//
//--------------------------------------------------------------------------------
// writeValues()
//
//    Retrieves the next several values in the read stream for this trace.
//
// Parameters:
//    _this          RecordFileTraceHandle*     The object to operate on
//                                              (the this pointer)
//
//    buffer         void*                      A buffer that contains the value
//                                              to write to the stream
//
//    data_size      long long                  The size of each value
//
//    type           unsigned int               The data type that the buffer is
//                                              expecting, as defined by the
//                                              RecordFileVariableType enumerable
//
//    value_count    unsigned int               The number of values to read
//
//    written        int&                       Will contain the number of values
//                                              written, if this call is
//                                              successful
//
// Returns:
//    integer that corresponds to RecordFileResponse indicating success or
//    failure, see RecordFileResponse for more information on return values
//
// Remarks:
//    If the value type that is being written is a buffered type (such as a
//    string, or blob type) then the buffer provided should be an array of
//    pointers to other buffers of equal length to the size provided. If the Data
//    Type is not a buffered type, then the buffer provided should be a single
//    contiguous memory block, containing the values separated by the data_size
//    provided.
//
//--------------------------------------------------------------------------------
// seek()
//
//    Retrieves the next several values in the read stream for this trace.
//
// Parameters:
//    _this          RecordFileTraceHandle*     The object to operate on
//                                              (the this pointer)
//
//    value_count    unsigned long long         The number of values to seek by
//
//    direction      int                        The direction to seek by, as defined
//                                              by the RecordFileSeekDirection
//                                              enumerable
//
// Returns:
//    integer that corresponds to RecordFileResponse indicating success or
//    failure, see RecordFileResponse for more information on return values
//
//--------------------------------------------------------------------------------
// reset()
//
//    Resets the read stream to the beginning of the trace
//
// Parameters:
//   _this          RecordFileTraceHandle*      The object to operate on
//                                              (the this pointer)
//
// Returns:
//    integer that corresponds to RecordFileResponse indicating success or
//    failure, see RecordFileResponse for more information on return values
//
//--------------------------------------------------------------------------------
// RecordFileTraceHandle_hash()
//
//    Return the hash value of the trace object.  They are used to quickly compare
//    handles to see if they refer to the same underlying object.
//
// Parameters:
//    _this          RecordFileTraceHandle*     The object to operate on
//                                              (the this pointer)
//
//    hash           long long                  The hash value for the object
//
// Returns:
//    integer that corresponds to RecordFileResponse indicating success or
//    failure, see RecordFileResponse for more information on return values
//
//--------------------------------------------------------------------------------
// RecordFileTraceHandle_equal()
//
//    Checks if two trace handles refer to the same trace object.
//
// Parameters:
//    _this          RecordFileTraceHandle*     The object to operate on
//                                              (the this pointer)
//
//    _that          RecordFileTraceHandle*     The object to test against
//
//    equal          int&                       This is 1 if the handles refer
//                                              to the same underlying objects.
//
// Returns:
//    integer that corresponds to RecordFileResponse indicating success or
//    failure, see RecordFileResponse for more information on return values
//
//--------------------------------------------------------------------------------
// close()
//
//    Closes this trace, freeing up all resources associated with the trace. All
//    traces should be closed, to ensure no memory leaks. Note: after the
//    structure is closed, it will be inoperable, but can be reused for other
//    return values.
//
// Parameters:
//   _this          RecordFileTraceHandle*      The object to operate on
//                                              (the this pointer)
//
// Returns:
//    integer that corresponds to RecordFileResponse indicating success or
//    failure, see RecordFileResponse for more information on return values
//--------------------------------------------------------------------------------

//=================================================================================
// RecordFileRunHandle
//---------------------------------------------------------------------------------
// This is a handle to a run set in the Record File. The run set is a collection of
// traces, that match the set structure defined by the call nodes
//---------------------------------------------------------------------------------
// RecordFileRunHandle_getId()
//
//    Retrieves the id of the trace
//
// Parameters:
//   _this          RecordFileRunHandle*        The object to operate on
//                                              (the this pointer)
//
//    id             unsigned int&              The buffer that will contain the ID
//                                              after this function is successful.
//
// Returns:
//   integer that corresponds to RecordFileResponse indicating success or
//   failure, see RecordFileResponse for more information on return values
//
//---------------------------------------------------------------------------------
// RecordFileRunHandle_getVariableList()
//
//    Gets the variable list, that contains name/value pairs for this object
//
// Parameters:
//   _this          RecordFileRunHandle*        The object to operate on
//                                              (the this pointer)
//
//    list           RecordFileVariableListHandle*   A blank handle to a variable list,
//                                                   to set to this variable list
//
// Returns:
//   integer that corresponds to RecordFileResponse indicating success or
//   failure, see RecordFileResponse for more information on return values
//
//---------------------------------------------------------------------------------
// RecordFileRunHandle_getTraceCount()
//
//    Retrieves the number of traces that are stored in this Run Set
//
// Parameters:
//   _this          RecordFileRunHandle*        The object to operate on
//                                              (the this pointer)
//
//    count          unsigned int&              The variable that will be filled
//                                              with the number of traces that this
//                                              run contains.
//
// Returns:
//   integer that corresponds to RecordFileResponse indicating success or
//   failure, see RecordFileResponse for more information on return values
//
//---------------------------------------------------------------------------------
// RecordFileRunHandle_getTrace()
//
//    Retrieves the Trace at the index for this run set
//
// Parameters:
//   _this          RecordFileRunHandle*        The object to operate on
//                                              (the this pointer)
//
//    index          unsigned int&              The index of the trace to retrieve
//
//    trace          RecordFileTraceHandle*     A handle to an initialized (zeroed)
//                                              structure to hold the trace that is
//                                              being retrieved.
//
// Returns:
//   integer that corresponds to RecordFileResponse indicating success or
//   failure, see RecordFileResponse for more information on return values
//
// Remarks:
//    The traces have no defined order.
//
//---------------------------------------------------------------------------------
// RecordFileRunHandle_fetchTrace()
//
//    Retrieves the Trace with id provided
//
// Parameters:
//   _this          RecordFileRunHandle*        The object to operate on
//                                              (the this pointer)
//
//    id             unsigned int&              The id of the trace to retrieve
//
//    trace          RecordFileTraceHandle*     A handle to an initialized (zeroed)
//                                              structure to hold the trace that is
//                                              being retrieved.
//
// Returns:
//   integer that corresponds to RecordFileResponse indicating success or
//   failure, see RecordFileResponse for more information on return values
//
// Remarks:
//    The traces have no defined order.
//
//---------------------------------------------------------------------------------
// RecordFileRunHandle_addTrace()
//
//    Adds a trace to the run, on the Trace-Call Provided.
//
// Parameters:
//   _this          RecordFileRunHandle*        The object to operate on
//                                              (the this pointer)
//
//    trace_call     RecordFileCallHandle*      The handle to the call to which the
//                                              structured location of the trace is
//                                              located.
//                                              Note: The call provided here must
//                                              be a trace type call.
//
//    data_type      unsigned int               The requested data type for this
//                                              trace, as defined by the
//                                              RecordFileVariableType enumerable
//
//    domain         RecordFileTraceHandle*     The domain trace of this trace,
//                                              This can be left blank of the trace
//                                              has no domain (or is a domain)
//
//    trace          RecordFileTraceHandle*     A handle to an initialized (zeroed)
//                                              structure to hold the trace that is
//                                              being added.
//
// Returns:
//   integer that corresponds to RecordFileResponse indicating success or
//   failure, see RecordFileResponse for more information on return values
//
//--------------------------------------------------------------------------------
// RecordFileRunHandle_hash()
//
//    Return the hash value of the run object.  They are used to quickly compare
//    handles to see if they refer to the same underlying object.
//
// Parameters:
//    _this          RecordFileRunHandle*       The object to operate on
//                                              (the this pointer)
//
//    hash           long long                  The hash value for the object
//
// Returns:
//    integer that corresponds to RecordFileResponse indicating success or
//    failure, see RecordFileResponse for more information on return values
//
//--------------------------------------------------------------------------------
// RecordFileRunHandle_equal()
//
//    Checks if two run handles refer to the same run object.
//
// Parameters:
//    _this          RecordFileRunHandle*       The object to operate on
//                                              (the this pointer)
//
//    _that          RecordFileRunHandle*       The object to test against
//
//    equal          int&                       This is 1 if the handles refer
//                                              to the same underlying objects.
//
// Returns:
//    integer that corresponds to RecordFileResponse indicating success or
//    failure, see RecordFileResponse for more information on return values
//
//---------------------------------------------------------------------------------
// RecordFileRunHandle_close()
//
//    Closes this trace, freeing up all resources associated with the trace. All
//    run sets should be closed, to ensure no memory leaks. Note: after the
//    structure is closed, it will be inoperable, but can be reused for other
//    return values.
//
//
// Parameters:
//   _this          RecordFileRunHandle*        The object to operate on
//                                              (the this pointer)
//
// Returns:
//   integer that corresponds to RecordFileResponse indicating success or
//   failure, see RecordFileResponse for more information on return values
//---------------------------------------------------------------------------------

//=================================================================================
// RecordFileVariableList
//---------------------------------------------------------------------------------
// This is a handle to a variable list of name/values pairs. The names may be
// presented in ASCII or UNICODE (however if names are in UNICODE they will be
// inaccessible to callers using the ASCII set only. Values are defined separate
// and are defined as one of the RecordFileVariableType enumerations
//---------------------------------------------------------------------------------
// getVariableTypeA()
//
//    Retrieves the Data Type for then variable that is named with the same name as
//    the name provided in the 'name' parameter
//
// Parameters:
//    _this          RecordFileVariableListHandle*       The object to operate on
//                                                       (the this pointer)
//
//    name           const char *               The string name of the value to be
//                                              retrieved. (Encoded in ASCII)
//
//    type           unsigned int&              An integer to place the retrieved
//                                              type information in, if the
//                                              function is successful The value is
//                                              defined by the
//                                              RecordFileVariableType enumeration.
//
// Returns:
//   integer that corresponds to RecordFileResponse indicating success or
//   failure, see RecordFileResponse for more information on return values
//
//---------------------------------------------------------------------------------
// getVariableTypeW()
//
//    Retrieves the Data Type for then variable that is named with the same name as
//    the name provided in the 'name' parameter
//
// Parameters:
//    _this          RecordFileVariableListHandle*       The object to operate on
//                                                       (the this pointer)
//
//    name           const wchar_t *            The string name of the value to be
//                                              retrieved. (Encoded in UNCIODE)
//
//    type           unsigned int&              An integer to place the retrieved
//                                              type information in, if the
//                                              function is successful The value is
//                                              defined by the
//                                              RecordFileVariableType enumeration.
//
// Returns:
//   integer that corresponds to RecordFileResponse indicating success or
//   failure, see RecordFileResponse for more information on return values
//
//---------------------------------------------------------------------------------
// getVariableLengthA()
//
//    Retrieves the Length of the buffer in Bytes of the data stored in the
//    variable that is named with the same name as the name provided in the 'name'
//    parameter
//
// Parameters:
//    _this          RecordFileVariableListHandle*       The object to operate on
//                                                       (the this pointer)
//
//    name           const char *               The string name of the value to be
//                                              retrieved. (Encoded in ASCII)
//
//    type           long long&                 An 64 bit integer to place the
//                                              retrieved length information in, if
//                                              the function is successful
//
// Returns:
//   integer that corresponds to RecordFileResponse indicating success or
//   failure, see RecordFileResponse for more information on return values
//
//---------------------------------------------------------------------------------
// getVariableLengthW()
//
//    Retrieves the Length of the buffer in Bytes of the data stored in the
//    variable that is named with the same name as the name provided in the 'name'
//    parameter
//
// Parameters:
//    _this          RecordFileVariableListHandle*       The object to operate on
//                                                       (the this pointer)
//
//    name           const wchar_t *            The string name of the value to be
//                                              retrieved. (Encoded in UNCIODE)
//
//    type           long long&                 An 64 bit integer to place the
//                                              retrieved length information in, if
//                                              the function is successful
//
// Returns:
//   integer that corresponds to RecordFileResponse indicating success or
//   failure, see RecordFileResponse for more information on return values
//
//---------------------------------------------------------------------------------
// getVariableA()
//
//    Retrieves the value in the variable named with the same name as the name
//    provided in the 'name' parameter. The value should be retrieved as the data
//    type provided in the 'data_type' field as defined by the
//    RecordFileVariableType enumeration.
//
// Parameters:
//    _this          RecordFileVariableListHandle*       The object to operate on
//                                                       (the this pointer)
//
//    name           const char *               The string name of the value to be
//                                              retrieved. (Encoded in ASCII)
//
//    buffer         void*                      The memory buffer to place the
//                                              value into.
//
//    buffer_size    long long                  the size of the buffer
//
//    type           unsigned int               the type variable to retrieve as
//                                              defined by the
//                                              RecordFileVariableType enumeration.
//
// Returns:
//   integer that corresponds to RecordFileResponse indicating success or
//   failure, see RecordFileResponse for more information on return values
//
// Remarks:
//    This function can fail if the value is not found, or no suitable conversion
//    could be found for the type it is stored as, and the type it is requested to
//    be.
//
//---------------------------------------------------------------------------------
// getVariableW()
//
//    Retrieves the value in the variable named with the same name as the name
//    provided in the 'name' parameter. The value should be retrieved as the data
//    type provided in the 'data_type' field as defined by the
//    RecordFileVariableType enumeration.
//
// Parameters:
//    _this          RecordFileVariableListHandle*       The object to operate on
//                                                       (the this pointer)
//
//    name           const wchar_t *            The string name of the value to be
//                                              retrieved. (Encoded in UNCIODE)
//
//    buffer         void*                      The memory buffer to place the
//                                              value into.
//
//    buffer_size    long long                  the size of the buffer
//
//    type           unsigned int               the type variable to retrieve as
//                                              defined by the
//                                              RecordFileVariableType enumeration.
//
// Returns:
//   integer that corresponds to RecordFileResponse indicating success or
//   failure, see RecordFileResponse for more information on return values
//
// Remarks:
//    This function can fail if the value is not found, or no suitable conversion
//    could be found for the type it is stored as, and the type it is requested to
//    be.
//
//---------------------------------------------------------------------------------
// setVariableA()
//
//    Sets the value in the variable with the provided name, to the value that was
//    provided.
//
// Parameters:
//    _this          RecordFileVariableListHandle*       The object to operate on
//                                                       (the this pointer)
//
//    name           const char *               The string name of the value to be
//                                              retrieved. (Encoded in ASCII)
//
//    buffer         void*                      The memory buffer that holds the
//                                              value.
//
//    buffer_size    long long                  the size of the buffer
//
//    type           unsigned int               the type variable to set as defined
//                                              by the RecordFileVariableType
//                                              enumeration.
//
// Returns:
//   integer that corresponds to RecordFileResponse indicating success or
//   failure, see RecordFileResponse for more information on return values
//
//---------------------------------------------------------------------------------
// setVariableW()
//
//    Sets the value in the variable with the provided name, to the value that was
//    provided.
//
// Parameters:
//    _this          RecordFileVariableListHandle*       The object to operate on
//                                                       (the this pointer)
//
//    name           const wchar_t *            The string name of the value to be
//                                              retrieved. (Encoded in UNCIODE)
//
//    buffer         void*                      The memory buffer that holds the
//                                              value.
//
//    buffer_size    long long                  the size of the buffer
//
//    type           unsigned int               the type variable to set as defined
//                                              by the RecordFileVariableType
//                                              enumeration.
//
// Returns:
//   integer that corresponds to RecordFileResponse indicating success or
//   failure, see RecordFileResponse for more information on return values
//
//---------------------------------------------------------------------------------
// RecordFileVariableListHandle_getCount()
//
//    Get the number of variables stored in this variable list
//
// Parameters:
//    _this          RecordFileVariableListHandle*  The object to operate on
//                                                 (the this pointer)
//
//    length         long long&                 The reference to the variable that
//                                              will be filled with the number of
//                                              variables in the list on success
//
// Returns:
//   integer that corresponds to RecordFileResponse indicating success or
//   failure, see RecordFileResponse for more information on return values
//
//---------------------------------------------------------------------------------
// RecordFileVariableListHandle_getNameA()
//
//    Get the name of the variable at the provided index in ANSI form.
//
// Parameters:
//    _this          RecordFileVariableListHandle*  The object to operate on
//                                                 (the this pointer)
//
//    index         long long                      The index into the variable list
//                                                 that for the name to retrieve
//
//    name          char*                          A pointer to the buffer that will
//                                                 be filled with the name of the
//                                                 variable in ANSI form.
//
//    buffer_size   long long                      The size in bytes of the name buffer.
//
// Returns:
//   integer that corresponds to RecordFileResponse indicating success or
//   failure, see RecordFileResponse for more information on return values
//
//---------------------------------------------------------------------------------
// RecordFileVariableListHandle_getNameW()
//
//    Get the name of the variable at the provided index in UNICODE form.
//
// Parameters:
//    _this          RecordFileVariableListHandle*  The object to operate on
//                                                 (the this pointer)
//
//    index         long long                      The index into the variable list
//                                                 that for the name to retrieve
//
//    name          wchar_t*                       A pointer to the buffer that will
//                                                 be filled with the name of the
//                                                 variable in UNICODE form.
//
//    buffer_size   long long                      The size in bytes of the name buffer.
//
// Returns:
//   integer that corresponds to RecordFileResponse indicating success or
//   failure, see RecordFileResponse for more information on return values
//
//---------------------------------------------------------------------------------
// RecordFileVariableListHandle_getNameSize()
//
//    Get the size of the string that holds the variable. This value will be in
//    the number of characters, regardless of the format stored in.
//
// Parameters:
//    _this         RecordFileVariableListHandle*  The object to operate on
//                                                 (the this pointer)
//
//    index         long long                      The index into the variable list
//                                                 that for the name to retrieve
//
//    length        long long&                     The variable that will be filled
//                                                 with the length of the name in
//                                                 characters.
//
// Returns:
//   integer that corresponds to RecordFileResponse indicating success or
//   failure, see RecordFileResponse for more information on return values
//
//--------------------------------------------------------------------------------
// RecordFileVariableListHandle_hash()
//
//    Return the hash value of the variable list object.  They are used to quickly
//    compare handles to see if they refer to the same underlying object.
//
// Parameters:
//    _this          RecordFileVariableListHandle*  The object to operate on
//                                                  (the this pointer)
//
//    hash           long long                      The hash value for the object
//
// Returns:
//    integer that corresponds to RecordFileResponse indicating success or
//    failure, see RecordFileResponse for more information on return values
//
//--------------------------------------------------------------------------------
// RecordFileVariableListHandle_equal()
//
//    Checks if two variable list handles refer to the same variable list object.
//
// Parameters:
//    _this          RecordFileVariableListHandle*  The object to operate on
//                                                  (the this pointer)
//
//    _that          RecordFileVariableListHandle*  The object to test against
//
//    equal          int&                           This is 1 if the handles refer
//                                                  to the same underlying objects.
//
// Returns:
//    integer that corresponds to RecordFileResponse indicating success or
//    failure, see RecordFileResponse for more information on return values
//
//---------------------------------------------------------------------------------
// close()
//
//    Closes this Variable list, freeing up all resources associated with the
//    trace.  traces should be closed, to ensure no memory leaks. Note: after the
//    structure is closed, it will be inoperable, but can be reused for other
//    return values.
//
// Parameters:
//    _this          RecordFileVariableListHandle*       The object to operate on
//                                                       (the this pointer)
//
// Returns:
//   integer that corresponds to RecordFileResponse indicating success or
//   failure, see RecordFileResponse for more information on return values
//---------------------------------------------------------------------------------

//=================================================================================
// RecordFileCreationStats
//---------------------------------------------------------------------------------
// This is a handle to a call in the call tree \ stack of the file.
//
// Contents:
//   iSectionSize   unsigned int      The size of the pages in the file. This
//                                    value should be set to one of the values
//                                    in the RecordFilePageSize enumerable
//
//   iReserveCount  unsigned int      The size of the file reserve at the
//                                    creation of the file, in counts of pages.
//                                    This value should be set to one of the
//                                    values in the RecordFileReserverSize
//                                    enumerable.
//
//   iGrowthRate    unsigned int      The size of the growth of this file in
//                                    counts of pages. This value should be set
//                                    to one of the values in the
//                                    RecordFileGrowthSize enumerable
//---------------------------------------------------------------------------------

//=================================================================================
// RecordFileComplex64
//---------------------------------------------------------------------------------
// A complex number represented by two 32 bit floating pointer numbers. This
// structure corresponds to the RFVT_Complex64 enumeration in the
// RecordFileVariableType enumerable
//
// Contents:
//   iReal    float (32bit)     32 bit floating pointer number that represents
//                              the real value of the complex number
//
//   iImag    float (32bit)     32 bit floating pointer number that represents
//                              the imaginary value of the complex number
//
//---------------------------------------------------------------------------------

//=================================================================================
// RecordFileComplex64
//---------------------------------------------------------------------------------
// A complex number represented by two 64 bit floating pointer numbers. This
// structure corresponds to the RFVT_Complex128 enumeration in the
// RecordFileVariableType enumerable
//
// Contents:
//   iReal    double (64bit)    64 bit floating pointer number that represents
//                              the real value of the complex number
//
//   iImag    double (64bit)    64 bit floating pointer number that represents
//                              the imaginary value of the complex number
//
//---------------------------------------------------------------------------------

//=================================================================================
// RecordFileResponse
//---------------------------------------------------------------------------------
// This enumerable represents the responses that can occur from a call to the
// library. This indicates success of the function call, or failure, and what
// kind of failure.
//
// Values:
//   RFR_SUCCESS             (0)      Method executed successfully
//
//   RFR_INVALID_HANDLE      (1)      Handle to "_this" function is invalid
//
//   RFR_INVALID_PARAMETER   (2)      One of the parameters was not an expected
//                                    value
//
//   RFR_FAIL                (0xFFFF) The function failed, but all input was
//                                    correct. This can indicate that failure
//                                    was a correct action of the execution.
//                                    Such as reading beyond the end of a stream
//
//---------------------------------------------------------------------------------

//=================================================================================
// RecordFileOpenType
//---------------------------------------------------------------------------------
// This enumerable enumerates the different ways a file can be opened or created.
//
// Values:
//   RFOT_CREATENEW          (0)      Create a new file. If a file already exists
//                                     then the function will fail.
//
//   RFOT_OPENEXISTING       (1)      Open a file that exists, if the file does
//                                    not exist, then the function will value
//
//   RFOT_OPEN_CREATE        (2)      Open a file if it exists, create it if it
//                                    does not.
//
//   RFOT_CREATEOVERWRITE    (3)      Create the file if it does not exist, if
//                                    the file does exist, overwrite the file.
//
//   RFOT_CREATERENAME       (4)      Create the file if it does not exists.
//                                    if the file does exist, add counters to
//                                    the end of the name, until a file can be
//                                    found that does not exist, and use that
//                                    file name.
//
//---------------------------------------------------------------------------------

//=================================================================================
// RecordFilePageSize
//---------------------------------------------------------------------------------
// This enumerable enumerates the different page sizes that are supported by
// the file for file creation. Larger page size may require less page swapping,
// which may be faster, but it may provide more wasted unused space. and require
// more memory to operate on.
//
// Values:
//   RFPS_DEFAULT            (0)      Use the default page size, allow the system
//                                    to pick the page size.
//
//   RFPS_1024               (1)      Use 1024 byte page sizes
//
//   RFPS_2048               (2)      Use 2048 byte page sizes
//
//   RFPS_4096               (3)      Use 4096 byte page sizes
//
//   RFPS_8192               (4)      Use 8192 byte page sizes
//
//   RFPS_16384              (5)      Use 16384 byte page sizes
//
//   RFPS_32768              (6)      Use 32768 byte page sizes
//
//   RFPS_65536              (7)      Use 65536 byte page sizes
//
//---------------------------------------------------------------------------------

//=================================================================================
// RecordFileReserverSize
//---------------------------------------------------------------------------------
// This enumerable enumerates the reserve sizes, this is the initial size of
// the file in pages. (To get the size in bytes multiply this value * the page
// size value). The large the initial size is, the longer it has until the first
// resizing operation. The resizing operation are semi-expensive, by allocating more
// at the start, it can postpone any resize operation.
//
// Values:
//   RFRS_DEFAULT            (0)      Use the default reserve size, allow the
//                                    system to pick the reserve size.
//
//   RFRS_1024               (1)      Reserve 1024 pages at file creation time
//
//   RFRS_2048               (2)      Reserve 2048 pages at file creation time
//
//   RFRS_4096               (3)      Reserve 4096 pages at file creation time
//
//   RFRS_8192               (4)      Reserve 8192 pages at file creation time
//
//   RFRS_16384              (5)      Reserve 16384 pages at file creation time
//
//   RFRS_32768              (6)      Reserve 32768 pages at file creation time
//
//   RFRS_65536              (7)      Reserve 65536 pages at file creation time
//
//   RFRS_131072             (8)      Reserve 131072 pages at file creation time
//
//   RFRS_262144             (9)      Reserve 262144 pages at file creation time
//
//   RFRS_524288             (10)     Reserve 524288 pages at file creation time
//
//   RFRS_1048576            (11)     Reserve 1048576 pages at file creation time
//
//---------------------------------------------------------------------------------

//=================================================================================
// RecordFileGrowthSize
//---------------------------------------------------------------------------------
// This enumerable enumerates the growth sizes, this is the amount the size of
// the file will grow when needing to allocate for file space, in pages. (To get
// the size in bytes multiply this value * the page size value). The large the
// growth size is, the fewer resizing operation it will need but the more
// potential space it may take up (temporary) while writing.  The resizing
// operation are  semi-expensive, by increasing the amount it resize it can
// reduce the number of resize operations.
//
// Values:
//   RFGS_DEFAULT            (0)      Use the default growth size, allow the
//                                    system to pick the growth size.
//
//   RFGS_256                (1)      Grow by 256 Pages on each growth operation
//
//   RFGS_512                (2)      Grow by 512 Pages on each growth operation
//
//   RFGS_1024               (3)      Grow by 1024 Pages on each growth operation
//
//   RFGS_2048               (4)      Grow by 2048 Pages on each growth operation
//
//   RFGS_4096               (5)      Grow by 4096 Pages on each growth operation
//
//   RFGS_8192               (6)      Grow by 8192 Pages on each growth operation
//
//   RFGS_16384              (7)      Grow by 16384 Pages on each growth operation
//
//   RFGS_32768              (8)      Grow by 32768 Pages on each growth operation
//
//   RFGS_65536              (9)      Grow by 65536 Pages on each growth operation
//
//   RFGS_131072             (10)     Grow by 131072 Pages on each growth operation
//
//   RFGS_262144             (11)     Grow by 262144 Pages on each growth operation
//
//   RFGS_524288             (12)     Grow by 524288 Pages on each growth operation
//
//   RFGS_1048576            (13)     Grow by 1048576 Pages on each growth operation
//
//---------------------------------------------------------------------------------

//=================================================================================
// RecordFileVariableType
//---------------------------------------------------------------------------------
// This enumerable enumerates the variable types that can be stored in this file.
// Some of the variable types in here are defined as a buffered type, meaning that
// they have no definitive size, and the size must be provided for each value to be
// set
//
// Note: Values in this enumerable are not continuous, there are spot reserved for
//       new value types and encodings.
//
// Values:
//    RFVT_Invalid        (0)         Unknown value
//
//    RFVT_Bit            (1)         This type stores a single bit of
//                                    information, buffers should be passed as a
//                                    byte
//
//    RFVT_Byte           (2)         This type stores a single byte of
//                                    information, buffers should be passed as a
//                                    byte
//
//    RFVT_Charater       (8)         This type stores a single ASCII encoded
//                                    charter, buffers should be passed as a char
//
//    RFVT_WideChar       (9)         This type stores a single UNICODE encoded
//                                    charter, buffers should be passed as a
//                                    wchar_t
//
//    RFVT_Int16          (16)        This type stores a single 16 bit little
//                                    endean encoded signed number, buffers should
//                                    be passed as a short
//
//    RFVT_UInt16         (17)        This type stores a single 16 bit little
//                                    endean encoded unsigned number, buffers
//                                    should be passed as a unsigned short
//
//    RFVT_Int32          (18)        This type stores a single 32 bit little
//                                    endean encoded signed number, buffers should
//                                    be passed as a int
//
//    RFVT_UInt32         (19)        This type stores a single 32 bit little
//                                    endean encoded unsigned number, buffers
//                                    should be passed as a unsigned int
//
//    RFVT_Int64          (20)        This type stores a single 64 bit little
//                                    endean encoded signed number, buffers
//                                    should be passed as a long long
//
//    RFVT_UInt64         (21)        This type stores a single 64 bit little
//                                    endean encoded unsigned number, buffers
//                                    should be passed as a unsigned long long
//
//    RFVT_Real32         (32)        This type stores a single 32 bit floating
//                                    point encoded real number, buffers should be
//                                    passed as a float
//
//    RFVT_Real64         (33)        This type stores a single 64 bit floating
//                                    point encoded real number, buffers should be
//                                    passed as a double
//
//    RFVT_Complex64      (64)        This type stores a single 64 bit complex
//                                    number encoded as 2 32 bit real numbers
//                                    charter, buffers should be passed as a
//                                    RecordFileComplex64
//
//    RFVT_Complex128     (65)        This type stores a single 128 bit complex
//                                    number encoded as 2 64 bit real numbers
//                                    charter, buffers should be passed as a
//                                    RecordFileComplex128
//
//    RFVT_StringAscii    (128)       This type stores a string of ASCII encoded
//                                    characters, This is a buffered type, string
//                                    can be of variable length. Buffers should be
//                                    passed as a char* (where it is an array of
//                                    chars)
//
//    RFVT_StringUnicode  (129)       This type stores a string of UNICODE encoded
//                                    characters, This is a buffered type, string
//                                    can be of variable length. Buffers should be
//                                    passed as a wchar_t* (where it is an array of
//                                    wchar_t)
//
//    RFVT_Blob           (255)       This type stores a blob of data (unknown
//                                    encoding) it is up to the reader/writer to
//                                    determine this data type.  This is a buffered
//                                    type, blobs can be of variable length.
//                                    Buffers should be passed as a void* (where it
//                                    is contiguous memory)
//
//---------------------------------------------------------------------------------

//=================================================================================
// RecordFileSeekDirection
//---------------------------------------------------------------------------------
// This enumerable enumerates the ways a trace can seek from its current position
//
// Values:
//    RFSD_ForwardFromBeginning       (0)   Seek starting from position 0. The
//                                          offset provided will be from position
//                                          0 of the trace read.
//
//    RFSD_ForwardFromCurrent         (1)   Seek forward starting from the current
//                                          position. The offset provided will move
//                                          forward from the current position
//
//    RFSD_BackwardFromCurrent        (2)   Seek Backward starting from the current
//                                          position. The offset provided will move
//                                          backwards from the current position
//---------------------------------------------------------------------------------
