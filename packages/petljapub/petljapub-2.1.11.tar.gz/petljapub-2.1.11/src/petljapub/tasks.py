import os, sys, glob, shutil, getpass, pathlib
import re
import json, yaml
from datetime import date
from string import Template
import tempfile

from invoke import task

from petljapub import logger

from petljapub.translit import lat_to_cyr, cyr_to_lat, lat_to_cyr_md
from petljapub.util import read_file, write_to_file, replace_in_file
from petljapub.md_util import PandocMarkdown, parse_front_matter
from petljapub.task import Task
from petljapub.competition import Competition
from petljapub.task_repository import TaskRepository
from petljapub.publication_repository import PublicationRepository
from petljapub.yaml_specification import YAMLSpecification, YAMLSpecificationVisitor, YAMLSpecificationVisitorLog
from petljapub.yaml_specification_visitor_stats import YAMLSpecificationVisitorStats
from petljapub.yaml_specification_visitor_runtime import RuntimeTaskVisitor, CalibrateTaskVisitor, PetljaRuntimeTaskVisitor
from petljapub.task_visitor_html import TaskVisitorHTML
from petljapub.publication_visitor_testing import PublicationVisitorTest
from petljapub.publication_visitor_html import PublicationVisitorHTML
from petljapub.publication_visitor_petlja import PublicationVisitorHTMLPetljaPackage
from petljapub.publication_visitor_tex import PublicationVisitorTeX
from petljapub.compilation import tgen_dir
from petljapub.plot_times import plot_times
from petljapub.configure_compilers import configure_compilers
from petljapub.config import read_config, add_config
from petljapub.messages import choose_language
from petljapub.petlja_account import set_petlja_login_info, get_petlja_session, remove_petlja_login_info

sys.stdout.reconfigure(encoding='utf-8')
# enable terminal colors on windows
if sys.platform == "win32":
    try:
        os.system("color")
    except:
        logger.warn("Could not set colored terminal")
        logger.color(False)

# directory where all auxiliary data files are stored
data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")


# identifier of the task in the current directory
def task_id():
    return Task.extract_id_from_dir(os.path.basename(os.getcwd()))

# check if the script is invoked from a task directory
def is_task_dir(dir, is_new_dir=False):
    st = task_id() + "-st.md"
    return Task.is_task_dir(dir) and (is_new_dir or os.path.isfile(st))

# ensure that script is called within a task directory
def ensure_task_dir(is_new_dir=False):
    dir = os.path.basename(os.getcwd())
    if not is_task_dir(dir, is_new_dir):
        msg = "Task directory must start by two leading digits followed by a space, a dash or an underscore (e.g. 01_task_name)"
        if not is_new_dir:
            msg += " and must contain -st.md file"
        logger.error(msg)
        return False
    return True
    
# check if the file exists and if it does not try to find it in the given default directory
def obtain_file(file, default_dir):
    if file and not os.path.isfile(file):
        default_file = os.path.join(default_dir, file)
        if not os.path.isfile(default_file):
            logger.warn("ignoring non-existent file", file)
            file = None
        else:
            logger.info("using preinstalled file:", default_file)
            file = default_file
    return file

# suffix of the solution file
def solution(n):
    return "ex" + str(n)

################################################################################
## initial configuration

@task
def configure(ctx):
    """
    Detect compilers for programming langauges (C++, C#, C, Python) and pandoc for generating LaTeX and HTML from Markdown. This command must be run prior to using petljapub.
    """
    set_language(ctx)
    configure_compilers()

@task
def set_language(ctx, lang=None):
    """
    Set the default language (en, sr-Cyrl, sr-Latn, ...)
    """
    if not lang:
        lang = choose_language()

    add_config("lang", lang)
    
    
################################################################################
## Processing of the current task
    
@task
def new(ctx, lang=None):
    """
    Start working on a new task (template files are generated)
    """
    if not ensure_task_dir(True):
        return
    if len(os.listdir(os.getcwd())) != 0:
        logger.error("directory must be empty")
        return

    if lang == None:
        lang = read_config("lang")
    if lang == None:
        logger.warn("No language is set. Using default language: en")
        logger.warn("Please configure language using 'petljapub set-language' command")
        lang = "en"
    
    template_dir = os.path.join(data_dir, '_task_template')
    task_name_cyr = lat_to_cyr(task_id().replace("_", " ").capitalize())
    subst = {
        "TASK_NAME": task_id(),
        "TASK_NAME_CYR": lat_to_cyr(task_id().replace("_", " ").capitalize()),
        "TASK_OWNER": getpass.getuser(),
        "DATE": date.today().strftime("%Y-%m-%d")
    }

    try:
        for file in os.listdir(template_dir):
            path = os.path.join(template_dir, file)
            if file.startswith("__") or not os.path.isfile(path):
                continue
            file_contents = read_file(path)
            write_to_file(os.path.basename(file).replace("task", task_id()),
                          Template(file_contents).safe_substitute(subst))

        lang_dir = os.path.join(template_dir, lang)
        if not os.path.isdir(lang_dir):
            logger.warn("Could not find templates for language", lang, "Using default language: en")
            lang_dir = os.path.join(template_dir, "en")
            
        for file in os.listdir(lang_dir):
            path = os.path.join(lang_dir, file)
            if file.startswith("__") or not os.path.isfile(path):
                continue
            file_contents = read_file(path)
            write_to_file(os.path.basename(file).replace("task", task_id()),
                          Template(file_contents).safe_substitute(subst))
            
    except:
        logger.error("Error copying template files")


