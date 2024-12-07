import sys, os

from .md_util import PandocMarkdown
from . import logger

# Visits and processes a single task.
# Based on the given task specification it is determined which
# components (statement, solutions, source codes) should be processed.
# Details of processing need to be specified in subclasses.

# Task specification is a dictionary in the same forma as given in
# yaml specifications of a publication.
class TaskVisitor:
    # called to process a single task it analyzes the given task
    # specification and based on it processes chosen components of the
    # task
    def visit_task(self, task, langs=[], task_spec=dict(), extra_info=None):
        # memorize auxiliary data so that it does not need to be
        # passed around in method parameters
        self._langs = langs
        self._task_spec = task_spec
        self._extra_info = extra_info

        # a hook called when the processing of the task is started
        # (the hook is defined by subclasses)
        self.task_start(task)
        
        # determine what components to print - if it is not specified
        # in the task specification, everything is processed
        print_spec = task_spec.get("print", "full")
        if type(print_spec) == list:
            self._what_to_print = print_spec
        else:
            self._what_to_print = {
                "full": ["statement", "io-description", "io-examples", "solution", "source"],
                "solution": ["statement", "io-description", "io-examples", "solution"],
                "statement": ["statement", "io-description", "io-examples"],
                "code": ["source"],
                "exclude": []
            }[print_spec]

        # do not print input output specification if requested by the user
        if task_spec.get("no-io", False):
            if "io" in self._what_to_print:
                self._what_to_print.remove("io-description") 
                self._what_to_print.remove("io-examples") 

        # print the start header (e.g., \begin{task} latex command)
        if not task_spec.get("no-title", False):
            self.task_header(task)
                
        # print the task title (if not requested otherwise)
        if not task_spec.get("no-title", False):
            self.task_title(task)

        # if the task statement should be processed
        if "statement" in self._what_to_print:
            # the hook (defined in subclasses) is called
            self.task_st(task)

        # if taks input-output description and examples should be processed
        if "io-description" in self._what_to_print or "io-examples" in self._what_to_print:
            # the hook (defined in subclasses) is called
            self.task_io(task,
                         description="io-description" in self._what_to_print,
                         examples="io-examples" in self._what_to_print)
            

        # finish processing the statement
        if "statement" in self._what_to_print:
            self.task_end_st(task)
    
        # if task solutions should be processed
        if "solution" in self._what_to_print:
            # solutions that need to be processed
            # it is not specified in the task_specification, then all solutions are processed
            solutions = task_spec.get("solutions", [])
            self.task_sol(task, solutions)
            
        # if source codes should be processed
        if "source" in self._what_to_print:
            # codes that need to be processed
            # it is not specified in the task_specification, then all codes from the specified solutions
            # are processed
            solutions = task_spec.get("solutions", [])
            codes = task_spec.get("code", None)
            functions = task_spec.get("functions", None)
            # auxiliary function used to process individual source codes 
            self.task_source_codes(task, codes, solutions, functions)


        # print the start footer (e.g., \end{task} latex command)
        if not task_spec.get("no-title", False):
            self.task_footer(task)
            
        # a hook called when the processing of the task is finished
        # (the hook is defined by subclasses)
        self.task_end(task)

        return self.task_result(task)

    # analyzes task metadata and the task repository to find all
    # available source codes, and processes the ones given by the task
    # specification
    def task_source_codes(self, task, selected_codes, selected_solutions, selected_functions):
        # find all available solutions (specified in the task metadata)
        all_sol_descs = task.solutions()
        # if metadata is missing, it is assumed that only one solution exists
        if not all_sol_descs:
            all_sol_descs = [{"name": "ex0", "lang": ["cpp", "cs", "c", "py"]}]
        # itterate through all solutions (and their descriptions)
        for sol_desc in all_sol_descs:
            # solution name ("ex0", "ex1", ...)
            sol_name = sol_desc["name"]
            # if only some solutions need to be processed and the
            # current sol_name is not among them, then the current code is
            # skipped
            if selected_solutions != [] and not sol_name in selected_solutions:
                continue
            # if only some codes need to be processed and the current
            # sol_name is not among them, then the current code is
            # skipped
            if selected_codes != None and not sol_name in selected_codes:
                continue
            for lang in sol_desc["lang"]:
                # process only codes in the current list of languages
                # (if the list is empty, all codes are processed)
                if not self._langs or lang in self._langs:
                    functions = None
                    if selected_functions:
                        if type(selected_functions) is str:
                            functions = [selected_functions]
                        elif type(selected_functions) is list:
                            functions = selected_functions
                        elif type(selected_functions) is dict and sol_name in selected_functions:
                            functions = selected_functions[sol_name]
                    # a hook called for an individual source code
                    # (defined in subclasses)
                    self.task_source_code(task, sol_name, sol_desc, lang, functions)

    # a list of hooks that need to be defined in subclasses
                
    # a hook called when the processing of the gien task is started
    def task_start(self, task):
        pass

    # a hook called to give the task header
    def task_header(self, task):
        pass
    
    # a hook called to process the task title
    def task_title(self, task):
        pass
        
    # a hook called to process the task statement
    def task_st(self, task):
        pass

    # a hook called to process the task input-output examples
    def task_io(self, task, description, examples):
        pass

    # a hook called after processing statement
    def task_end_st(self, task):
        pass
    
    # a hook called to process solution description, including only
    # solutions from the given list of solutions ("ex0", "ex1", ...)
    # and only on selected languages ("cs", "cpp", "py", ...)
    def task_sol(self, task, sols):
        pass

    # a hook called to process a single source code for the task with
    # the given task_id, with the given solution name (e.g., "ex0"),
    # in the given language (e.g., "cs"), where the metadata
    # description of the solution is also known
    def task_source_code(self, task, sol_name, sol_desc, lang, functions):
        pass

    # a hook called to give the task header
    def task_footer(self, task):
        pass

    # a hook called when the processing of the gien task is ended
    def task_end(self, task):
        pass

    # result of task processing
    def task_result(self, task):
        pass
