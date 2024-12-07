import os, sys
import re
import tempfile

import json, yaml

from functools import partial

from .util import read_file
from .serialization import DirectoryWriter, ZipWriter, MarkdownSerializer, HTMLMarkdownSerializer
from . import md_util
from . import markdown_magic_comments
from . import source_code_magic_comments
from . import code_parser
from . import javascript
from .publication_visitor import PublicationVisitor
from .task_visitor import TaskVisitor
from .task_repository import TaskRepository
from .publication_repository import PublicationRepository
from .yaml_specification import YAMLSpecification, YAMLSpecificationVisitor
from .md_content_processor import MDContentProcessor, OutputOrganizerHierarchy, LinkProcessorHTML, ReferenceProcessorHTML, ImageProcessorCopy
from . import logger

from .messages import msg
from . import messages


# Prepares a publication in a series of HTML files, ready for publishing on the web
class PublicationVisitorHTML(PublicationVisitor, TaskVisitor):
    # yaml_specification - yaml specification of the publication
    # task_repo, publication_repo - repositories of tasks and publication texts
    # dst - destination to store the resulting files (either a directory path, or a zip file path)
    # langs - programming languages included in the publication
    # html - if True, then the Markdown files are converted to HTML (using pypandoc)
    # join_langs - if True, then solutions for all included languages are stored in a single file
    # standalone - if True, all HTML files are standalone (they include a header and the footer and are ready for viewin)
    # css - link to the css file used to style the resulting HTML
    # section_number_depth - depth of section numbering
    def __init__(self, yaml_specification, task_repo, publication_repo, dst, langs,
                 html=False, join_langs=False, standalone=False,
                 css=None, header=None, translit=lambda x: x, babel=None, section_number_depth=3):
        # call super constructors
        TaskVisitor.__init__(self)
        PublicationVisitor.__init__(self, yaml_specification, task_repo, publication_repo, langs=langs)

        # construct appropriate file writing mechanism (either a zip file, or an ordinary file system)
        if dst.endswith(".zip"):
            self._writer = ZipWriter(dst)
        else:
            self._writer = DirectoryWriter(dst)

        # construct appropriate Markdown serialization object (either
        # raw markdown or conversion to HTML)
        if html:
            self._md_serializer = HTMLMarkdownSerializer(self._writer, header=header, standalone=standalone, css=css, translit=translit, babel=babel)
        else:
            self._md_serializer = MarkdownSerializer(self._writer, header, translit=translit)

        # set the i18n
        if babel:
            messages.set_language(babel)
            
        # remember parameters
        self._join_langs = join_langs
        self._standalone = standalone

        # javascript language switcher id
        self._switcher_id = 0
        # javascript popup id
        self._popup_id = 0

        # tasks are not inline by default
        self._inline_task = False

        # dictionary that maps section paths to section titles (read from index.md files)
        self._section_titles = {}
        self._section_number_depth = section_number_depth

        # construct the appropriate processors
        self._output_organizer = OutputOrganizerHierarchy()
        image_processor = ImageProcessorCopy(self._writer, self._output_organizer)
        link_processor = LinkProcessorHTML(self._yaml_specification, self._task_repo, self._publication_repo, self._output_organizer)
        reference_processor = ReferenceProcessorHTML()
        self._md_processor = MDContentProcessor(link_processor, image_processor, reference_processor, "html")

        # list of files that should be serialized at the end
        self._files = []

    # directory where html files for the current task will be stored
    # (taking into account the section in which that task occurs)
    def task_output_dir(self, task_id, section_path=None):
        if not section_path:
            section_path = self._extra_info["section_path"]

        # inline tasks go to the section path
        if self._inline_task:
            return self._output_organizer.output_dir(section_path)

        # regular tasks have their own dir
        return self._output_organizer.output_dir(os.path.join(section_path, task_id))
        
    # join solutions in all languages and add switcher if there is more than one language
    def join_languages(self, lang_md):
        self._switcher_id += 1
        # join languages
        joined_md = ""
        for lang in lang_md:
            joined_md += javascript.div(lang_md[lang], lang, self._switcher_id)
        # add switcher if there is more than one language
        if len(lang_md) > 1:
            joined_md = javascript.add_switcher(joined_md, self._langs, self._switcher_id)
        return joined_md
    
    def start(self):
        # open file serialization 
        self._md_serializer.open()


    # process included tasks
    def include_task(self, section_path, level, task_spec_lines):
        self._inline_task = True
        try:
            task_spec = yaml.safe_load("\n".join(task_spec_lines))
        except:
            logger.error("Failed to load yaml task specification")
            return ""
        task_result = self.task(section_path, level, task_spec["id"], task_spec)
        self._inline_task = False
        result = md_util.degrade_headings(task_result, 1, unnumbered=True, unlisted=True) if task_result != None else ""
        return result

    # process multichoice (abc) questions
    def process_abc(self, abc_spec_lines):
        try:
            abc_spec = yaml.safe_load("\n".join(abc_spec_lines))
        except:
            logger.error("Failed to load abc question specification")
            return ""
        self.abc_question_id += 1
        return javascript.abc_question(abc_spec, self.abc_question_id)

    def process_javascript(self, section_path, md_file_path, javascript_spec_lines):
        def copy(file_name):
            logger.info("Copy:", file_name, verbosity=4)
            dst_dir = self._output_organizer.output_dir(section_path)
            dst_path = os.path.join(dst_dir, file_name)
            src_path = os.path.join(os.path.dirname(md_file_path), file_name)
            self._writer.copy_file(src_path, dst_path)
            
        try:
            javascript_spec = yaml.safe_load("\n".join(javascript_spec_lines))
        except:
            logger.error("Failed to load yaml javascript specification")
            return ""
            
        if not "src" in javascript_spec:
            logger.error("No src in javascript specification")
            return ""
            
        copy(javascript_spec["src"])
        if "extra" in javascript_spec:
            if isinstance(javascript_spec["extra"], str):
                copy(javascript_spec["extra"])
            else:
                for file_name in javascript_spec["extra"]:
                    copy(file_name)

        height = int(javascript_spec["height"]) if "height" in javascript_spec else None
        title = javascript_spec["title"] if "title" in javascript_spec else ""
        popup = "popup" in javascript_spec
        iframe = javascript.iframe(javascript_spec["src"], title=title, height=height, popup=popup)
        if popup:
            self._popup_id += 1
            return javascript.popup(msg("SHOW_APPLET"), iframe, self._popup_id)
        else:
            self.contains_iframes = True
            return iframe
    
    def read_and_process_md(self, md_file_name, section_path, level):
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
        
        # process content and join langs if necessary
        if markdown_magic_comments.contains_block(md, "lang"):
            lang_md = self._md_processor.process(section_path, md_file_path, md,
                                                 level=level, langs=self._langs)
            joined_md = self.join_languages(lang_md)
            md = joined_md
        else:
            md = self._md_processor.process(section_path, md_file_path, md, level=level, langs=None)

        # process included tasks
        md = markdown_magic_comments.replace_magic_comment_directives(md, "task", partial(self.include_task, section_path, level))

        # process embedded questions
        self.abc_question_id = 0
        md = markdown_magic_comments.replace_magic_comment_directives(md, "abc", self.process_abc)

        # process embedded javascript applets
        self.contains_iframes = False            
        md = markdown_magic_comments.replace_magic_comment_directives(md, "javascript", partial(self.process_javascript, section_path, md_file_path))
        if self.contains_iframes:
            md = javascript.resize_iframes(md)

        return title, md

    def create_toc(self, section_path, md_files, subsections, tasks):
        md = ""

        def link_target(path):
            target_path = self._md_serializer.path(path)
            return os.path.relpath(target_path, section_path)

        # process md files
        if md_files:
            md += "\n\n"
            for md_file in md_files:
                md_file_path = os.path.join(section_path, md_file)
                title = self._publication_repo.title(md_file_path)
                md += md_util.list_item(md_util.link(title, link_target(md_file_path)))
        
        # process subsections
        if subsections:
            md += "\n\n{}:\n\n".format(md_util.bold(msg("SECTIONS")))
            for subsection in subsections:
                index_md = os.path.join(subsection, "index.md")
                title = self._publication_repo.index_title(subsection)
                md += md_util.list_item(md_util.link(title, link_target(index_md)))
        if tasks:
            # process tasks
            md += "\n{}:\n\n".format(md_util.bold(msg("TASKS")))
            for task_id in tasks:
                task = self._task_repo.task(task_id)
                if not task:
                    logger.error(task_id, "not present in the task repository")
                    continue
                st_md_file = task.id() + "-st.md"
                task_dir = self.task_output_dir(task.id(), section_path)
                st_md_path = os.path.join(task_dir, st_md_file)
                md += md_util.list_item(md_util.link(task.title(), link_target(st_md_path)))
        return md
        
    # process the given publication source Markdown file
    def md_file(self, section_path, level, md_file_name, unnumbered=False):
        logger.info("Markdown file:", md_file_name)
        # read and process given markdown file
        title, md = self.read_and_process_md(md_file_name, section_path, level)
        # write the result to the file (converting to HTML if necessary)
        path = os.path.join(section_path, md_file_name)
        self._files.append({"type": "md_file", "path": path, "md": md, "title": title, "time": self._publication_repo.modification_time(path), "unnumbered": unnumbered})

    def section_start(self, section_path, level, md_files, subsections, tasks):
        logger.info("Section:", section_path)
        # process index.md for the section, if available        
        if not (self._publication_repo.contains_index(section_path)):
            logger.error(os.path.join(section_path, "index.md"), "does not exist in the publication repository")
            return
            
        # remember the title for this section
        title, _ = self._publication_repo.read_index(section_path)
        self._section_titles[section_path] = title

        # read and process the content
        title, md = self.read_and_process_md("index.md", section_path, level)
        # Make internal TOC for this section
        md += self.create_toc(section_path, md_files, subsections, tasks)
            
        # write the result to the file (converting to HTML if necessary)
        path = os.path.join(section_path, "index.md")
        self._files.append({"type": "section", "path": path, "md": md, "title": title, "time": self._publication_repo.modification_time(path)})


    def task_start(self, task):
        if not self._inline_task:
            logger.info("Task:", task.id())
        # task statement in Markdown format
        self._st_md = ""
        
    def task_title(self, task):
        # append the title of the task as a heading
        self._st_md += md_util.heading(task.title()) + "\n\n"
        
    def task_st(self, task):
        current_occurrence = self._extra_info["current_occurrence"]
        # warn if this is a repeated task that it already occurred in the publication
        if current_occurrence > 1:
            self._st_md += md_util.italic(msg("REPEATED_TASK")) + "\n\n"
            
        # append the statement content, read from the task repository
        self._st_md += task.statement() + "\n\n"
        # process obtained md
        self._st_md = self._md_processor.process(self.task_output_dir(task.id()), task.st_path(), self._st_md, langs=None)

    def task_io(self, task, description=True, examples=True):
        # read input-output specification
        if description and examples:
            md = task.io()
        elif description:
            md = task.io_description()
        elif examples:
            md = task.io_examples()
        # process and append io to the statement md
        self._st_md += self._md_processor.process(self.task_output_dir(task.id()), task.st_path(), task.io(), langs=None)

    def task_end_st(self, task):
        # append the link to the solution
        if not self._inline_task and self._standalone and "solution" in self._what_to_print:
            self._st_md += "\n\n{}\n\n".format(md_util.link(md_util.italic(msg("SOLUTION")), self._md_serializer.path(task.id() + "-sol.md")))
            
    def solution_title(self, task, statement_link=True):
        # solution title
        title = md_util.heading("{} - {}".format(task.title(), msg("SOLUTION")))
        # add link to the problem statement
        if statement_link and self._standalone:
            title += "\n\n" + md_util.link(md_util.italic(msg("STATEMENT")), self._md_serializer.path(task.id() + "-st.md"))
        return title
            
    def task_sol(self, task, sols):
        # process the solution content separately for each language
        sol_md = task.sol_content()
        # if some solutions are selected, then print only them
        if sols:
            sol_md = markdown_magic_comments.filter_by_key(sol_md, "sol", sols)


        # output paths
        task_dir = self.task_output_dir(task.id())
        md_file_path = task.sol_path()

        # process embedded javascript applets
        self.contains_iframes = False            
        sol_md = markdown_magic_comments.replace_magic_comment_directives(sol_md, "javascript", partial(self.process_javascript, task_dir, md_file_path))
        if self.contains_iframes:
            sol_md = javascript.resize_iframes(sol_md)
            
        self._sol_md = self._md_processor.process(task_dir, md_file_path, sol_md, langs=self._langs)

    def task_source_code(self, task, sol_name, sol_desc, lang, functions):
        # read the source code from the repository
        code = task.src_code(sol_name, lang)
        if not code:
            logger.error("missing code", task.id(), sol_name, lang)
            return
        # remove the magic comments (retain the whole source code)
        whole_code = source_code_magic_comments.remove_magic_comments(code)
        # process the magic comments
        code = source_code_magic_comments.process_magic_comments(code)
        # extract just specific functions
        if functions != None:
            code = code_parser.extract_funs(lang, code, functions)

        # surround code with Markdown markup for program source code
        whole_code = "\n" + md_util.md_source_code(whole_code, lang)
        code = "\n" + md_util.md_source_code(code, lang)

        if len(whole_code) != len(code):
            code = javascript.div_code_fragment(code)
            whole_code = javascript.div_whole_code(whole_code)
            code = javascript.add_fragment_whole_switcher(code + whole_code)

        # insert the code to appropriate place in the solution for its language
        if "solution" in self._what_to_print:
            self._sol_md[lang] = markdown_magic_comments.insert_content(self._sol_md[lang], "sol", sol_name, code, "code", "here")
        else:
            if not hasattr(self, "_sol_md"):
                self._sol_md = dict()
            self._sol_md[lang] = code

    def task_result(self, task):
        # join solutions in all languages and add switcher
        joined_sol_md = ""
        if "statement" in self._what_to_print:
            joined_sol_md += md_util.heading(msg("SOLUTION"), 2) + "\n"
        joined_sol_md += self.join_languages(self._sol_md)
        return self._st_md + "\n" + joined_sol_md
        
    def task_end(self, task):
        current_occurrence = self._extra_info["current_occurrence"]
        total_occurrences = self._extra_info["total_occurrences"]
        if current_occurrence < total_occurrences:
            # notify that the problem has other solutions
            md = md_util.italic(msg("ADDITIONAL_SOLUTIONS_EXIST"))
            self._st_md += md + "\n\n"

        if not self._inline_task:
            # write statement to file
            st_path = os.path.join(self.task_output_dir(task.id()), task.id() + "-st.md")
            self._files.append({"type": "task-st", "path": st_path, "md": self._st_md, "title": task.title(), "time": task.modification_time()})

            if "solution" in self._what_to_print:
                title = "{} - {}".format(task.title(), msg("SOLUTION"))
                if not self._join_langs:
                    # write solutions in every language into separate files (converting to HTML if necessary)
                    for lang in self._sol_md:
                        # add title
                        sol_md = self.solution_title(task) + "\n\n"
                        # add solution in the current language
                        sol_md += self._sol_md[lang]
                        # write solution to file (converting to HTML if necessary)
                        sol_path = os.path.join(self.task_output_dir(task.id()), "{}-{}-sol.md".format(task.id(), lang))
                        self._files.append({"type": "task-sol", "path": sol_path, "md": sol_md, "title": title, "time": task.modification_time()})
                else:
                    # add title
                    joined_sol_md = self.solution_title(task) + "\n\n"
                    # join solutions in all languages and add switcher
                    joined_sol_md += self.join_languages(self._sol_md)
                    # write the result into a single solution file (converting to HTML if necessary)
                    sol_path = os.path.join(self.task_output_dir(task.id()), "{}-sol.md".format(task.id()))
                    self._files.append({"type": "task-sol", "path": sol_path, "md": joined_sol_md, "title": title, "time": task.modification_time()})

            
    # action called at the end of publication processing 
    def end(self):
        # labels
        label = {}

        # number sections and collect section labels
        section_numbers = []
        for f in self._files:
            if (f["type"] == "section" or f["type"] == "md_file"):
                if f.get('unnumbered', False):
                    continue
                
                for heading in md_util.headings_in_md(f['md']):
                    if heading["unnumbered"]:
                        continue

                    title = heading["title"]
                    level = heading["level"]
                    while len(section_numbers) < level:
                        section_numbers.append(0)
                    while len(section_numbers) > level:
                        section_numbers.pop()
                    section_numbers[level-1] += 1
                    number = ".".join(map(str, section_numbers))
                    anchor = None
                    if "label" in heading:
                        (label_type, label_value) = md_util.analyze_label(heading["label"])
                        anchor = label_type + ":" + label_value
                        if label_type not in label:
                            label[label_type] = dict()
                        label[label_type][label_value] = number

                    if level <= self._section_number_depth:
                        f['md'] = md_util.change_heading(f['md'], title, level, md_util.heading(number + " " + title, level, anchor=anchor))

        # collect label depths
        specs = messages.div_specs
        depth = dict()
        for key in specs:
            if "html" in specs[key]:
                specs[key] = specs[key]["html"]
            if "counter" in specs[key]:
                depth[key] = specs[key]["counter"]
                        
        # collect other labels
        label_num = {}
        section_numbers = []
        for f in self._files:
            result = []
            for line in f["md"].split("\n"):
                if (f["type"] == "section" or f["type"] == "md_file") and not f.get('unnumbered', False):
                    for heading in md_util.headings_in_md(line):
                        print(heading)
                        level = heading["level"]
                        while len(section_numbers) < level:
                            section_numbers.append(0)
                        while len(section_numbers) > level:
                            section_numbers.pop()
                        section_numbers[level-1] += 1

                        # reset counters
                        for key in depth:
                            if level <= depth[key]:
                                if key in label_num:
                                    del label_num[key]
                
                for (key, value) in md_util.labels_in_md(line):
                    # label is already defined
                    if key in label and value in label[key]:
                        continue
                
                    if key not in label_num:
                        label_num[key] = 1
                    else:
                        label_num[key] = label_num[key] + 1
                    if key not in label:
                        label[key] = dict()

                    number = ".".join(map(str, section_numbers[0:depth.get(key, 0)]))
                    if number:
                        label[key][value] = number + "." + str(label_num[key])
                    else:
                        label[key][value] = str(label_num[key])

                    line = md_util.remove_label(line, key, value)
                result.append(line)
            f["md"] = "\n".join(result)

        # resolve references
        for f in self._files:
            for (key, value) in md_util.references_in_md(f["md"]):
                if (key not in label) or (value not in label[key]):
                    logger.warn("Undefined reference:", md_util.reference(key, value))
                else:
                    f["md"] = md_util.replace_reference(f["md"], key, value, str(label[key][value]))


        # add previous/next links
        sections = [(i, f['path']) for (i, f) in enumerate(self._files) if f["type"] == "section" or f["type"] == "md_file"]
        for i in range(len(sections)):
            div = "\n\n<div class='prev-next-links'>\n"
            if i > 0:
                (prev_i, prev_path) = sections[i-1]
                (curr_i, curr_path) = sections[i]
                target_path = re.sub(".md$", ".html", os.path.relpath(prev_path, os.path.dirname(curr_path)))
                div += "<div class='prev-link'>" + md_util.link("<<" + msg("PREVIOUS"), target_path) + "</div>\n"
            if i < len(sections) - 1:
                (curr_i, curr_path) = sections[i]
                (next_i, next_path) = sections[i+1]
                target_path = re.sub(".md$", ".html", os.path.relpath(next_path, os.path.dirname(curr_path)))
                div += "<div class='next-link'>" + md_util.link(">>" + msg("NEXT"), target_path) + "</div>\n"
            div += "</div>\n"
            self._files[curr_i]['md'] += div

        # do the serialization
        for f in self._files:
            logger.info("Writing:", f["title"])
            self._md_serializer.write(f["path"], f["md"], title=f["title"], md_time=f.get("time", None))

