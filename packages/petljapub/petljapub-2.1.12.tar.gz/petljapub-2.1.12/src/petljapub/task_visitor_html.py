import os, sys
import re
import argparse

from .task import Task
from .task_visitor import TaskVisitor
from .md_util import PandocMarkdown, md_source_code, images_in_md
from . import markdown_magic_comments
from . import source_code_magic_comments
from . import code_parser
from . import javascript
from . import messages
from .serialization import DirectoryWriter, ZipWriter, MarkdownSerializer, HTMLMarkdownSerializer
from . import logger
from .messages import msg
from .md_content_processor import MDContentProcessor, LinkProcessorRaw, ReferenceProcessorHTML, OutputOrganizerSingleDir, ImageProcessorCopy

class TaskVisitorHTML(TaskVisitor):
    def __init__(self, css=None, header=None, translit=lambda x: x, babel=None):
        self._md = ""
        self._css = css
        self._header = header
        self._translit = translit
        self._babel = babel
        
        # set the i18n
        if babel:
            messages.set_language(babel)
        

    # task is started
    def task_start(self, task):
        # open writer and HTML serializer
        self._writer = DirectoryWriter(task.build_dir())
        self._md_serializer = HTMLMarkdownSerializer(self._writer, standalone=True, css=self._css, header=self._header, translit=self._translit, babel=self._babel)
        self._md_serializer.open()
        self._md_processor = MDContentProcessor(LinkProcessorRaw(), ImageProcessorCopy(self._writer, OutputOrganizerSingleDir(task.build_dir())), ReferenceProcessorHTML(), "html")
        self._task = task

    def process_md(self, md_file_path, md, langs):
        return self._md_processor.process("", md_file_path, md, langs)
        
    # a hook called to process the task title
    def task_title(self, task):
        self._st_md = "# " + task.title() + "\n\n"
        
    # a hook called to process the task statement
    def task_st(self, task):
        # append the statement content, read from the task repository
        self._st_md += task.statement() + "\n\n"
        self._st_md = self.process_md(task.st_path(), self._st_md, None)

    # a hook called to process task input and output
    def task_io(self, task, description=True, examples=True):
        # read input-output specification
        if description and examples:
            md = task.io()
        elif description:
            md = task.io_description()
        elif examples:
            md = task.io_examples()
        # append it to the statement md
        self._st_md += task.io()
        
    # a hook called to process solution description, including only
    # solutions from the given list of solutions ("ex0", "ex1", ...)
    # and only on selected languages ("cs", "cpp", "py", ...)
    def task_sol(self, task, sols):
        self._sol_md = task.sol_content()
        if self._langs:
            self._sol_md = self.process_md(task.sol_path(), self._sol_md, self._langs)
        else:
            self._sol_md = self.process_md(task.sol_path(), self._sol_md, self._task.langs())
            

    # a hook called to process a single source code for the task with
    # the given task_id, with the given solution name (e.g., "ex0"),
    # in the given language (e.g., "cs"), where the metadata
    # description of the solution is also known
    def task_source_code(self, task, sol_name, sol_desc, lang, functions):
        # read the source code from the repository
        code = task.src_code(sol_name, lang)
        if not code:
            logger.error("missing code", task.id(), sol_name, lang)
            return
        # remove the magic comments (retain the whole source code)
        code = source_code_magic_comments.remove_magic_comments(code)
        # extract just specific functions
        if functions != None:
            code = code_parser.extract_funs(lang, code, functions)
        
        # surround it with Markdown markup for program source code
        code = "\n" + md_source_code(code, lang)
        # insert the code to appropriate place in the solution for its language
        self._sol_md[lang] = markdown_magic_comments.insert_content(self._sol_md[lang], "sol", sol_name, code, "code", "here")
    
    # task is ended
    def task_end(self, task):
        if self._langs:
            langs = list(set(self._langs) & set(task.langs()))
        else:
            langs = task.langs()
            
        # join solutions in all languages and write them into a single file
        joined_sol_md = ""
        for lang in langs:
            joined_sol_md += javascript.div(self._sol_md[lang], lang)

        # add javascript language switcher
        if len(langs) != 1:
            joined_sol_md = javascript.add_switcher(joined_sol_md, langs)

        md = self._st_md + "# " + msg("SOLUTION") + "\n\n" + joined_sol_md
        self._md_serializer.write(task.id() + ".md", md, title=task.title())

        logger.info("HTML file written:", os.path.join(task.build_dir_name(), task.id() + ".html"))
