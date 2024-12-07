import sys, os, pathlib
import re
import yaml
from .util import read_file, is_all_ascii
from . import logger
from .translit import lat_to_cyr

# split initial Metadata in Yaml format from the rest of the file in
# Markdown format
def parse_front_matter(fname):
    # Taken from Jekyll
    # https://github.com/jekyll/jekyll/blob/3.5-stable/lib/jekyll/document.rb#L13
    YAML_FRONT_MATTER_REGEXP = r"\A---\s*\n(.*?)\n?^((---|\.\.\.)\s*$\n?)"

    file = read_file(fname)
    if file is None:
        logger.error("reading file:", fname)
        return "", {}

    match = re.search(YAML_FRONT_MATTER_REGEXP, file, re.DOTALL|re.MULTILINE)
    if not match:
        logger.error("parsing file:", fname)
        return "", {}
    
    try:
        header = yaml.safe_load(match.group(1))
        content = match.string[match.end():]
        return content, header
    except:
        logger.error("parsing file:", fname)
        return "", {}

# surround the given text with the verbatim environment in the given language
def md_latex(md):
    return f"~~~{{=latex}}\n{md}\n~~~\n"
    
# surround the given text with the verbatim environment in the given language
def md_verbatim(md, lang_id):
    return f"~~~{lang_id}\n{md}~~~\n"

# surround the given source code in a given programming language with
# appropriate markdown formating (~~~)
def md_source_code(code, lang, title=None):
    lang_id = {"cpp": "cpp", "cs": "cs", "py": "python"}.get(lang, lang) # defaults to lang if not "cpp", "cs", "py"
    result_md = title + "\n" if title else ""
    result_md += md_verbatim(code, lang_id)
    return result_md

link_re = r"\[([^]\n]*)\]\(([-a-zA-Z_0-9./]*)\)"
image_re = r"!" + link_re

# find all links in a Markdown document (returns list of pairs
# containing link title and link path)

def link(title, path):
    return "[{}]({})".format(title, path)

def links_in_md(md):
    result = []
    for link in re.finditer("(?<![!])" + link_re, md):
        result.append((link.group(1), link.group(2)))
    return result

# replaces link with the given new content
def replace_link(md, old_title, old_path, new_content):
    old_link = link(old_title, old_path)
    return md.replace(old_link, new_content)

def change_link(md, old_title, old_path, new_title, new_path):
    new_link = link(new_title, new_path)
    return replace_link(md, old_title, old_path, new_link)

# find all images in a Markdown document (returns list of pairs
# containing image title and image path)
def images_in_md(md):
    result = []
    for image in re.finditer(image_re, md):
        result.append((image.group(1), image.group(2)))
    return result

def exclude_code_blocks(md):
    backtick_pattern = r'(^```.*?```)'
    tilde_pattern = r'(^~~~.*?~~~)'
    #TODO: add indented code blocks
    cleaned_content = re.sub('|'.join([backtick_pattern, tilde_pattern]), '', md, flags=re.DOTALL | re.MULTILINE)
    return cleaned_content

def exclude_backtick_strings(program_text):
    string_pattern = r'`(?:\\.|[^`\\])*`'  # Matches both single and double quoted strings
    text_without_strings = re.sub(string_pattern, ' ', program_text)
    return text_without_strings

def formulas_in_md(md):
    math_patterns = [
        r'\$(.*?)\$',
        r'\$\$(.*?)\$\$'
    ]
    formulas = []
    for pattern in math_patterns:
        matches = re.findall(pattern, exclude_backtick_strings(exclude_code_blocks(md)), re.DOTALL)
        formulas.extend(matches)
    return formulas

# check if a math formula contains only ASCII characters
def is_ascii_formula(formula):
    mathrm_pattern = re.compile(r'\\mathrm{.*?}', re.DOTALL)
    formula = re.sub(mathrm_pattern, '', formula)
    return is_all_ascii(formula)

