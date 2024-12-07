import sys, re
from petljapub.messages import msg
from petljapub import logger 

TEXT_WIDTH_IN_CHARS = 84
TEXT_WIDTH_IN_CM = 14 # cm
CHAR_WIDTH = TEXT_WIDTH_IN_CM / TEXT_WIDTH_IN_CHARS
MARGIN = 2*CHAR_WIDTH
MIN_COLUMN_WIDTH = 1.2 # cm
MIN_EXPLANATION_WIDTH = TEXT_WIDTH_IN_CM / 2

# max width (in cm) of a parsed example (input or output)
# only fixed width items are taken into account (verbatim text and images) 
def max_width(buffer):
    result = 0
    IN_VERBATIM = False
    for line in buffer:
        if re.match(r"\\emph{" + msg("EXPLANATION") + r"}", line):
            result = max(result, MIN_EXPLANATION_WIDTH)
        elif re.search(r"\\begin{verbatim}", line):
            IN_VERBATIM = True
        elif re.search(r"\\end{verbatim}",  line):
            IN_VERBATIM = False
        else:
            if IN_VERBATIM:
              result = max(result, max(len(line) * CHAR_WIDTH, MIN_COLUMN_WIDTH))
            else:
                if re.search(r"\\includegraphics", line):
                    match = re.search(r'width=([\d.]+)\\textwidth', line)
                    if match:
                        width = match.group(1)
                        result = max(result, float(width) * TEXT_WIDTH_IN_CM)
    return result

# check if this item is a task explanation
def is_explanation(item):
    for line in item:
        if re.match(r"\\emph{" + msg("EXPLANATION") + r"}", line):
            return True
    return False

# check if this item is input
def is_input(item):
    for line in item:
        if re.match(r"\\emph{" + msg("INPUT") + r"}", line):
            return True
    return False

# check if this item is output
def is_output(item):
    for line in item:
        if re.match(r"\\emph{" + msg("OUTPUT") + r"}", line):
            return True
    return False

# check if example contains an explanation
def contains_explanation(example):
    for item in example:
        if isinstance(item, list) and is_explanation(item):
            return True
    return False

# removes the figure environment (since it can not be put in minipage)
def remove_figure_environment(example):
    result = []
    for item in example:
        if isinstance(item, list):
            result_item = []
            for line in item:
                if not '\\begin{figure}' in line and not '\\end{figure}' in line and not '\\caption{}' in line:
                    if '\\caption{' in line:
                        line = re.sub(r'\\caption\{(.+?)\}', r'\n\n\1\n\n', line)
                    elif re.search(r"\\includegraphics", line):
                        match = re.search(r'width=([\d.]+)\\textwidth', line)
                        if match:
                            width = match.group(1)
                            line = line.replace(match.group(0), "width=" + str(float(width) * TEXT_WIDTH_IN_CM) + "cm")
                    result_item.append(line)
            result.append(result_item)
        else:
            result.append(item)
    return result

# total width of an example if its items (input, output, explanation) are placed
# horizontally, next to each other
def example_width_horizontal(example):
    width = 0
    for item in example:
        if isinstance(item, list):
            width += max_width(item) + MARGIN
    return width + MARGIN

# total width of an example if only its input and output are placed
# horizontally, next to each other, and other items (explanation)
# are place below
def example_width_io_horizontal(example):
    width = 0
    for item in example:
        if isinstance(item, list):
            if is_input(item) or is_output(item):
                width += max_width(item) + MARGIN
    for item in example:
        if isinstance(item, list):
            if not is_input(item) and not is_output(item):
                width = max(width, max_width(item) + MARGIN)
    return width + MARGIN


# total width of an example if its items (input and output) are placed
# vertically, one below the other.
def example_width_vertical(example):
    max_w = 0
    for item in example:
        if isinstance(item, list):
            max_w = max(max_w, max_width(item)) + MARGIN
    return max_w

