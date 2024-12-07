#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include "EmtCoSim/EmtCoSim.h"

static PyObject *CosimError;

static int initialized = 0;
static int instance = 0;

typedef struct {
    PyObject_HEAD
    int instance;
    EmtdcCosimulation_Channel *channel;
    int recv_size;
    int send_size;
} ChannelObject;

static int library_check() {
    if (initialized != 1) {
        PyErr_Format(CosimError, "Library is not initialized");
        return 0;
    }
    return 1;
}

static int instance_check(ChannelObject *self) {
    if (initialized != 1) {
        PyErr_Format(CosimError, "Library is not initialized");
        return 0;
    }
    if (self->instance != instance) {
        PyErr_Format(CosimError, "Obsolete channel reference");
        return 0;
    }
    return 1;
}

static void
Channel_dealloc(ChannelObject *self)
{
    Py_TYPE(self)->tp_free((PyObject *) self);
}

static PyObject *
Channel_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
    ChannelObject *self;
    self = (ChannelObject *) type->tp_alloc(type, 0);
    if (self != NULL) {
        self->instance = instance;
        self->channel = NULL;
    }
    return (PyObject *) self;
}

static int
Channel_init(ChannelObject *self, PyObject *args, PyObject *kwargs)
{
    static char *kwlist[] = {"id", NULL};
    int channel_id;

    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "i", kwlist, &channel_id))
        return -1;

    if (!library_check())
        return -1;

    self->channel = EmtdcCosimulation_FindChannel(channel_id);
    if (self->channel == NULL)
        return PyErr_Format(CosimError, "No such channel: %d", channel_id), -1;

    self->recv_size = self->channel->GetRecvSize(self->channel);
    self->send_size = self->channel->GetSendSize(self->channel);

    return 0;
}

static PyObject *
Channel_get_value(ChannelObject *self, PyObject *args)
{
    double time;
    int index;

    if (!PyArg_ParseTuple(args, "di", &time, &index))
        return NULL;

    if (!instance_check(self))
        return NULL;

    if (index < 0 || index >= self->recv_size)
        return PyErr_Format(PyExc_IndexError, "Invalid index: %d",
                            index);
    
    double value = self->channel->GetValue(self->channel, time, index);

    return PyFloat_FromDouble(value);
}

static PyObject *
Channel_get_values(ChannelObject *self, PyObject *args)
{
    double time;

    if (!PyArg_ParseTuple(args, "d", &time))
        return NULL;

    if (!instance_check(self))
        return NULL;

    PyObject *values = PyTuple_New(self->recv_size);
    for (int index=0; index<self->recv_size; index++) {
        double value = self->channel->GetValue(self->channel, time,
                                               index);
        PyTuple_SET_ITEM(values, index, PyFloat_FromDouble(value));
    }

    return values;
}

static PyObject *
Channel_set_value(ChannelObject *self, PyObject *args)
{
    double value;
    int index;

    if (!PyArg_ParseTuple(args, "di", &value, &index))
        return NULL;

    if (!instance_check(self))
        return NULL;

    if (index < 0 || index >= self->send_size)
        return PyErr_Format(PyExc_IndexError, "Invalid index: %d",
                            index);

    self->channel->SetValue(self->channel, value, index);

    Py_RETURN_NONE;
}

static PyObject *
Channel_set_values(ChannelObject *self, PyObject *args)
{
    if (!instance_check(self))
        return NULL;

    if (PyTuple_Size(args) != self->send_size)
        return PyErr_Format(CosimError, "%d values expected",
                            self->send_size);
    
    for (int index=0; index<self->send_size; index++) {
        PyObject *val = PyTuple_GET_ITEM(args, index);
        double value = PyFloat_AsDouble(val);
        if (PyErr_Occurred())
            return NULL;

        self->channel->SetValue(self->channel, value, index);
    }

    Py_RETURN_NONE;
}

static PyObject *
Channel_send(ChannelObject *self, PyObject *args)
{
    double time;

    if (!PyArg_ParseTuple(args, "d", &time))
        return NULL;

    if (!instance_check(self))
        return NULL;

    self->channel->Send(self->channel, time);

    Py_RETURN_NONE;
}

static PyObject *
Channel_get_id(ChannelObject *self, void *closure)
{
    if (!instance_check(self))
        return NULL;

    return PyLong_FromLong(self->channel->GetChannelId(self->channel));
}

static PyObject *
Channel_get_send_size(ChannelObject *self, void *closure)
{
    if (!instance_check(self))
        return NULL;

    return PyLong_FromLong(self->send_size);
}

static PyObject *
Channel_get_recv_size(ChannelObject *self, void *closure)
{
    if (!instance_check(self))
        return NULL;

    return PyLong_FromLong(self->recv_size);
}


