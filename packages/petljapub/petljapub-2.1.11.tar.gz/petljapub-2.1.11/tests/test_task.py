import unittest
import os
from src.petljapub.task import Task
from src.petljapub.messages import set_language

class TestTask(unittest.TestCase):
    def setUp(self):
        set_language("sr-Cyrl")
        self.task = Task("tests/data/01 Formule/01 geometrija/01 trening")

        self.st = """Спортиста се на почетку тренинга загрева тако што трчи по ивицама
правоугаоног терена дужине $$d$$ и ширине $$s$$. Написати програм
којим се одређује колико метара претрчи спортиста док једном обиђе
терен.

![Спортиста](trening.jpg)"""

        self.input_desc = """У првој линији стандардног улаза се налази целобројна вредност $$d$$
($$0 < d \\leq 100$$), а у следећој линији целобројна вредност $$s$$
($$0 < s \\leq 100$$) које редом представљају дужину и ширину терена
изражену у метрима."""

        self.output_desc = """Цео број метара које претрчи спортиста док једном обиђе терен."""

        self.example = """## Пример

### Улаз

~~~
50 
25
~~~

### Излаз

~~~
150
~~~
"""

        self.st_content = self.st + "\n\n## Улаз\n\n" + self.input_desc + "\n\n## Излаз\n\n" + self.output_desc + "\n\n" + self.example
    
    def test_is_task_dir(self):
        self.assertTrue(Task.is_task_dir("01 trening"))
        self.assertTrue(Task.is_task_dir("24_trening"))
        self.assertTrue(Task.is_task_dir("53-trening"))
        self.assertTrue(Task.is_task_dir("05 sportski trening"))
        self.assertTrue(Task.is_task_dir("72_sportski_trening"))
        self.assertTrue(Task.is_task_dir("14_3d_grafika"))
        self.assertFalse(Task.is_task_dir("01trening"))
        self.assertFalse(Task.is_task_dir("1 trening"))

        self.assertEqual(Task.extract_id_from_dir("01 trening"), "trening")
        self.assertEqual(Task.extract_id_from_dir("32_trening"), "trening")
        self.assertEqual(Task.extract_id_from_dir("05 sportski trening"), "sportski trening")
        
    def test_basic_info(self):
        base_dir = "tests/data/01 Formule/01 geometrija"
        self.task.extract_example_testcases()
        self.task.generate_testcases()
        self.assertEqual(self.task.id(), "trening")
        self.assertEqual(self.task.dir(), os.path.join(base_dir, "01 trening"))
        self.assertEqual(self.task.status(), "KOMPLETAN")
        self.assertEqual(self.task.title(), "Тренинг")
        self.assertEqual(self.task.timelimit(), 1.0)
        self.assertEqual(len(self.task.solutions()), 1)
        self.assertEqual(self.task.solution("ex0")["name"], "ex0")
        self.assertEqual(self.task.expected_status("ex0"), "OK")
        self.assertEqual(set(self.task.langs()), {"py", "cs", "cpp"})
        self.assertEqual(self.task.statement(), self.st)
        self.assertEqual(self.task.input_description(), self.input_desc)
        self.assertEqual(self.task.output_description(), self.output_desc)
        self.assertEqual(self.task.st_content(), self.st_content)
        
        self.assertEqual(self.task.number_of_example_testcases(), 1)
        self.assertEqual(self.task.example_testcases(), [os.path.join(self.task.example_testcases_dir(), "trening_01.in")])
        self.assertEqual(self.task.number_of_generated_testcases(), 10)
        self.assertEqual(self.task.generated_testcases(), [os.path.join(self.task.generated_testcases_dir(), "trening_{:02d}.in".format(i)) for i in range(1, 11)])
        self.assertEqual(self.task.number_of_crafted_testcases(), 0)

        self.assertEqual(self.task.st_path(), os.path.join(self.task.dir(), "trening-st.md"))
        self.assertEqual(self.task.sol_path(), os.path.join(self.task.dir(), "trening-sol.md"))
        self.assertEqual(self.task.src_file_name("ex0", "py"), "trening.py")
        self.assertEqual(self.task.src_file_path("ex0", "py"), os.path.join(self.task.dir(), "trening.py"))
        self.assertEqual(self.task.src_file_name("ex1", "cpp"), "trening-ex1.cpp")
        self.assertEqual(self.task.src_file_path("ex1", "cpp"), os.path.join(self.task.dir(), "trening-ex1.cpp"))
        self.assertEqual(self.task.build_dir(), os.path.join(self.task.dir(), "_build"))
        self.assertEqual(self.task.exe_file_name("ex0", "cpp"), "trening.exe")
        self.assertEqual(self.task.exe_file_path("ex0", "cpp"), os.path.join(self.task.dir(), "_build", "trening.exe"))
        self.assertEqual(self.task.exe_file_name("ex1", "cpp"), "trening-ex1.exe")
        self.assertEqual(self.task.exe_file_path("ex1", "cpp"), os.path.join(self.task.dir(), "_build", "trening-ex1.exe"))
        self.assertEqual(self.task.exe_file_name("ex1", "cs"), "trening-ex1-cs.exe")
        self.assertEqual(self.task.exe_file_path("ex1", "cs"), os.path.join(self.task.dir(), "_build", "trening-ex1-cs.exe"))
        self.assertEqual(self.task.exe_file_name("ex1", "py"), "trening-ex1.py")
        self.assertEqual(self.task.exe_file_path("ex1", "py"), os.path.join(self.task.dir(), "_build", "trening-ex1.py"))
        self.assertEqual(self.task.tgen_src_file_name("cpp"), "trening-tgen.cpp")
        self.assertEqual(self.task.tgen_src_path("cpp"), os.path.abspath(os.path.join(self.task.dir(), "trening-tgen.cpp")))
        self.assertEqual(self.task.tgen_exe_file_name(), "trening-tgen.exe")
        self.assertEqual(self.task.tgen_exe_path(), os.path.join(self.task.dir(), "_build", "trening-tgen.exe"))
        self.assertEqual(self.task.testcases_dir(), os.path.join(self.task.dir(), "_build", "testcases"))
        self.assertEqual(self.task.generated_testcases_dir(), os.path.join(self.task.dir(), "_build", "testcases", "generated"))
        self.assertEqual(self.task.example_testcases_dir(), os.path.join(self.task.dir(), "_build", "testcases", "example"))
        self.assertEqual(self.task.crafted_testcases_dir(), os.path.join(self.task.dir(), "_build", "testcases", "crafted"))
        self.assertEqual(self.task.generated_testcase_path(4), os.path.join(self.task.dir(), "_build", "testcases", "generated", "trening_04.in"))
        self.assertEqual(self.task.example_testcase_path(2), os.path.join(self.task.dir(), "_build", "testcases", "example", "trening_02.in"))
        self.assertEqual(self.task.crafted_testcase_path(7), os.path.join(self.task.dir(), "_build", "testcases", "crafted", "trening_07.in"))
        self.assertFalse(self.task.has_checker())
        self.assertEqual(self.task.checker_src_file_name(), "trening-check.cpp")
        self.assertEqual(self.task.checker_exe_file_name(), "trening-check.exe")
        self.assertEqual(self.task.checker_src_path(), os.path.join(self.task.dir(), "trening-check.cpp"))
        self.assertEqual(self.task.checker_exe_path(), os.path.join(self.task.dir(), "_build", "trening-check.exe"))
