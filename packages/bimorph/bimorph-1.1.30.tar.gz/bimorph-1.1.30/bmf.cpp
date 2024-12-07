#include <boost/python.hpp>

class Example {
public:
    Example(int x) : data(x) {}
    int get_data() { return data; }
private:
    int data;
};

BOOST_PYTHON_MODULE(example) {
   using namespace boost::python;
	class_<Example>("Example", init<int>())
        .def("get_data", &Example::get_data);
}