@task
def clean(ctk):
    """
    Delete all generated files
    """

    if not ensure_task_dir(True):
        return
    
    task = Task(os.getcwd())
    task.clear_build_dir()


@task(help = {
    'lang': "Programming language of the solution that is compiled (e.g., cpp, cs, py)",
    'sol': "The number of the solution that is compiled (e.g. for compiling program-ex2.cpp the value 2 should be given). If not specified, the main solution is compiled (e.g., program.cpp)."
})
def compile(ctx, lang, sol=0):
    """
    Compile a solution file for the current task
    """

    if not ensure_task_dir():
        return
    task = Task(os.getcwd())
    task.compile(solution(sol), lang)
    

@task
def c(ctx, lang, sol=0):
    """
    Compile a solution file for the current task (shortcut for 'petljapub compile')
    """
    compile(ctx, lang, sol)


@task(help = {
    'lang': "Programming language of the solution that is run (e.g., cpp, cs, py)",
    'sol': "The number of alternative solution that is run (for running program-ex2.cpp the value 2 should be given). If not specified, the main solution is run (e.g., program.cpp).",
    'example': "Run on the example testcase with the given number, printing result to stdout.",
    'generated': "Run on the generated testcase with the given number, printing result to stdout.",
    'crafted': "Run on the crafted testcase with the given number, printing result to stdout.",
    'testcase': "Run on the generated testcase with the given number, printing result to stdout.",
    'timelimit': "Set a timelimit in miliseconds",
    'verbosity': "Level of messages printed to the user (from 0/quiet to 5/full)"
})
def run(ctx, lang, sol=0, testcase=-1, example=-1, generated=-1, crafted=-1, verbosity=3, timelimit=None):
    """
    Run a solution interactively (using stdin and stdout) or on a given testcase (assuming that testcases have been generated)
    """

    logger.verbosity(verbosity)
    
    # testcase is just a synonym for generated
    if testcase >= 1:
        generated = testcase

    if not ensure_task_dir():
        return
    task = Task(os.getcwd())
    testcase = None
    if example >= 1:
        testcase = task.testcase_path("example", example)
    elif generated >= 1:
        testcase = task.testcase_path("generated", generated)
    elif crafted >= 1:
        testcase = task.testcase_path("crafted", crafted)

    if testcase:
        status = task.run(solution(sol), lang, testcase=testcase, output="stdout",timelimit=timelimit)
        if status != "OK":
            logger.warn("program exited with status", status)
    else:
        logger.info("Running interactively, enter input:")
        task.run_interactive(solution(sol), lang)
    
@task
def r(ctx, lang, sol=0, testcase=-1, example=-1, generated=-1, crafted=-1, verbosity=3, timelimit=None):
    """
    Run a solution (shortcut for 'petljapub run')
    """
    run(ctx, lang, sol, testcase, example, generated, crafted, verbosity, timelimit)
    
    
@task(help={
    'crafted_dir': "Directory where crafted tests are stored",
    'verbosity': "Level of messages printed to the user (from 0/quiet to 5/full)"
    })
def tests_gen(ctx, crafted_dir=None, verbosity=3):
    """
    Generate all testcases for the current task
    """
    if not ensure_task_dir():
        return
    
    logger.verbosity(verbosity)
    
    task = Task(os.getcwd())
    task.prepare_all_testcases(crafted_dir)

@task
def tg(ctx, crafted_dir=None, verbosity=3):
    """
    Generate all testcases for the current task (shortcut for 'petljapub tests-gen')
    """
    tests_gen(ctx, crafted_dir, verbosity)
    
@task
def tests_zip(ctx, crafted_dir=None):
    """
    Generate zip with all testcases for the current task
    """
    if not ensure_task_dir():
        return
    
    task = Task(os.getcwd())
    task.tests_zip(crafted_dir)

@task
def tz(ctx, crafted_dir=None):
    """
    Generate zip with all testcases for the current task (shortcut for 'petljapub tests-zip')

    """

    tests_zip(ctx, crafted_dir)
    
