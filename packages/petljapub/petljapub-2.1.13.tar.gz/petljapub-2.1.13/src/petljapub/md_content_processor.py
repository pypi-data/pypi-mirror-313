import os

from . import markdown_magic_comments
from . import md_util
from . import yaml_specification
from . import logger

################################################################################
# Base class for all output organizers

# Output organizers map the logical hierarchy given by the yaml file
# (and physical hierarchy of the input files) to the physical
# hierarchy of output files
class OutputOrganizer:
    def __init__(self):
        pass

    def output_dir(section_path):
        pass

# All output files are put into a single directory
class OutputOrganizerSingleDir(OutputOrganizer):
    def __init__(self, output_dir):
        self._output_dir = output_dir

    def output_dir(self, section_path):
        return self._output_dir
    

# Output hiearchy matches the one given by the YAML file
class OutputOrganizerHierarchy(OutputOrganizer):
    def __init__(self, base_dir="."):
        self._base_dir = base_dir
    
    def output_dir(self, section_path):
        return os.path.join(self._base_dir, section_path)

################################################################################
# Base class for all image processors

# process all images in a given md file    
class ImageProcessor:
    # process all images in the md content that is stored in an md
    # file specified by its section_path and md_file_path
    def process(self, section_path, md_file_path, md):
        # process all images
        for (title, image) in md_util.images_in_md(md):
            logger.info("Copy image:", image, verbosity=4)
            input_dir = os.path.dirname(md_file_path)
            src_image_path = os.path.join(input_dir, image)
            self.process_image(src_image_path, section_path, os.path.dirname(image))
        return md

    # process image given by the src_image path that is contained in a
    # file in the given section path, where relative_dir is the path
    # to the image specified within the md file
    def process_image(self, src_image_path, section_path, relative_dir):
        pass
    
# image are copied as they are processed
class ImageProcessorCopy(ImageProcessor):
    def __init__(self, writer, output_organizer):
        self._writer = writer
        self._output_organizer = output_organizer

    def process_image(self, src_image_path, section_path, relative_dir):
        image = os.path.basename(src_image_path)
        dst_dir = self._output_organizer.output_dir(section_path)
        dst_image_path = os.path.join(dst_dir, relative_dir, image)
        self._writer.copy_file(src_image_path, dst_image_path)

################################################################################
# Base class for all link processors
        
# process all links in a given md file    
class LinkProcessor:
    # process all links in the given markdown content stored in a file
    # given by the current_dir and current_file (in the input hierarchy)
    def process(self, current_dir, current_file, md):
        pass

# instead of titles, show link paths
class LinkProcessorRaw(LinkProcessor):
    def process(self, current_dir, current_file, md):
        for (link_title, link_id) in md_util.links_in_md(md):
            md = md_util.replace_link(md, link_title, link_id, "[{}]".format(md_util.italic(link_id)))
        return md

# process all links with respect to the given publication
class LinkProcessorPublication(LinkProcessor):
    def __init__(self, yaml_specification, task_repo, publication_repo):
        self._yaml_specification = yaml_specification
        self._task_repo = task_repo
        self._publication_repo = publication_repo

    # when links are marked by <!--- span:link ---> exclude all links
    # that are not present in the current publication
    def exclude_links_not_in_publication(self, md):
        def do_exclude(lines):
            links_in_pub = True
            for (_, link_id) in md_util.links_in_md("".join(lines)):
                if  not self._yaml_specification.contains_task(link_id) and not self._yaml_specification.contains_section(link_id):
                    links_in_pub = False
                    break
            return lines if links_in_pub else []

        md = markdown_magic_comments.process_by_key_value(md, "span", "link",
                                                          do_exclude)
        return md
    
    def process(self, section_path, md_file_path, md):
        md = self.exclude_links_not_in_publication(md)
        for (link_title, link_id) in md_util.links_in_md(md):
            if link_title or ("/" in link_id):
                # links should only contain task or section ids
                # raw links are kept unchanged
                logger.warn("raw link", link_title, link_id, " is left unchanged")
            elif self._task_repo.contains_task(link_id):
                # find the title of the linked task
                task_title = self._task_repo.task(link_id).title()
                # find the sections that it occurrs in
                task_sections = self._yaml_specification.sections_containing_task(link_id)
                if task_sections:
                    # assume that links points to the first task occurrence
                    task_section = task_sections[0]
                    md = self.format_task_link(md, link_title, link_id, task_section, task_title, section_path)
                else:
                    # warn if the task exists, does not occurr in the publication, and remove link
                    # (only print the linked task title in italic)
                    md = md_util.replace_link(md, link_title, link_id, md_util.italic(task_title))
                    logger.warn(section_path, md_file_path, "- link to task", link_id, "not in publication")
            elif self._publication_repo.contains_index(link_id):
                # find the title of the linked section
                link_section_title = self._publication_repo.index_title(link_id)
                link_section_path = self._yaml_specification.section_path(link_id)
                if link_section_path != None:
                    md = self.format_section_link(md, link_title, link_id, link_section_title, link_section_path, section_path)
                    pass
                else:
                    # warn if the task exists, does not occurr in the publication, and remove link
                    # (only print the linked section title in italic)
                    md = md_util.replace_link(md, link_title, link_id, md_util.italic(link_section_title))
                    logger.warn(section_path, md_file_path, " - link to section", link_id, "not in publication")
            elif self._publication_repo.contains_md_file(os.path.join(section_path, link_id)):
                logger.warn("Linking md files is not supported:", link_id)
            else:
                logger.error("non-existent link", link_id, "in", md_file_path)
        return md

    # format link to the given task
    def format_task_link(self, md, link_title, link_id, task_section, task_title, section_path):
        pass

    # format link to the given section
    def format_section_link(self, md, link_title, link_id, section_title, section_path, current_dir):
        pass
    
    
