from functions.run_python_file import run_python_file

print("Result for calculator's usage instructions:")
print(run_python_file("calculator", "main.py"))

print("\nResult for running the calculator:")
print(run_python_file("calculator", "main.py", ["3 + 5"]))

print("\nResult for running the calculator's tests successfully:")
print(run_python_file("calculator", "tests.py"))

print("This result should return an error):")
print(run_python_file("calculator", "../main.py"))

print("This result should return an error):")
print(run_python_file("calculator", "nonexistent.py"))

print("This result should return an error):")
print(run_python_file("calculator", "lorem.txt"))