@task
def compile_checker(ctx):
    """
    Compile custom checker (if exists)
    """
    if not ensure_task_dir():
        return
    task = Task(os.getcwd())
    task.compile_checker()

@task(help={
    'lang': "Programming language of the solution that is tested (e.g., cpp, cs, py)",
    'sol': "The number of the solution that is tested (e.g. for compiling program-ex2.cpp the value 2 should be given). If not specified, the main solution is tested (e.g., program.cpp).",
    'timelimit': "Time limit in miliseconds for each testcase (1 seconds is the default value)",
    'verbosity': "Level of messages printed to the user (from 0/quiet to 5/full)",
    'outputs': 'If this flag is set, user program outputs are saved'
})
def test(ctx, lang=[], sol=[], example=-1, generated=-1, crafted=-1, timelimit=None, outputs=False, verbosity=3):
    """
    Test the given solution for the current task
    """
    if not ensure_task_dir():
        return
    
    task = Task(os.getcwd())
    logger.verbosity(verbosity)

    if not ensure_task_dir():
        return
    task = Task(os.getcwd())
    if example >= 1:
        input = task.testcase_path("example", example)
        output = input[:-2] + "out"
        status, time = task.test_on_testcase(solution(sol), lang, input, output, timelimit=timelimit, save_output_dir=task.example_test_output_dir() if outputs else None)
        logger.info(status)
        logger.info("Time: ", round(time), "ms")
    elif generated >= 1:
        input = task.testcase_path("generated", generated)
        output = input[:-2] + "out"
        status, time = task.test_on_testcase(solution(sol), lang, input, output, timelimit=timelimit, save_output_dir=task.generated_test_output_dir() if outputs else None)
        logger.info(status)
        logger.info("Time: ", round(time), "ms")
    elif crafted >= 1:
        input = task.testcase_path("crafted", crafted)
        output = input[:-2] + "out"
        status, time = task.test_on_testcase(solution(sol), lang, input, output, timelimit=timelimit, save_output_dir=task.crafted_test_output_dir() if outputs else None)
        logger.info(status)
        logger.info("Time: ", round(time), "ms")
    else:
        scoring_reporter = None
        if task.has_scoring():
            scoring_reporter = Task.ScoringReporter(task)
            
        task.test_on_all_testcases("ex" + str(sol), lang, timelimit=timelimit, save_outputs=outputs, reporter=scoring_reporter)

@task
def t(ctx, lang, sol=0, example=-1, generated=-1, crafted=-1, timelimit=None, outputs=False, verbosity=3):
    """
    Test the given solution for the current task (shortcut for 'petljapub test')
    """
    test(ctx, lang, sol, example, generated, crafted, timelimit, outputs, verbosity)
    
    
@task(
    iterable=["lang"],
    help={'lang': "Add language that should be tested (if no languages are specified, all languages are tested)",
          'timelimit': "Time limit for every testcase (in miliseconds)",
          'verbosity': "Level of messages printed to the user (from 0/quiet to 5/full)"})
def test_all(ctx, lang=[], timelimit=None, verbosity=3):
    """
    Test all solutions for the current task
    """
    if not ensure_task_dir():
        return
    task = Task(os.getcwd())
    logger.verbosity(verbosity)
    
    scoring_reporter = None
    if task.has_scoring():
        scoring_reporter = Task.ScoringReporter(task)
    task.test_all(langs=lang, timelimit=timelimit, reporter=scoring_reporter)
    
@task(help={})
def scoring_yaml(ctx, subtask=False):
    """
    Generate yaml for scoring testcases
    """
    if not ensure_task_dir():
        return
    task = Task(os.getcwd())
    task.generate_scoring_yaml(subtask)
    
    
@task(iterable=["lang"],
      help={
    'force': "If not true, times can be read from time.json file (if it is available)",
    'timelimit': "Time limit (in miliseconds) for each solution run",
    'repeat': "For better accurracy, solutions runs are repeated and median value is used",
    'plot': "Graphically show runtimes (using bar plot)",
    'lang': "Plot only runtime for the given language",
    'sol': "Plot only runtime for the given solution"
})
def runtime(ctx, force=False, timelimit=None, repeat=3, plot=False, sol=None, lang=[]):
    """
    Measure runtime for the current task
    """
    if not ensure_task_dir():
        return
    task = Task(os.getcwd())
    times = task.measure_all_runtimes(force=force,repeat=repeat,timelimit=timelimit,langs=lang)
    if plot:
        plot_times(times, langs=lang, sol=sol)

    
@task(iterable=["lang"],
      help={
      'min_timelimit': "Minimal time limit that can be set (e.g. 50ms)",
      'max_timelimit': "Maximal time limiit (a warning is issue if timelimit is greater)",
      'margin': "",
      'petlja_set_timelimit': "If true, timelimit is set on the remote server petlja.org",
      'prefix': "Prefix of the task alias on petlja.org",
      'force': "If this flag is set, runtime on all testcases is measured from scratch",
      'verbosity': "Level of messages printed to the user (from 0/quiet to 5/full)",
      'lang': "Add language that should be used for callibration (if no languages are specifed, all languages are used)"
      })
