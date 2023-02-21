import os
import re


class Function:
    def __init__(self, name, arguments, return_type):
        self.name = name
        self.arguments = arguments
        self.return_type = return_type

    def __repr__(self):
        return f"{self.return_type} {self.name}({', '.join(self.arguments)})"


class GlobalVariable:
    def __init__(self, name, type):
        self.name = name
        self.type = type

    def __repr__(self):
        return f"{self.type} {self.name}"


class Method:
    def __init__(self, name, arguments, return_type):
        self.name = name
        self.arguments = arguments
        self.return_type = return_type

    def __repr__(self):
        return f"{self.return_type} {self.name}({', '.join(self.arguments)})"


class Field:
    def __init__(self, name, type):
        self.name = name
        self.type = type

    def __repr__(self):
        return f"{self.type} {self.name}"


class Class:
    def __init__(self, name):
        self.name = name
        self.methods = []
        self.fields = []

    def add_method(self, method):
        self.methods.append(method)

    def add_field(self, field):
        self.fields.append(field)

    def __repr__(self):
        return f"class {self.name}"


def parse_file(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()

    functions = []
    global_variables = []
    classes = []
    current_class_name = None
    current_class = None

    for line in lines:
        line = line.strip()
        if line.startswith('class '):
            class_name = line.split(' ')[1]
            current_class_name = class_name
            current_class = Class(class_name)
            classes.append(current_class)
        elif re.search(r'^\s*};', line):
            current_class_name = None
            current_class = None
        elif current_class_name and re.search(r'^\s*(\w+)\s+(\w+)\s*\(.*\)\s*;', line):
            method_name = re.search(r'^\s*(\w+)\s+(\w+)\s*\(.*\)\s*;', line).group(2)
            method_return_type = re.search(r'^\s*(\w+)\s+(\w+)\s*\(.*\)\s*;', line).group(1)
            method_args = re.search(r'^\s*(\w+)\s+\w+\s*\((.*)\)\s*;', line).group(2)
            method_args = re.sub(r'/\*.*\*/', '', method_args)
            method_args = re.sub(r'//.*', '', method_args)
            method_args = re.sub(r'\s+', ' ', method_args).strip()
            method_args = re.split(r',\s*', method_args)
            method = Method(method_name, method_args, method_return_type)
            current_class.add_method(method)
        elif current_class_name and re.search(r'^\s*(\w+)\s+(\w+)\s*;', line):
            field_name = re.search(r'^\s*(\w+)\s+(\w+)\s*;', line).group(2)
            field_type = re.search(r'^\s*(\w+)\s+(\w+)\s*;', line).group(1)
            field = Field(field_name, field_type)
            current_class.add_field(field)
        elif re.search(r'^\s*(\w+)\s+(\w+)\s*\(.*\)\s*;', line):
            function_name = re.search(r'^\s*(\w+)\s+(\w+)\s*\(.*\)\s*;', line).group(2)
            function_args = re.search(r'^\s*(\w+)\s+\w+\s*\((.*)\)\s*;', line).group(2)
            function_args = re.sub(r'/\*.*\*/', '', function_args)
            function_args = re.sub(r'//.*', '', function_args)
            function_args = re.sub(r'\s+', ' ', function_args).strip()
            function_args = re.split(r',\s*', function_args)
            function_return_type = re.search(r'^\s*(\w+)\s+(\w+)\s*\(.*\)\s*;', line).group(1)
            function = Function(function_name, function_args, function_return_type)
            functions.append(function)
        elif re.search(r'^\s*(\w+)\s+(\w+)\s*;', line):
            global_variable_name = re.search(r'^\s*(\w+)\s+(\w+)\s*;', line).group(2)
            global_variable_type = re.search(r'^\s*(\w+)\s+(\w+)\s*;', line).group(1)
            global_variable = GlobalVariable(global_variable_name, global_variable_type)
            global_variables.append(global_variable)

    return functions, global_variables, classes


if __name__ == '__main__':
    directory_path = "C:\\Projekty\\LushLandsGithub\\LushLands\\"
    for filename in os.listdir(directory_path):
        if filename.endswith(".h"):
            file_path_ = os.path.join(directory_path, filename)
            header_data = parse_file(file_path_)
            print()
