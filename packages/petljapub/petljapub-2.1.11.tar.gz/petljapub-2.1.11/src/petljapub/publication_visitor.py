import os, sys

from .task_visitor import TaskVisitor
from .yaml_specification import YAMLSpecificationVisitor, YAMLSpecification
from .task_repository import TaskRepository
from .publication_repository import PublicationRepository
from .md_util import PandocMarkdown

from . import logger

# Specialization of YAMLSpecification visitor that processes each task
# by the given visitor for a task in publication
class PublicationVisitor(YAMLSpecificationVisitor):
    def __init__(self, yaml_specification, task_repo, publication_repo, task_visitor=None, langs=[]):
        self._yaml_specification = yaml_specification
        self._task_repo = task_repo
        self._publication_repo = publication_repo
        self._task_visitor = task_visitor if task_visitor else self
        self._langs = langs
        self._task_occurrence = dict()

    # delegates task processing to the task visitor, counting task occurrences
    def task(self, section_path, level, task_id, task_spec):
        task = self._task_repo.task(task_id)
        if not task:
            logger.error(task_id, "not available in the task repository")
            return
        
        # issue a warning for all incomplete tasks
        if not task.is_complete():
            logger.warn("incomplete task", task.id(), verbosity=4)

        # increment occurrence number for the current task
        self._task_occurrence[task.id()] = self._task_occurrence.get(task.id(), 0) + 1

        # delegate processing to the task in publication visitor
        extra_info = {
                        "yaml": self._yaml_specification,
                        "section_path": section_path,
                        "level": level,
                        "current_occurrence": self._task_occurrence[task.id()],
                        "total_occurrences": len(self._yaml_specification.sections_containing_task(task.id()))
                     }
        return self._task_visitor.visit_task(task, self._langs, task_spec, extra_info)