static PyMethodDef Channel_methods[] = {
    {"get_value", (PyCFunction) Channel_get_value, METH_VARARGS,
        "get_value(self, time, index)\n--\n\n"
        "Retrieve the value on the given index of the channel for\n"
        "the time indicated.\n"
        "\n"
        "This call will block until the sender publishes the channel\n"
        "values for the requested time.\n"
        "\n"
        "0 <= `index` < `Channel.recv_size`\n"
    },
    {"set_value", (PyCFunction) Channel_set_value, METH_VARARGS,
        "set_value(self, value, index)\n--\n\n"
        "Store a value in the given index for sending to the remote end."
        "\n"
        "0 <= `index` < `Channel.send_size`\n"
    },
    {"get_values", (PyCFunction) Channel_get_values, METH_VARARGS,
        "get_values(self, time)\n--\n\n"
        "Retrieve all values of the channel for the time indicated.\n"
        "\n"
        "This call will block until the sender publishes the channel\n"
        "values for the requested time.\n"
        "\n"
        "Returns `Channel.recv_size` values."
    },
    {"set_values", (PyCFunction) Channel_set_values, METH_VARARGS,
        "set_values(self, *values)\n--\n\n"
        "Set all values of the channel.\n"
        "\n"
        "Raise an error if the number of values given is not `Channel.send_size`."
    },
    {"send", (PyCFunction) Channel_send, METH_VARARGS,
        "send(self, time)\n--\n\n"
        "Send the stored values to the remote end, indicating these\n"
        "values become valid when the remote end reaches the given time."
    },
    {NULL}  /* Sentinel */
};

static PyGetSetDef Channel_getsetters[] = {
    {"id", (getter) Channel_get_id, NULL,
        "The channel id (read-only)",
        NULL
    },
    {"send_size", (getter) Channel_get_send_size, NULL,
        "Number of channel values sent to the remote end. (read-only)",
        NULL
    },
    {"recv_size", (getter) Channel_get_recv_size, NULL,
        "Number of channel values received from the remote end. (read-only)",
        NULL
    },
    {NULL}  /* Sentinel */
};

static PyTypeObject ChannelType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name = "mhi.cosim.Channel",
    .tp_doc = "A channel object for a given `channel_id`\n\n"
              "Example::\n\n"
              "    channel = mhi.cosim.Channel(1)\n",
    .tp_basicsize = sizeof(ChannelObject),
    .tp_itemsize = 0,
    .tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
    .tp_new = Channel_new,
    .tp_init = (initproc) Channel_init,
    .tp_dealloc = (destructor) Channel_dealloc,
    //.tp_members = Channel_members,
    .tp_methods = Channel_methods,
    .tp_getset = Channel_getsetters,
};


static PyObject *
cosim_initialize_cfg(PyObject *self, PyObject *args)
{
    const char *config;

    if (!PyArg_ParseTuple(args, "s", &config))
        return NULL;
    
    if (initialized)
        return PyErr_Format(CosimError, "Already initialized");
    
    EmtdcCosimulation_InitializeCosimulationCfg(config);
    initialized++;
    instance++;

    Py_RETURN_NONE;
}

static PyObject *
cosim_finalize(PyObject *self, PyObject *args)
{
    if (initialized != 1)
        return PyErr_Format(CosimError, "Not initialized");
        
    EmtdcCosimulation_FinalizeCosimulation();
    initialized--;

    Py_RETURN_NONE;
}

static PyMethodDef CosimMethods[] = {
    {"initialize_cfg", cosim_initialize_cfg, METH_VARARGS,
        "initialize_cfg(config_file)\n--\n\n"
        "Call this function to start the Co-Simulation Process. Only call this\n"
        "function once per process.  This function accepts the host\n"
        "and port specified in a configuration file.\n"
    },
    {"finalize", cosim_finalize, METH_NOARGS,
        "finalize()\n--\n\n"
        "Call this function to end the Co-Simulation process.\n"
    },
    {NULL, NULL, 0, NULL}
};

static const char * cosim_doc = "\
MHI PSCAD Cosimulation Extension\n\
";

static struct PyModuleDef cosim_module = {
    PyModuleDef_HEAD_INIT,
    "mhi.cosim",    /* name of module */
    NULL,           /* module documentation, may be NULL */
    -1,             /* size of per-interpreter state of the module,
                       or -1 if the module keeps state in global variables. */
    CosimMethods
};


PyMODINIT_FUNC
PyInit__cosim(void)
{
    PyObject *m;
    
    if (PyType_Ready(&ChannelType) < 0)
        return NULL;
    
    m = PyModule_Create(&cosim_module);
    if (m == NULL)
        return NULL;
    
    Py_INCREF(&ChannelType);
    if (PyModule_AddObject(m, "Channel", (PyObject *) &ChannelType) < 0) {
        Py_DECREF(&ChannelType);
        Py_DECREF(m);
        return NULL;
    }
    
    CosimError = PyErr_NewException("mhi.cosim.Error", NULL, NULL);
    Py_INCREF(CosimError);
    if (PyModule_AddObject(m, "Error", CosimError) < 0)
    {
        Py_XDECREF(CosimError);
        Py_CLEAR(CosimError);
        Py_DECREF(&ChannelType);
        Py_DECREF(m);
        return NULL;
    }

    return m;
}

