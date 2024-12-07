from .publication_visitor import PublicationVisitor
from .task_visitor import TaskVisitor
from . import logger
import json
import os

class TestReporter:
    def __init__(self, task, report_json_file):
        self._task = task
        self._report_json_file = report_json_file
        if os.path.isfile(self._report_json_file):
            self._report = json.load(open(self._report_json_file, "r"))
        else:
            self._report = dict()
            self._report["id"] = task.id()

    def should_test(self, sol, lang):
        if not os.path.isfile(self._report_json_file):
            return True
        src = self._task.src_file_path(sol, lang)
        if not os.path.isfile(src):
            logger.error(f"Source file {src} does not exist")
            return False
        if os.path.getmtime(self._report_json_file) < os.path.getmtime(src):
            return True
        if not sol in self._report:
            return True
        if not lang in self._report[sol]:
            return True
        return False

    def report_testcase(self, sol, lang, testcase_number, testcase, result, time):
        if not sol in self._report:
            self._report[sol] = dict()
        if not lang in self._report[sol]:
            self._report[sol][lang] = dict()
        if not "testcases" in self._report[sol][lang]:
            self._report[sol][lang]["testcases"] = dict()
        self._report[sol][lang]["testcases"][testcase] = (result, time)

    def report_solution(self, sol, lang, statuses, max_time):
        if not sol in self._report:
            self._report[sol] = dict()
        if not lang in self._report[sol]:
            self._report[sol][lang] = dict()
        self._report[sol][lang]["status"] = statuses
        self._report[sol][lang]["max_time"] = max_time

    def end(self):
        print(json.dumps(self._report, indent=4), file=open(self._report_json_file, "w"))


class PublicationVisitorTest(PublicationVisitor, TaskVisitor):
    def __init__(self, yaml_specification, task_repo, force=False, timeout=2):
        PublicationVisitor.__init__(self, yaml_specification, task_repo, None)
        TaskVisitor.__init__(self)
        self._yaml_specification = yaml_specification
        self._force = force
        self._timeout = timeout
            
    def task_sol(self, task, sols):
        reporter = TestReporter(task, os.path.join(task.build_dir(), "test_report.json"))
        task.test_all(langs=self._yaml_specification.langs(), sols=sols, force=self._force, timeout=self._timeout, reporter=reporter)
