#include <Python.h>
#include "DynamsoftImageProcessing.h"
#ifdef __cplusplus
extern "C" {
#endif

static PyObject* py_getversion(PyObject* self, PyObject* args) {
    const char* version = dynamsoft::dip::CImageProcessingModule::GetVersion();
    return PyUnicode_FromString(version);
}

static PyMethodDef MyMethods[] = {
    {"getversion", py_getversion, METH_NOARGS, "Get the version."},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef MyModule = {
    PyModuleDef_HEAD_INIT,
    "DynamsoftImageProcessing",
    NULL,
    -1,
    MyMethods
};
PyMODINIT_FUNC PyInit__DynamsoftImageProcessing(void) {
    return PyModule_Create(&MyModule);
}
#ifdef __cplusplus
}
#endif
