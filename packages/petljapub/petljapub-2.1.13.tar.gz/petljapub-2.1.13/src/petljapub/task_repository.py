import sys, os, glob
import re
import yaml
import pathlib
from enum import Enum

from .md_util import parse_front_matter
from .util import dump_file, read_file

from .task import Task
from . import logger

# access a repository of problems
#  - read data from problem specifications (statements, solutions, souce code)
#  - compile solutions, generate testcases, run and check validity

# The central functionality of the class is to return a Task object for the task
# specified by a unique task identifier (the method task(task_id)).

class TaskRepository:
    # initialize repository stored in the given root_dir
    def __init__(self, root_dir, normalize_md=lambda x: x, translit=lambda x: x):
        self._root_dir = root_dir
        self._normalize_md = normalize_md
        self._translit = translit
        self._tasks = self.__collect_tasks(root_dir)

    # check if the directory contains a task with the given ID
    def contains_task(self, task_id):
        return task_id in self._tasks

    # return the task with the given ID
    def task(self, task_id):
        return self._tasks.get(task_id, None)

    # return the collection of all tasks
    def tasks(self):
        return self._tasks

    # recursively traverse all subdirectories of the source directory,
    # find all task specifications and build a mapping from task
    # identifiers to directories
    def __collect_tasks(self, src_dir):
        tasks = {}
        # recursive enumeration of all subdirectories
        for path in sorted(pathlib.Path(src_dir).rglob('*'), key=os.path.abspath):
            # check if the current path is a task specification 
            if path.name.endswith('-st.md'):
                st_file = path
                # get the directory where it is stored  
                task_dir = os.path.dirname(st_file)
                # extract the task ID from the directory name
                task_id = Task.extract_id_from_dir(task_dir)
                # add the task to the mapping 
                if task_id in tasks:
                    logger.error("duplicate task identifier", task_id, "\n",
                                 tasks[task_id].dir(), "\n",
                                 task_dir)
                else:
                    tasks[task_id] = Task(task_dir, self._normalize_md, self._translit)
        return tasks
    
if __name__ == '__main__':
    import argparse, sys
    parser = argparse.ArgumentParser(description='Publication repository')
    parser.add_argument('root_dir', type=str,
                        help='Root directory of the publication')
    args = parser.parse_args()
    repo = TaskRepository(args.root_dir)
    for line in sys.stdin:
        line = line.strip()
        print(repo.task(line).title())
