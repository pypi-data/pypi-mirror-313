import sys, os, re
import traceback
import tempfile
from petljapub.messages import msg
from petljapub import logger
from petljapub.compilation import run_latex


def get_preamble(latex_content):
    preamble_match = re.match(r'(.*?)\\begin{document}', latex_content, re.DOTALL)
    preamble = preamble_match.group(1) if preamble_match else ''
    return preamble

def get_textwidth_and_charwidth(latex_content):
    latex_content = get_preamble(latex_content) + r"""
    \usepackage{calc}

    \begin{document}
    \makeatletter
    \newwrite\tempfile
    \immediate\openout\tempfile=texwidth.txt

    % Write \textwidth in points (pt) without the unit
    \immediate\write\tempfile{\the\textwidth}

    % Measure the width of the character "0" in verbatim mode and write in pt
    \newlength{\charwidth}
    \settowidth{\charwidth}{\texttt{0}}
    \immediate\write\tempfile{\the\charwidth}

    \immediate\closeout\tempfile
    \makeatother
    \end{document}
    """

    with tempfile.TemporaryDirectory() as tmpdir:
        tex_path = os.path.join(tmpdir, 'temp.tex')
        txt_path = os.path.join(tmpdir, 'texwidth.txt')

        with open(tex_path, 'w') as f:
            f.write(latex_content)

        # Run pdflatex to generate the output files
        run_latex(tex_path, no_latex_mk=True, quiet=True, timeout=3000)
        
        # Read the resulting texwidth.txt file to find the default text width and char width
        with open(txt_path, 'r') as f:
            lines = f.readlines()
            if len(lines) >= 2:
                text_width = lines[0].strip()
                char_width = lines[1].strip()
            else:
                text_width = None
                char_width = None

    return text_width, char_width


# max width (in cm) of a parsed example (input or output)
# only fixed width items are taken into account (verbatim text and images) 
def max_width(buffer):
    global MIN_EXPLANATION_WIDTH, CHAR_WIDTH, MIN_COLUMN_WIDTH
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

# check if example contains an explanation
def contains_explanation(example):
    for item in example:
        if isinstance(item, list) and is_explanation(item):
            return True
    return False

# removes the figure environment (since it can not be put in minipage)
def remove_figure_environment(example):
    # pandoc splits some captions into multiple lines, so we need to
    # join them
    def join_multiline_captions(text_lines):
        joined_lines = []
        in_caption = False
        current_caption = []
        
        for line in text_lines:
            stripped_line = line.strip()
            if stripped_line.startswith(r'\caption{'):
                in_caption = True
                current_caption.append(stripped_line)
            elif in_caption:
                current_caption.append(stripped_line)
                if stripped_line.endswith('}'):
                    in_caption = False
                    # Join all lines of the current caption
                    full_caption = ' '.join(current_caption)
                    joined_lines.append(full_caption)
                    current_caption = []
            else:
                joined_lines.append(line)
        return joined_lines

    
    result = []
    for item in example:
        if isinstance(item, list):
            result_item = []
            for line in join_multiline_captions(item):
                if '\\begin{figure}' in line or '\\end{figure}' in line:
                    result_item.append("\\medskip")
                elif '\\caption{}' in line:
                    continue
                else:
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

# total width of an example if its items (input and output) are placed
# horizontally, next to each other
def example_width_horizontal(example):
    global MARGIN
    width = 0
    for item in example:
        if isinstance(item, list):
            width += max_width(item) + MARGIN
    return width + MARGIN

# total width of an example if its items (input and output) are placed
# vertically, one below the other.
def example_width_vertical(example):
    global MARGIN
    max_w = 0
    for item in example:
        if isinstance(item, list):
            max_w = max(max_w, max_width(item)) + MARGIN
    return max_w

