import re

def is_fun_declaration(line, fun_id):
    id_re = r"[a-z_][a-z0-9_]*"
    declaration_re = r"\s*def\s+{}\s*(\(\s*\)|\(\s*{}\s*(,\s*{})*\s*\))\s*:\s*".format(id_re, id_re, id_re)
    return bool(re.match(declaration_re, line, re.IGNORECASE))    
    

# FIXME: works only for function declarations in one line
def extract_fun(py, fun_id):

    def empty(s):
        return s.strip() == ""

    def count_spaces(s):
        return len(s) - len(s.lstrip())
    
    in_declaration = False
    result = []
    for line in py.split("\n"):
        if is_fun_declaration(line, fun_id):
            in_declaration = True
            leading_spaces = count_spaces(line)
            result.append(line)
        else:
            if in_declaration:
                if not empty(line) and count_spaces(line) <= leading_spaces:
                    in_declaration = False
                    while empty(result[-1]):
                        result.pop()
                    return "\n".join(result)
                else:
                    result.append(line)
    return ""
