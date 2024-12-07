import os
import json
import datetime
import xml.etree.ElementTree as ET
from xml.dom import minidom

from .publication_visitor_html import PublicationVisitorHTML
from .util import read_file
from . import logger

# Extend HTML publication visitor with additional functionallity
# related to the Petlja foundation packaging
class PublicationVisitorHTMLPetljaPackage(PublicationVisitorHTML):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def start(self):
        super().start()
        self.write_index_json()

    def end(self):
        self._writer.write("section-titles.json", json.dumps(self._section_titles, indent=4, ensure_ascii=False))
        super().end()
        

    def task_end(self, task):
        super().task_end(task)
        
        task_dir = os.path.join("metadata", self.task_output_dir(task.id()))

        # Write metadata about the task to XML files
        self._writer.write(os.path.join(task_dir, "ProblemAttributes.xml"),
                           self.attributes_XML(task))
        self._writer.write(os.path.join(task_dir, "ProblemContent.xml"),
                           self.content_XML(task))

        # Copy all testcases to the output directory for the task
        if self._generate_tests:
            task.clear_testcases()
        
        if task.number_of_generated_testcases() + task.number_of_crafted_testcases() == 0:
            task.prepare_all_testcases()

        def write_testcase(testcase):
            testcase_content = read_file(testcase)
            if testcase_content is None:
                logger.error(testcase, " - invalid file")
                return
            testcases_dir = os.path.join(task_dir, "TestCases")
            if os.path.basename(os.path.dirname(testcase)) == "example":
                testcase_path = os.path.join(testcases_dir, "_" + os.path.basename(testcase))
            else:
                testcase_path = os.path.join(testcases_dir, os.path.basename(testcase))
            self._writer.write(testcase_path, testcase_content)
        
        for testcase in task.all_testcases():
            write_testcase(testcase)
            write_testcase(testcase[:-2] + "out")

        # Copy custom checker if it exists
        if task.has_checker():
            self._writer.copy_file(task.checker_src_path(), os.path.join(task_dir, task.checker_src_file_name()))
        
    def write_index_json(self):
        yaml = self._yaml_specification
        index = dict()
        index["Alias"] = yaml.alias()
        index["Title"] = yaml.title()
        index["ImageUrl"] = yaml.thumb()
        index["Description"] = yaml.short_description()
        index["Path"] = "index.html"
        index["Sections"] = []
        self._writer.write("index.json", json.dumps(index, indent=4, ensure_ascii=False))
        desc = yaml.full_description()
        if desc:
            _, desc_content = self._publication_repo.read_md_file(desc)
            self._md_serializer.write(desc, desc_content)
        else:
            logger.warn("No full description file specified")

    def attributes_XML(self, task):
        metadata = task.metadata()
        
        xml = dict()
        xml["Type"] = metadata.get("type", 0)
        xml["Title"] = metadata["title"]
        xml["Timelimit"] = round(task.timelimit())
        xml["Memlimit"] = metadata.get("memlimit", 64)
        xml["Owner"] = metadata.get("owner", "")
        xml["Origin"] = metadata.get("origin", "")
        xml["StatusUpdated"] = metadata.get("status-od", datetime.date.today().strftime("%Y-%m-%d"))
        root = ET.Element("ProblemAttributes")
        root.set("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
        root.set("xmlns:xsd", "http://www.w3.org/2001/XMLSchema")
        for (key, value) in xml.items():
            child = ET.SubElement(root, key)
            child.text = str(value)
        xml_str = minidom.parseString(ET.tostring(root)).toprettyxml(indent="   ")
        return xml_str

    def content_XML(self, task):
        def dict_to_XML(dct, root):
            for (key, value) in dct.items():
                child = ET.SubElement(root, key)
                if isinstance(value, str):
                    child.text = str(value)
                else:
                    dict_to_XML_string(value, child)
        
        xml = dict()
        xml["ProblemStatement"] = (os.path.sep + os.path.join(self.task_output_dir(task.id()), task.id() + "-st.md")).replace("/", "\\")
        xml["Input"] = ""
        xml["Output"] = ""
        xml["ExampleInput"] = ""
        xml["ExampleOutput"] = ""
        xml["ProblemSolution"] = (os.path.sep + os.path.join(self.task_output_dir(task.id()), task.id() + "-sol.md")).replace("/", "\\") if self._task_spec.get("print", "full") == "full" else ""
        xml["SolutionPublic"] = "true" if self._task_spec.get("print", "full") == "full" else "false"

        if "extra-info" in self._task_spec:
            xml["ExtraInfo"] = self._task_spec["extra-info"]
        
        root = ET.Element("Data")
        root.set("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
        root.set("xmlns:xsd", "http://www.w3.org/2001/XMLSchema")
        problem = ET.SubElement(root, "ProblemCardPart")
        for (key, value) in xml.items():
            child = ET.SubElement(problem, key)
            child.text = str(value)
        xml_str = minidom.parseString(ET.tostring(root)).toprettyxml(indent="   ")
        return xml_str
