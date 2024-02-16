

import unittest
import textwrap 
import ast

def check_imports(code):
    allowed_libs = set(['sys', 'os', 'json'])
    tree = ast.parse(code)

    for node in ast.walk(tree):
        if isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
            for alias in node.names:
                if alias.name not in allowed_libs:
                    raise Exception(f"Import of non-standard library detected: {alias.name}")
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == '__import__':
            if node.args and isinstance(node.args[0], ast.Str):
                module_name = node.args[0].s
                if module_name not in allowed_libs:
                    raise Exception(f"Import of non-standard library detected: {module_name}")



class TestCheckImports(unittest.TestCase):
    def test_allowed_imports(self):
        """Test code with only allowed imports."""
        code = textwrap.dedent("""
        import os
        import sys
        import json
        """)
        try:
            check_imports(code)
        except Exception as e:
            self.fail(f"Unexpected exception for allowed imports: {e}")

    def test_disallowed_imports(self):
        """Test code with a disallowed import."""
        code = textwrap.dedent("""
        import requests
        """)
        with self.assertRaises(Exception) as context:
            check_imports(code)
        self.assertIn("Import of non-standard library detected: requests", str(context.exception))

    def test_no_imports(self):
        """Test code with no imports."""
        code = textwrap.dedent("""
        def foo():
            return 'bar'
        """)
        try:
            check_imports(code)
        except Exception as e:
            self.fail(f"Unexpected exception for code without imports: {e}")

    def test_edge_case_imports(self):
        """Test code that might trick the static analysis."""
        code = textwrap.dedent("""
        __import__("requests")
        """)
        with self.assertRaises(Exception) as context:
            check_imports(code)
        self.assertIn("Import of non-standard library detected:", str(context.exception))

if __name__ == "__main__":
    unittest.main()

