import os, sys, re

default_read_encoding = "utf-8-sig"
default_write_encoding = "utf-8"

# read the content of the whole textual file
def read_file(file_path, encoding=default_read_encoding):
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding=encoding) as file:
                content = file.read()
                return content
        except:
            return None
    else:
        return None
    
# write the content into a textual file
def write_to_file(file_path, content, encoding=default_write_encoding):
    with open(file_path, "w", encoding=encoding) as file:
        print(content, file=file)

# dump the content of a file on to stdout
def dump_file(file_path, encoding=default_read_encoding):
    print(read_file(file_path, encoding))


# replace regular expression in the file
def replace_in_file(file_path, pattern, repl):
    content = read_file(file_path)
    if not content:
        return False
    content = re.sub(pattern, repl, content)
    write_to_file(file_path, content)
    return True

# check if char is ascii
def is_ascii(char):
    return ord(char) < 128

# check if all chars in a string are ascii
def is_all_ascii(s):
    return all(is_ascii(char) for char in s)

