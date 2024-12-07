import os, sys
import re
import yaml

from . import md_util, markdown_magic_comments, source_code_magic_comments, code_parser

from .serialization import DirectoryWriter, ZipWriter, MarkdownSerializer, TeXMarkdownSerializer
from .publication_visitor import PublicationVisitor
from .task_visitor import TaskVisitor
from .task import Task
from .task_repository import TaskRepository
from .publication_repository import PublicationRepository
from .yaml_specification import YAMLSpecification, YAMLSpecificationVisitor
from .compilation import run_latex

from .md_content_processor import OutputOrganizerSingleDir, ImageProcessorCopy, LinkProcessorTex, ReferenceProcessorTex, MDContentProcessor

from . import logger
from . import messages
from .messages import msg

# Prepares a publication in a single Markdown (or LaTeX) file, ready
# for converting to PDF
class PublicationVisitorTeX(PublicationVisitor, TaskVisitor):
    def __init__(self, yaml_specification, task_repo, publication_repo, dst,
                 tex=False, pdf=False, langs=[], header=None, babel=None, translit=lambda x: x, standalone=True, tex_template=None, quiet=False):
        # call super constructors
        TaskVisitor.__init__(self)
        PublicationVisitor.__init__(self, yaml_specification, task_repo, publication_repo, langs=langs)

        if len(langs) != 1:
            logger.error("Cannot generate tex for multiple programming languages")
            sys.exit()

        # filename and dirname of the resulting md or tex document
        self._dst_file = os.path.basename(dst)
        self._dst_dir = os.path.dirname(dst)
        
        # construct a writing mechanism to dst directory
        self._writer = DirectoryWriter(self._dst_dir)

        # set the i18n
        if babel:
            messages.set_language(babel)

        # construct appropriate Markdown serialization object (either
        # raw markdown or conversion to HTML)
        if tex:
            self._md_serializer = TeXMarkdownSerializer(self._writer, header=header, babel=babel, standalone=standalone, tex_template=tex_template, translit=translit, fix_latex=True)
        else:
            self._md_serializer = MarkdownSerializer(self._writer, header, translit=translit)
        # remember if pdf file should be generated
        self._pdf = pdf

        # tasks are not inline by default
        self._inline_task = False

        # make LaTeX quiet
        self._quiet = quiet
        
        # construct the appropriate processors
        output_organizer = OutputOrganizerSingleDir(".")
        image_processor = ImageProcessorCopy(self._writer, output_organizer)
        link_processor = LinkProcessorTex(self._yaml_specification, self._task_repo, self._publication_repo)
        reference_processor = ReferenceProcessorTex()
        self._md_processor = MDContentProcessor(link_processor, image_processor, reference_processor, "tex")

    # process given md content using the constructed markdown processor
    def process(self, section_path, md_file_path, md, level, langs, unnumbered=False, unlisted=False):
        # process the content
        lang_md = self._md_processor.process(section_path, md_file_path, md,
                                             level=level, langs=langs, unnumbered=unnumbered, unlisted=unlisted)
        # join languages (there will be only one)
        md = ""
        for lang in lang_md:
            md += lang_md[lang]
        return md
        
    # start of the whole publication
    def start(self):
        # open file serialization 
        self._md_serializer.open()
        
        # resulting content
        self._result_md = ""

    # process a single markdown file to be included in publication
    def md_file(self, section_path, level, md_file_name, unnumbered=False):
        # path to the md file
        md_file_path = os.path.join(section_path, md_file_name)        
        # read the content
        metadata, content = self._publication_repo.read_md_file(md_file_path)
        title = metadata.get("title", "")
        # build markdown content - start with the title
        md = md_util.heading(title)
        # add label if it exists
        if "label" in metadata:
            md += " " + md_util.label("sec", metadata["label"]) + "\n"
        # add content
        md += "\n\n" + content

        # exclude all javascript
        md = markdown_magic_comments.exclude(md, "div", ["javascript"])
        
        # process the content
        md = self.process(section_path, md_file_path, md, level, self._langs, unnumbered=unnumbered)

        # process included tasks
        def include_task(task_spec_lines):
            try:
                task_spec = yaml.safe_load("\n".join(task_spec_lines))
            except:
                logger.error("Failed to load yaml task specification")
                return ""
            task_result = self.task(section_path, level + 1, task_spec["id"], task_spec)
            return task_result if task_result != None else ""
        self._inline_task = True
        md = markdown_magic_comments.replace_magic_comment_directives(md, "task", include_task)
        self._inline_task = False


        # process multichoice (abc) questions
        def process_abc(abc_spec_lines):
            try:
                abc_spec = yaml.safe_load("\n".join(abc_spec_lines))
            except:
                logger.error("Failed to load abc question specification")
                return ""
            process_abc.question_id += 1
            process_abc.answers[process_abc.question_id] = abc_spec["correct"]
            return md_util.italic(msg("QUESTION")) + " " + str(process_abc.question_id) + ". " + abc_spec["question"]  + "\n\n" + md_util.enumerate(abc_spec["answers"], compact=True)

        process_abc.question_id = 0
        process_abc.answers = dict()
        md = markdown_magic_comments.replace_magic_comment_directives(md, "abc", process_abc)

        if process_abc.answers:
            md += md_util.italic(msg("ANSWERS")) + ": "
            for key, val in process_abc.answers.items():
                md += str(key) + ") " + ",".join(val) + " "
        
        # append it to the result
        self._result_md += md + "\n\n"
        
    # start of a section in a publication
    def section_start(self, section_path, level, md_files, subsections, tasks):
        logger.info("Section:", section_path)
        # process index.md, if exists
        if self._publication_repo.contains_index(section_path):
            self.md_file(section_path, level, "index.md")
        else:
            logger.warning("non-existent section:", section_path)

    # start of a new task
    def task_start(self, task):
        if not self._inline_task:
            logger.info("Task:", task.id())
        self._task_md = ""

    # header of the task
    def task_header(self, task):
        self._task_md += md_util.md_latex("\\begin{task}")
        
    # print the task title
    def task_title(self, task):
        # title of this task
        title = "{}: {}".format(msg("TASK"), task.title())
        # build an anchor for referencing this task  
        anchor = task.id()
        current_occurrence = self._extra_info["current_occurrence"]
        if current_occurrence > 1:
            anchor += "_" + str(current_occurrence)
        md = md_util.heading(title, self._extra_info["level"], anchor=anchor, unnumbered=True)
        # build heading and append it to the result
        self._task_md += md + "\n\n"

        # Printing all attributes and their values
        if "flags" in self._task_spec:
            for flag in self._task_spec["flags"]:
                flags = self._yaml_specification._yaml.get("flags", dict())
                if flag in flags:
                    self._task_md += md_util.italic(flags[flag])
                    self._task_md += "\n\n"
            

    # first time the task occurs, we print its full statement and next
    # times only reference to the original statement
    def task_st(self, task):
        current_occurrence = self._extra_info["current_occurrence"]
        if current_occurrence > 1:
            # append message to the resulting string
            msg_repeated = msg("REPEATED_TASK")
            md = "{} {}\n\n{}".format(md_util.italic(msg("REPEATED_TASK")),
                                      md_util.link(msg("LOOKUP_TASK"), "#" + task.id()),
                                      md_util.italic(msg("TRY_TO_SOLVE")))
        else:
            # load the problem statement from the repository
            md = task.statement()

            # exclude all javascript
            md = markdown_magic_comments.exclude(md, "div", ["javascript"])
            
            # process the content
            md = self.process(self._extra_info["section_path"], task.st_path(), md, self._extra_info["level"], self._langs)

            
        # append content to the resulting string
        self._task_md += md + "\n\n"

    def task_io(self, task, description=True, examples=True):
        # inner headings are collapsed to save space
        def format_inner_headings(text):
            # collapse inner headings
            text = md_util.remove_headings(text, 2, r"**", r"**\\nopagebreak")
            text = md_util.remove_headings(text, 3, r"*", r"*\\nopagebreak")
            # remove blank lines behind inner headings so that they
            # are printed in the same line with the rest of the text (to save space)
            for m in (msg("INPUT"), msg("OUTPUT")):
                text = md_util.keep_with_next(text, md_util.bold(m))
            return text
        
        current_occurrence = self._extra_info["current_occurrence"]
        if current_occurrence == 1:
            # read input-output specification
            if description and examples:
                md = task.io()
            elif description:
                md = task.io_description()
            elif examples:
                md = task.io_examples()
            # format inner headings
            md = format_inner_headings(md)
            # process the content
            md = self.process(self._extra_info["section_path"], task.st_path(), md, self._extra_info["level"]+1, self._langs)

            # append content to the resulting string
            self._task_md += md + "\n\n"
        
        
    def task_sol(self, task, sols):
        # load the problem solution from the repository
        md = task.sol_content()
        # if some solutions are selected, then print only them
        if sols:
            md = markdown_magic_comments.filter_by_key(md, "sol", sols)

        # exclude all javascript
        md = markdown_magic_comments.exclude(md, "div", ["javascript"])
            
        # process markdown
        md = self.process(self._extra_info["section_path"], task.sol_path(), md,
                          level=self._extra_info["level"], langs=self._langs, unnumbered=True, unlisted=True)
        md = md_util.heading(msg("SOLUTION"), self._extra_info["level"] + 1, unnumbered=True, unlisted=True) + "\n\n" + md

        # append solution to the resulting string
        self._task_md += md + "\n\n"

    def task_source_code(self, task, sol_name, sol_desc, lang, functions):
        # load the source code from the repository
        code = task.src_code(sol_name, lang)
        if not code:
            logger.error("missing code", task.id(), sol_name, lang)
            return
        # process the magic comments
        code = source_code_magic_comments.process_magic_comments(code)
        # extract just specific functions
        if functions != None:
            code = code_parser.extract_funs(lang, code, functions)
        # surround it with Markdown markup for program source code
        code = "\n" + md_util.md_source_code(code, lang)
        # insert formated code to appropriate places within the resulting solution
        if "solution" in self._what_to_print:
            self._task_md = markdown_magic_comments.insert_content(self._task_md, "sol", sol_name, code, "code", "here")
        else:
            self._task_md += code

    def task_report_pending_occurrences(self, task, current_occurrence, total_occurrences):
        # message and link to the additional occurrences
        md = md_util.italic(md_util.link(msg("ADDITIONAL_SOLUTIONS"), "#{}_{}".format(task.id(), current_occurrence + 1)))
        # append it to the resulting string
        self._task_md += md + "\n\n"

    def task_footer(self, task):
            self._task_md += md_util.md_latex("\\end{task}")
        
    def task_end(self, task):
        current_occurrence = self._extra_info["current_occurrence"]
        total_occurrences = self._extra_info["total_occurrences"]
        if current_occurrence < total_occurrences:
            self.task_report_pending_occurrences(task, current_occurrence, total_occurrences)
        if not self._inline_task:
            self._result_md += self._task_md + "\n\n"
                    
    def task_result(self, task):
        return self._task_md
            
    def end(self):
        # write the result to the file (converting to TeX if necessary)
        self._md_serializer.write(self._dst_file, self._result_md)
        if self._pdf:
            dst_path = os.path.join(self._dst_dir, self._dst_file)
            logger.info("Running LaTeX on", dst_path)
            (status, p) = run_latex(dst_path, quiet=self._quiet)
            if status != "OK" or p.returncode != 0:
                logger.error("There were errors when running LaTeX")
