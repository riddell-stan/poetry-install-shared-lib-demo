# distutils: language=c++
# cython: language_level=3
from libcpp cimport bool
from libcpp.string cimport string

# wrap the constructor and two methods defined in `google/protobuf/wrappers.pb.h`.
# See `wrappers.proto` for the file which generated `wrappers.pb.h`.
cdef extern from "<google/protobuf/wrappers.pb.h>" namespace "google::protobuf":
    cdef cppclass StringValue:
        StringValue()
        void set_value(string& value)
        string& value()

def example_string():
    cdef StringValue message
    message.set_value(b"this is a test string")
    return message.value()
