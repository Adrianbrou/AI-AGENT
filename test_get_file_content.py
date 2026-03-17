from functions.get_file_content import get_file_content

print("Result for 'lorem.txt' file")
print((get_file_content("calculator", "lorem.txt")))

print("Result for 'main.py' file")
print(get_file_content("calculator", "main.py"))

print("\nResult for 'pkg/calculator.py' file:")
print(get_file_content("calculator", "pkg/calculator.py"))

print("\nResult for '/bin/cat' file:")
print(get_file_content("calculator", "/bin/cat") )

print("\nResult for 'pkg/does_not_exist.py' file:")
print(get_file_content("calculator", "pkg/does_not_exist.py"))