def print_example(example, current_width):
    result = []

    MAX_WIDTH = TEXT_WIDTH_IN_CM

    HORIZONTAL = 1     # all items horizontally 
    IO_HORIZONTAL = 2  # only io horizontally
    VERTICAL = 2       # all items vertically

    # is there an explanation within the exapmle?
    explanation = contains_explanation(example)
    
    # are items placed horizontally or vertically
    layout = HORIZONTAL
    example_width = example_width_horizontal(example)
    if example_width > MAX_WIDTH:
        layout = IO_HORIZONTAL
        example_width = example_width_io_horizontal(example)
        if example_width > MAX_WIDTH:
            layout = VERTICAL
            example_width = example_width_vertical(example)

    # move to new line if there is an explanation present
    # or the content does not fit to the current line
    if explanation or current_width + example_width >= MAX_WIDTH:
        result.append("\n")
        current_width = 0

    # if there is an explanation, example should span the whole width
    if explanation:
        example_width = MAX_WIDTH

    # figures should not be present (they can be present only in the
    # explanation)
    if explanation:
        example = remove_figure_environment(example)

    # add the example width to the current line width
    current_width += example_width

    if layout == HORIZONTAL or layout == IO_HORIZONTAL:
        result.append("\\begin{minipage}[t]{%.2fcm}" % example_width)

    # start layout - width of current items
    total_width = 0
    for item in example:
        if isinstance(item, list):
            if is_explanation(item):
                # move explanation to new line
                if layout == IO_HORIZONTAL or total_width + MIN_EXPLANATION_WIDTH >= MAX_WIDTH:
                    result.append("\n")
                width = MAX_WIDTH - total_width - MARGIN
            else:
                width = max_width(item) + MARGIN
            total_width += width
            if layout == HORIZONTAL or layout == IO_HORIZONTAL:
                result.append("\\begin{minipage}[t]{%.2fcm}" % width)
            for line in item:
                result.append(line)
            if layout == HORIZONTAL or layout == IO_HORIZONTAL:
                result.append("\\end{minipage}")
        else:
            result.append(item)
    if layout == HORIZONTAL or layout == IO_HORIZONTAL:
        result.append("\\end{minipage}")

    return result, current_width

def print_examples(examples):
    result = []
    current_width = 0
    for example in examples:
        example_result, current_width = print_example(example, current_width)
        result.extend(example_result)
    result.append("\n")
    return result

        
def fix_examples_layout(tex):
    result = []
    
    STATE_INITIAL = 0
    STATE_INPUT = 1
    STATE_OUTPUT = 2
    STATE_EXPLANATION = 3
    STATE_EXAMPLE = 4

    state = STATE_INITIAL

    examples = []

    EXAMPLE_RE = re.compile(r"\\textbf{" + msg("EXAMPLE") + r"(\s\d+)?}")
    INPUT_STR = "\\emph{" + msg("INPUT") + "}"
    OUTPUT_STR = "\\emph{" + msg("OUTPUT") + "}"
    EXPLANATION_STR = "\\emph{" + msg("EXPLANATION") + "}"
    END_EXAMPLE_RE = re.compile(r"\\textbf{" + msg("SOLUTION") + r"}|\\hypertarget")
    END_VERBATIM_STR = "\\end{verbatim}"

    line_no = 0
    while line_no < len(tex):
        line = tex[line_no].rstrip()
        line_no += 1
        if state == STATE_INITIAL:
            if EXAMPLE_RE.match(line):
                state = STATE_EXAMPLE
                example = [line, "\n"]
            else:
                result.append(line)
        elif state == STATE_EXAMPLE:
            if EXAMPLE_RE.match(line):
                examples.append(example)
                example = [line, "\n"]
            elif line == INPUT_STR:
                state = STATE_INPUT
                buffer = [line]
            elif line == OUTPUT_STR:
                state = STATE_OUTPUT
                buffer = [line]
            elif line == EXPLANATION_STR:
                state = STATE_EXPLANATION
                buffer = [line]
            elif END_EXAMPLE_RE.match(line):
                examples.append(example)
                result.extend(print_examples(examples))
                examples = []
                state = STATE_INITIAL
                result.append("")
                result.append(line)
        elif state == STATE_INPUT or state == STATE_OUTPUT:
            buffer.append(line)
            if line == END_VERBATIM_STR:
                example.append(buffer)
                state = STATE_EXAMPLE
        elif state == STATE_EXPLANATION:
            if EXAMPLE_RE.match(line):
                example.append(buffer)
                examples.append(example)
                example = [line, "\n"]
                state = STATE_EXAMPLE
            elif END_EXAMPLE_RE.match(line):
                example.append(buffer)
                examples.append(example)
                result.extend(print_examples(examples))
                examples = []
                state = STATE_INITIAL
                result.append("")
                result.append(line)
            else:
                buffer.append(line)
    return "\n".join(result)

def fix_latex(tex):
    logger.info("Correcting LaTeX layout")
    result = fix_examples_layout(tex)
    result = re.sub(r"\\addcontentsline", r"\\phantomsection\\addcontentsline", result)
    # avoid empty lines at the beginning and end of environments
    result = re.sub(r"\\begin{([^}]+)}\n+", r"\\begin{\1}\n", result)
    result = re.sub(r"\n+\\end",r"\n\\end", result)
    return result
                
if __name__ == "__main__":
    tex = sys.stdin.readlines()
    tex = fix_latex(tex)
    print(tex)
