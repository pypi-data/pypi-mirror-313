import subprocess
import re
from petljapub import logger
from petljapub import config


def get_version(command, options):
    try: 
        result = subprocess.run([command] + options, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        version_line = result.stdout.decode('utf-8').strip().split('\n')[0]
        m = re.search(r'[0-9]+[.][0-9]+([.][0-9]+)*', version_line)
        return m.group(0)
    except:
        return None

def version_ok(version, required_version):
    return list(map(int, version.split("."))) >= \
           list(map(int, required_version.split(".")))

def check_compiler(name, command, options, required_version):
    version = get_version(command, options)
    if not version:
        logger.warn("No", name, "installed or not in path")
        return False
    if not version_ok(version, required_version):
        logger.warn("Found", name, version, "but version >=", required_version, "is required")
        return False
    else:
        logger.info("Found", name, version)
        return True

def configure_compilers():
    logger.info("---------- checking python --------------------")
    python = None
    if check_compiler("python3", "python3", ["--version"], "3.7") and not python:
        python = "python3"
    elif check_compiler("python", "python", ["--version"], "3.7") and not python:
        python = "python"
        
    logger.info("---------- checking C++ compilers -------------")
    cpp_compiler = None
    if check_compiler("g++", "g++", ["--version"], "4.9") and not cpp_compiler:
        cpp_compiler = "G++"
    elif check_compiler("MSVC++", "cl", [""], "14.1") and not cpp_compiler:
        cpp_compiler = "MSVC++"

    logger.info("---------- checking C compilers ---------------")
    c_compiler = None
    if check_compiler("gcc", "gcc", ["--version"], "0.0"):
        c_compiler = "GCC"

    logger.info("---------- checking C# compilers --------------")
    cs_compiler = None
    if check_compiler("mono", "mono", ["--version"], "6.8") and not cs_compiler:
        cs_compiler = "MONO"
    elif check_compiler("mono", "mcs", ["--version"], "6.8") and not cs_compiler:
        cs_compiler = "MONO"
    elif check_compiler("MSVC#", "csc", ["--version"], "3.1") and not cs_compiler:
        cs_compiler = "MSVC#"
    elif check_compiler(".NET", "dotnet", ["--version"], "3.1") and not cs_compiler:
        cs_compiler = ".NET"

    logger.info("---------- checking pandoc --------------------")
    pandoc_required_version = "2.0"
    pandoc = check_compiler("pandoc", "pandoc", ["--version"], pandoc_required_version)

    logger.info("---------- checking LaTeX --------------------")
    latex_required_version = "3.141"
    latex = check_compiler("LaTeX", "xelatex", ["--version"], latex_required_version)
    latexmk_required_version = "4.6"
    latex_mk = check_compiler("LaTeX Make", "latexmk", ["--version"], latexmk_required_version)
    
    logger.info("---------- Final report  ----------------------")
    
    if not cpp_compiler:
        logger.error("No C++ compiler found. Please install one (g++ or MSVC++) and ensure it is in the path.")
    if not c_compiler:
        logger.warn("No C compiler found. Please install gcc and ensure it is in the path, or it will not be possible to work with C files.")
    if not cs_compiler:
        logger.warn("No C# compiler found. Please install one (.NET FRAMEWORK, .NET CORE or MonoDevelop) and ensure it is in the path, or it will not be possible to work with C# files.")
    if not pandoc:
        logger.warn("No pandoc >=", pandoc_required_version, "found. Please install it (https://pandoc.org/) or it will not be possible to generate HTML and LaTeX publications.")
    if not latex:
        logger.warn("No LaTeX found. Please install it or it will not be possible to generate PDF documents.")
    if not latex_mk:
        logger.warn("No LaTeX Make system found.")
        

    config.add_configs({"pandoc": pandoc, "cpp_compiler": cpp_compiler, "cs_compiler": cs_compiler, "c_compiler": c_compiler, "python": python, "latex": latex, "latex_mk": latex_mk})
        
        
if __name__ == '__main__':
    check_compilers()
