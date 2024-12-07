from .yaml_specification import YAMLSpecification, YAMLSpecificationVisitor
from .task_repository import TaskRepository
from . import logger

class YAMLSpecificationVisitorStats(YAMLSpecificationVisitor):
    def __init__(self, yaml, task_repo):
        self._yaml = yaml
        self._task_repo = task_repo
        self.tasks = dict()

    def task(self, path, level, task_id, task_spec):
        if not (task_id in self.tasks):
            self.tasks[task_id] = set()

        if task_spec and "solutions" in task_spec:
            solutions = task_spec["solutions"]
        else:
            task = self._task_repo.task(task_id)
            if task:
                solutions = list(map(lambda x: x["name"], self._task_repo.task(task_id).solutions()))
            else:
                logger.error("Task not in repository:", task_id)
                solutions = []
            
        for sol in solutions:
            self.tasks[task_id].add(sol)

    def end(self):
        total_tasks = 0
        total_solutions = 0
        for task_id, solutions in self.tasks.items():
            print(task_id, ":", ", ".join(list(solutions)))
            total_tasks += 1
            total_solutions += len(solutions)
        print("---------------------------")
        print("Total tasks:", total_tasks)
        print("Total solutions:", total_solutions)

        print("---------------------------")
        print("Tasks not in yaml:")
        for task_id in self._task_repo.tasks():
            if not(task_id in self.tasks):
                print(task_id)

if __name__ == '__main__':
    import os, sys
    import argparse
    from . import logger
    
    parser = argparse.ArgumentParser(description='Read and analyze YAML specification')
    parser.add_argument('yaml', type=str,
                        help='YAML file')
    parser.add_argument('--tasks-dir', type=str, default=None,
                        help='Directory where tasks are stored')

    args = parser.parse_args()

    tasks_dir = args.tasks_dir
    if not tasks_dir:
        tasks_dir = os.path.dirname(args.yaml)

    if not os.path.isfile(args.yaml):
        logger.error("YAML file does not exist")
        sys.exit(-1)

    if tasks_dir and not os.path.isdir(tasks_dir):
        logger.error(tasks_dir, "is not a directory")
        sys.exit(-1)
        
    yaml = YAMLSpecification(args.yaml)
    repo = TaskRepository(tasks_dir)
    yaml.traverse(YAMLSpecificationVisitorStats(yaml, repo))