def calibrate(ctx, verbosity=3, min_timelimit=50, max_timelimit=1000, margin=1.25, force=False, petlja_set_timelimit=False, prefix="", lang=[]):
    """
    Automatically determine and set timelimit for the current task
    """
    logger.verbosity(verbosity)
    if not ensure_task_dir():
        return
    task = Task(os.getcwd())
    task.calibrate(min_timelimit=min_timelimit, max_timelimit=max_timelimit, margin=margin, petlja_set_timelimit=petlja_set_timelimit, prefix=prefix, langs=lang, force=force)

@task(iterable=["lang"],
      help={
      'lang': "Add language that should be included (if no languages are specified, all languages are included)",
      'css': "CSS stylesheet",
      'header': "Header included into md file before conversion to HTML",
      'lat': "If this flag is set, all content ist transliterated to latin alphabet",
      })
def html_preview(ctx, lang=[], css="pandoc.css", header="header.md", lat=False, babel=None):
    """
    Generate HTML preview for the current task
    """
    
    if not ensure_task_dir():
        return

    # if files do not exist, try to find preinstalled files in the data directory
    css = obtain_file(css, os.path.join(data_dir, "html"))
    header = obtain_file(header, os.path.join(data_dir, "md"))

    translit = (lambda x: x) if not lat else cyr_to_lat
    if not babel:
        babel = read_config("lang")
    task = Task(os.getcwd(), normalize_md=PandocMarkdown.fix)

    task_visitor = TaskVisitorHTML(css, header, translit=translit, babel=babel)
    task_visitor.visit_task(task, lang)

################################################################################
## Processing of yaml specifications

@task
def new_yaml(ctx, name, tasks_dir=None):
    """
    Generate a yaml file template that specifies publication content and metadata
    """
    path = os.path.join(data_dir, "template.yaml")
    file_contents = read_file(path)
    subst = {
        "ALIAS": "",
        "AUTHOR": getpass.getuser(),
        "THUMB": "",
        "DATE": date.today().strftime("%Y-%m-%d")
    }

    yaml_content = Template(file_contents).safe_substitute(subst)

    if tasks_dir:
        if not os.path.isdir(tasks_dir):
            logger.error(tasks_dir, "is not a directory")
            
        task_repo = TaskRepository(tasks_dir)
        content = []
        for task in task_repo.tasks():
            content.append({task : {"print": "full"}})

        yaml_content = yaml.safe_load(yaml_content)
        yaml_content["content"] = content
        yaml_content = yaml.dump(yaml_content, sort_keys=False)
    
    if not name.endswith(".yaml"):
        name += ".yaml"
        
    write_to_file(name, yaml_content)
        

@task(help={'tasks-dir': "Directory where tasks are stored (if different from the one where the YAML file resides)"})
def generate_yaml(ctx, tasks_dir):
    if tasks_dir and not os.path.isdir(tasks_dir):
        logger.error(tasks_dir, "is not a directory")
    task_repo = TaskRepository(tasks_dir)
    for task in task_repo.tasks():
        print(task)


@task(help={'yaml': "YAML specification of the publication",
            'tasks-dir': "Directory where tasks are stored (if different from the one where the YAML file resides)",
            'force': "Force retesting of all solutions",
            'timelimit': "Time limit in miliseconds for running each testcase",
            'verbosity': "Level of messages printed to the user (from 0/quiet to 5/full)"})
def yaml_test(ctx, yaml, tasks_dir=None, pub_dir=None, force=False, timelimit=None, verbosity=3):
    """
    Check correctness of all solutions for all tasks specified in a yaml file
    """
    logger.verbosity(verbosity)

    if not tasks_dir:
        tasks_dir = os.path.dirname(yaml)
    if not pub_dir:
        pub_dir = os.path.dirname(yaml)

    if not os.path.exists(yaml):
        logger.error(yaml, "does not exist")
        return

    if not os.path.isfile(yaml):
        logger.error(yaml, "is not a regular file")
        return

    if tasks_dir and not os.path.isdir(tasks_dir):
        logger.error(tasks_dir, "is not a directory")

    if pub_dir and not os.path.isdir(pub_dir):
        logger.error(pub_dir, "is not a directory")
        
    task_repo = TaskRepository(tasks_dir)
    pub_repo = PublicationRepository(pub_dir)
    yaml_specification = YAMLSpecification(yaml)
    yaml_specification.traverse(PublicationVisitorTest(yaml_specification, task_repo, force, timelimit))

