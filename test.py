import ast

string = "[1,2,3]\n"

# Convert the string to a list
result = ast.literal_eval(string)

print(result)
