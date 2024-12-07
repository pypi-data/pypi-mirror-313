import sys, os
import re
import math

def num_decimals(str):
    m = re.search(r'[.]([0-9]+)$', str)
    if not(m):
        return 0
    return len(m.group(1))

def compare_tokens(expected_token, token):
    expected_token = expected_token.strip()
    token = token.strip()
    if expected_token == token:
        return True
    try:
        nd = num_decimals(expected_token)
        if nd == 0:
            return False
        expected_value = float(expected_token)
        value = float(token)
        eps = math.pow(10, nd) * 1.1
        return abs(expected_value - value) <= eps
    except:
        return False

def compare_strings(expected_output, output):
    expected_tokens = expected_output.split() 
    tokens = output.split()
    if len(expected_tokens) != len(tokens):
        return False
    for expected_token, token in zip(expected_tokens, tokens):
        if not(compare_tokens(expected_token, token)):
            return False
    return True

def compare_files(file_sol, file_out):
    if not os.path.exists(file_sol) or not os.path.exists(file_out):
        return False
    with open(file_sol) as f:
        expected_output = f.read()
    with open(file_out) as f:
        output = f.read()
    return compare_strings(expected_output, output)

if __name__ == "__main__":
    ret = compare_files(sys.argv[1], sys.argv[2])
    if compare_files(sys.argv[1], sys.argv[2]):
        sys.exit(0)
    else:
        sys.exit(-1)