@task(help={
    'yaml': "YAML specification of the publication",
    'tasks-dir': "Directory where tasks are stored (if different from the one where the YAML file resides)",
    'force': "If not true, times can be read from time.json file (if it is available)",
    'timelimit': "Time limit (in miliseconds) for each solution run",
    'repeat': "For better accurracy, solutions runs are repeated and median value is used",
    'verbosity': "Level of messages printed to the user (from 0/quiet to 5/full)"
})
def yaml_runtime(ctx, yaml, tasks_dir=None, pub_dir=None, force=False, timelimit=1000, repeat=3, verbosity=3):
    """
    Measure runtime for all tasks specified in the yaml file
    """
    logger.verbosity(verbosity)
    
    if not tasks_dir:
        tasks_dir = os.path.dirname(yaml)
        
    if not os.path.exists(yaml):
        logger.error(yaml, "does not exist")
        return
    
    if not os.path.isfile(yaml):
        logger.error(yaml, "is not a regular file")
        return

    if tasks_dir and not os.path.isdir(tasks_dir):
        logger.error(tasks_dir, "is not a directory")
        
    task_repo = TaskRepository(tasks_dir)
    yaml_specification = YAMLSpecification(yaml)

    params = {
        "force": force,
        "timelimit": timelimit,
        "repeat": repeat,
        "langs": yaml_specification.langs()
    }
    yaml_specification.traverse(RuntimeTaskVisitor(task_repo, params))

@task
def yaml_calibrate(ctx, yaml, tasks_dir=None, pub_dir=None, force=False, timelimit=None):
    """
    Automatically determine time limit for each task
    """

    if not tasks_dir:
        tasks_dir = os.path.dirname(yaml)
    
    task_repo = TaskRepository(tasks_dir)
    yaml_specification = YAMLSpecification(yaml)
    
    params = {
        "force": force,
        "timelimit": timelimit,
        "langs": yaml_specification.langs()
    }
    
    yaml_specification.traverse(CalibrateTaskVisitor(task_repo, params))
    

# report statistics about the publication
@task(help={'yaml': "YAML specification of the publication",
            'tasks-dir': "Directory where tasks are stored (if different from the one where the YAML file resides)"})
def yaml_stats(ctx, yaml, tasks_dir=None):
    """
    Report statistics about tasks in yaml file and repository

    """
    if not tasks_dir:
        tasks_dir = os.path.dirname(yaml)

    if not os.path.exists(yaml):
        logger.error(yaml, "does not exist")
        return

    if not os.path.isfile(yaml):
        logger.error(yaml, "is not a regular file")
        return

    if tasks_dir and not os.path.isdir(tasks_dir):
        logger.error(tasks_dir, "is not a directory")

    yaml = YAMLSpecification(yaml)
    task_repo = TaskRepository(tasks_dir)
    yaml.traverse(YAMLSpecificationVisitorStats(yaml, task_repo))
    
# build the publication in html format
@task(help={'yaml': "YAML specification of the publication",
            'tasks-dir': "Directory where tasks are stored (if different from the one where the YAML file resides)",
            'pub-dir': "Directory where publication files are stored (if different from the one where the YAML file resides)",
            'dst': "Location where generated files are stored (directory or a ZIP file)",
            'standalone': "Controls if standalone HTML files are generated, or just HTML fragments to be included in other HTML files",
            'join-langs': "Controls whether a single or seperate HTML files are generated for different programming languages",
            'css': "CSS stylesheet to be applied to standalone HTML files",
            'header': "A header to be prepended to each Markdown file before conversion to HTML is applied",
            'lat': "If this flag is set, all content ist transliterated to latin alphabet",
            'cyr': "If this flag is set, all content ist transliterated to cyrillic alphabet",
            'verbosity': "Level of messages printed to the user (from 0/quiet to 5/full)"})
def yaml_html(ctx, yaml, dst, tasks_dir=None, pub_dir=None, standalone=True, join_langs=True, css=None, header="header.md", babel=None, lat=False, cyr=False, verbosity=3):
    """
    Build task or publication in HTML format
    """
    logger.verbosity(verbosity)

    if not tasks_dir:
        tasks_dir = os.path.dirname(yaml)
    if not pub_dir:
        pub_dir = os.path.dirname(yaml)

    if not os.path.exists(yaml):
        logger.error(yaml, "does not exist")
        return

    if not os.path.isfile(yaml):
        logger.error(yaml, "is not a regular file")
        return

    if tasks_dir and not os.path.isdir(tasks_dir):
        logger.error(tasks_dir, "is not a directory")
        return

    if pub_dir and not os.path.isdir(pub_dir):
        logger.error(pub_dir, "is not a directory")
        return

    css = obtain_file(css, os.path.join(data_dir, "html"))
    header = obtain_file(header, os.path.join(data_dir, "md"))
        
    yaml = YAMLSpecification(yaml)
    translit = (lambda x: x)
    if lat:
        translit = cyr_to_lat
    if cyr:
        translit = lat_to_cyr_md
        
    if not babel:
        babel = yaml.babel() or read_config("lang")

    task_repo = TaskRepository(tasks_dir, normalize_md=PandocMarkdown.fix)
    pub_repo = PublicationRepository(pub_dir, normalize_md=PandocMarkdown.fix)

        
    visitor = PublicationVisitorHTML(yaml, task_repo, pub_repo, dst, langs=yaml.langs(),
                                     html=True, standalone=standalone, css=css, header=header, join_langs=join_langs, translit=translit, babel=babel)
    yaml.traverse(visitor)

