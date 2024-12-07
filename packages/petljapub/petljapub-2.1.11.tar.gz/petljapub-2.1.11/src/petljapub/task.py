import math
import re
import sys
import requests
import os, glob, shutil
import tempfile
import time
import statistics
import yaml
import json
import pathlib
from dataclasses import asdict

from enum import Enum

from .md_util import parse_front_matter
from . import md_util
from .messages import msg
from .util import read_file, write_to_file, dump_file, default_read_encoding

from .compilation import compile_c, compile_cpp, compile_cs, run_py, run_exe
from .default_checker import compare_files
from .serialization import ZipWriter
from .petlja_account import get_petlja_session

from . import logger

import petlja_api

base_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(base_dir, "data")


# Parse the problem statement and extract it's important parts
#   - problem description
#   - input format description
#   - output format description
#   - examples (example input, example output, example description)
class StParser:
    class State(Enum):
        STATEMENT = 1
        INPUT = 2
        OUTPUT = 3
        EXAMPLE = 4
        EXAMPLE_INPUT = 5
        EXAMPLE_OUTPUT = 6
        EXAMPLE_EXPLANATION = 7
    
    def __init__(self, st):
        self._st = st
        self._state = StParser.State.STATEMENT
        self._statement = ""
        self._input_description = ""
        self._output_description = ""
        self._examples = []
        self.parse()

    def new_example(self):
        self._examples.append({"input": "", "output": "", "explanation": ""})

    def parse(self):
        text = {StParser.State.INPUT: [md_util.heading(msg("INPUT"), 2), md_util.heading(msg("INPUT_DESC"), 2)],
                StParser.State.OUTPUT: [md_util.heading(msg("OUTPUT"), 2), md_util.heading(msg("OUTPUT_DESC"), 2)],
                StParser.State.EXAMPLE: [md_util.heading(msg("EXAMPLE"), 2)],
                StParser.State.EXAMPLE_INPUT: [md_util.heading(msg("INPUT"), 3)],
                StParser.State.EXAMPLE_OUTPUT: [md_util.heading(msg("OUTPUT"), 3)],
                StParser.State.EXAMPLE_EXPLANATION: [md_util.heading(msg("EXPLANATION"), 3)]
        }

        # check if the line starts with some of the give prefixes
        def startswith(line, prefixes):
            return any(line.startswith(s) for s in prefixes)

        self._state = StParser.State.STATEMENT
        
        for line in self._st.split("\n"):
            if self._state == StParser.State.STATEMENT:
                if startswith(line, text[StParser.State.INPUT]):
                    self._state = StParser.State.INPUT
                else:
                    self._statement += line + "\n"
            elif self._state == StParser.State.INPUT:
                if startswith(line, text[StParser.State.OUTPUT]):
                    self._state = StParser.State.OUTPUT
                else:
                    self._input_description += line + "\n"
            elif self._state == StParser.State.OUTPUT:
                if startswith(line, text[StParser.State.EXAMPLE]):
                    self._state = StParser.State.EXAMPLE
                    self.new_example()
                else:
                    self._output_description += line + "\n"
            elif self._state == StParser.State.EXAMPLE:
                if startswith(line, text[StParser.State.EXAMPLE_INPUT]):
                    self._state = StParser.State.EXAMPLE_INPUT
            elif self._state == StParser.State.EXAMPLE_INPUT:
                if startswith(line, text[StParser.State.EXAMPLE_OUTPUT]):
                    self._state = StParser.State.EXAMPLE_OUTPUT
                else:
                    self._examples[-1]["input"] += line + "\n"
            elif self._state == StParser.State.EXAMPLE_OUTPUT:
                if startswith(line, text[StParser.State.EXAMPLE_EXPLANATION]):
                    self._state = StParser.State.EXAMPLE_EXPLANATION
                elif startswith(line, text[StParser.State.EXAMPLE]):
                    self._state = StParser.State.EXAMPLE
                    self.new_example()
                else:
                    self._examples[-1]["output"] += line + "\n"
            elif self._state == StParser.State.EXAMPLE_EXPLANATION:
                if startswith(line, text[StParser.State.EXAMPLE]):
                    self._state = StParser.State.EXAMPLE
                    self.new_example()
                else:
                    self._examples[-1]["explanation"] += line + "\n"

    def statement(self):
        return self._statement.strip()

    def input_description(self):
        return self._input_description.strip()

    def output_description(self):
        return self._output_description.strip()

    def examples(self, strip_md_verbatim):
        verb_strs = ["~~~", "```"]

        def strip_newline(str):
            str = re.sub(r"^[ \t]*\n", "", str, count=1)
            str = re.sub(r"\n[ \t]*$", "", str, count=1)
            return str
        
        def split_output_and_explanation(output):
            for verb_str in verb_strs:
                parts = output.split(verb_str, 2)
                if len(parts) == 3:
                    (_, output, explanation) = parts
                    output = verb_str + output + verb_str
                    explanation = explanation.strip()
                    return (output, explanation)
            return (output, "")

        for i in range(len(self._examples)):
            self._examples[i]["input"] = self._examples[i]["input"].strip()
            (output, explanation) = split_output_and_explanation(self._examples[i]["output"])
            self._examples[i]["output"] = output
            if explanation != "":
                self._examples[i]["explanation"] = explanation + "\n" + self._examples[i]["explanation"]

            if strip_md_verbatim:
                for verb_str in verb_strs:
                    self._examples[i]["input"] = strip_newline(self._examples[i]["input"].strip(verb_str))
                    self._examples[i]["output"] = strip_newline(self._examples[i]["output"].strip(verb_str))

        return self._examples
    
