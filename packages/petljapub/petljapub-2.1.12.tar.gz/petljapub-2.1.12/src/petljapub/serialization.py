import os, sys
import re
import tempfile
from zipfile import ZipFile
import shutil
import yaml

import pypandoc

from .util import default_write_encoding, read_file, write_to_file
from . import logger
from .messages import msg, div_latex_environments
from .config import read_config
from .fix_latex import fix_latex

# Abstract interface for writing files in a directory structure
class Writer:
    def open(self):
        pass

    # write the content into a file specified by the destination path
    def write(self, dst_file_path, content):
        pass

    # modification time of the destination file (None if unkonwn)
    def modification_time(self, dst_file_path):
        pass

    # copy the file given by the source path to the destination path
    def copy_file(self, src_file_path, dst_file_path):
        pass
    
    def close(self):
        pass

# Writing files in the ordinary filesystem
class DirectoryWriter(Writer):
    # all files are stored in the given destination directory
    def __init__(self, dst_dir):
        self._dst_dir = dst_dir

    # ensure that given directory exists (create it if it does not)
    def ensure_dir(self, path):
        if path and not os.path.isdir(path):
            try:
                os.makedirs(path)
            except:
                logger.error("Could not make directory", path)
            
    def open(self):
        self.ensure_dir(self._dst_dir)

    # write the content into a file determined by its relative filename path
    # (in the destination directory)
    def write(self, dst_file_path, content):
        full_path = os.path.join(self._dst_dir, dst_file_path)
        self.ensure_dir(os.path.dirname(full_path))
        try:
            write_to_file(full_path, content)
            return True
        except:
            logger.error("Error writing to file", full_path)
            return False

    # modification time of the destination file (None if unkonwn)
    def modification_time(self, dst_file_path):
        full_path = os.path.join(self._dst_dir, dst_file_path)
        if not os.path.isfile(full_path):
            return None
        return os.path.getmtime(full_path)

    # copy the src file (given by an absolute path or a relative path
    # within the current working directory) to a dst file determined
    # by its relative filename path (in the destination directory)
    def copy_file(self, src_file_path, dst_file_path):
        if not os.path.isfile(src_file_path):
            logger.error("Error copying file. Source file", src_file_path, "does not exist")
            return False
        full_dst_path = os.path.join(self._dst_dir, dst_file_path)
        self.ensure_dir(os.path.dirname(full_dst_path))
        if not os.path.isfile(full_dst_path) or os.path.getmtime(src_file_path) > os.path.getmtime(full_dst_path):
            try:
                shutil.copyfile(src_file_path, full_dst_path)
            except:
                logger.error("Error copying file", src_file_path, "to", full_dst_path)
                return False
        return True

# Writing files in a zip archive
class ZipWriter(Writer):
    def __init__(self, zip_path):
        self._zip_path = zip_path

    def open(self):
        self._zip_file = ZipFile(self._zip_path, 'w')
        
    # write the content into a file determined by filename path
    # (within the zip file)
    def write(self, dst_file_path, content, encoding=default_write_encoding):
        try:
            tmpfile = tempfile.NamedTemporaryFile(delete=False, mode="w", encoding=encoding)
            tmpfile.write(content)
            tmpfile.close()
        except:
            logger.error("Could not create temporary file")
            return False

        try:
            self._zip_file.write(tmpfile.name, dst_file_path)
        except:
            logger.error("Could not write file to zip", dst_file_path)
            return False
            
        try:
            os.remove(tmpfile.name)
        except:
            logger.warn("Could not remove temporary file", tmpfile.name)

        return True

    # copy the src file (given by an absolute path or a relative path
    # within the current working directory) to a dst file determined
    # by its relative filename path (in in zip file)
    # dst_file_path - must contain a file name (not just a directory)
    def copy_file(self, src_file_path, dst_file_path):
        if not os.path.isfile(src_file_path):
            logger.error("Error copying file to zip. Source file", src_file_path, "does not exist")
            return False
        if not dst_file_path in self._zip_file.namelist():
            try:
                self._zip_file.write(src_file_path, dst_file_path)
            except:
                logger.error("Could not write file to zip", dst_file_path)
                return False
        else:
            logger.warn("SKIP:", dst_file_path, "- it already exists in zip")
        return True
    
    def close(self):
        self._zip_file.close()


def check_pandoc():
    if not read_config('pandoc'):
        logger.error("Pandoc is not properly configured. Ensure that it is installed and configure it using 'petljapub configure-compilers'")
        return False
    return True
        
# Serialization of Markdown files (with possible format conversion)
class MarkdownSerializer:
    # files are written using a given writer
    def __init__(self, writer, header=None, translit=lambda x: x):
        self._writer = writer
        if header:
            self._header = read_file(header)
            if self._header is None:
                logger.error("Error reading header file", header)
        else:
            self._header = None
        self._translit = translit

    def open(self):
        self._writer.open()

    def can_skip(self, md_path, md_time):
        file_time = self._writer.modification_time(self.path(md_path))
        return file_time and file_time > md_time
        
    # write the given content in the file determined by the given path
    def write(self, md_path, md_content, title=None, md_time=None):
        # skip serialization if md_content is older than the current file
        if md_time and self.can_skip(md_path, md_time):
            logger.info("Skipping existing: ", md_path, verbosity=4)
            return
        if self._header:
            md_content = self._header + "\n" + md_content
        md_content = self._translit(md_content)
        if title:
            title = self._translit(title)
        return self._writer.write(self.path(md_path), self.transform(md_content, title))

    def close(self):
        self._writer.close()

    # possible filename conversions (extension replacement)
    def path(self, md_path):
        return md_path

    # possible content format conversions
    def transform(self, md_content, title):
        return md_content

