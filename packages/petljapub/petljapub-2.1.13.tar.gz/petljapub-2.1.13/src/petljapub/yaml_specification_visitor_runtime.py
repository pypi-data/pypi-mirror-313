import sys, os, glob
import math
import tempfile
import json
import time
import statistics

from .yaml_specification import YAMLSpecification, YAMLSpecificationVisitor
from .task_repository import TaskRepository
from .task import Task

# supported programming languages
langs = ["cs", "cpp"]

# append all timings for a given task to a given csv file
def append_time_to_csv(task, csv_file):
    time_json = time_json_path(task)
    # skip all tasks for which there are no time measurments
    if not os.path.isfile(time_json):
        return
    # load data from the json file
    time_json = json.load(open(time_json, "r"))
    # process all solutions
    for sol in time_json["times"]:
        # and all languages
        for lang in time_json["times"][sol]:
            # store relevant data in a row and append it to the csv file
            row = []
            row.append("\"" + time_json["dir"] + "\"")
            row.append(time_json["id"])
            row.append(sol)
            row.append(lang)
            for time in time_json["times"][sol][lang]:
                if not time.endswith("_TO"):
                    time_str = str(time_json["times"][sol][lang][time])
                    if time + "_TO" in time_json["times"][sol][lang]:
                        time_str += "TO"
                    row.append(time_str)
            # append row to csv_file
            csv = open(csv_file, "a")
            print(",".join(row), file=csv)
            csv.close()


# Auxiliary visitor class for processing yaml specification

def measure_all_runtimes(task, params, task_spec=None, petlja=False, session=None):
    force = params.get("force", False)
    repeat = params.get("repeat", 1)
    timelimit = params.get("timelimit", None)
    langs = params.get("langs", [])
    solutions = []
    if task_spec:
        solutions=task_spec.get("solutions", [])
    if not petlja:
        task.measure_all_runtimes(force=force, repeat=repeat, timelimit=timelimit, langs=langs, solutions=solutions)
    else:
        task.petlja_measure_all_runtimes(force=force, timelimit=timelimit, langs=langs, solutions=solutions, session=session)
    

# measure runtime for each task specified in the yaml specification
class RuntimeTaskVisitor(YAMLSpecificationVisitor):
    def __init__(self, repo, params):
        self._repo = repo
        self._params = params
    
    def task(self, path, level, task_id, task_spec):
        task = self._repo.task(task_id)
        measure_all_runtimes(task, self._params, task_spec)
        
# determine timeout for each task specified in the yaml specification
class CalibrateTaskVisitor(YAMLSpecificationVisitor):
    def __init__(self, repo, params):
        self._repo = repo
        self._params = params
    
    def task(self, path, level, task_id, task_spec):
        task = self._repo.task(task_id)
        task.calibrate()

# append time data to a csv file for each task specified in the yaml specification
class TimeCSVVisitor(YAMLSpecificationVisitor):
    def __init__(self, repo, csv_file, params):
        self._repo = repo
        self._csv_file = csv_file
        self._params = params
    
    def task(self, path, level, task_id, task_spec):
        task = self._repo.task(task_id)
        measure_all_runtimes(task, self._params)
        append_time_to_csv(task, self._csv_file)

# measure runtime for each task specified in the yaml specification on the sever petlja.org
class PetljaRuntimeTaskVisitor(YAMLSpecificationVisitor):
    def __init__(self, repo, params, session):
        self._repo = repo
        self._params = params
        self._session = session
    
    def task(self, path, level, task_id, task_spec):
        task = self._repo.task(task_id)
        measure_all_runtimes(task, self._params, task_spec, petlja=True, session=self._session)
        
            
# Main program
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Measure solution runtimes')
    parser.add_argument('task_spec', type=str,
                        help='task specification (either a task base directory or a yaml file with a list of tasks)')
    parser.add_argument('-t', '--timelimit', type=float, default=2,
                        help='timelimit for each testcase in seconds')
    parser.add_argument('-r', '--repeat', type=int, default=3,
                        help='nuber of testcase repetitions (for better accuracy)')
    parser.add_argument('-f', '--force', action='store_true',
                        help='force execution of solutions')
    parser.add_argument('-csv', '--csv', type=str, 
                        help='generate csv of all timings')
    parser.add_argument('-c', '--calibrate', action='store_true',
                        help='calibrate time limit')

    args = parser.parse_args()

    params = {
        "force": args.force,
        "timelimit": args.timelimit,
        "repeat": args.repeat
    }

    if args.task_spec == '.':
        args.task_spec = os.getcwd()
    
    if args.task_spec.endswith('.yml') or args.task_spec.endswith('.yaml'):
        if not os.path.isfile(args.task_spec):
            sys.exit("Error reading YAML file")
        yaml = YAMLSpecification(args.task_spec)
        repo = TaskRepository(os.path.dirname(args.task_spec))
        if args.csv != None:
            yaml.traverse(TimeCSVVisitor(repo, args.csv, params))
        elif args.calibrate:
            yaml.traverse(CalibrateVisitor(repo, params))
        else:
            yaml.traverse(RuntimeTaskVisitor(repo, params))
    else:
        args.task_spec = args.task_spec.rstrip(os.path.sep)
        task = Task(args.task_spec)
        print(json.dumps(measure_all_runtimes(task, params), indent=4))