class Task:
    def __init__(self, task_dir, normalize_md = lambda x: x, translit = lambda x: x):
        self._task_dir = task_dir
        self._task_id = Task.extract_id_from_dir(task_dir)
        self._normalize_md = normalize_md
        self._translit = translit

    # check if the given dir is a legal task dir name (it must start
    # with two digits, followed by a space, dash or an underscore)
    @staticmethod
    def is_task_dir(dir):
        return re.match(r"\d{2}[_ -].+", dir)

    # check if the given dir contains a created task
    # it must be a legal task dir name and must contain a -st.md file
    @staticmethod
    def is_task(dir):
        return (Task.is_task_dir(os.path.basename(dir)) and
                os.path.exists(os.path.join(dir, Task.extract_id_from_dir(dir) + "-st.md")))
         
        
    # extract id of the task from its directory name (remove two leading digits)
    # e.g. 01 task_id -> task_id
    @staticmethod
    def extract_id_from_dir(dir):
        return re.sub(r'^\d{2}[a-z]?[ _-]', '',
                      os.path.basename(dir)).rstrip(os.path.sep)

    # id of the task
    def id(self):
        return self._task_id

    # alias for task on petlja.org
    # takes the task id and removes everything that isn't a word character,
    # a dash or an underscore and makes everything lowercase to comply with
    # the petlja problem alias format
    def alias(self, prefix=""):
        return re.sub(r"[^a-z0-9]", "", (prefix + self.id()).lower())
        
    # title of the task
    def title(self):
        title = self.metadatum('title')
        return title

    # full path of the directory of the task
    def dir(self):
        return self._task_dir
    
    # last modification of some source file of the task
    def modification_time(self):
        return max(os.path.getmtime(file)
                   for file in glob.glob(os.path.join(self.dir(), '*')))

    # status of the task
    def status(self):
        return self.metadatum('status')

    # check if the status of the task denotes the task as completed
    def is_complete(self):
        return self.status().upper() == msg("COMPLETE").upper()

    # timelimit (in miliseconds) set in the metadata
    def timelimit(self):
        timelimit = self.metadatum('timelimit')
        if timelimit != None:
            return round(float(timelimit) * 1000)
        else:
            return 1000 # default is 1 second

    # memory limit (in megabytes) set in the metadata
    def memorylimit(self):
        return self.metadatum('memlimit')

    # list of solutions (and their descriptions) of the task
    def solutions(self):
        sols = self.metadatum('solutions')
        if not sols:
            sols = []
        return sols

    # description for the given solution
    def solution(self, sol_name):
        for sol in self.solutions():
            if sol["name"] == sol_name:
                return sol
        return None

    # expected status for the given solution
    def expected_status(self, sol_name):
        solutions = self.solutions()
        for sol in solutions:
            if sol["name"] == sol_name:
                if "expected-status" in sol:
                    return sol["expected-status"]
                else:
                    return "OK"
        return "OK"

    # available languages
    def langs(self):
        solutions = self.solutions();
        result = set()
        for sol in solutions:
            for lang in sol["lang"]:
                result.add(lang)
        return list(result)

    # check and warn for various erros in the content format
    def check_errors(self, content):
        def check_nonascii_latex(content):
            for formula in md_util.formulas_in_md(content):
                if not md_util.is_ascii_formula(formula):
                    logger.warn(self.id(), " non-ascii characters found in LaTeX markup:", formula)
        check_nonascii_latex(content)
    
    # raw text of the statement of the task
    def st_content(self):
        if not hasattr(self, "_st"):
            # parse -st.md file
            self._st, metadata = parse_front_matter(self.st_path())
            # apply normalizations
            self._st = self._normalize_md(self._st)
            self._st = self._translit(self._st)
            # check errors in the statement
            self.check_errors(self._st)
        return self._st

    # text of the task description (without input and output)
    def statement(self):
        parser = StParser(self.st_content())
        return parser.statement()

    # text of the input format description
    def input_description(self):
        parser = StParser(self.st_content())
        return parser.input_description()

    # text of the output format description
    def output_description(self):
        parser = StParser(self.st_content())
        return parser.output_description()

    # examples of input and output
    def examples(self, strip_md_verbatim=False):
        parser = StParser(self.st_content())
        return parser.examples(strip_md_verbatim)

    # complete IO specification (description + examples)
    def io(self):
        return self.io_description() + self.io_examples()
        
    # IO description
    def io_description(self):
        md = ""
        md += md_util.heading(msg("INPUT_DESC"), 2) + "\n\n" + self.input_description() + "\n\n"
        md += md_util.heading(msg("OUTPUT_DESC"), 2) + "\n\n" + self.output_description() + "\n\n"
        return md

    # IO examples
    def io_examples(self):
        md = ""
        examples = self.examples()
        for i, example in enumerate(examples):
            example_num = " " + str(i+1) if len(examples) > 1 else ""
            md += md_util.heading(msg("EXAMPLE"), 2) + example_num + "\n\n"
            md += md_util.heading(msg("INPUT"), 3) + "\n\n" + example["input"] + "\n\n"
            md += md_util.heading(msg("OUTPUT"), 3) + "\n\n" +example["output"] + "\n\n"
            if example["explanation"]:
                md += md_util.heading(msg("EXPLANATION"), 3) + "\n\n" + example["explanation"] + "\n\n"
        return md
    
    # raw content of the solution descriptions of the task
    def sol_content(self):
        # parse sol-md file
        sol, metadata = parse_front_matter(self.sol_path())

        # warn if raw links are present
        m = re.search(r'(?<![!])\[[^]()]+\]\([^)]+\)', sol, re.MULTILINE)
        if m:
            logger.error("raw link", m.group(0).replace("\n", " "), "in", self.id())
        
        # apply normalizations
        sol = self._normalize_md(sol)
        sol = self._translit(sol)
        # check errors in the solution (e.g., non-ascii in LaTeX)
        self.check_errors(sol)
        return sol

    # raw source code for the given solution ("ex0", "ex1", ...)  in
    # the given language ("cs", "cpp", "py", ...) 
    def src_code(self, sol_id, lang):
        src_file = self.src_file_path(sol_id, lang)
        code = read_file(src_file)
        if code is None:
            logger.error("Error reading code", src_file)
            return None
        # convert tabs to spaces
        code = code.replace('\t', ' '*8)
        return code.rstrip()

    # the list all generated testcases paths
    def generated_testcases(self):
        testcases = os.path.join(self.generated_testcases_dir() , "*.in")
        return sorted(glob.glob(testcases))

    # return the number of generated testcases
    def number_of_generated_testcases(self):
        return len(self.generated_testcases())

    # the list all example testcases paths
    def example_testcases(self):
        testcases = os.path.join(self.example_testcases_dir() , "*.in")
        return sorted(glob.glob(testcases))
    
    # return the number of example testcases
    def number_of_example_testcases(self):
        return len(self.example_testcases())

    # the list all crafted testcases paths
    def crafted_testcases(self):
        testcases = os.path.join(self.crafted_testcases_dir() , "*.in")
        return sorted(glob.glob(testcases))
    
    # return the number of crafted testcases
    def number_of_crafted_testcases(self):
        return len(self.crafted_testcases())

    # the list of all testcase paths
    def all_testcases(self):
        return self.example_testcases() + self.generated_testcases() + self.crafted_testcases()
    

    # generate yaml description of testcases
    def generate_scoring_yaml(self, subtask=False):
        ex = self.number_of_example_testcases()
        gen = self.number_of_generated_testcases()
        cft = self.number_of_crafted_testcases()

        if not subtask:
            scores = []
            for i in range(1, ex + 1):
                scores.append({'name': i, 'score': 0})
            for i in range(ex + 1, ex + gen + cft + 1):
                scores.append({'name': i, 'score': 1})
            
            data = {'type': 'testcase',
                    'score_total': gen + cft,
                    'score_overrides': scores,
                    'public': list(range(1, ex+1))}
        else:
            groups = []
            for i in range(1, ex + 1):
                groups.append({'id': i, 'score': 0, 'testcases': [i]})
            groups.append({'id': ex + 1, 'score': gen + cft, 'testcases': list(range(ex+1, ex+gen+cft+1))})
            data = {'type': 'subtask',
                    'score_total': gen + cft,
                    'groups': groups,
                    'public': list(range(1, ex+1))}

        # ensure that the build dir exists
        build_dir = self.build_dir()
        if not os.path.isdir(build_dir):
            try:
                os.makedirs(build_dir)
            except:
                logger.error("Could not create build directory", build_dir)
            
        file = self.scoring_path()
        write_to_file(file,
                      yaml.dump(data, sort_keys = False, default_flow_style=None))
        logger.info(file, "successfully generated")

    def load_scoring_yaml(self, encoding=default_read_encoding):
        if not self.has_scoring():
            logger.error("scoring.yaml not present")
            return None
        try:
            with open(self.scoring_path(), encoding=encoding) as file:
                scoring = yaml.safe_load(file)
            if 'type' not in scoring or scoring['type'] not in {'subtask', 'testcase'}:
                logger.error('Error parsing type of ', self.scoring_path())
            return scoring
        except:
            logger.error("Error parsing scoring.yaml")
            return None
        
    # check if there is a custom checker for the task
    def has_checker(self):
        return os.path.isfile(self.checker_src_path())

    # check if the task has crafted testcases
    def has_crafted_testcases(self):
        return self.metadatum("crafted-dir") != None

    def crafted_testcases_input_dir(self):
        return self.metadatum("crafted-dir")
    
    # check if there is a main file for the task (for functional tasks)
    def has_main(self):
        return os.path.isfile(self.main_src_path())

    # check if there is a scoring file for the task
    def has_scoring(self):
        return os.path.isfile(self.scoring_path())
    
    # get gcc compiler flags
    def gcc_flags(self):
        return self.metadatum("gcc-flags")
    
    # full metadata
    def metadata(self):
        # read the metadata from the -st.md file
        stmd_file = self.st_path()
        text, metadata = parse_front_matter(stmd_file)
        return metadata

    # a single entry from the metadata
    def metadatum(self, key):
        # read all metadata
        metadata = self.metadata()
        # get the entry for the specified key
        if key in metadata:
            data = metadata[key]
            if key == "title":
                data  = self._translit(data)
            return data
        return None


    ####################################################################
    # Paths and file names
    
    # full path of the -st.md file
    def st_path(self):
        return os.path.join(self.dir(), self.id() + "-st.md")
        
    # full path of the -sol.md file
    def sol_path(self):
        return os.path.join(self.dir(), self.id() + "-sol.md")

    # name of the source file for the given solution ("ex0",
    # "ex1", ...)  in the given language ("cs", "cpp", "py", ...)
    def src_file_name(self, sol_id, lang):
        suffix = "" if sol_id == "ex0" else "-" + sol_id
        return self.id() + suffix + "." + lang
    
    # full path of the source file for the given solution ("ex0",
    # "ex1", ...)  in the given language ("cs", "cpp", "py", ...)
    def src_file_path(self, sol_id, lang):
        return os.path.join(self.dir(), self.src_file_name(sol_id, lang))

    # name of the build directory
    @staticmethod
    def build_dir_name():
        return "_build"

    # full path of the build directory (where exe and testcases are stored)
    def build_dir(self):
        return os.path.join(self.dir(), Task.build_dir_name())
    
    def clear_build_dir(self):
        if os.path.isdir(self.build_dir()):
            try:
                shutil.rmtree(self.build_dir())
            except:
                logger.error("Error removing directory", Task.build_dir_name())

    # name of the executable file for the given solution ("ex0",
    # "ex1", ...)  in the given language ("cs", "cpp", "py", ...)
    def exe_file_name(self, sol, lang):
        lang_ = "-" + lang if lang != "cpp" else ""
        sol_name = "-" + sol if sol != "ex0" else ""
        if lang == "py":
            return self.id() + sol_name + ".py"
        return self.id() + sol_name + lang_ + ".exe"
    
    # full path of the executable file for the given solution ("ex0",
    # "ex1", ...)  in the given language ("cs", "cpp", "py", ...)
    def exe_file_path(self, sol, lang):
        return os.path.join(self.build_dir(), self.exe_file_name(sol, lang))

    # name of the test generator source file
    def tgen_src_file_name(self, lang):
        return self.id() + "-tgen." + lang

    # name of the test generator executable file (in the build directory)
    def tgen_exe_file_name(self):
        return self.id() + "-tgen.exe"

    # full path for the test generator source file
    def tgen_src_path(self, lang):
        return os.path.abspath(os.path.join(self.dir(), self.tgen_src_file_name(lang)))

    # full path for the test generator exe file (in the build directory)
    def tgen_exe_path(self):
        return os.path.join(self.build_dir(), self.tgen_exe_file_name())

    # directories where testcases are stored
    @staticmethod
    def testcases_dir_name():
        return "testcases"

    @staticmethod
    def generated_testcases_dir_name():
        return os.path.join(Task.testcases_dir_name(), "generated")

    @staticmethod
    def example_testcases_dir_name():
        return os.path.join(Task.testcases_dir_name(), "example")

    @staticmethod
    def crafted_testcases_dir_name():
        return os.path.join(Task.testcases_dir_name(), "crafted")

    # full path of the root directory where all testcases are stored
    def testcases_dir(self):
        return os.path.join(self.build_dir(), Task.testcases_dir_name())

    # full path to the zipped testcases file
    def zipped_testcases_path(self):
        return os.path.join(self.build_dir(), "testcases.zip")
    
    # full path of the directory where generated testcases are stored
    def generated_testcases_dir(self):
        return os.path.join(self.build_dir(), Task.generated_testcases_dir_name())

    # full path of the directory where example testcases are stored
    def example_testcases_dir(self):
        return os.path.join(self.build_dir(), Task.example_testcases_dir_name())

    # full path of the directory where crafted testcases are stored
    def crafted_testcases_dir(self):
        return os.path.join(self.build_dir(), Task.crafted_testcases_dir_name())
    
    # full path of a generated testcase with a given number
    def generated_testcase_path(self, i):
        in_file = self.id() + "_" + str(i).zfill(2) + ".in"
        return os.path.join(self.generated_testcases_dir(), in_file)

    # full path of an example testcase with a given number
    def example_testcase_path(self, i):
        in_file = self.id() + "_" + str(i).zfill(2) + ".in"
        return os.path.join(self.example_testcases_dir(), in_file)

    # full path of a crafted testcase with a given number
    def crafted_testcase_path(self, i):
        in_file = self.id() + "_" + str(i).zfill(2) + ".in"
        return os.path.join(self.crafted_testcases_dir(), in_file)

    # full path of a testcase (first param is "example", "crafted", or "generated")
    def testcase_path(self, testcase_type, testcase_no):
        if testcase_type[0].lower()  == "e":
            return self.example_testcase_path(testcase_no)
        if testcase_type[0].lower() == "c":
            return self.crafted_testcase_path(testcase_no)
        if testcase_type[0].lower() == "g":
            return self.generated_testcase_path(testcase_no)
        return ""

    # testing output dir
    def test_output_dir(self):
        return os.path.join(self.build_dir(), "output")

    # output dir for example testcases
    def example_test_output_dir(self):
        return os.path.join(self.test_output_dir(), "example")

    # output dir for generated testcases
    def generated_test_output_dir(self):
        return os.path.join(self.test_output_dir(), "generated")

    # output dir for crafted testcases
    def crafted_test_output_dir(self):
        return os.path.join(self.test_output_dir(), "crafted")
    
    # name of the source file with the custom checker
    def checker_src_file_name(self):
        return self.id() + "-check.cpp"

    # name of the executable file of the custom checker
    def checker_exe_file_name(self):
        return self.id() + "-check.exe"
    
    # full path of the source file with the custom checker
    def checker_src_path(self):
        return os.path.join(self.dir(), self.checker_src_file_name())

    # full source code of the checker
    def checker_src(self):
        return read_file(self.checker_src_path())

    # full path of the executable file of the custom checker
    def checker_exe_path(self):
        return os.path.join(self.build_dir(), self.checker_exe_file_name())

    # default checker exe file path
    def default_checker_exe_path(self):
        return os.path.join(base_dir, "DefaultChecker.exe")

    # name of the source file with the main function (for functional tasks)
    def main_src_file_name(self):
        return self.id() + "-main.cpp"

    # full path of the source file with the main function (for functional tasks)
    def main_src_path(self):
        return os.path.join(self.dir(), self.main_src_file_name())

    # full path of the -scoring.yaml file
    def scoring_path(self):
        return os.path.join(self.dir(), self.id() + "-scoring.yaml")
    
    ####################################################################
    # Compiling and running

    # compile source code for the given solution ("ex0", "ex1", ...)
    # in the given language ("cs", "cpp", "py", ...) 
    def compile(self, sol, lang, force=False):
        if lang == "py":
            return True
        
        # full paths of the source and resulting exe file
        src_file = self.src_file_path(sol, lang)
        exe_file = self.exe_file_path(sol, lang)

        # report error if source file does not exist
        if not os.path.isfile(src_file):
            logger.error("input file", src_file, "does not exist")
            return False
        
        # ensure that the build dir exists
        build_dir = self.build_dir()
        if not os.path.isdir(build_dir):
            try:
                os.makedirs(build_dir)
            except:
                logger.error("Could not create build directory", build_dir)
                return
                
        # if exe file exists and it is newer than the source file
        # and compilation is not forced, we are done
        if os.path.isfile(exe_file) and os.path.getmtime(exe_file) > os.path.getmtime(src_file) and not force:
            return True

        logger.info("Compiling:", os.path.basename(src_file))
        
        # call the compiler for the given programming language
        if lang == "cpp":
            extra_src_files = []
            if self.has_main():
                extra_src_files = [self.main_src_path()]
            flags = self.gcc_flags()
            if flags != None:
                logger.info("Using user specified flags:", flags)
            if not compile_cpp(src_file, exe_file, extra_src_files=extra_src_files, flags=flags):
                return False
        elif lang == "cs":
            if not compile_cs(src_file, exe_file):
                return False
        elif lang == "c":
            if not compile_c(src_file, exe_file):
                return False
        else:
            logger.error("compilation not supported for language", lang)
            return False
        return True

    def clear_testcases(self):
        dir = os.path.abspath(self.testcases_dir())
        try:
            if os.path.isdir(dir):
                shutil.rmtree(dir)
        except:
            logger.warn("Could not remove testcases directory", dir)
    
    # extract testcases from examples on the problem statement
    def extract_example_testcases(self):
        logger.info("Extracting testcases from given examples:", self.id())
        # ensure that the directory for storing test cases exists
        examples_dir = self.example_testcases_dir()
        if not os.path.isdir(examples_dir):
            try:
                os.makedirs(examples_dir)
            except:
                logger.error("Could not create example testcases directory", examples_dir)
        # process all examples given in the problem statement
        examples = self.examples(strip_md_verbatim=True)
        for i, example in enumerate(examples):
            try:
                logger.info("Extracting example testcase", i)
                # extract input file
                input = self.example_testcase_path(i+1)
                write_to_file(input, example["input"])
                output = input[:-2]+"out"
                write_to_file(output, example["output"])
            except:
                logger.error("Error extracting example testcase", i)
        n = self.number_of_example_testcases()
        logger.info(f"Extracted {n} example{'' if n == 1 else 's'}")
                
    
    # generate testcases for the task with the given ID
    def generate_testcases(self):
        # test generator source
        tgen_src_cpp = self.tgen_src_path("cpp")
        tgen_src_py = self.tgen_src_path("py")

        # if the task has only crafted testcases, skip generating testcases
        if (not os.path.exists(tgen_src_cpp) and
            not os.path.exists(tgen_src_py) and
            self.has_crafted_testcases()):
            return
        
        logger.info("Generating tests:", logger.bold(self.id()))

        # ensure that the directory for storing generated test cases exists
        generated_dir = self.generated_testcases_dir()
        if os.path.isdir(generated_dir):
            try:
                shutil.rmtree(generated_dir)
            except:
                logger.error("Could not remove ", generated_dir)
                
        try:
            os.makedirs(generated_dir)
        except:
            logger.error("Could not create generated test cases directory", generated_dir)
            return
        
        
        ## try the C++ generator
        if os.path.exists(tgen_src_cpp):
            # check if the gen_test function is empty
            with open(tgen_src_cpp) as tgen:
                content = tgen.read()
                if re.search(r"void gen_test\([^)]*\)\s*{\s*}", content):
                    logger.warn(tgen_src_cpp + " - gen_test function is empty - generating testcases skipped")
                    return

            # compile the c++ test generator
            tgen_exe = self.tgen_exe_path()
            if not compile_cpp(tgen_src_cpp, tgen_exe):
                logger.error("compiling test generator failed")
                return False

            # run the test generator
            logger.info("Generating test inputs - running test generator:", os.path.relpath(tgen_exe, self.dir()))
            exe_file = os.path.abspath(tgen_exe)
            args = [self.id(), Task.generated_testcases_dir_name()]
            if logger.verbosity() > 3:
                args.append("True")
            status, p = run_exe(exe_file, args=args, cwd=self.build_dir())
            if status == "RTE":
                logger.error("RTE while generating testcases")
                return False
            
        ## try the Python generator
        elif os.path.exists(tgen_src_py):
            # check if the gen_test function is empty
            with open(tgen_src_py) as tgen:
                content = tgen.read()
                if re.search(r"def gen_test\([^)]*\):\s*pass", content):
                    logger.warn(tgen_src_py + " - gen_test function is empty - generating testcases skipped")
                    return
            
            # run the python test generator
            logger.info("Generating test inputs - running test generator:", os.path.relpath(tgen_src_py, self.dir()))
            args = [tgen_src_py, self.id(), Task.generated_testcases_dir_name()]
            if logger.verbosity() > 3:
                args.append("True")
            tgen_py = os.path.join(data_dir, "tgen", "tgen.py")
            status, p = run_py(tgen_py, args=args, cwd=self.build_dir())
            if status == "RTE":
                logger.error("RTE while generating testcases")
                return False
        else:
            logger.warn(tgen_src_cpp + " does not exist - generating testcases skipped")
            return


        # compile the main solution used to generate outputs
        if not self.compile("ex0", "cpp", force=True):
            logger.error("compiling main solution failed")
            return False

        exe_file = self.exe_file_path("ex0", "cpp")
        logger.info("Generating test outputs - running default cpp solution:", os.path.relpath(exe_file, self.dir()))
        for testcase_num, input in enumerate(self.generated_testcases()):
            try:
                in_file = open(input)
                output = input[:-2] + "out"
                out_file = open(output, "w")
                logger.info("generating", os.path.relpath(output, self.dir()), "using", os.path.relpath(exe_file, self.dir()), verbosity=4)
                status, p = run_exe(exe_file, in_file=in_file, out_file=out_file)
                in_file.close()
                out_file.close()
            except:
                    logger.error("error generating output", output)

        logger.info("Generated", self.number_of_generated_testcases(), "testcases")
        return True

    
    # copy crafted testcases to testcases dir and generate expected output using default cpp solution, when
    # the default output files are not provided
    def prepare_crafted_testcases(self, crafted_dir):
        logger.info("Preparing crafted tests:", self.id())

        # check if valid directory is supplied
        if not os.path.isdir(crafted_dir):
            logger.error(crafted_dir, "is not a valid directory")
        
        # compile the main solution used to generate outputs
        if not self.compile("ex0", "cpp", force=False):
            logger.error("compiling main solution failed")
            return False
        
        # ensure that the target directory for storing crafted test cases exists
        target_dir = self.crafted_testcases_dir()
        if not os.path.isdir(target_dir):
            try:
                os.makedirs(target_dir)
            except:
                logger.error("Could not create crafted testcases directory", target_dir)

        # process every testcase found in the supplied crafted_dir
        i = 0
        for input in sorted(glob.glob(os.path.join(self.dir(), crafted_dir, "*.in"))):
            i += 1
            logger.info("copying", input, verbosity=4)
            target_input = self.crafted_testcase_path(i)
            target_output = self.crafted_testcase_path(i)[:-2] + "out"
            
            try:
                shutil.copy(input, target_input)
            except:
                logger.error("error copying", input)
                continue

            # copy output file if it exists in the crafted_dir
            output = input[:-2] + "out"
            if os.path.isfile(output):
                logger.info("copying", output, verbosity=4)
                try:
                    shutil.copy(output, target_output)
                except:
                    logger.error("error copying", output)
                    continue
            else:
            # generate output file
                exe_file = self.exe_file_path("ex0", "cpp")
                logger.info("generating", os.path.relpath(output, self.dir()), "using", os.path.relpath(exe_file, self.dir()), verbosity=4)
                try:
                    in_file = open(input)
                    out_file = open(target_output, "w")
                    status, p = run_exe(exe_file, in_file=in_file, out_file=out_file)
                except:
                    logger.error("error generating output", target_output)

    def tests_zip(self, crafted_dir=None):
        zip_file = self.zipped_testcases_path()
        
        if os.path.exists(zip_file) and os.path.getmtime(zip_file) >= self.modification_time():
            logger.info("Zip with testcases is up to date")
            return False
        
        self.clear_build_dir()

        if self.has_crafted_testcases() and crafted_dir == None:
            crafted_dir = self.crafted_testcases_input_dir()
        
        self.prepare_all_testcases(crafted_dir)
        
        writer = ZipWriter(zip_file)
        writer.open()

        i = 1
        for testcase_in in (self.example_testcases() + self.crafted_testcases() + self.generated_testcases()):
            logger.info(testcase_in, verbosity=4)
            writer.copy_file(testcase_in, "{:02d}.in".format(i))
            testcase_out = testcase_in[0:-2] + "out"
            logger.info(testcase_out, verbosity=4)
            writer.copy_file(testcase_out, "{:02d}.out".format(i))
            i += 1
        writer.close()
        logger.info("Testcases stored in", zip_file)
        return True

    def prepare_all_testcases(self, crafted_dir=None):
        self.extract_example_testcases()
        self.generate_testcases()
        if crafted_dir == None and self.has_crafted_testcases():
            crafted_dir = self.crafted_testcases_input_dir()
        if crafted_dir:
            self.prepare_crafted_testcases(crafted_dir)
        
    # compile custom checker
    def compile_checker(self, force=True):
        # check if the checker exists
        if not self.has_checker():
            logger.error("no custom checker for", self.id())
            return False
        src = self.checker_src_path()
        exe = self.checker_exe_path()
        # skip compilation if it is not forced and exe file already exists
        if not force and os.path.isfile(exe):
            return True
        logger.info("Compiling checker:", os.path.basename(src))
        # compile the checker
        if not compile_cpp(src, exe):
            logger.error("compiling checker")
            return False
        return True
    
    # run a given exe file on a given testcase with a given time limit (in milisecond)
    # testcase can be either a full path or a generated test-case number 
    def run(self, sol, lang, testcase, timelimit=None, output=None):
        if not timelimit:
            timelimit = self.timelimit()
        elif type(timelimit) != 'float':
            timelimit = float(timelimit)

        logger.info("Timelimit:", timelimit, verbosity=5)
        
        # open in_file
        if isinstance(testcase, int):
            testcase = self.generated_testcase_path(testcase)
        if not os.path.isfile(testcase):
            logger.error("Testcase", testcase, "does not exist")
            return "RTE"
        in_file = open(testcase)

        # open out_file
        if output == None:
            out_file = tempfile.TemporaryFile()
        elif output != "stdout":
            try:
                out_file = open(output, "w")
            except:
                logger.error("Output file", output, "could not be created")
                return "RTE"
        else:
            out_file = sys.stdout

        # compile if necessary
        if not self.compile(sol, lang, False):
            return "CE"

        # run exe or interpret python
        if lang == "py":
            status, p = run_py(self.src_file_path(sol, lang), in_file=in_file, out_file=out_file, timeout=timelimit)
        else:
            exe_file = self.exe_file_path(sol, lang)
            status, p = run_exe(exe_file, in_file=in_file, out_file=out_file, timeout=timelimit)

        # close files
        in_file.close()
        if output != "stdout":
            out_file.close()

        # return execution status
        return status


    # run a given exe file interactively (reading from stdin and writing to stdout)
    def run_interactive(self, sol, lang):
        if not self.compile(sol, lang, False):
            return "CE"

        if lang == "py":
            return run_py(self.src_file_path(sol, lang), sys.stdin, sys.stdout)
        else:
            exe_file = self.exe_file_path(sol, lang)
            status, p = run_exe(exe_file, in_file=sys.stdin, out_file=sys.stdout)
            return status

    # Testing correctness of solutions
    
    # check the correctness of a given solution on the given testcase
    def test_on_testcase(self, sol, lang, input, expected_output, testcase_number=None, timelimit=None, save_output_dir=None):
        if testcase_number:
            logger.info("testing testcase", testcase_number, os.path.basename(input), verbosity=4)
        else:
            logger.info("testing testcase", os.path.basename(input), verbosity=4)
            
        # compares expected and obtained output using a custom checker
        # for a given task
        def custom_checker_compare(output, expected_output, input):
            exe_file = self.checker_exe_path()
            args = [output, expected_output, input]
            status, p = run_exe(exe_file, args=args, check=False)
            return status == "OK" and p.returncode == 0

        # compares expected and obtained output using the default checker
        def default_checker_compare(output, expected_output, input):
            # if a compiled default checker exists, it is used
            if os.path.exists(self.default_checker_exe_path()):
                exe_file = self.default_checker_exe_path()
                args = [expected_output, output, input]
                status, p = run_exe(exe_file, args=args, check=False)
                return status == "OK" and p.returncode == 0
            # otherwise the python implementation is used (default_checker)
            return compare_files(expected_output, output)

        # test_01.in -> 01
        num = input[-5:-3] if re.search(r"\d{2}[.]in$", input) else ""
        
        # _build/tmp01.out
        user_output = os.path.join(self.build_dir(),
                                   "tmp" + num + ".out")

        # run solution skipping check if execution was terminated
        # due to timeout
        start_time = time.time()
        if timelimit == None:
            timelimit = self.timelimit()
        status = self.run(sol, lang, input, timelimit, user_output)
        ellapsed_time = round(1000*(time.time() - start_time))
        
        if status == "RTE":
            logger.warn(self.id(), sol, lang, "runtime error while executing program")
        
        # if program was executed successfully
        if status == "OK":
            # check correctness of the output
            if self.has_checker():
                OK = custom_checker_compare(user_output, expected_output, input)
            else:
                OK = default_checker_compare(user_output, expected_output, input)

            # report error
            if not OK:
                status = "WA"
                # log error details
                logger.warn("WA", os.path.basename(self.exe_file_path(sol, lang)), os.path.basename(input), verbosity=3)
                if logger.verbosity() >= 5:
                    logger.info("Program output:", user_output, verbosity=4)
                    dump_file(user_output)
                    logger.info("..............................", verbosity=4)
                    logger.info("Expected output:", expected_output, verbosity=4)
                    dump_file(expected_output)
                    logger.info("..............................", verbosity=4)


        # if necessarry, remove temporary file with the user output
        if os.path.isfile(user_output):
            if save_output_dir == None:
                try:
                    os.remove(user_output)
                except:
                    logger.warn("Could not remove user output file", user_output)
            else:
                save_output_path = os.path.join(save_output_dir, os.path.basename(expected_output))
                logger.info("Saving output", os.path.relpath(save_output_path, os.getcwd()), verbosity=4)
                try:
                    os.makedirs(os.path.dirname(save_output_path), exist_ok=True)
                    shutil.copy(user_output, save_output_path)
                except:
                    logger.warn("Could not save output file", save_output_path)    

        return status, ellapsed_time


    @staticmethod
    def final_status(statuses):
        if statuses["RTE"] > 0:
            status = "RTE"
        elif statuses["WA"] > 0:
            status = "WA"
        elif statuses["TLE"] > 0:
            status = "TLE"
        else:
            status = "OK"
        return status
        
    
    # test correctness of a given solution on given list of testcases
    def test_on_given_testcases(self, sol, lang, testcases, testcase_numbers=None, timelimit=None, expected_status=None, force=False, reporter=None, save_outputs_dir=None):
        # skip testing if testing is not forced and the reporter says that the
        # test can be skipped
        if not force and reporter and reporter.should_test(sol, lang) == False:
            return None

        if testcase_numbers == None:
            testcase_numbers = list(range(1, len(testcases) + 1))

        # compile solution
        if not self.compile(sol, lang):
            logger.error("Compilation failed for", sol, lang)
            return None

        # compile custom checker if it exists
        if self.has_checker():
            if not self.compile_checker():
                return None

        logger.info("Running:", self.exe_file_name(sol, lang))

        # count testcase statuses
        statuses = {"OK": 0, "WA": 0, "TLE": 0, "RTE": 0}

        # check every testcase
        max_time = 0
        for input, testcase_number in zip(testcases, testcase_numbers):
            expected_output = input[:-2] + "out" # test_01.in -> test_01.out

            # run test and measure ellapsed time
            result, ellapsed_time = self.test_on_testcase(sol, lang, input, expected_output, timelimit=timelimit, testcase_number=testcase_number, save_output_dir=save_outputs_dir)
            max_time = max(max_time, ellapsed_time)

            if reporter:
                reporter.report_testcase(sol, lang, testcase_number, os.path.basename(input), result, ellapsed_time)
                        
            statuses[result] += 1;
                
        logger.info(statuses)
        logger.info(f"Max time: {max_time}ms")

        if reporter:
            reporter.report_solution(sol, lang, statuses, max_time)

        status = Task.final_status(statuses)

        if expected_status == None:
            expected_status = self.expected_status(sol)
            
        if status != expected_status:
            if status == "OK" and self.expected_status(sol) == "TLE":
                logger.warn(self.id(), sol, lang, "status " + status + " different than expected " + expected_status)
            else:
                logger.error(self.id(), sol, lang, "status " + status + " different than expected " + expected_status)

        if reporter:
            reporter.end()
            
        return statuses

    # test correctness of a given solution on all example testcases
    def test_on_example_testcases(self, sol, lang, force=False, reporter=None, save_outputs=False):
        logger.info("Testing on example testcases")
        # ensure that all example testcases are extracted
        if self.number_of_example_testcases() == 0:
            self.extract_example_testcases()
            
        save_outputs_dir = self.example_test_output_dir() if save_outputs else None
        start = 1
        testcase_numbers = list(range(start, start+self.number_of_example_testcases()))
        return self.test_on_given_testcases(sol, lang, self.example_testcases(), testcase_numbers=testcase_numbers, force=force, reporter=reporter, save_outputs_dir=save_outputs_dir, expected_status="OK")

    
    # test correctness of a given solution on all generated testcases
    def test_on_generated_testcases(self, sol, lang, timelimit=None, force=False, reporter=None, save_outputs=False):
        logger.info("Testing on generated testcases")
        # ensure that generated testcases exist
        if self.number_of_generated_testcases() == 0:
            self.generate_testcases()

        start = self.number_of_example_testcases() + 1
        testcase_numbers = list(range(start, start+self.number_of_generated_testcases()))
        save_outputs_dir = self.generated_test_output_dir() if save_outputs else None
        return self.test_on_given_testcases(sol, lang, self.generated_testcases(), testcase_numbers=testcase_numbers, timelimit=timelimit, force=force, reporter=reporter, save_outputs_dir=save_outputs_dir)

    # test correctness of a given solution on all crafted testcases
    def test_on_crafted_testcases(self, sol, lang, timelimit=None, force=False, reporter=None, save_outputs=False):
        if self.number_of_crafted_testcases() > 0:
            logger.info("Testing on crafted testcases")
            start = self.number_of_example_testcases() + self.number_of_generated_testcases() + 1
            testcase_numbers = list(range(start, start+self.number_of_crafted_testcases()))
            save_outputs_dir = self.crafted_test_output_dir() if save_outputs else None
            return self.test_on_given_testcases(sol, lang, self.crafted_testcases(), timelimit=timelimit, force=force, reporter=reporter, save_outputs_dir=save_outputs_dir)
        return None

    # check correctness of a given solution on all testcases (example and generated)
    def test_on_all_testcases(self, sol, lang, timelimit=None, force=False, reporter=None, save_outputs=False):
        if not force and reporter and reporter.should_test(sol, lang) == False:
            return None
        
        # compile solution
        if not self.compile(sol, lang):
            logger.error("Compilation failed for", sol, lang)
            return None

        if not self.test_on_example_testcases(sol, lang, force=force, reporter=reporter, save_outputs=save_outputs):
            return False
        if not self.test_on_generated_testcases(sol, lang, timelimit=timelimit, force=force, reporter=reporter, save_outputs=save_outputs):
            return False
        if not self.test_on_crafted_testcases(sol, lang, timelimit=timelimit, force=force, reporter=reporter, save_outputs=save_outputs):
            return False
        return True

    # class that uses testing results and scoring.yaml to count the
    # final score for the task being tested
    class ScoringReporter:
        def __init__(self, task):
            self._task = task
            self._results = dict()
            self._score = 0

        def score(self):
            return self._score
        
        def should_test(self, sol, lang):
            return True
        
        def report_testcase(self, sol, lang, testcase_number, testcase, result, time):
            self._results[testcase_number] = result == "OK"
            
        def report_solution(self, sol, lang, statuses, max_time):
            pass
        
        def end(self):
            scoring_yaml = self._task.load_scoring_yaml()
            self._score = 0
            scoring_type = scoring_yaml.get('type', '')
            if scoring_type == 'testcase':
                for testcase in scoring_yaml.get('score_overrides', []):
                    if 'name' in testcase:
                        t = testcase['name']
                        if self._results.get(t, False):
                            self._score += testcase.get('score', 0)
            elif scoring_type == 'subtask':
                for group in scoring_yaml.get('groups', dict()):
                    group_OK = all(map(lambda t: self._results.get(t, False), group.get('testcases', [])))
                    if group_OK:
                        self._score += group.get('score', 0)
            logger.info("Score:", self._score)
            # reset results
            self._results = dict()
    

    # test correctness of all existing solutions of a given task
    def test_all(self, langs=[], sols=[], timelimit=None, force=False, reporter=None):
        # log what checker is going to be used
        if self.has_checker():
            logger.info("Running custom checker...", verbosity=4)
        else:
            logger.info("Running default checker...", verbosity=4)
            
        # find existing, listed solutions (by intersecting sols and self.solutions())
        if not sols:
            sols = self.solutions()
        else:
            sols = [sol for sol in self.solutions() if sol["name"] in sols]
            
        # process all existing, listed solutions
        for sol in sols:
            # in all existing and listed langugages
            for lang in sol["lang"]:
                if langs and not lang in langs: continue
                # run the check
                self.test_on_all_testcases(sol["name"], lang=lang, timelimit=timelimit, force=force, reporter=reporter)

        if reporter:
            reporter.end()
    

    # Run all tests and measure runtime

    # full path to time.json file for a task with the given task_id in a
    # given source repository
    def time_json_path(self):
        return os.path.join(self.build_dir(), "time.json")

    # run all tests (all solutions specified in -st.md on all testcases)
    # for the given tasks
    def measure_all_runtimes(self, force=False, repeat=3, timelimit=None, solutions=[], langs=[]):
        # if the timing file already exists and run is not force, just
        # return data read from the file
        time_json = self.time_json_path()
        if not force and os.path.isfile(time_json):
            logger.info("Results loaded from", time_json)
            return json.load(open(time_json, "r"))

        # determine time limit
        timelimit = timelimit or self.timelimit()
        logger.info(f"Running with the timelimit of {timelimit}ms", verbosity=4)
        
        # otherwise run the tests
        logger.info(logger.bold(self.id()), "-", "running tests to measure time...", verbosity=2)
        
        # generate testcases if they do not exist
        num_testcases = self.number_of_generated_testcases() + \
                        self.number_of_crafted_testcases()
        logger.info("Found {} testcases".format(num_testcases))
        if num_testcases == 0:
            logger.info("Generating tests")
            self.prepare_all_testcases()
     
        # run tests and store the results in a dictionary
        result = {}
        result["id"] = self.id()
        result["dir"] = self.dir()
        
        # dictionary for storing all times
        all_times = {}

        # considering all generated and crafted testcases
        testcases = [*self.generated_testcases(), *self.crafted_testcases()]
        if len(testcases) == 0:
            logger.error("No testcases found - measuring runtime aborted")
            return None

        # process all solutions
        for sol in self.solutions():
            # if the list of solutions is reduced, skip unlisted solutions
            if solutions and sol["name"] not in solutions:
                continue
            
            logger.info("Solution:", sol["name"])
     
            # dictionary for storing times for a given solution
            sol_times = {}
            
            # process all programming languages for that solution
            for lang in sol["lang"]:
                # skip languages
                if langs and lang not in langs:
                    continue

                logger.info("Language:", lang)
                
                # compile solution
                if not self.compile(sol["name"], lang, False):
                    logger.error("compilation failed", self.src_file_name(sol["name"], lang))
                    continue

                # count testcase statuses
                statuses = {"OK": 0, "WA": 0, "TLE": 0, "RTE": 0}
                
                # dictionary for storing times for a specific language
                lang_times = {}

                logger.info("Running on generated and crafted testcases - number of repetitions:", repeat)

                num_timeout = 0

                # iterate through all testcases
                for infilename in testcases:
                    # for better accuracy the test is repeated several
                    # number of times, and median time is calculated
                    ellapsed_times = []
                    for i in range(repeat):
                        # extract test number (e.g., _build/testcases/generated/testcase_01.in -> 01.in)
                        test_number = os.path.basename(infilename)[-5:]
                        
                        # run test and measure ellapsed time
                        start_time = time.time()
                        status = self.run(sol["name"], lang, infilename, timelimit)
                        statuses[status] += 1
                        if status == "TLE":
                            ellapsed_times.append(float('inf'))
                        else:
                            ellapsed_time = time.time() - start_time
                            ellapsed_times.append(ellapsed_time * 1000)
     
                    # calculate median time
                    M = statistics.median(ellapsed_times)
                    timeout = M == float('inf')
                    lang_times[test_number] = round(M) if not timeout else float('inf')
                    # note if timeout
                    if timeout:
                        lang_times[test_number + "_TO"] = True
                        num_timeout += 1
                sol_times[lang] = lang_times

                status = Task.final_status(statuses)
                M = max(lang_times.values())
                if M != float('inf'):
                    logger.info(f"Max testcase runtime {M}ms")
                else:
                    logger.info(f"TLE on {num_timeout} testcases")
                    if self.expected_status(sol["name"]) != status:
                        logger.warn(f"{sol['name']} {lang}: status {status} different than expected {self.expected_status(sol['name'])}")
                
            all_times[sol["name"]] = sol_times
            
        result["times"] = all_times
        
        # store results in the time.json file
        with open(time_json, "w") as time_json_file:
            print(json.dumps(result, indent=4), file=time_json_file)

        logger.info(f"Results written to {time_json} file")
        return result

    # determine time limits for the given task
    def calibrate(self, langs=[], min_timelimit=50, max_timelimit=1000, margin=1.25, force=False, prefix="", petlja_set_timelimit=False):
        logger.info("Calibrating:", logger.bold(self.id()))
        
        # results of the calibration are stored in a dictionary
        calibration = {}
        calibration["dir"] = self.dir()
        calibration["id"] = self.id()

        # measure all runtimes (or read them from a file)
        times = self.measure_all_runtimes(force=force)['times']

        # group times by expected status - OK and TLE
        OK_times = []
        TLE_times = []
        for sol in times:
            sol_times = []
            for lang in times[sol]:
                if langs and lang not in langs: continue
                # time for the slowest testcase
                max_time = max(times[sol][lang].values())
                sol_times.append(max_time)
            if not sol_times:
                continue
            status = self.expected_status(sol)
            if status == "OK":
                OK_times.append(max(sol_times))
            elif status == "TLE":
                TLE_times.append(min(sol_times))

        # calculate time limit with a given margin
        max_time = max(OK_times)
        if max_time == float("inf"):
            logger.error(logger.bold(self.id()), "-", "problem could not be solved within the given time limit")
            return
        
        timelimit = math.ceil(margin * max_time)
        if timelimit < min_timelimit:
            logger.warn(f"Adjusting time limit {timelimit}ms to minimum time limit value {min_timelimit}ms", verbosity=4)
            timelimit = min_timelimit
        if timelimit > max_timelimit:
            logger.warn(f"Time limit {timelimit}ms is above maximum timelimit value {max_timelimit}ms")

        logger.info(f"Time limit: {timelimit}ms")
        calibration["timelimit"] = timelimit

        # determine the quality of the calculated timelimit 
        if TLE_times:
            if timelimit > min(TLE_times):
                quality = "FAIL"
            elif margin * timelimit > min(TLE_times):
                quality = "TIGHT"
            else:
                quality = "OK"
        else:
            quality = "OK"
        calibration["quality"] = quality

        # detailed explanation of the calibration quality
        details = {}
        for sol in times:
            details[sol] = {}
            details[sol]["status"] = self.expected_status(sol)
            for lang in times[sol]:
                if langs and lang not in langs: continue
                # number of testcases that pass
                OK = sum(1 for test, time in times[sol][lang].items() if test[-2:] == "in" and time <= timelimit)
                # number of testcases that fail
                TLE = len(times[sol][lang].items()) - OK
                details[sol][lang] = {}
                details[sol][lang]["testcases"] = str(OK) + "+" + str(TLE)
                # max time for all testcases
                max_time = max(times[sol][lang].values())
                details[sol][lang]["max_time"] = max_time
        calibration["details"] = details
        
        if calibration["quality"] == "OK":
            logger.info(f"Quality: {calibration['quality']}")
        elif calibration["quality"] == "TIGHT":
            logger.warn(f"Quality: {calibration['quality']}")
        elif calibration["quality"] == "FAIL":
            logger.error(f"Quality: {calibration['quality']}, skipping")
        
        # write the timelimit value in -st.md file
        if calibration["quality"] != "FAIL":
            self.set_timelimit(timelimit)
            if petlja_set_timelimit:
                self.petlja_set_timelimit(timelimit, prefix=prefix)

        # return the result
        return calibration
    

    ####################################################################
    # Modifying task data
    
    # set timelimit (given in miliseconds)
    def set_timelimit(self, timelimit):
        try:
            text, metadata = parse_front_matter(self.st_path())
            metadata["timelimit"] = timelimit/1000
            write_to_file(self.st_path(),
                          "---\n" + yaml.dump(metadata, sort_keys = False, default_flow_style=None, allow_unicode=True) + "---\n\n" + text)
        except:
            logger.error("Writting timelimit to file failed")
    
    
    ####################################################################
    # petlja_api
    
    def petlja_publish(self, session=None, prefix=""):
        # session that will be used
        session_ = None
            
        try:
            # login to petlja if necessary
            try:
                session_ = session or get_petlja_session()
            except Exception as e:
                logger.error(e)
                return None

            title = self.title()
            alias = self.alias(prefix)
            # create problem
            try:
                problem_id = petlja_api.create_problem(session_, title, alias)
            except NameError as e:
                logger.error(e)
                return None
            except ValueError:
                logger.warning(f"Problem with alias {alias} already exists.")
                # if get_problem_id also fails, then the user doesn't have
                # the permission to add the problem
                try:
                    problem_id = petlja_api.get_problem_id(session_, alias)
                except ValueError:
                    logger.error(f"You don't have the permission to add problem with alias {alias}")
                    return None
            
                overwrite_prompt = input("Overwrite? (no/yes) ")
                if overwrite_prompt == 'yes':
                    logger.info(f"Overwriting problem {self.id()} with its current version")
                else:
                    return problem_id
            
            logger.info(f"Added problem {title} with alias {alias}")

            try:
                # upload statement
                tmp_st_file = tempfile.NamedTemporaryFile("w+", delete=False, encoding='utf-8')
                tmp_st_file.write(self.st_content())
                tmp_st_file.seek(0)
                petlja_api.upload_statement(session_, problem_id, tmp_st_file.name)
                tmp_st_file.close()
                os.unlink(tmp_st_file.name)        
                logger.info(f"Uploaded statement: {self.st_path()}")
            except:
                logger.error("There was an error uploading task statement")

            try:
                # upload testcases
                if self.tests_zip():
                    petlja_api.upload_testcases(session_, problem_id, self.zipped_testcases_path())
                    logger.info(f"Uploaded testcases: {self.zipped_testcases_path()}")
            except:
                logger.error("There was an error uploading testcases")

            try:
                # set timelimit
                if self.timelimit():
                    timelimit = self.timelimit()
                    petlja_api.set_time_limit(session_, problem_id, timelimit)
                    logger.info(f"Time limit set to {timelimit}ms")

                # set memory limit
                if self.memorylimit():
                    memlimit = self.memorylimit()
                    petlja_api.set_memory_limit(session_, problem_id, memlimit)
                    logger.info(f"Memory limit set to {memlimit}MB")
            except:
                logger.error("There was an error setting timelimit")
            
            return problem_id

        finally:
            # if the session is opened within this call, close it
            if session_ and not session:
                logger.info("Closing petlja session")
                session_.cookies.clear()
                session_.close()
            

    def petlja_get_problem_id(self, session=None, prefix=""):
        # session that will be used
        session_ = None
            
        try:
            # login to petlja if necessarry
            try:
                session_ = session or get_petlja_session()
            except Exception as e:
                logger.error(e)
                return None

            title = self.title()
            alias = self.alias(prefix)
            try:
                problem_id = petlja_api.get_problem_id(session_, alias)
                logger.info("Problem id:", problem_id, verbosity=5)
                return problem_id
            except ValueError:
                logger.warn(f"Problem {self.title()} with alias {self.alias()} does not exist on petlja.org. Try running 'petljapub petlja-publish' first.")
                return None
            
        finally:
            # if the session is opened within this call, close it
            if session_ and not session:
                logger.info("Closing petlja session")
                session_.cookies.clear()
                session_.close()

    def petlja_get_competition_id(self, session=None, competition_dir=None):
        # session that will be used
        session_ = None
        
        try:
            # login to petlja if necessarry
            try:
                session_ = session or get_petlja_session()
            except Exception as e:
                logger.error(e)
                return None, None

            # FIXME importing here to avoid circular import
            from .competition import Competition
        
            # Try to find a competition on petlja.org
            try:
                # if the competition dir is not specified
                if not competition_dir:
                    # assume that the parent dir is a competition dir
                    competition_dir = os.path.dirname(self.dir())

                competition = Competition(competition_dir)
                competition_id = petlja_api.get_competition_id(session_, competition.alias)
                logger.info("Competition id:", competition_id, verbosity=5)
                return competition_id, competition
            except ValueError:
                logger.warn(f'There is no competition with the alias {competition.alias}. Try running "petljapub create-competition" first.')
                return None, None
            except PermissionError as e:
                logger.warn(e)
                return None, None
            
        finally:
            # if the session is opened within this call, close it
            if session_ and not session:
                logger.info("Closing petlja session")
                session_.cookies.clear()
                session_.close()
    
    def petlja_set_timelimit(self, timelimit, session=None, prefix=""):
        # session that will be used
        session_ = None
        try:
            # login to petlja if necessarry
            try:
                session_ = session or get_petlja_session()
            except Exception as e:
                logger.error(e)
                return None

            problem_id = self.petlja_get_problem_id(session_, prefix)
            if problem_id == None:
                logger.error("Could not set time limit")
                return
            petlja_api.set_time_limit(session_, problem_id, timelimit)

        finally:
            # if the session is opened within this call, close it
            if session_ and not session:
                logger.info("Closing petlja session")
                session_.cookies.clear()
                session_.close()
    
    def petlja_test_on_all_testcases(self, sol, lang, session=None, competition_dir=None, detailed=False, timelimit=None):
        # session that will be used
        session_ = None
        
        try:
            # login to petlja if necessary
            try:
                session_ = session or get_petlja_session()
            except Exception as e:
                logger.error(e)
                return None
        
            # Try to find a competition on petlja.org
            competition_id, competition = self.petlja_get_competition_id(competition_dir=competition_dir, session=session_)
        
            prefix = ""
            if competition:
                prefix = competition.task_prefix()
            
            # try to find the task on petlja
            problem_id = self.petlja_get_problem_id(session=session_, prefix=prefix)

            # if the task is included in a competition, test it in that competition
            if competition_id and problem_id:
                # try to set the timelimit
                try:
                    if timelimit != None:
                        petlja_api.set_time_limit(session_, problem_id, timelimit)
                        logger.info(f"Temporarily set timelimit to {timelimit}ms", verbosity=4)
                except:
                    logger.warn(f"Could not set timelimit. Testing with the old timelimit.")

                
                # submit the solution and print the score
                try:
                    src = pathlib.Path(self.src_file_path(sol, lang))
                    logger.info("Submitting task:", src)
            
                    if detailed:
                        result = asdict(petlja_api.submit_solution_detailed(session_, competition_id, problem_id, src))
                        logger.info(f'Score: {result["score"]}')
                        if result["compile_error"]:
                            logger.error(f'Compile error')
                            return None
                        else:
                            for testcase_result in result["testcase_results"]:
                                logger.info("Status:", testcase_result["status"],
                                            "Time[ms]:", testcase_result["time_ms"],
                                            "Memory[MB]:", testcase_result["memory_mb"],
                                            verbosity=5)
                            ret = result
                    else:
                        score = petlja_api.submit_solution(session_, competition_id, problem_id, src)
                        logger.info(f'Score: {score}')
                        ret = int(score)
                except Exception as e:
                    logger.error(e)

                # FIXME: use old time timit from the server
                # try to set the timelimit
                if timelimit != None:
                    try:
                        petlja_api.set_time_limit(session_, problem_id, self.timelimit())
                        logger.info(f"Restored timelimit to {self.timelimit()}ms", verbosity=4)
                    except:
                        logger.warn("Could not reset time limit after testing")

                return ret
            else:
                # the task is not included in a competition, test it using the raw testing API
                logger.warn("Task is not included in a competition. Testing using the petlja API.")
                try:
                    result = self.petlja_api_submit_solution_raw(sol, lang, timelimit=timelimit)
                    if result["compile_error"]:
                        logger.error(f'Compile error')
                        return None
                    else:
                        for testcase_result in result["testcase_results"]:
                            logger.info(f"#{testcase_result['number']}",
                                        "Status:", testcase_result["status"],
                                        "Time[ms]:", testcase_result["time_ms"],
                                        "Memory[MB]:", testcase_result["memory_mb"],
                                        verbosity=4)
                        logger.info("Score:", result['score'])
                        return result
                except Exception as e:
                    logger.error("Error testing task")
                    logger.error(e)
        finally:
            # if the session is opened within this call, close it
            if session_ and not session:
                logger.info("Closing petlja session")
                session_.cookies.clear()
                session_.close()
                            
    # check if all solutions match their expected score
    def petlja_test_all_scores(self, session=None):
        # session that will be used
        session_ = None
        
        try:
            # login to petlja if necessary
            try:
                session_ = session or get_petlja_session()
            except Exception as e:
                logger.error(e)
                return None
            
            tests_passed = True
            num_tested = 0
            for sol in self.solutions():
                if "expected-score" not in sol or not sol["expected-score"]:
                    logger.warning(f'Solution {sol["name"]} does not have an expected score '
                                   'specified in the statement metadata. Skipping...')
                    continue
                for lang in sol["lang"]:
                    sol_id = sol["name"]
                    score = self.petlja_test_on_all_testcases(lang, sol_id, session=session_)
                    num_tested += 1
                    if not score:
                        tests_passed = False
                        continue

                    sol_filename = self.src_file_name(sol_id, lang)
                    if score != sol["expected-score"]:
                        logger.error(f'Solution {sol_filename} does not match expected score:\n'
                                     f'Expected: {sol["expected-score"]} Got: {score}')
                        tests_passed = False
                    else:
                        logger.info(f'Solution {sol_filename} matches expected score', verbosity=3)
                        logger.info(f'Expected: {sol["expected-score"]} Got: {score}', verbosity=4)

            if tests_passed:
                if num_tested > 0:
                    logger.info("All tests passed!")
                else:
                    logger.error("Some tests failed!")

            return tests_passed
            
        finally:
            # if the session is opened within this call, close it
            if session_ and not session:
                logger.info("Closing petlja session")
                session_.cookies.clear()
                session_.close()
        

    # run all tests (all solutions specified in -st.md on all testcases)
    # for the given tasks
    def petlja_measure_all_runtimes(self, force=False, competition_dir=None, langs=[], solutions=[], timelimit=None, session=None):
        # session that will be used
        session_ = None
        
        try:
            # if the timing file already exists and run is not force, just
            # return data read from the file
            time_json = self.time_json_path()
            if not force and os.path.isfile(time_json):
                logger.info("Results loaded from", time_json)
                return json.load(open(time_json, "r"))
     
            # otherwise run the tests
            logger.info(logger.bold(self.id()), "-", "running tests to measure time...")

            # use the given session or open a new one
            try:
                session_ = session or get_petlja_session()
            except:
                logger.error("Could not log in to petlja.org")
                return None

            # run tests and store the results in a dictionary
            result = {}
            result["id"] = self.id()
            result["dir"] = self.dir()
        
            # dictionary for storing all times
            all_times = {}

            # process all solutions
            for sol in self.solutions():
                # if the list of solutions is reduced, skip unlisted solutions
                if solutions and sol["name"] not in solutions:
                    continue
            
                logger.info("Solution:", sol["name"])
     
                # dictionary for storing times for a given solution
                sol_times = {}
            
                # process all programming languages for that solution
                for lang in sol["lang"]:
                    # skip languages
                    if langs and lang not in langs:
                        continue

                    logger.info("Language:", lang)
                
                    # dictionary for storing times for a specific language
                    lang_times = {}

                    results = self.petlja_test_on_all_testcases(sol["name"], lang, session=session_, competition_dir=competition_dir, detailed=True, timelimit=timelimit)
                    if results == None or not results.get("testcase_results", []):
                        logger.error("Skipping...")
                        continue
                    
                    OK = True
                    num_timeout = 0
                    num_wa = 0
                    for num, testcase in enumerate(results["testcase_results"], 1):
                        lang_times[num] = testcase["time_ms"]
                        if testcase["status"] != "OK":
                            OK = False
                            if testcase["status"] == "TLE":
                                num_timeout += 1
                                lang_times[num] = float('inf')
                            if testcase["status"] == "WA":
                                num_wa += 1
                        
                    M = max(lang_times.values())
                    if M != float('inf'):
                        logger.info(f"Max testcase runtime {M}ms")
                    else:
                        logger.info(f"TLE on {num_timeout} testcases")
                        if self.expected_status(sol["name"]) != "TLE":
                            logger.warn("status TLE different than expected " + self.expected_status(sol))

                    if num_wa > 0 and self.expected_status(sol["name"]) != "WA":
                        logger.warn(f"WA on {num_wa} testcases")
                        
                    sol_times[lang] = lang_times

                    
                all_times[sol["name"]] = sol_times
            result["times"] = all_times
        
            # store results in the time.json file
            with open(time_json, "w") as time_json_file:
                print(json.dumps(result, indent=4), file=time_json_file)

            logger.info(f"Results written to {time_json} file")
            return result
            
        finally:
            # if the session is opened within this call, close it
            if session_ and not session:
                logger.info("Closing petlja session")
                session_.cookies.clear()
                session_.close()

    ####################################################################
    # raw petlja_api
                
    def petlja_api_submit_solution_raw(self, sol, lang, timelimit=None):
        languageId = {
            "cs": "1",
            "py": "9",
            "cpp": "11"
        }
        url = "https://petlja.org/api/competition/submit-custom-task-grading"
        source_code = self.src_code(sol, lang)
        data = {
            "authKey": "2c39329a-7824-4fb1-9dd8-6637b293a23f",
            "type": "0",
            "languageId": languageId[lang],
            "source": source_code
        }
        if timelimit:
            data["timeLimit"] = timelimit
            logger.info(f"TimeLimit: {timelimit}ms")

        self.tests_zip()
        test_cases_zip_path = self.zipped_testcases_path()
        files = {
            "testCasesZip": ("testcases.zip", open(test_cases_zip_path, 'rb'), 'application/zip')
        }

        if self.has_checker():
            data["checkerLanguage"] = languageId["cpp"]
            data["checker"] = self.checker_src()

        logger.info(url, data, verbosity=5)
        response = requests.post(url, data=data, files=files)
        if response.status_code == 200:
            result = response.json()
            if not result['succeeded']:
                logger.error("Not succeeded")
            else:
                if result['value'].startswith('compile error'):
                    compile_error = True
                else:
                    score = 0
                    compile_error = False
                    testcase_results = []
                    for testcase in result['value'].split(";")[:-1]:
                        pattern = r"test case #(\d+) \[(\d+(\.\d+)?) ms/(\d+(\.\d+)?) MB\] \+(\w+)"
                        match = re.search(pattern, testcase)
                        if match:
                            testcase_number = match.group(1)
                            execution_time = round(float(match.group(2)))
                            memory_usage = match.group(4)
                            status = match.group(6)
                            testcase_results.append({"number": testcase_number,
                                                     "status": status,
                                                     "time_ms": execution_time,
                                                     "memory_mb": memory_usage})
                            if status == "OK":
                                score += 1

                        pattern = r"failed case #(\d+) \[(\d+(\.\d+)?)\s*ms/(\d+(\.\d+)?)\s*MB\] : ([a-z ]+)"
                        match = re.search(pattern, testcase)
                        if match:
                            testcase_number = match.group(1)
                            execution_time = round(float(match.group(2)))
                            memory_usage = match.group(4)
                            if match.group(6) == "cpu time restraint broken":
                                status = "TLE"
                            elif match.group(6) == "incorrect output":
                                status = "WA"
                            else:
                                status = "RTE"
                            testcase_results.append({"number": testcase_number,
                                                     "status": status,
                                                     "time_ms": execution_time,
                                                     "memory_mb": memory_usage})

                return {"score": score,
                        "compile_error": compile_error,
                        "testcase_results": testcase_results}
        else:
            print("Error:", response.status_code, response.text)
                
