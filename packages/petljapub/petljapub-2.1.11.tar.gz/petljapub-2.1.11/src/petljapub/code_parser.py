from . import cpp_parser
from . import py_parser

def extract_fun(lang, code, fun_id):
    if lang == "py":
        return py_parser.extract_fun(code, fun_id)
    else:
        return cpp_parser.extract_fun(code, fun_id)

def extract_funs(lang, code, fun_ids):
    return "\n\n".join([extract_fun(lang, code, fun).rstrip("\n") for fun in fun_ids]) + "\n"
