from functions.write_file import write_file

print("Result for writing to calculator/lorem.txt with content:")
print(write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum"))

print("\nResult for writing to calculator/pkg/morelorem.txt with content:")
print(write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"))

print("\nResult for writing to calculator/tmp/temp.txt with content:")
print(write_file("calculator", "/tmp/temp.txt", "this should not be allowed"))

