import unittest
from src.petljapub.md_util import *

class TestMDUtil(unittest.TestCase):

    def test_parse_front_matter(self):
        content, header = parse_front_matter('tests/data/01 Formule/01 geometrija/01 trening/trening-st.md')
        self.assertEqual(content[0:9], "Спортиста")
        self.assertEqual(header['title'], "Тренинг")
        
    def test_md_source_code(self):
        self.assertEqual(md_source_code("#include <iostream>", "cpp"), "~~~cpp\n#include <iostream>~~~\n")
        self.assertEqual(md_source_code("using System;", "cs"), "~~~cs\nusing System;~~~\n")
        self.assertEqual(md_source_code("import math", "py"), "~~~python\nimport math~~~\n")
        self.assertEqual(md_source_code("#include <stdio.h>", "c"), "~~~c\n#include <stdio.h>~~~\n")

    def test_link(self):
        self.assertEqual(link("Наслов", "putanja"), "[Наслов](putanja)")

    def links_md(self):
        return """# Наслов
Ovde je [линк](link) на средини реда.
[Линк](link) на почетку реда.
На крају реда је [линк](link)
Линк [који има више речи](putanja).
Линк [садржи "наводнике"](putanja).
Линк [садржи (заграде)](putanja).
Линк [наслов](/slozena/putanja).
Покушај [линка у
више редова](putanja).
Ово је ![слика](slika).
Ево је још једна ![слика са (мало) дужим описом](/slozena/putanja/slika.jpg).
"""

    def test_links_in_md(self):
        links = links_in_md(self.links_md())
        self.assertEqual(len(links), 7)
        self.assertEqual(links[0], ("линк", "link"))
        self.assertEqual(links[1], ("Линк", "link"))
        self.assertEqual(links[2], ("линк", "link"))
        self.assertEqual(links[3], ("који има више речи", "putanja"))
        self.assertEqual(links[4], ("садржи \"наводнике\"", "putanja"))
        self.assertEqual(links[5], ("садржи (заграде)", "putanja"))
        self.assertEqual(links[6], ("наслов", "/slozena/putanja"))

    def test_images_in_md(self):
        images = images_in_md(self.links_md())
        self.assertEqual(len(images), 2)
        self.assertEqual(images[0], ("слика", "slika"))
        self.assertEqual(images[1], ("слика са (мало) дужим описом", "/slozena/putanja/slika.jpg"))

    def test_change_link(self):
        md = "Ovde je [линк](link) на средини реда."
        self.assertEqual(change_link(md, "линк", "link", "веза", "veza"), "Ovde je [веза](veza) на средини реда.")

    def test_replace_link(self):
        md = "Ovde je [линк](link) на средини реда."
        self.assertEqual(replace_link(md, "линк", "link", "*веза*"), "Ovde je *веза* на средини реда.")

    def test_format(self):
        self.assertEqual(bold("abc"), "**abc**")
        self.assertEqual(italic("abc"), "*abc*")
        
    def test_heading(self):
        self.assertEqual(heading("Наслов", 2), "## Наслов")
        self.assertEqual(heading("Наслов", 2, unnumbered=True, unlisted=True), "## Наслов {.unnumbered .unlisted}")
        self.assertEqual(heading("Наслов", 2, anchor="here"), "## Наслов {#here}")
        self.assertEqual(heading("Наслов", 2, unnumbered=True, anchor="here"), "## Наслов {#here .unnumbered}")

    def test_headings_in_md(self):
        md = """# Ово је главни наслов
## ово је поднаслов
~~~cpp
#include <iostream>
# include <string>
using namespace std;
~~~
# Ово је опет главни наслов
"""
        self.assertEqual(len(headings_in_md(md)), 3)
        
        
    def test_analyze_heading(self):
        heading = analyze_heading("## Наслов")
        self.assertEqual(heading["title"], "Наслов")
        self.assertEqual(heading["level"], 2)
        heading = analyze_heading("Наслов")
        self.assertIsNone(heading["title"])
        self.assertIsNone(heading["level"])
        heading = analyze_heading("## Наслов поглавља {#sec:naslov}")
        self.assertEqual(heading["title"], "Наслов поглавља")
        self.assertEqual(heading["level"], 2)
        self.assertEqual(heading["label"], "{#sec:naslov}")
        heading = analyze_heading("## Без броја {#sec:bezbroja .unnumbered}")
        self.assertEqual(heading["title"], "Без броја")
        self.assertEqual(heading["level"], 2)
        self.assertEqual(heading["label"], "{#sec:bezbroja}")
        self.assertTrue(heading["unnumbered"])
        heading = analyze_heading("# ABC {#abc .unlisted}")
        self.assertEqual(heading["title"], "ABC")
        self.assertEqual(heading["level"], 1)
        self.assertEqual(heading["label"], "{#sec:abc}")
        self.assertFalse(heading["unnumbered"])
        self.assertTrue(heading["unlisted"])
        

    def test_heading_levels(self):
        md = """# Ово је главни наслов
## ово је поднаслов
~~~cpp
#include <iostream>
# include <string>
using namespace std;
~~~
# Ово је опет главни наслов
## ово је поднаслов
### ово је подподнаслов
## ово је поднаслов
# Још један главни наслов"""
        self.assertEqual(min_heading_level(md), 1)
        self.assertEqual(max_heading_level(md), 3)

        mdd = """### Ово је главни наслов
#### ово је поднаслов
~~~cpp
#include <iostream>
# include <string>
using namespace std;
~~~
### Ово је опет главни наслов
#### ово је поднаслов
##### ово је подподнаслов
#### ово је поднаслов
### Још један главни наслов"""        

        self.assertEqual(degrade_headings(md, 3), mdd)

    def test_remove_headings(self):
        self.assertEqual(remove_headings("## Ово је наслов", 2, "*"), "*Ово је наслов*")
        self.assertEqual(remove_headings("## Ово је наслов\nЗдраво\n# Главни наслов\n## Joш један наслов\nЗдраво", 2, "**"),
                         "**Ово је наслов**\nЗдраво\n# Главни наслов\n**Joш један наслов**\nЗдраво")

    def test_keep_with_next(self):
        md = """*Задатак*

Ово је текст."""

        self.assertEqual(keep_with_next(md, "*Задатак*"), "*Задатак*: Ово је текст.")

        md = """*Задатак*

  - Ово је текст."""

        self.assertEqual(keep_with_next(md, "*Задатак*"), "*Задатак*:\n\n  - Ово је текст.")
        

    def test_pandoc_dollars(self):
        md = """Dvostruki dolari $$x^2$$.
Jednostruki dolari $x^2$.

$$x^2$$

i

$x^2 + 
3x - 2$

i

$x^2 + 3y$ {#eq:xy}

i

$
x_3 + 4
$   {#eq:x34}

$x_5$
"""
        md_fixed = """Dvostruki dolari $x^2$.
Jednostruki dolari $x^2$.

$$x^2$$

i

$$x^2 + 
3x - 2$$

i

$$x^2 + 3y$$ {#eq:xy}

i

$$
x_3 + 4
$$   {#eq:x34}

$$x_5$$

"""
        self.assertEqual(PandocMarkdown.fix_latex_dollars(md), md_fixed)
        

    def testLabelsAndReferences(self):
        md = """# Naslov {#sec:naslov}

U poglavlju @sec:naslov videli smo svašta.
Evo reference sa tačkom na kraju @sec:naslov.

{#lemma:prva} {#lemma_druga}

@lemma:prva
@lemma_druga
"""

        labels = labels_in_md(md)
        self.assertEqual(len(labels), 2)
        self.assertEqual(labels[0], ("sec", "naslov"))
        self.assertEqual(labels[1], ("lemma", "prva"))
        references = references_in_md(md)
        self.assertEqual(len(references), 3)
        self.assertEqual(references[0], ("sec", "naslov"))
        self.assertEqual(references[1], ("sec", "naslov"))
        self.assertEqual(references[2], ("lemma", "prva"))
        self.assertEqual(label("sec", "intro"), "{#sec:intro}")
        self.assertEqual(reference("sec", "intro"), "@sec:intro")
        lbl = analyze_label("{#sec:intro}")
        self.assertEqual(lbl[0], "sec")
        self.assertEqual(lbl[1], "intro")
        self.assertEqual(replace_reference("@lemma:abc", "lemma", "abc", "\\ref{abc}"), "\\ref{abc}")