# build the publication in html format for petlja publishing
@task(help={'yaml': "YAML specification of the publication",
            'dst': "Location where generated files are stored (directory or a zip file)",
            'tasks-dir': "Directory where tasks are stored (if different from the one where the YAML file resides)",
            'pub-dir': "Directory where publication files are stored (if different from the one where the YAML file resides)",
            'join-langs': "Controls whether a single or seperate HTML files are generated for different programming languages",
            'header': "A header to be prepended to each Markdown file before conversion to HTML is applied",
            'lat': "If this flag is set, all content ist transliterated to latin alphabet",
            'generate-tests': "Forces generating all test cases from scratch"})
def yaml_petlja_package(ctx, yaml, dst, tasks_dir=None, pub_dir=None, join_langs=True, header="header.md", lat=False, generate_tests=False,verbosity=3):
    """
    Build package for publishing the publication on petlja.org
    """
    logger.verbosity(verbosity)

    if not tasks_dir:
        tasks_dir = os.path.dirname(yaml)
    if not pub_dir:
        pub_dir = os.path.dirname(yaml)

    if not os.path.exists(yaml):
        logger.error(yaml, "does not exist")
        return

    if not os.path.isfile(yaml):
        logger.error(yaml, "is not a regular file")
        return
    
    if tasks_dir and not os.path.isdir(tasks_dir):
        logger.error(tasks_dir, "is not a directory")
        return

    if pub_dir and not os.path.isdir(pub_dir):
        logger.error(pub_dir, "is not a directory")
        return

    header = obtain_file(header, os.path.join(data_dir, "md"))
    
    task_repo = TaskRepository(tasks_dir, normalize_md=PandocMarkdown.fix)
    pub_repo = PublicationRepository(pub_dir, normalize_md=PandocMarkdown.fix)
    
    yaml = YAMLSpecification(yaml)
    translit = (lambda x: x) if not lat else cyr_to_lat
    visitor = PublicationVisitorHTMLPetljaPackage(yaml, task_repo, pub_repo, dst, langs=yaml.langs(),
                                                  html=True, header=header, join_langs=join_langs, translit=translit)
    visitor._generate_tests = generate_tests
    yaml.traverse(visitor)

# build the publication in latex format ready for producing pdf
@task(help={'yaml': "YAML specification of the publication",            
            'dst': "Path of the resulting file (all image files are saved in the same directory)",
            'tasks-dir': "Directory where tasks are stored (if different from the one where the YAML file resides)",
            'pub-dir': "Directory where publication files are stored (if different from the one where the YAML file resides)",
            'header': "A header to be prepended to the Markdown file before conversion to TeX is applied",
            'tex-template': "A tex template to be used",
            'babel': "language code for the multilingual (babel, polyglossia) package (en, sr-Latn, sr-Cyrl, english, serbian, serbianc, ...)",
            'quiet': "make LaTeX processing quiet",
            'lat': "If lat is true, cyrillic is converted to latin script",            
            'cyr': "If cyr is true, latin is converted to cyrillic script",            
})
def yaml_tex(ctx, yaml, dst, tasks_dir=None, pub_dir=None, header='header.md', babel=None, tex_template='default.latex', standalone=True, quiet=False, lat=False, cyr=False):
    """
    Build publication in LaTeX format
    """
    if not tasks_dir:
        tasks_dir = os.path.dirname(yaml)
    if not pub_dir:
        pub_dir = os.path.dirname(yaml)

    if not os.path.exists(yaml):
        logger.error(yaml, "does not exist")
        return

    if not os.path.isfile(yaml):
        logger.error(yaml, "is not a regular file")
        return

    if tasks_dir and not os.path.isdir(tasks_dir):
        logger.error(tasks_dir, "is not a directory")
        return

    if pub_dir and not os.path.isdir(pub_dir):
        logger.error(pub_dir, "is not a directory")
        return

    if os.path.exists(dst) and not os.path.isfile(dst):
        logger.error(dst, "exists but is not a regular file")
        return

    if dst.endswith(".md"):
        tex = False
        pdf = False
    elif dst.endswith(".tex"):
        tex = True
        pdf = False
    elif dst.endswith(".pdf"):
        dst = dst[:-3] + "tex"
        tex = True
        pdf = True
    else:
        logger.error("Destination must have *.md, *.tex or *.pdf extension")
        return
        
    header = obtain_file(header, os.path.join(data_dir, "md"))
    tex_template = obtain_file(tex_template, os.path.join(data_dir, "tex"))
    translit = (lambda x: x)
    if lat:
        translit = cyr_to_lat
    if cyr:
        translit = lat_to_cyr_md

    task_repo = TaskRepository(tasks_dir, normalize_md=PandocMarkdown.fix, translit=translit)
    pub_repo = PublicationRepository(pub_dir, normalize_md=PandocMarkdown.fix, translit=translit)
    
    yaml = YAMLSpecification(yaml)
    langs = yaml.langs()

    if not babel:
        babel = yaml.babel() or read_config("lang")

    visitor = PublicationVisitorTeX(yaml, task_repo, pub_repo, dst, langs=langs, tex=tex, pdf=pdf, header=header, babel=babel, standalone=standalone, tex_template=tex_template, quiet=quiet)
    yaml.traverse(visitor)

