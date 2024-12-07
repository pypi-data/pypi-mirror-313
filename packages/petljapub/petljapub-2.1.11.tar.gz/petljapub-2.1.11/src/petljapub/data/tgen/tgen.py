import importlib
import sys, os

def load_module_from_path(module_name, module_path):
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module

def gen_tests(tests_name, testcase_dir, print_info=False):
    for test_num in range(1, gen_test_module.test_count + 1):
        # Create file name with zero-padded test number
        file_name = f"{testcase_dir}/{tests_name}_{test_num:02d}.in"

        # Print info if necessary
        if print_info:
            print(f"INFO: generating test input {test_num}...")

        # Open the file and generate the test
        with open(file_name, 'w') as tin:
            gen_test_module.gen_test(test_num, tin)

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Module with gen_test function expected", file=sys.stderr)
        sys.exit()

    gen_test_module_path = sys.argv[1]
    with open("/home/filip/pp_tmp.txt", "w") as pp_file:
        print(gen_test_module_path, file=pp_file)
    gen_test_module = load_module_from_path("gen_test_module", gen_test_module_path)
    
    # default tests_name is "test_01.in", "test_02.in", ...
    tests_name = "test"
    # default testcase_dir
    testcase_dir = "."
    # no info messages are printed by default
    print_info = False

    if len(sys.argv) > 2:
        tests_name = sys.argv[2]
    if len(sys.argv) > 3:
        testcase_dir = sys.argv[3]
    if len(sys.argv) > 4:
        print_info = True

    gen_tests(tests_name, testcase_dir, print_info)
