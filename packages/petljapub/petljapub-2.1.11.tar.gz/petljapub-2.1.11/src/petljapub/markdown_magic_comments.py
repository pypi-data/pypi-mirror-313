import re, sys
from . import logger
from . import messages
from . import md_util
from . import javascript

def magic_comment_re(key, value):
    return r"\s*<!---\s*({})\s*:\s*({})([^\n]*)--->".format(key, value)

def is_magic_comment(key, value, str):
    return re.match(magic_comment_re(key, value), str)

def is_magic_comment_end(key, str):
    return is_magic_comment(key, "end", str)

def is_magic_comment_start(key, str):
    return is_magic_comment(key, r"\S+", str) and not is_magic_comment_end(key, str)

# auxiliary function that splits strings like: "word [a long sentence] word" into ["word", "a long sentence", "word"]
def split_string_with_brackets(input_string):
    # Regular expression to find words and sentences within brackets
    pattern = r'(\[[^\[\]]+\])|\b(\w+)\b'
    matches = re.findall(pattern, input_string)
    result = [match[0] if match[0] else match[1] for match in matches]
    return result

def magic_comment_key_value(str):
    m = re.match(magic_comment_re(r"\S+", r"\S+"), str)
    result = {
        "key": m.group(1),
        "value": m.group(2)
    }
    for param in split_string_with_brackets(m.group(3).strip()):
        if param[0]=='[' and param[-1]==']':
            if "title" in result:
                logger.warn("Title is already defined: ", result["title"], " - ", param[1:-1])
            result["title"] = param[1:-1]
        else:
            if "label" in result:
                logger.warn("Label is already defined: ", result["label"], " - ", param)
            result["label"] = param
    return result
    
    

# Checks if there is a block surrounded by the given key
# <!--- key:... --->
# ...
# <!--- key:end --->
def contains_block(md, key):
    for line in md.split("\n"):
        if is_magic_comment_start(key, line):
            return True
    return False

    
# Add the given content to the block marked by
# <!--- key:value --->
#  ...
# <!--- key:end --->
# - If there is a directive 
#     <!--- key_place:value_place --->
#   inside the block, the content is inserted in place of that directive.
# - If there is no such directive, the content is added to the end of
#   the block.
# - If there is no such block, the given content is added to the end of md
def insert_content(md, key, value, content, key_place=None, value_place=None):
    # automaton states
    sWAIT_START = 0
    sWAIT_END = 1
    sCOPY_TO_END = 2
    # copy one by one line
    result = []
    state = sWAIT_START
    content_inserted = False
    for line in md.split("\n"):
        skip_line = False
        if is_magic_comment(key, value, line):
            state = sWAIT_END
        elif state == sWAIT_END:
            if key_place and value_place and is_magic_comment(key_place, value_place, line):
                content_inserted = True
                skip_line = True
                result.append(content)
            if is_magic_comment_end(key, line):
                if not content_inserted:
                    result.append(content)
                state = sCOPY_TO_END
        if not skip_line:
            result.append(line)
    # if we did not find the sought block, the content is added to the end
    if state == sWAIT_START:
        logger.warn("magic comments insert content - block not found, key={}, value={}".format(key, value))
        result.append(content)
    return "\n".join(result)


def process_by_key(md, key, f=lambda lines, value: lines):
    value_stack = []
    result_stack = [[]]
    for line in md.split("\n"):
        if is_magic_comment_start(key, line):
            comment = magic_comment_key_value(line)
            value_stack.append(comment["value"])
            result_stack.append([line])
        elif is_magic_comment_end(key, line):
            if not value_stack:
                logger.error("magic comments")
            result_stack[-1].append(line)
            value = value_stack.pop()
            top = result_stack.pop()
            result_stack[-1].extend(f(top, value))
        else:
            result_stack[-1].append(line)
    return "\n".join(result_stack[-1])