label_re = r"\{?\s*#([-:\w\d]+):([-:\w\d]+)\s*\}?"
reference_re = r"@([-:\w\d]+):([-:\w\d]+)"

skip_labels = ["fig", "tbl", "eq"]

def analyze_label(label):
    m = re.match(label_re, label)
    if m:
        return (m.group(1), m.group(2))
    else:
        return (None, None)

def labels_in_md(md):
    result = []
    for label in re.finditer(label_re, exclude_code_blocks(md)):
        # these keys are handled by xnos pandoc filters
        if label.group(1) not in skip_labels:
            result.append((label.group(1), label.group(2)))
    return result

def references_in_md(md):
    result = []
    for reference in re.finditer(reference_re, exclude_code_blocks(md)):
        if reference.group(1) not in skip_labels:
            result.append((reference.group(1), reference.group(2)))
    return result

def label(key, value):
    return "{" + "#{}:{}".format(key, value) + "}"

def replace_label(md, key, value, content):
    return md.replace(label(key, value), content)

def remove_label(md, key, value):
    return replace_label(md, key, value, "")

def reference(key, value):
    return "@{}:{}".format(key, value)

def replace_reference(md, key, value, content):
    regex = reference(key, value) + r"\b"
    # use lambda to ensure that content will be a literal string
    return re.sub(regex, lambda _: content, md)

def max_heading_level(md):
    max_level = 0
    for line in md.split('\n'):
        m = re.match(r"^(#+)\s+(.+)$", line)
        if m:
            max_level = max(max_level, len(m.group(1)))
    return max_level

def min_heading_level(md):
    min_level = sys.maxsize
    for line in md.split('\n'):
        m = re.match(r"^(#+)\s+(.+)$", line)
        if m:
            min_level = min(min_level, len(m.group(1)))
    return 0 if min_level == sys.maxsize else min_level

# build bold text
def bold(text):
    return "**{}**".format(text)

# build italic text
def italic(text):
    return "*{}*".format(text)

# build level k heading
def heading(title, level = 1, unnumbered=False, unlisted=False, anchor=None):
    result = "#" * level + " " + title
    extra = []
    if anchor != None:
        extra.append("#" + anchor)
    if unnumbered:
        extra.append(".unnumbered")
    if unlisted:
        extra.append(".unlisted")
    if extra != []:
        result += " {" + " ".join(extra) + "}"
    return result

# build list item
def list_item(text):
    return "  - {}\n".format(text)

# build an enumeration
def enumerate(items, compact=False):
    sep = "\n" if compact else "\n\n"
    return sep.join(map(lambda s: "  a) " + s, items5))

heading_re = r"""
^                      # Start of the string
(?P<hashes>\#+)\s*     # One or more hashes followed by optional whitespace
(?P<title>[^{#\n]+)\s* # Title (any character except {, #, or newline), followed by optional whitespace
(?P<label>\{[^}]+\})?  # Optional label in curly braces
$                      # End of the string
"""

def analyze_heading(text):
    m = re.match(heading_re, text, flags=re.VERBOSE)
    result = {"title": None, "level": None, "unnumbered": False, "unlisted": False}
    if m:
        result["level"] = len(m.group("hashes"))
        result["title"] = m.group("title").strip()
        if m.group("label"):
            label_parts = m.group("label")[1:-1].split()
            for part in label_parts:
                if part[0] == '#':
                    (label_type, label_value) = analyze_label(part)
                    if label_type == None:
                        label_type = "sec"
                        label_value = part[1:]
                    result["label"] = label(label_type, label_value)
                elif part == ".unnumbered":
                    result["unnumbered"] = True
                elif part == ".unlisted":
                    result["unlisted"] = True
    return result


def headings_in_md(text):
    result = []
    for heading in re.finditer(heading_re, exclude_code_blocks(text), flags=re.MULTILINE|re.VERBOSE):
        h = analyze_heading(heading.group(0))
        result.append(h)
    return result
    