def print_example(example, current_width):
    global TEXT_WIDTH_IN_CM, CHAR_WIDTH, MARGIN, MIN_COLUMN_WIDTH, MIN_EXPLANATION_WIDTH
    result = []

    MAX_WIDTH = TEXT_WIDTH_IN_CM

    # figures must not be present in minipages
    # figures only appear in example explanations
    explanation = contains_explanation(example)
    if explanation:
        example = remove_figure_environment(example)

    example_width = example_width_horizontal(example)
    if example_width > MAX_WIDTH:
        example_width = example_width_vertical(example)

    if explanation or current_width + example_width >= MAX_WIDTH:
        result.append("\n")
        current_width = 0

    horizontal_blocks = []
    current_horizontal_block = []
    current_horizontal_block_width = 0
    horizontal_block_widths = []
    for item in example:
        item_width = max_width(item)
        if current_horizontal_block_width > 0:
            current_horizontal_block_width += MARGIN
        if is_explanation(item):
            item_width = max(item_width, MAX_WIDTH - current_horizontal_block_width)
        if current_horizontal_block_width + item_width > MAX_WIDTH:
            if current_horizontal_block:
                horizontal_blocks.append(current_horizontal_block)
                horizontal_block_widths.append(current_horizontal_block_width)
            current_horizontal_block = []
            current_horizontal_block_width = 0
            if is_explanation(item):
                item_width = MAX_WIDTH
        current_horizontal_block.append(item)
        current_horizontal_block_width += item_width
    horizontal_blocks.append(current_horizontal_block)
    horizontal_block_widths.append(current_horizontal_block_width)

    if current_width > 0:
        result.append(f"\hspace{{{MARGIN}cm}}")
        current_width += MARGIN
    for i in range(len(horizontal_blocks)):
        block = horizontal_blocks[i]
        block_width = horizontal_block_widths[i]
        if i > 0:
            result.append("\n")
        result.append("\\begin{minipage}[t]{%.2fcm}%%" % block_width)
        current_width_in_block = 0
        for j in range(len(block)):
            item = block[j]
            if isinstance(item, list):
                if is_explanation(item):
                    width = block_width - current_width_in_block
                else:
                    width = max_width(item)
                    if j < len(block) - 1:
                        width += MARGIN
                current_width_in_block += width
                
                result.append("\\begin{minipage}[t]{%.2fcm}%%" % width)
                for line in item:
                    result.append(line)
                result.append("\\end{minipage}%%")
            else:
                result.append(item)
        result.append("\\end{minipage}%%")
        
        current_width += block_width
        if current_width > MAX_WIDTH:
            result.append("\n")
            current_width = 0

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
    global TEXT_WIDTH_IN_CM, CHAR_WIDTH, MARGIN, MIN_COLUMN_WIDTH, MIN_EXPLANATION_WIDTH
    textwidth, charwidth = None, None
    try:
        textwidth, charwidth = get_textwidth_and_charwidth("\n".join(tex))
    except Exception as e:
        logger.error(e)
        logger.warn("Could not get textwidth")
    if textwidth == None:
        textwidth = "396.85pt" # 14 cm
        charwidth = "5.66928571429pt" # assuming 70 chars per line
        logger.warn("using default pagewidth of 14cm")
        
    logger.info("Textwidth:", textwidth, verbosity=4)
    logger.info("Charwidth:", charwidth, verbosity=4)
    PT_TO_CM = 0.0352778
    TEXT_WIDTH_IN_CM = float(textwidth[:-2]) * PT_TO_CM
    CHAR_WIDTH = float(charwidth[:-2])  * PT_TO_CM
    MARGIN = 2*CHAR_WIDTH
    MIN_COLUMN_WIDTH = 1.2 # cm
    MIN_EXPLANATION_WIDTH = TEXT_WIDTH_IN_CM / 2
    
    result = []
    
    STATE_INITIAL = 0
    STATE_INPUT = 1
    STATE_OUTPUT = 2
    STATE_EXPLANATION = 3
    STATE_EXAMPLE = 4

    state = STATE_INITIAL

    examples = []

    EXAMPLE_RE = re.compile(r"\\textbf{" + msg("EXAMPLE") + r"(\s\d+)?}\s*(\\nopagebreak)?")
    INPUT_STR = re.compile(r"\\emph{" + msg("INPUT") + r"}\s*(\\nopagebreak)?")
    OUTPUT_STR = re.compile(r"\\emph{" + msg("OUTPUT") + r"}\s*(\\nopagebreak)?")
    EXPLANATION_STR = re.compile(r"\\emph{" + msg("EXPLANATION") + r"}\s*(\\nopagebreak)?")
    END_EXAMPLE_RE = re.compile(r"\\textbf{" + msg("SOLUTION") + r"}\s*(\\nopagebreak)?" + "|" +
                                r"\\(sub)*section\*{" + msg("SOLUTION") + r"}" + "|" +
                                r"\\hypertarget")
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
            elif INPUT_STR.match(line):
                state = STATE_INPUT
                buffer = [line]
            elif OUTPUT_STR.match(line):
                state = STATE_OUTPUT
                buffer = [line]
            elif EXPLANATION_STR.match(line):
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
    try:
        result = fix_examples_layout(tex)
    except:
        logger.warning("Failed to correct LaTeX layout")
        print(traceback.format_exc())
        result = "\n".join(tex)

    result = re.sub(r"\\addcontentsline", r"\\phantomsection\\addcontentsline", result)
    # avoid empty lines at the beginning and end of environments
    result = re.sub(r"\\begin{([^}]+)}\n+", r"\\begin{\1}\n", result)
    result = re.sub(r"\n+\\end",r"\n\\end", result)
    return result
                
if __name__ == "__main__":
    tex = list(map(lambda line: line.rstrip(), sys.stdin.readlines()))
    tex = fix_latex(tex)
    print(tex)