# Log the contents of the yaml specification
@task(help={'yaml': "YAML specification of the publication",            
            'tasks-dir': "Directory where tasks are stored (if different from the one where the YAML file resides)",
            'pub-dir': "Directory where publication files are stored (if different from the one where the YAML file resides)"
})
def yaml_log(ctx, yaml, tasks_dir=None, pub_dir=None):
    """
    Log the contents of the yaml specification
    """
    if not tasks_dir:
        tasks_dir = os.path.dirname(yaml)
    if not pub_dir:
        pub_dir = os.path.dirname(yaml)

    if not os.path.exists(yaml):
        logger.error(yaml, "does not exist")
        return

    if not os.path.isfile(yaml):
        logger.error(yaml, "is not a regular file")
        return

    if tasks_dir and not os.path.isdir(tasks_dir):
        logger.error(tasks_dir, "is not a directory")
        return

    if pub_dir and not os.path.isdir(pub_dir):
        logger.error(pub_dir, "is not a directory")
        return

    task_repo = TaskRepository(tasks_dir, normalize_md=PandocMarkdown.fix)
    pub_repo = PublicationRepository(pub_dir, normalize_md=PandocMarkdown.fix)
    
    yaml = YAMLSpecification(yaml)
    visitor = YAMLSpecificationVisitorLog(yaml, task_repo, pub_repo)
    yaml.traverse(visitor)
    
@task
def tgen_hpp(ctx):
    """
    Copy tgen include files to current directory
    """
    for filename in glob.glob(os.path.join(tgen_dir(), "tgen*.hpp")):
        shutil.copy(filename, os.getcwd())

@task
def rename(ctx, old, new):
    """
    Rename a task (creating its copy with a new name)
    Usage: petljapub rename old_name new_name (without numbers)
    """
    old_files = glob.glob("*"+old)
    if not old_files:
        logger.error(old, "does not exist")
        return
    if len(old_files) > 1:
        logger.error("multiple", old, "directories exist")
        return
    old_dir = old_files[0]
    new_dir = re.sub(old, new, old_dir)
    if os.path.isdir(new_dir):
        logger.error(new_dir, "already exists")
        return
    os.makedirs(new_dir)
    for f in glob.glob(os.path.join(old_dir, old+"*")):
        new_f = os.path.join(new_dir, re.sub(old, new, os.path.basename(f)))
        shutil.copyfile(f, new_f)
    # rename task_name --- obsolete
    replace_in_file(os.path.join(new_dir, new + "-tgen.cpp"),
                    '\"' + old + '\"',
                    '\"' + new + '\"')
    logger.info(new_dir, "succesfully created")    
        
################################################################################
# petlja_api

import petlja_api

@task
def petlja_set_login_info(ctx):
    """
    Set the petlja.org login information
    """
    set_petlja_login_info()

@task
def petlja_remove_login_info(ctx):
    """
    Remove the petlja.org login information
    """
    remove_petlja_login_info()    

@task(help={
    'prefix': "Prefix of the task alias on remote server petlja.org"
    })
def petlja_publish(ctx, prefix=""):
    """
    Publish the current task to petlja.org
    """

    if not ensure_task_dir(True):
        return
    
    task = Task(os.getcwd())
    task.petlja_publish(prefix=prefix)

@task(help = {
    'name': "Competition name",
    'description': "Text describing the competition",
    'prefix': "Prefix for each task",
    'verbosity': "Level of messages printed to the user (from 0/quiet to 5/full)"
})
def petlja_create_competition(ctx, name=None, prefix=None, description=None, alias=None, verbosity=3):
    """
    Create competition for current directory on arena.petlja.org
    """

    logger.verbosity(verbosity)

    competition_dir = os.getcwd()
    
    if not Competition.is_competition_dir(competition_dir):
        logger.error("Competition folder must have at least one task folder as its subfolder")
        return
    comp = Competition(competition_dir, name=name, description=description, prefix=prefix, alias=alias)
    comp.petlja_publish()    

