import re

type_re = r"(const\s+)?[a-z_*&<>]+(\s+[a-z_*&<>]+)*"
id_re = r"[&*]?[a-z_][a-z0-9_]*"
param_re = r"({}\s+{})*".format(type_re, id_re)

def is_fun_declaration(line, fun_id):
    if not fun_id:
        fun_id = id_re
    declaration_re = r"^\s*{}\s+{}(\(\)|\({}(\s*,\s*{})*\))\s*{{?\s*$".format(type_re, fun_id, param_re, param_re)
    return bool(re.match(declaration_re, line, re.IGNORECASE | re.MULTILINE))

def is_partial_fun_declaration(line):
    declaration_re = r"^{}\s+{}(\(\)|\({}(\s*,\s*{})*\s*)$".format(type_re, id_re, param_re, param_re)
    return bool(re.match(declaration_re, line, re.IGNORECASE))
    

def is_line_comment(line):
    return bool(re.match(r"^\s*//", line, re.IGNORECASE))

def extract_fun(cpp, fun_id):
    in_declaration = False
    result = []
    comments = []
    partial = None
    functions = []
    for line in cpp.split("\n"):
        if is_partial_fun_declaration(line):
            partial = [line]
            continue
        if partial:
            partial.append(line)
            line = "\n".join(partial)
            if "{" in line:
                partial = None
        if is_fun_declaration(line, fun_id):
            in_declaration = True
            result = [comment for comment in comments]
            result.append(line)
            num_braces = line.count("{")
        else:
            if in_declaration:
                result.append(line)
                for c in line:
                    if c == "{":
                        num_braces += 1
                    elif c == "}":
                        num_braces -= 1
                if num_braces == 0:
                    in_declaration = False
                    functions.append("\n".join(result) + "\n\n")
        if not in_declaration:
            if is_line_comment(line):
                comments.append(line)
            else:
                comments = []

    return "".join(functions)
            
