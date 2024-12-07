import unittest
from src.petljapub.publication_repository import PublicationRepository

class TestPublicationRepository(unittest.TestCase):
    def setUp(self):
        self.repo = PublicationRepository("tests/data/")

    def test_extract_key(self):
        self.assertEqual(PublicationRepository.extract_key("00 stack/01 implementation/file.md"), "implementation")
        self.assertEqual(PublicationRepository.extract_key("00 stack/01 implementation"), "implementation")
    
    def test_resolve_path(self):
        # existing path
        self.assertEqual(self.repo.resolve_path("01 Formule/01 geometrija"), "tests/data/01 Formule/01 geometrija")
        self.assertEqual(self.repo.resolve_path("01 Formule/formule.md"), "tests/data/01 Formule/formule.md")
        # existing dir
        self.assertEqual(self.repo.resolve_path("01 Formule/01 geometrija/01 trening/trening-st.md"), "tests/data/01 Formule/01 geometrija/01 trening/trening-st.md")
        self.assertEqual(self.repo.resolve_path("01 Formule/01 geometrija/01 trening/error.md"), "tests/data/01 Formule/01 geometrija/01 trening/error.md")
        # relative path
        self.assertEqual(self.repo.resolve_path("01 geometrija"), "tests/data/01 Formule/01 geometrija")
        self.assertEqual(self.repo.resolve_path("geometrija"), "tests/data/01 Formule/01 geometrija")

    def test_index_md(self):
        self.assertTrue(self.repo.contains_index("geometrija"))
        self.assertEqual(self.repo.index_md("geometrija"), "tests/data/01 Formule/01 geometrija/index.md")
        metadata, _ = self.repo.read_index("geometrija")
        self.assertEqual(metadata["title"], "Геометријске формуле")

    def test_read_md_file(self):
        self.assertEqual(self.repo.title("01 Formule/formule.md"), "Списак формула")
        metadata, content = self.repo.read_md_file("01 Formule/formule.md")
        self.assertEqual(metadata["title"], "Списак формула")