@task(help={'lang': "Programming language of the solution that is tested (e.g., cpp, cs, py)",
            'sol': "The number of the solution that is tested (e.g. for compiling program-ex2.cpp the value 2 should be given). If not specified, the main solution is tested (e.g., program.cpp).",
            'verbosity': "Level of messages printed to the user (from 0/quiet to 5/full)",
            'competition-dir': "Directory that contains a competition with the current task",
            'timelimit': "Time limit (in miliseconds)"})
def petlja_test(ctx, lang, sol=0, verbosity=3, competition_dir=None, timelimit=None):
    """
    Test the given solution for the current task on petlja.org online judge
    """
    if not ensure_task_dir():
        return
    
    task = Task(os.getcwd())
    logger.verbosity(verbosity)
    task.petlja_test_on_all_testcases(solution(sol), lang, competition_dir=competition_dir, detailed=verbosity>3, timelimit=timelimit)

@task
def pt(ctx, lang, sol=0, verbosity=3, competition_dir=None, timelimit=None):
    """
    Test the given solution for the current task on petlja.org online judge (shortcut for petlja-test)
    """
    logger.verbosity(verbosity)
    petlja_test(ctx, sol, lang, verbosity, competition_dir, timelimit)

@task
def petlja_test_all_scores(ctx, verbosity=3):
    """
    Verify that the current task solutions achieve the expected score specified in the task statement metadata
    """
    
    logger.verbosity(verbosity)

    if not ensure_task_dir():
        return

    logger.verbosity(verbosity)
    task = Task(os.getcwd())
    task.petlja_test_all_scores()

@task(help={
    'force': "If true, all tests are run from scratch",
    'competition_dir': "Directory of a competition that contains the task",
    'verbosity': "Level of messages printed to the user (from 0/quiet to 5/full)",
    'timelimit': "Time limit (in miliseconds) for each solution run"
    })
def petlja_runtime(ctx, force=False, competition_dir=None, verbosity=3, timelimit=None):
    """
    Measure all runtimes on the remote server petlja.org
    """

    logger.verbosity(verbosity)
    
    if not ensure_task_dir():
        return

    logger.verbosity(verbosity)
    task = Task(os.getcwd())
    task.petlja_measure_all_runtimes(force=force, competition_dir=competition_dir, timelimit=timelimit)
    
@task
def petlja_calibrate(ctx, verbosity=3, min_timelimit=50, max_timelimit=1000, margin=1.25, prefix=""):
    """
    Automatically determine time limit and set it on petlja.org
    """
    calibrate(ctx, verbosity=verbosity, min_timelimit=min_timelimit, max_timelimit=max_timelimit, margin=margin, petlja_set_timelimit=True, prefix=prefix)
    
    
@task
def petlja_test_raw(ctx, lang, sol=0):
    if not ensure_task_dir():
        return
    
    task = Task(os.getcwd())
    task.petlja_api_submit_solution_raw(solution(sol), lang)
    

@task(help={
    'yaml': "YAML specification of the publication",
    'tasks-dir': "Directory where tasks are stored (if different from the one where the YAML file resides)",
    'force': "If not true, times can be read from time.json file (if it is available)",
    'timelimit': "Time limit (in miliseconds) for each solution run",
    'verbosity': "Level of messages printed to the user (from 0/quiet to 5/full)"
})
def petlja_yaml_runtime(ctx, yaml, tasks_dir=None, pub_dir=None, force=False, timelimit=1.0, verbosity=3):
    """
    Measure runtime for all tasks specified in the yaml file on the server petlja.org
    """
    logger.verbosity(verbosity)
    
    if not tasks_dir:
        tasks_dir = os.path.dirname(yaml)
        
    if not os.path.exists(yaml):
        logger.error(yaml, "does not exist")
        return
    
    if not os.path.isfile(yaml):
        logger.error(yaml, "is not a regular file")
        return

    if tasks_dir and not os.path.isdir(tasks_dir):
        logger.error(tasks_dir, "is not a directory")
        
    task_repo = TaskRepository(tasks_dir)
    yaml_specification = YAMLSpecification(yaml)

    params = {
        "force": force,
        "timelimit": timelimit,
        "langs": yaml_specification.langs()
    }

    session = None
    try:
        session = get_petlja_session()
    except:
        logger.error("Could not log in to petlja.org")
        return

    try:
        yaml_specification.traverse(PetljaRuntimeTaskVisitor(task_repo, params, session))
    finally:
        if session:
            session.cookies.clear()
            session.close()