class LinkProcessorNoLinks(LinkProcessorPublication):
    def __init__(self, yaml_specification, task_repo, publication_repo):
        super().__init__(yaml_specification, task_repo, publication_repo)

    def format_task_link(self, md, link_title, link_id, task_section, task_title, current_dir):
        return md_util.replace_link(md, link_title, link_id, md_util.italic(task_title))
    
class LinkProcessorTex(LinkProcessorPublication):
    def __init__(self, yaml_specification, task_repo, publication_repo):
        super().__init__(yaml_specification, task_repo, publication_repo)

    def format_task_link(self, md, link_title, link_id, task_section, task_title, current_dir):
        return md_util.change_link(md, link_title, link_id, task_title, "#" + link_id)

    def format_section_link(self, md, link_title, link_id, section_title, section_path, current_dir):
        return md_util.change_link(md, link_title, link_id, section_title, "#" + section_title.lower().replace(" ", "-"))
    

class LinkProcessorHTML(LinkProcessorPublication):
    def __init__(self, yaml_specification, task_repo, publication_repo, output_organizer):
        super().__init__(yaml_specification, task_repo, publication_repo)
        self._output_organizer = output_organizer

    def task_output_dir(self, task_id, task_section):
        task = self._task_repo.task(task_id)
        return self._output_organizer.output_dir(os.path.join(task_section, task.id()))
    
    def format_task_link(self, md, link_title, link_id, task_section, task_title, current_dir):
        link_target = os.path.join(self.task_output_dir(link_id, task_section), link_id + "-st.html")
        link_path = os.path.relpath(link_target, current_dir)
        return md_util.change_link(md, link_title, link_id, task_title, link_path)

    def format_section_link(self, md, link_title, link_id, section_title, section_path, current_dir):
        link_path = os.path.relpath(section_path, current_dir)
        return md_util.change_link(md, link_title, link_id, section_title, link_path)

################################################################################
# Base class for all reference processors

# process all labels (e.g., {#lemma:first}) and references in the md file (e.g., @lemma:first)
class ReferenceProcessor:
    def __init__(self):
        pass

    def process(self, md):
        return md

class ReferenceProcessorTex(ReferenceProcessor):
    def  __init__(self):
        pass

    def process(self, md):
        for (key, value) in md_util.labels_in_md(md):
            md = md_util.replace_label(md, key, value, "\\label{" + key + ":" + value + "}")
            
        for (key, value) in md_util.references_in_md(md):
            md = md_util.replace_reference(md, key, value, "\\ref{" + key + ":" + value + "}")
            
        return md

class ReferenceProcessorHTML(ReferenceProcessor):
    def  __init__(self):
        pass

    def process(self, md):
        return md


################################################################################
    
# process the content of a given md file
class MDContentProcessor:
    def __init__(self, link_processor, image_processor, reference_processor, target):
        self._link_processor = link_processor
        self._image_processor = image_processor
        self._reference_processor = reference_processor
        self._target = target

    # process the content md that is stored in a file specified by section_path and md_file_path (given in the input hierarchy)
    def process(self, section_path, md_file_path, md, langs=None, level=None, unnumbered=False, unlisted=False):
        logger.info("Processing:", section_path, md_file_path, langs, verbosity=5)
        # the name of the file
        md_file_name = os.path.basename(md_file_path)
        
        # exclude divs marks for exclusion
        md = markdown_magic_comments.exclude(md, "div", ["exclude"])
        # format remaining divs
        md = markdown_magic_comments.format_divs(md, self._target)

        # degrade headings
        if level != None:
            md = md_util.degrade_headings(md, level, unnumbered=unnumbered, unlisted=unlisted)
            
        # process links
        if self._link_processor != None:
            md = self._link_processor.process(section_path, md_file_path, md)
        
        # process images
        if self._image_processor != None:
            md = self._image_processor.process(section_path, md_file_path, md)

        # process references
        if self._reference_processor != None:
            md = self._reference_processor.process(md)

        # process languages
        if langs == None:
            return md
        else:
            lang_md = {}
            for lang in langs:
                lang_md[lang] = markdown_magic_comments.exclude_all_except(md, "lang", langs)
            return lang_md
