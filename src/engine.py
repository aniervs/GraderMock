import os
import dis
import resource
import unittest

def get_testcases(problem_path: str):
    """
    A generator that yields the tuples (input, output)
    Params:
    ---
    problem_path (str): the relative path to the problem's directory
    """
    
    path = f"./assets/problems/{problem_path}/testcases"
    
    input_dict = {}
    output_dict = {}
    

    for d in os.listdir(path):
        
        with open(path + "/" + d, "r") as file:
            if d.startswith("output"):
                testcase_id = d[6:]
                output_dict[testcase_id] = file.read()
            elif d.startswith("input"):
                testcase_id = d[5:]
                input_dict[testcase_id] = file.read()
    
    testcases_ids = sorted(list(input_dict.keys()))
    
    for id in testcases_ids:
        yield input_dict[id], output_dict[id]

def check_is_valid_python(code: str):
    """
    returns True if it's valid Python code
    return False otherwise
    """
    try:
        dis.Bytecode(code)
    except SyntaxError:
        return False 
    return True 
    

def run_code(code : str, problem_path: str, memory_limit_mb: int = 1024) -> str | list[str]:
    """
    Params:
    ---
    code (str): the source code to evalute, in Python!
    problem_path (str): the relative path to the problem's directory
    return (verdicts): either "CE" or a list of verdicts from  [AC, MLE, RTE, TLE, WA]
    """
    
    if not check_is_valid_python(code):
        return "CE"
    
    verdicts = []
    
    resource.setrlimit(resource.RLIMIT_AS, (memory_limit_mb * 1024 * 1024, resource.RLIM_INFINITY))
    
    for input, output in get_testcases(problem_path):
        with open("input_file.txt", "w") as file:
            file.write(input)
        try:
            exec(code)
            
            _, max_memory_used_kb = resource.getrusage(resource.RUSAGE_CHILDREN)
            max_memory_used_mb = max_memory_used_kb / 1024
            
            if max_memory_used_mb > memory_limit_mb:
                verdicts.append("MLE")
                continue

            with open("output_file.txt", "r") as file:
                if file.read() == output:
                    verdicts.append("AC")
                else:
                    verdicts.append("WA")
                
        except Exception:
            verdicts.append("RTE")
            continue 
    
    try:
        os.remove("input_file.txt")
    except FileNotFoundError:
        pass 
    
    try:
        os.remove("output_file.txt")
    except FileNotFoundError:
        pass 

    return verdicts
    
 
class TestCodeEvaluation(unittest.TestCase):

    def test_correct_execution(self):
        code_to_evaluate = """
            print("Hello, World!")
            """

        problem_path = "example_problem"
        memory_limit = 256  

        verdicts = run_code(code_to_evaluate, problem_path, memory_limit)
        self.assertEqual(verdicts, ["AC"])

    def test_memory_limit_exceeded(self):
        code_to_evaluate = """
# Intentionally trying to allocate more memory 
memory_list = [0] * (1024 * 1024 * 1024)  # 1 GB
"""

        problem_path = "example_problem"
        memory_limit = 1  

        verdicts = run_code(code_to_evaluate, problem_path, memory_limit)
        self.assertEqual(verdicts, ["MLE"])

if __name__ == '__main__':
    unittest.main()