def process_by_key_value(md, key, value, f=lambda lines: lines):
    def f_val(lines, val):
        if val != value:
            return lines
        return f(lines)
    return process_by_key(md, key, f_val)
        


# The markdown content md contains blocks
# <!--- key:value --->
#    ...
# <!--- key:end --->
# the next function excludes everything that is marked by values different from
# the give ones (if ok=True) or equal to the give ones (if ok=False)
def filter_by_key(md, key, given_values, ok=True):
    if not given_values:
        logger.warn("filtering magic comments - empty list of values")

    # check if the value is among given_values
    def value_is_given(value, given_values):
        return not set(given_values).isdisjoint(re.split(r",\s*", value))

    def keep_value(block, value):
        if value_is_given(value, given_values) == ok:
            return block
        else:
            return []

    return process_by_key(md, key, keep_value)

# The markdown content md contains blocks
# <!--- key:value --->
#    ...
# <!--- key:end --->
# the next function exclude every block that is marked by one of the given values
def exclude(md, key, exclude_values):
    return filter_by_key(md, key, exclude_values, False)
    
# The markdown content md contains blocks
# <!--- key:value --->
#    ...
# <!--- key:end --->
# the next function excludes everyt block that is not marked by one of the given values
def exclude_all_except(md, key, keep_values):
    return filter_by_key(md, key, keep_values, True)


def is_magic_comment_directive_start(key, line):
    return re.match(r"^\s*<!---\s*{}\s*$".format(key), line)

def is_magic_comment_directive_end(line):
    return re.match(r"^\s*--->\s*$", line)

def pass_lines(lines):
    pass

def process_magic_comment_directives(md, key, f=pass_lines):
    in_comment = False
    for line in md.split('\n'):
       if is_magic_comment_directive_start(key, line):
           in_comment = True
           lines = []
       elif in_comment and is_magic_comment_directive_end(line):
           f(lines)
           in_comment = False
       else:
           if in_comment:
               lines.append(line)
    
def collect_magic_comment_directives(md, key):
    def f(lines, result):
        result.append("\n".join(lines))
    result = []
    process_magic_comment_directives(md, key, lambda lines: f(lines, result))
    return result
    
def replace_magic_comment_directives(md, key, f=lambda lines: ""):
    result = []
    in_comment = False
    for line in md.split('\n'):
       if is_magic_comment_directive_start(key, line):
           in_comment = True
           lines = []
       elif in_comment and is_magic_comment_directive_end(line):
           result.append(f(lines))
           in_comment = False
       else:
           if in_comment:
               lines.append(line)
           else:
               result.append(line)
    
    return "\n".join(result)


# TODO: this should be split into separate function for each target
#
# Change all
# <!--- div:xxx --->
#   ...
# <!--- div:end --->
#
# to
#
# <div class="xxx">
#   ...
# </div>
#
# or
#
# \begin{xxx}
#   ...
# \end{xxx}
# 
# also giving titles to selected divs, as specified by the div specification.
# For example, if the dictionary contains {"xxx": "**Title.**"} the previous div is changed to
#
# <div class="xxx">
#   **Title.**
#   ...
# </div>
#
# or
#
# If the div specification contains the directive "caption", the tex
# title is given as "\caption{...}" instead of "[...]"
#
# If skip_div_tags is True, div tags are removed (suitable for latex with nested divs)
#
# Parameter target is usually one of "html" or "tex" and allows giving specific formating for each
# target format
#
#
# If the div specification contains the directive "counter", then divs
# are numberred (by adding labels and referrences)

