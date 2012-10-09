#include <Python.h>

#include <string>

#include <boost/python.hpp>
#include <parser.h>

using namespace boost::python;

void
parser(const struct parser_param *param)
{
    Py_Initialize(); // safe to call multiple times

    object mod = import("python_global_tags");
    list defs = 
        extract<list>(
            mod.attr("process_python_file")(param->file));
    
    for (int i = 0; i < len(defs); ++i)
    {
        tuple def = extract<tuple>(defs[i]);
        
        std::string symbol = extract<std::string>(def[0]);
        int line_no        = extract<int>(def[1]);
        std::string code   = extract<std::string>(def[2]);

        param->put(PARSER_DEF, 
                   symbol.c_str(), 
                   line_no, 
                   param->file, 
                   code.c_str(), 
                   param->arg);
    }
}
