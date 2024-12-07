import unittest
import yaml
from src.petljapub.markdown_magic_comments import *

class TestMarkdownMagicComments(unittest.TestCase):
    def test_is_magic_comment(self):
        self.assertTrue(is_magic_comment("div", "proof", "<!--- div:proof --->"))
        self.assertTrue(is_magic_comment("div", "proof", " \n  <!--- div:proof --->  \n "))
        self.assertFalse(is_magic_comment("div", "proof", "Comment:\n<!--- div:proof --->"))
        self.assertFalse(is_magic_comment("div", "proof", "<!--- div:complexity --->"))
        self.assertTrue(is_magic_comment_end("div", "<!--- div:end --->"))
        self.assertFalse(is_magic_comment_end("span", "<!--- div:end --->"))
        self.assertFalse(is_magic_comment_end("div", "<!--- div:proof --->"))
        self.assertTrue(is_magic_comment_start("div", "<!--- div:proof --->"))
        self.assertFalse(is_magic_comment_start("span", "<!--- div:proof --->"))
        self.assertFalse(is_magic_comment_start("div", "<!--- div:end --->"))

    def test_is_magic_comment_directive(self):
        self.assertTrue(is_magic_comment_directive_start("task", "<!--- task"))
        self.assertTrue(is_magic_comment_directive_start("task", "<!--- task   "))
        self.assertTrue(is_magic_comment_directive_start("task", "<!---   task   "))
        self.assertTrue(is_magic_comment_directive_start("task", "<!---task "))
        self.assertFalse(is_magic_comment_directive_start("task", "<!---task start"))
        self.assertFalse(is_magic_comment_directive_start("task", "<!--- subtask"))
        self.assertFalse(is_magic_comment_directive_end("<!--- subtask"))

    def test_collect_magic_comment_directives(self):
        md = """<!--- task
name: test
print: full
--->"""
        self.assertEqual(collect_magic_comment_directives(md, "task"), ["name: test\nprint: full"])

        md = """This is some text. 

<!--- task
name: test
print: full
--->

Another task.

<!--- task
name: second
print: full
--->

ABC

<!---abc
question: Pitanje?
--->
"""
        self.assertEqual(collect_magic_comment_directives(md, "task"), ["name: test\nprint: full", "name: second\nprint: full"])

        self.assertEqual(replace_magic_comment_directives(md, "task"), "This is some text. \n\n\n\nAnother task.\n\n\n\nABC\n\n<!---abc\nquestion: Pitanje?\n--->\n")

        def f_join(lines):
            return "\n".join(lines)
        
        self.assertEqual(replace_magic_comment_directives(md, "task", f_join), "This is some text. \n\nname: test\nprint: full\n\nAnother task.\n\nname: second\nprint: full\n\nABC\n\n<!---abc\nquestion: Pitanje?\n--->\n")

        def f_yaml(lines):
            specs = yaml.safe_load("\n".join(lines))
            return specs["name"]

        self.assertEqual(replace_magic_comment_directives(md, "task", f_yaml), "This is some text. \n\ntest\n\nAnother task.\n\nsecond\n\nABC\n\n<!---abc\nquestion: Pitanje?\n--->\n")
        
        
    def test_magic_comment_key_value(self):
        comment = magic_comment_key_value("<!--- div:proof --->")
        self.assertEqual(comment["key"], "div")
        self.assertEqual(comment["value"], "proof")
        comment = magic_comment_key_value("  \n <!--- div:proof --->  ")
        self.assertEqual(comment["key"], "div")
        self.assertEqual(comment["value"], "proof")
        comment = magic_comment_key_value("  \n <!--- div:lemma prva --->  ")
        self.assertEqual(comment["key"], "div")
        self.assertEqual(comment["value"], "lemma")
        self.assertEqual(comment["label"], "prva")
        comment = magic_comment_key_value("  \n <!--- div:lemma prva [naslov] --->  ")
        self.assertEqual(comment["key"], "div")
        self.assertEqual(comment["value"], "lemma")
        self.assertEqual(comment["label"], "prva")
        self.assertEqual(comment["title"], "naslov")
        comment = magic_comment_key_value("  \n <!--- div:lemma [ovo je dugacak naslov] --->  ")
        self.assertEqual(comment["key"], "div")
        self.assertEqual(comment["value"], "lemma")
        self.assertEqual(comment["title"], "ovo je dugacak naslov")

    def test_contains_block(self):
        md = """# Title
<!--- div:proof --->
Proof
<!--- div:end --->
"""
        self.assertTrue(contains_block(md, "div"))
        self.assertFalse(contains_block(md, "lang"))

    def test_insert_content(self):
        md = """# Title
<!--- sol:ex0 --->
First line.
<!--- code:here --->
Second line.
<!--- sol:end --->
The end."""

        expected_md = """# Title
<!--- sol:ex0 --->
First line.
<!--- code:here --->
Second line.
INSERT
<!--- sol:end --->
The end."""

        self.assertEqual(insert_content(md, "sol", "ex0", "INSERT"), expected_md)

        expected_md = """# Title
<!--- sol:ex0 --->
First line.
INSERT
Second line.
<!--- sol:end --->
The end."""

        self.assertEqual(insert_content(md, "sol", "ex0", "INSERT", "code", "here"), expected_md)

        expected_md = """# Title
<!--- sol:ex0 --->
First line.
<!--- code:here --->
Second line.
<!--- sol:end --->
The end.
INSERT"""

        self.assertEqual(insert_content(md, "sol", "ex1", "INSERT"), expected_md)
        

    def test_exclude(self):

        md = """# Title

<!--- div:exclude --->
Text 1.
<!--- div:end --->

<!--- div:keep --->
Text 2.
<!--- div:end --->

The end."""

        md_expected = """# Title


<!--- div:keep --->
Text 2.
<!--- div:end --->

The end."""
        
        self.assertEqual(exclude(md, "div", ["exclude"]), md_expected)
        self.assertEqual(exclude_all_except(md, "div", ["keep"]), md_expected)

    def test_format_divs(self):

        md = """# Title

<!--- div:proof --->
Text 1.
<!--- div:end --->

<!--- div:complexity --->
Text 2.
<!--- div:end --->

<!--- div:other --->
Text 3.
$$a + b = c$$
<!--- div:end --->

The end."""

        md_expected = """# Title

<div class="proof">
**Proof.**
Text 1.
</div>

<div class="complexity">
*Complexity analysis:*
Text 2.
</div>

<div class="other">
Text 3.
$$a + b = c$$


</div>

The end."""

        div_titles = {"proof": "**Proof.**", "complexity": "*Complexity analysis:*"}
        self.assertEqual(format_divs(md, "html", div_titles), md_expected)

