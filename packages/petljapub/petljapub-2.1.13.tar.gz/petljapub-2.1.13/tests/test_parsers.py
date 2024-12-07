import unittest
from src.petljapub import cpp_parser
from src.petljapub import py_parser
from src.petljapub import code_parser

class TestParsers(unittest.TestCase):
    def test_cpp_is_fun(self):
        line = "vector<int> formirajDrvo(const vector<int>& a) {"
        self.assertTrue(cpp_parser.is_fun_declaration(line, "formirajDrvo"));
        line = "vector<int> formirajDrvo(const vector<int>& a"
        self.assertFalse(cpp_parser.is_fun_declaration(line, "formirajDrvo"));
        self.assertTrue(cpp_parser.is_partial_fun_declaration(line));
        line = "void formirajDrvo(const vector<int>& a, vector<int>& drvo,\nsize_t k, size_t x, size_t y) {"
        self.assertTrue(cpp_parser.is_fun_declaration(line, "formirajDrvo"));
        

    def test_cpp_is_line_comment(self):
        line = "// komentar"
        self.assertTrue(cpp_parser.is_line_comment(line))
        
    def test_cpp_extract_fun(self):
        gorivo = """int gorivo(int potrosnja, int rastojanje) {
   if (potrosnja * rastojanje % 100 == 0)
      return (potrosnja * rastojanje) / 100;
   else
      return (potrosnja * rastojanje) / 100 + 1;
}"""

        main = """int main()
{
   int rastojanje;
   cin >> rastojanje;
   int potrosnja1, potrosnja2, potrosnja3;
   cin >> potrosnja1 >> potrosnja2 >> potrosnja3;
   cout << gorivo(potrosnja1, rastojanje) +
   gorivo(potrosnja2, rastojanje) +
   gorivo(potrosnja3, rastojanje) << endl;
   return 0;
}"""
        
        cpp = """#include <iostream>
using namespace std;

{}

{}
""".format(gorivo, main)
        
        self.assertTrue(cpp_parser.is_fun_declaration("int gorivo(int potrosnja, int rastojanje) {", "gorivo"))
        self.assertTrue(cpp_parser.is_fun_declaration("int main()", "main"))
        self.assertFalse(cpp_parser.is_fun_declaration("cout << gorivo(potrosnja1, rastojanje)", "gorivo"))
        
        self.assertEqual(cpp_parser.extract_fun(cpp, "gorivo"), gorivo + "\n\n")
        self.assertEqual(cpp_parser.extract_fun(cpp, "main"), main + "\n\n")
        self.assertEqual(cpp_parser.extract_fun(cpp, "test"), "")
        self.assertEqual(code_parser.extract_fun("cpp", cpp, "gorivo"), gorivo + "\n\n")

    def test_py_extract_fun(self):
        gorivo = """def gorivo(potrosnja, rastojanje):
  if potrosnja * rastojanje % 100 == 0:
      return (potrosnja * rastojanje) // 100
  else:
      return (potrosnja * rastojanje) // 100 + 1"""

        py = """{}

rastojanje = int(input())
potrosnja1 = int(input())
potrosnja2 = int(input())
potrosnja3 = int(input())
print(gorivo(potrosnja1, rastojanje) +
      gorivo(potrosnja2, rastojanje) + 
      gorivo(potrosnja3, rastojanje))""".format(gorivo)

        self.assertTrue(py_parser.is_fun_declaration("def gorivo(potrosnja, rastojanje):", "gorivo"))
        self.assertTrue(py_parser.is_fun_declaration("  def gorivo(  potrosnja, rastojanje) :  ", "gorivo"))
        self.assertTrue(py_parser.is_fun_declaration("def gorivo(potrosnja,rastojanje):", "gorivo"))

        self.assertEqual(py_parser.extract_fun(py, "gorivo"), gorivo)

        self.assertEqual(code_parser.extract_fun("py", py, "gorivo"), gorivo)
