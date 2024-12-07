import re

# iz koda uklanjamo delove oznacene sa
#   // -*- hide -*-
#   ...
#   // -*- show -*-
#
#   i
#
#   // -*- ellipsis -*-
#   ...
#   // -*- show -*-
#
# pri cemu se na mesto ellipsis ubacuje komentar // ...
# i nakon toga uklanjamo nepotrebno uvlacenje koda (bar jedna
# linija koda mora da pocne na levoj margini)
def process_magic_comments(src):

    def last_nonempty_line(lines):
        for line in lines[::-1]:
            if line.strip():
                return line
        return ""

    def num_leading_spaces(str):
        return len(str) - len(str.lstrip())
    
    def min_leading_spaces(lines):
        return min(num_leading_spaces(line) for line in lines if line.strip())

    # uklanjamo nepotrebno uvlacenje celog bloka koda
    def remove_extra_indent(lines):
        min_indent = min_leading_spaces(lines)
        result = ""
        for line in lines:
            if line.strip():
                result += line[min_indent:]
            else:
                result += line
        return result

    TABS_TO_SPACES = 4
        
    # stanja automata
    sHIDE = 0
    sSHOW = 1

    # prepisujemo liniju po liniju, sakrivajuci kod i azurirajuci najmanje uvlacenje
    state = sSHOW
    result = []
    for line in src.split("\n"):
        if re.match(r"\s*(\/\/|#) -\*- hide -\*-", line):
            state = sHIDE
        else:
            m = re.match(r"\s*(\/\/|#) -\*- ellipsis -\*-", line)
            if m:
                comment_sign = m.group(1)
                state = sHIDE
                if result:
                    prev_nonempty_line = last_nonempty_line(result)
                    indent = num_leading_spaces(prev_nonempty_line)
                    if re.match(r"\s*{\s*", prev_nonempty_line):
                        indent += TABS_TO_SPACES
                else:
                    indent = 0
                result.append(" " * indent +  comment_sign + " ...\n")
            elif re.match(r"\s*(\/\/|#) -\*- show -\*-", line):
                state = sSHOW
            elif state == sSHOW:
                result.append(line.replace("\t", " " * TABS_TO_SPACES) + "\n")

    # specijalan slucaj kada se uvlacenja prvog magicnog komentara
    # //... ne moze odrediti na osnovu prethodne linije, pa je moramo
    # odrediti na osnovu sledece
    if len(result) > 1 and result[0].startswith("// ..."):
        result[0] = num_leading_spaces(result[1]) * " " + result[0]
            
    return remove_extra_indent(result)

# cisti izvorni kod od magicnih komentara
def remove_magic_comments(src):
    result = ""
    for line in src.split("\n"):
        # ako nije magicni komentar, liniju kopiramo na izlaz
        if not re.match(r"\s*(//|#)\s*-\*-", line):
            result += line + "\n"
    return result

if __name__ == '__main__':
    from task_repository import TaskRepository
    repo = TaskRepository('_zadaci/01 Zbirka_1')
    src = repo.source_code('prosecno_odstupanje_od_minimuma', 'ex0', 'cs')
    print(process_magic_comments(src))
    print(remove_magic_comments(src))
