from .translit import cyr_to_lat
from . import logger
from .config import read_config

en = {
    "TASK"        : "Task",
    "TASKS"       : "Tasks",
    "STATEMENT"   : "Statement",
    "SOLUTION"    : "Solution",
    "INPUT"       : "Input",
    "OUTPUT"      : "Output",
    "INPUT_DESC"  : "Input description",
    "OUTPUT_DESC" : "Output description",
    "EXPLANATION" : "Explanation",
    "EXAMPLE"     : "Example",
    "SECTIONS"    : "Sections",
    "REPEATED_TASK" : "This task is repeated.",
    "TRY_TO_SOLVE"  : "Try to solve the task using techniques described in this section.",
    "LOOKUP_TASK"   : "Show the task statement.",
    "ADDITIONAL_SOLUTIONS" : "See different solutions of this task.",
    "ADDITIONAL_SOLUTIONS_EXIST" : "This task has multiple solutions.",
    "FIGURE" : "Figure",
    "CHECK": "Check",
    "QUESTION": "Question",
    "ANSWERS": "Answers",
    "SHOW_APPLET": "Show applet",
    "TABLE": "Table",
    "WHOLE_CODE": "Show complete code",
    "CODE_FRAGMENT": "Show code fragments",
    "PREVIOUS": "Previous",
    "NEXT": "Next",
    "ALGORITHM": "Algorithm",
    "COMPLETE": "Complete"
}

srCyrl = {
    "TASK"         : "Задатак",
    "TASKS"        : "Задаци",
    "STATEMENT"    : "Поставка",
    "SOLUTION"     : "Решење",
    "INPUT"        : "Улаз",
    "OUTPUT"       : "Излаз",
    "INPUT_DESC"   : "Опис улаза",
    "OUTPUT_DESC"  : "Опис излаза",
    "EXPLANATION"  : "Објашњење",
    "SECTIONS"     : "Поглавља",
    "EXAMPLE"      : "Пример",
    "REPEATED_TASK" : "Овај задатак је поновљен у циљу увежбавања различитих техника решавања.",
    "TRY_TO_SOLVE"  : "Покушај да задатак урадиш коришћењем техника које се излажу у овом поглављу.",
    "LOOKUP_TASK"   : "Види текст задатка.",
    "ADDITIONAL_SOLUTIONS" : "Види другачија решења овог задатка.",
    "ADDITIONAL_SOLUTIONS_EXIST" : "Овај задатак има и другачија решења у делу збирке који следи.",
    "FIGURE" : "Слика",
    "CHECK": "Провери",
    "QUESTION": "Питање",
    "ANSWERS": "Одговори",
    "SHOW_APPLET": "Прикажи аплет",
    "TABLE": "Табела",
    "WHOLE_CODE": "Прикажи комплетан кôд",
    "CODE_FRAGMENT": "Прикажи фрагменте кода",
    "PREVIOUS": "Претходно",
    "NEXT": "Следеће",
    "ALGORITHM": "Алгоритам",
    "COMPLETE": "Комплетан"
}

srLatn = {key : cyr_to_lat(value) for key, value in srCyrl.items()}

languages = {
    "en" : en,
    "sr" : srLatn,
    "serbian": srLatn,
    "sr-Latn": srLatn,
    "serbianc": srCyrl,
    "sr-Cyrl": srCyrl
}

language_names = {
    "en" : "English",
    "sr-Latn" : "Serbian (latin)",
    "sr-Cyrl" : "Serbian (cyrillic)"
}

dictionary = en        

def set_language(language):
    global lang, dictionary
    lang = language
    logger.info("Using lanugage:", language, verbosity=4)
    dictionary = get_dictionary(language)

def choose_language():
    while True:
        print(f"Select language (1-{len(language_names)}):")
        for i, lang in enumerate(language_names):
            print(f"({i+1}) [{lang}] {language_names[lang]}")
        n = int(input())
        if 1 <= n and n <= len(language_names):
            break;
    i, lang = list(enumerate(language_names))[n-1]
    logger.info(f"Selected: [{lang}] {language_names[lang]}")
    return lang

def get_dictionary(language):
    if language in languages:
        return languages[language]
    else:
        logger.warn("Unkonwn language", lang, " - using default language en")
        return languages["en"]

def msg(key, language=None):
    global dictionary
    if language == None:
        return dictionary.get(key, "")
    else:
        return get_dictionary(language).get(key, "")


# TODO: move out from messages.py

# Specification for special divs formating (e.g., some divs in the
# input code should get titles). These are usually specified in the
# yaml file.
div_specs = dict()
# Some divs are going to be convrted to some specified LaTeX environments
div_latex_environments = dict()
def set_div_specs(specs):
    global div_specs
    global div_latex_environments
    div_specs = specs
    # extract divs that should be converted to LaTeX environments
    for div in div_specs:
        specs = div_specs[div]
        if isinstance(specs, dict):
            if "tex" in specs:
                specs = specs["tex"]
                if "environment" in specs:
                    div_latex_environments[div] = [specs["environment"]]
    
set_language(read_config("lang") or "en")
