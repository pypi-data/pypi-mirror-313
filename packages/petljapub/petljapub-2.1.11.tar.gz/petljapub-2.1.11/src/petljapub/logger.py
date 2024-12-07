import sys, os

# 0 - quit
# 1 - only errors
# 2 - only errors and warnings
# 3 - errors, warings and info
# >3 - more details
_verbosity = 3

_warn_stream = sys.stderr
_error_stream = sys.stderr
_info_stream = sys.stderr

_use_color = True

class color_codes:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def color(use_color):
    global _use_color
    _usе_color = use_color
    
def color_text(text, color):
    global _use_color
    if _use_color and os.getenv('ANSI_COLORS_DISABLED') is None:
        text = f"{color}{text}{color_codes.ENDC}"
        return text

def bold(text):
    return color_text(text, color_codes.BOLD)

def verbosity(v=None):
    global _verbosity
    if v is not None:
        _verbosity = v
    else:
        return _verbosity

def err(*str):
    global _verbosity
    if _verbosity > 0:
        print(color_text("ERROR:", color_codes.FAIL), *str, file=_error_stream)

def error(*str):
    err(*str)
        
def warn(*str, verbosity=1):
    global _verbosity
    if _verbosity > verbosity:
        print(color_text("WARNING:", color_codes.WARNING), *str, file=_warn_stream)

def warning(*str):
    warn(*str)

def info(*str, verbosity=3):
    global _verbosity
    if _verbosity >= verbosity:
        print(color_text("INFO:", color_codes.OKGREEN), *str, file=_info_stream)
