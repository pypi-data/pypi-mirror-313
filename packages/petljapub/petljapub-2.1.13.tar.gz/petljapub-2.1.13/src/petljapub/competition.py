import re
import os
import glob

import petlja_api
from .task import Task
from . import logger
from . import md_util
from .petlja_account import get_petlja_session

class Competition:
    def __init__(self, dir, name="", description="", alias="", prefix=""):
        self.dir = dir
        self.name = name
        self.description = description
        self.alias = alias
        self.id = None
        self.prefix = prefix

        # if params are not specifed they can be read from a config file
        index = os.path.join(self.dir, 'index.md')
        if os.path.exists(index):
            _, metadata = md_util.parse_front_matter(index)
            self.name = self.name or metadata.get("name", "")
            self.description = self.description or metadata.get("description", "")
            self.prefix = self.prefix or metadata.get("prefix", "")
            self.alias = self.alias or metadata.get("alias", "")
            self.id = metadata.get('id', "")

        if not self.alias:
            self.alias = Task.extract_id_from_dir(self.dir)
        if not self.id:
            self.id = Task.extract_id_from_dir(self.dir)

        self.prefix = Competition.fix_format(self.prefix)
        self.alias = Competition.fix_format(self.alias)
        self.id = Competition.fix_format(self.id)

    @staticmethod
    def is_competition_dir(dir):
        return any(Task.is_task_dir(d) for d in os.listdir(dir))

    @staticmethod
    def fix_format(text):
        # ensure alias and id are in the correct format
        text = text.replace(' ', '-')
        text = text.replace('_', '-')
        text = re.sub(r"[^a-zA-Z0-9\-]", "", text).lower() 
        return text

    def task_prefix(self):
        return self.prefix
    
    def petlja_publish(self):
        try:
            sess = get_petlja_session()
        except Exception as e:
            logger.error(e)
            return None

        update = False
        name = self.name if self.name else self.id
        try:
            competition_id = petlja_api.create_competition(sess, name, self.alias, self.description)
            logger.info(f"Competition {self.alias} successfully created")
        except ValueError:
            update = True
            logger.info("Competition already created, updating problems")
            competition_id = petlja_api.get_competition_id(sess, self.alias)
            
        logger.info("Competition id: ", competition_id, verbosity=4)

        existing_problems = petlja_api.get_added_problem_ids(sess, competition_id)
        
        problem_names = []
        for problem_dir in sorted(glob.glob(os.path.join(self.dir, '**'), recursive=True)):
            if not Task.is_task(problem_dir):
                continue
            task = Task(problem_dir)
            try:
                problem_id = task.petlja_publish(sess, self.prefix)
                if problem_id in existing_problems:
                    petlja_api.remove_problem(sess, competition_id, problem_id)
                petlja_api.add_problem(sess, competition_id, problem_id)
                problem_names.append(task.title())
                if task.has_scoring():
                    petlja_api.upload_scoring(sess, competition_id, problem_id, task.scoring_path())
                    logger.info("Added", os.path.basename(task.scoring_path()))
                logger.info("Problem", task.id(), "added to the competition")
            except ValueError:
                logger.error(f"Error in publishing task {task.id()} - skipped")
                continue

        
        if update:
            logger.info(f'Competition "{self.alias}" updated')
        else:
            logger.info(f'Created competiton "{self.alias}" with following problems: {problem_names}')
        
