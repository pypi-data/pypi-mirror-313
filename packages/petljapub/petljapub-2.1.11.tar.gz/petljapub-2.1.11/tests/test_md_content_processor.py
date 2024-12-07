import unittest
from src.petljapub.md_content_processor import OutputOrganizerSingleDir, OutputOrganizerHierarchy, LinkProcessorRaw, LinkProcessorPublication, LinkProcessorNoLinks, LinkProcessorTex, LinkProcessorHTML, ImageProcessor, ReferenceProcessor, MDContentProcessor
from src.petljapub.yaml_specification import YAMLSpecification
from src.petljapub.task_repository import TaskRepository
from src.petljapub.publication_repository import PublicationRepository

class TestOutputOrganizer(unittest.TestCase):
    def test_single_dir(self):
        organizer = OutputOrganizerSingleDir("_build")
        self.assertEqual(organizer.output_dir(""), "_build")
        self.assertEqual(organizer.output_dir("task"), "_build")

    def test_hierarchy(self):
        organizer = OutputOrganizerHierarchy("_build")
        self.assertEqual(organizer.output_dir(""), "_build/")
        self.assertEqual(organizer.output_dir("01 Formule/trening"), "_build/01 Formule/trening")
        
class TestLinkFormater(unittest.TestCase):
    def setUp(self):
        self.yaml_specification = YAMLSpecification("tests/data/pub.yaml")
        self.task_repo = TaskRepository("tests/data")
        self.publication_repo = PublicationRepository("tests/data")

    def test_raw(self):
        md_original = "[](trening)"
        formater = LinkProcessorRaw()
        self.assertEqual(formater.process("", "ponoc-st.md", md_original),
                         "[*trening*]")
        
    def test_no_links(self):
        md_original = "[](trening)"
        formater = LinkProcessorNoLinks(self.yaml_specification, self.task_repo, self.publication_repo)
        self.assertEqual(formater.process("", "ponoc-st.md", md_original),
                         "*Тренинг*")
        self.assertEqual(formater.process("01 Aritmetika/01 Formule/02 celobrojno_deljenje", "ponoc-st.md", md_original),
                         "*Тренинг*")

    def test_tex(self):
        md_original = "[](trening)"
        formater = LinkProcessorTex(self.yaml_specification, self.task_repo, self.publication_repo)
        self.assertEqual(formater.process("", "ponoc-st.md", md_original),
                         "[Тренинг](#trening)")
        self.assertEqual(formater.process("01 Aritmetika/01 Formule/02 celobrojno_deljenje", "ponoc-st.md", md_original),
                         "[Тренинг](#trening)")

    def test_html(self):
        md_original = "[](trening)"
        organizer = OutputOrganizerHierarchy()
        formater = LinkProcessorHTML(self.yaml_specification, self.task_repo, self.publication_repo, organizer)
        
        self.assertEqual(formater.process("", "ponoc-st.md", md_original),
                         "[Тренинг](01 Formule/01 geometrija/trening/trening-st.html)")
        self.assertEqual(formater.process("01 Formule/02 celobrojno_deljenje/01 ponoc", "ponoc-st.md", md_original),
                         "[Тренинг](../../01 geometrija/trening/trening-st.html)")

class TestLinkProcessor(unittest.TestCase):
    def test_exclude_not_in_publication(self):
        yaml_specification = YAMLSpecification("tests/data/pub.yaml")
        task_repo = TaskRepository("data")
        publication_repo = PublicationRepository("data")
        formater = LinkProcessorPublication(yaml_specification, task_repo, publication_repo)
        md = """
<!--- span:link --->
Линк [Тренинг](trening).
<!--- span:end --->
<!--- span:link --->
Линк [Непознат](nepoznat).
<!--- span:end --->
<!--- span:link --->
Један линк је познат [Тренинг](trening), а један је [Непознат](nepoznat).
<!--- span:end --->
"""
        md_expected = """
<!--- span:link --->
Линк [Тренинг](trening).
<!--- span:end --->
"""
        self.assertEqual(formater.exclude_links_not_in_publication(md), md_expected)

        
class MockImageProcessor(ImageProcessor):
    def __init__(self):
        self._commands = []
        
    def process_image(self, src_image_path, section_path, relative_dir):
        self._commands.append((src_image_path, section_path, relative_dir))

    def commands(self):
        return self._commands
    
        
class TestMDContentProcessor(unittest.TestCase):
    def test(self):
        md_original = """# Heading

This is ordinary test.
<!--- div:exclude --->
This should be excluded!
<!--- div:end --->

Here is an image

 ![Image](image.jpeg)

Another one

 ![Another image](images/another.png){ width=8cm }

The end.
"""

        md_expected = """## Heading

This is ordinary test.

Here is an image

 ![Image](image.jpeg)

Another one

 ![Another image](images/another.png){ width=8cm }

The end.
"""
        image_processor = MockImageProcessor()
        reference_processor = ReferenceProcessor()
        
        processor = MDContentProcessor(None, image_processor, reference_processor, "html")
        self.assertEqual(md_expected, processor.process("01 trening", "trening", md_original, ["cpp"], 2)["cpp"])
        image_commands = image_processor.commands()
        self.assertEqual(len(image_commands), 2)
        (src, dst, rel_dir) = image_commands[0]
        self.assertEqual(src, "image.jpeg")
        self.assertEqual(dst, "01 trening")
        self.assertEqual(rel_dir, "")
        (src, dst, rel_dir) = image_commands[1]
        self.assertEqual(src, "images/another.png")
        self.assertEqual(dst, "01 trening")
        self.assertEqual(rel_dir, "images")