# degrade all headings so that # becomes # * level
def degrade_headings(md, level, unnumbered=False, unlisted=False):
    in_code = False
    result = []
    for line in md.split('\n'):
        if line.startswith("~~~") or line.startswith("```"):
            in_code = not in_code
        hd = analyze_heading(line)
        if not in_code and hd["title"]:
            anchor = None
            if "label" in hd:
                (label_type, label_value) = analyze_label(hd["label"])
                anchor = label_type + ":" + label_value
            result.append(heading(hd["title"], hd["level"] + level - 1, unnumbered=unnumbered, unlisted=unlisted, anchor=anchor))
        else:
            result.append(line)
    return "\n".join(result)

# remove headings and replace them by ordinary text (it might be normal, italic, or bold)
def remove_headings(md, level, before, after=None):
    if after == None:
        after = before
    heading_re = r"^" + "#"*level + r"\s+(\S+([ ]\S+)*)[ ]*$"
    return re.sub(heading_re, before + r"\1" + after, md, flags=re.MULTILINE)

# change the given heading by the given replacement text
def change_heading(md, title, level, replacement):
    hashes = "#"*level
    title = title.replace("\\", r"\\")
    heading_re = f"^{hashes}\s+{title}.*$"
    replacement = replacement.replace("\\", r"\\")
    return re.sub(heading_re, replacement, md, flags=re.MULTILINE)
    

# remove blank lines after given (heading) text, so that it fits into
# same line with the text that follows it (to save space)
def keep_with_next(text, heading):
    text = re.sub(r"^{}\s*(?![-])".format(re.escape(heading)), "{}: ".format(heading), text, flags=re.MULTILINE)
    # the exception are itemized enumerations behind inner headings
    text = re.sub(r"^{}[:]?\s*-".format(re.escape(heading)), "{}:\n\n  -".format(heading), text, flags=re.MULTILINE)
    return text
    

class PandocMarkdown:
    # fix latex $ signs in accordance with Pandoc Markdown dialect
    @staticmethod
    def fix_latex_dollars(md):
        # replace $$ by $ for inline maths
        md = re.sub(r"\$\$", "$", md)
        # put $$ around displayed maths
        # single displayed line
        md = re.sub(r"\n\n\s*\$(.+)\$([ \t]*{.+})?\s*(\n\n|\n\Z|\Z)", r"\n\n$$\1$$\2\n\n", md)
        # multiple displayed lines
        md = re.sub(r"\n\n\s*\$([^$]+)\$([ \t]*{.+})?\s*(\n\n|\n\Z|\Z|\n(?=<!---))", r"\n\n$$\1$$\2\n\n", md)
        return md

    # fix indentation of itemized lists in accordance with Pandoc
    # Markdown dialect
    @staticmethod
    def fix_itemize(md):
        return re.sub(r"^-(?!(\d|\n|[-]))", "  -", md)

    # fix nobreaking space
    @staticmethod
    def fix_nbsp(md):
        words = ["tj", "tzv", "engl", "it", "fr", "nem", "hol", "gr", "češ"]
        words.extend(list(map(lat_to_cyr, words)))
        pattern_noend = r'\b(' + '|'.join(words) + r')\. '
        pattern_end = r'\b(' + '|'.join(words) + r')\.\s*$'
        in_code = False
        lines = md.split("\n")
        result = []
        for line in lines:
            if line.startswith("~~~") or line.startswith("```"):
                in_code = not in_code
            if not in_code:
                line = re.sub(pattern_noend, r'\1.\\ ', line)
                line = re.sub(pattern_end, r'\1.\\ ', line)
            result.append(line)
        md = "\n".join(result)
        md = re.sub(r"[.]\\ \n\s*", ".\\ ", md)
        return md
    
    # fix Markdown content in accordance with Pandoc Markdown dialect
    @staticmethod
    def fix(md):
        md = PandocMarkdown.fix_latex_dollars(md)
        md = PandocMarkdown.fix_itemize(md)
        md = PandocMarkdown.fix_nbsp(md)
        return md


if __name__ == '__main__':
    pass