# Serialization of Markdown files converting them to HTML
class HTMLMarkdownSerializer(MarkdownSerializer):
    def __init__(self, writer, header=None, translit=lambda x: x, standalone=False, css=None, babel=None):
        super().__init__(writer, header, translit)
        # if standalone is true, HTML header and footer are added to the content
        self._standalone = standalone
        # optional CSS stylesheet
        self._css = css
        # multilingual support
        self._babel = babel
        
    # extension .md is replaced by .html
    def path(self, md_path):
        return re.sub(r".md$", ".html", md_path)

    # markdown format is converted to HTML
    def transform(self, md_content, title):
        # HACK: \protect does not work with mathjax so ve remove it
        md_content = md_content.replace("\\protect", "")
        # HACK: \symbf does not work with mathjax so ve remove it
        md_content = md_content.replace("\\symbf", "")
        # convert md to html
        html = self.md_to_html(md_content, title)
        # change verbatim text blocks from <code>...</code> to <div class='verbatim-text'>...</div>
        html = re.sub(r"<pre>\s*<code>(((?!<code).)*)</code>\s*</pre>", r"<pre><div class='verbatim-text'>\1</div></pre>", html, 0, re.DOTALL)
        return html

    # conversion of Markdown to HTML (via pypandoc)
    def md_to_html(self, md, title):
        if not check_pandoc():
            return "Pandoc is not properly configured"

        ### HACK: remove \latin{...} and \cyr{...} markup
        md = re.sub(r"\\(latin|cyr)\{([^}]*)\}", r"\2", md)
        
        # for mathematical formulae and cross-referencing filter (pandoc-xnos)
        extra_args = ['--eol=lf', '--mathjax=https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.7/MathJax.js?config=TeX-MML-AM_CHTML', '--filter=pandoc-xnos']
        # generate standalone HTML files (with HTML header and footer)
        if self._standalone:
            extra_args.append('--standalone')
        # apply the given stylesheet
        if self._css:
            extra_args.append('-H')
            extra_args.append(self._css)
        # set language
        if self._babel:
            extra_args.append('-V')
            extra_args.append('lang=' + self._babel)
            extra_args.append('-M')
            extra_args.append('fignos-caption-name=' + msg("FIGURE", self._babel))
            extra_args.append('-M')
            extra_args.append('tablenos-caption-name=' + msg("TABLE", self._babel))
        # set title
        if title:
            extra_args.append('-M')
            extra_args.append('pagetitle=' + title)

        # do the conversion
        logger.info("Converting Markdown to HTML using Pandoc")
        html = pypandoc.convert_text(md, 'html', format='md', extra_args=extra_args)

        return html

# Serialization of Markdown files converting them to LaTeX
class TeXMarkdownSerializer(MarkdownSerializer):
    def __init__(self, writer, header=None, babel=None, translit=lambda x: x, standalone=False, tex_template=None, fix_latex=False):
        super().__init__(writer, header, translit)
        # if standalone is true, HTML header and footer are added to the content
        self._standalone = standalone
        self._tex_template = tex_template
        self._fix_latex = fix_latex
        self._babel = babel

    # extension .md is replaced by .tex
    def path(self, md_path):
        return re.sub(r".md$", ".tex", md_path)

    # markdown format is converted to HTML
    def transform(self, md_content, title):
        return self.md_to_tex(md_content)

    # conversion of Markdown to HTML (via pypandoc)
    def md_to_tex(self, md):
        if not check_pandoc():
            return "Pandoc is not properly configured"
        # cross-referencing filter (pandoc-xnos)
        extra_args = ['--eol=lf', '--filter=pandoc-xnos']
        # generate standalone HTML files (with HTML header and footer)
        if self._standalone:
            extra_args.append('--standalone')
        if self._tex_template:
            extra_args.append('--template')
            extra_args.append(self._tex_template)
        if self._babel:
            extra_args.append('-V')
            extra_args.append('lang=' + self._babel)

        # do the conversion
        logger.info("Converting Markdown to LaTeX using Pandoc")
        if len(md) >= 100_000:
            logger.info("This can take a while...")

        tex = pypandoc.convert_text(md, 'tex', format='md', extra_args=extra_args)

        ######
        # hack, since pandoc does not correctly treat language codes for serbian
        if self._babel in ["sr", "serbian", "sr-Latn"]:
            tex = tex.replace("\\setmainlanguage[]{serbian}", "\\setmainlanguage[script=Latin]{serbian}")
            tex = tex.replace("\\babelprovide[main,import]{serbian}", "\\babelprovide[main,import]{serbian-latin}")
        elif self._babel in ["serbianc", "sr-Cyrl"]:
            tex = tex.replace("\\setmainlanguage[]{serbian}", "\\setmainlanguage[script=Cyrillic]{serbian}")
            tex = tex.replace("\\babelprovide[main,import]{serbianc}", "\\babelprovide[main,import]{serbian-cyrillic}")
            
        ######
        # hack, pandoc-tablenos sometimes introduces double labels, so we fix that
        tex = re.sub(r"\\label{([^}]+)}}\\label{[^}]+}", r"}\\label{\1}", tex)

        
        if self._fix_latex:
            tex = fix_latex(tex.split("\n"))

        return tex
    
