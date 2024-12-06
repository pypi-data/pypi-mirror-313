#include <Python.h>

#if !defined(_WIN32) && !defined(_WIN64)
#define DCPD_API __attribute__((visibility("default")))
#else
#ifdef DCPD_EXPORTS
#define DCPD_API __declspec(dllexport)
#else
#define DCPD_API __declspec(dllimport)
#endif
#endif
#ifdef __cplusplus
extern "C" {
#endif
DCPD_API const char* DM_GetLibVersion();	

static PyObject* py_getversion(PyObject* self, PyObject* args) {
    const char* version = DM_GetLibVersion();
    return PyUnicode_FromString(version);
}

static PyMethodDef MyMethods[] = {
    {"getversion", py_getversion, METH_NOARGS, "Get the version."},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef MyModule = {
    PyModuleDef_HEAD_INIT,
    "DynamsoftCodeParserDedicator",
    NULL,
    -1,
    MyMethods
};

PyMODINIT_FUNC PyInit__DynamsoftCodeParserDedicator(void) {
    return PyModule_Create(&MyModule);
}
#ifdef __cplusplus
}
#endif