def format_divs(md, target, div_specs=None, skip_div_tags=False):
    system_divs = ["javascript", "center"]
    
    # are there any pseudocode algorithms (if yes, then the library pseudocode.js is included) 
    has_pseudocode = False
    
    if div_specs == None:
        div_specs = messages.div_specs

    div_end_stack = []
    div_type_stack = []
    result = []
    lines = md.split('\n')
    line_no = 0
    in_algorithm = False
    while line_no < len(lines):
        line = lines[line_no]
        line_no += 1
        # start of a div
        if is_magic_comment_start('div', line):
            comment = magic_comment_key_value(line)

            # type of this div (e.g., for div:lemma type is lemma)
            div_type = comment["value"]

            # specification for this div type (read from configuration file)
            specs = None
            if div_type in div_specs:
                specs = div_specs[div_type]
                if isinstance(specs, dict) and target in specs:
                    specs = specs[target]

            if specs == None and div_type not in system_divs:
                logger.warning(f"No specification for {div_type} found")
                specs = {}
                    
            # title of this div
            div_title = None
            if "title" in comment:
                div_title = comment["title"]

            # label of this div
            div_label = comment.get("label", None)

            
            # algorithms in html are handeled specially
            if div_type == "algorithm" and target == "html":
                has_pseudocode = True
                in_algorithm = True
                result.append("```{=html}")
                result.append("<pre class='pseudocode'>")
                result.append("\\begin{algorithm}")
                result.append(f"\\caption{{{div_title}}}")
            elif div_type == "algorithmic" and target == "html":
                result.append("\\begin{algorithmic}")
            elif not skip_div_tags:
                if target == "tex":
                    result.append("```{=latex}")
                    result.append(f"\\begin{{{div_type}}}")
                    if div_title != None:
                        if specs.get("caption", False):
                            result.append(f"\\caption{{{div_title}}}")
                        else:
                            result.append(f"[{div_title}]")
                    result.append("```")
                else:
                    if div_title != None:
                        result.append(f"<div class=\"{div_type}\" title=\"{div_title}\">")
                    else:
                        result.append(f"<div class=\"{div_type}\">")

            if div_label != None:
                result.append(md_util.label(div_type, div_label))

            # starting text and ending text for this div are read from the configuration
            div_start = None
            div_end = None
            if specs:
                if isinstance(specs, str):
                    div_start = specs
                elif isinstance(specs, dict):
                    if "start" in specs:
                        div_start = specs["start"]
                    if "end" in specs:
                        div_end = specs["end"]

            if div_start != None:
                if "counter" in specs:
                    if div_label == None:
                        if not div_type in format_divs.label_num:
                            format_divs.label_num[div_type] = 0
                        format_divs.label_num[div_type] += 1
                        div_label = "__{}__{}__".format(div_type, format_divs.label_num[div_type])
                        result.append(md_util.label(div_type, div_label))
                    div_start = div_start.replace("#", md_util.reference(div_type, div_label))
                else:
                    div_start = re.sub(r"\s*#", "", div_start)
                if target == "html" and "title" in comment:
                    div_start += " *[{}]*".format(comment["title"])
                result.append(div_start)
                
            div_end_stack.append(div_end)
            div_type_stack.append(div_type)

        # end of a div
        elif is_magic_comment_end('div', line):
            div_end = div_end_stack[-1]
            div_end_stack.pop()
            div_type = div_type_stack[-1]
            div_type_stack.pop()
            
            if div_end != None:
                if result[-1].strip().endswith("$$"):
                    result.append("\n")
                result.append(div_end)
            if div_type == "algorithm" and target == "html":
                result.append("\\end{algorithm}")
                result.append("</pre>")
                result.append("```")
                in_algorithm = False
            elif div_type == "algorithmic" and target == "html":
                result.append("\\end{algorithmic}")
            elif not skip_div_tags:
                if result[-1].startswith(" ") or result[-1].strip().endswith("$$"):
                    result.append("\n")
                if target == "tex":
                    result.append("```{=latex}")
                    result.append(f"\\end{{{div_type}}}")
                    result.append("```")
                else:
                    result.append("</div>")
        else:
            result.append(line)
    md = "\n".join(result)


    if has_pseudocode:
        return javascript.pseudocode(md, messages.msg("ALGORITHM"))
    else:
        return md

format_divs.label_num = dict()
