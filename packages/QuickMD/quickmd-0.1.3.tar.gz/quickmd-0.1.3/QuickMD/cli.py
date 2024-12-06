import ast
import os
import argparse


def get_type_hints(function_node):
    """Extract type hints from the function node."""
    if function_node.returns:
        return_type = ast.unparse(function_node.returns)
    else:
        return_type = "None"

    arg_types = {}
    for arg in function_node.args.args:
        if arg.annotation:
            arg_types[arg.arg] = ast.unparse(arg.annotation)
        else:
            arg_types[arg.arg] = "Any"

    return arg_types, return_type


def parse_python_file(file_path: str):
    """Parse given Python file and extract functions, classes, and methods."""
    with open(file_path, "r") as file:
        file_content = file.read()

    tree = ast.parse(file_content)
    functions = []
    classes = []

    class_method_names = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            func_name = node.name
            if func_name in class_method_names:
                continue  # Skip methods already added as class methods
            docstring = ast.get_docstring(node)
            arg_types, return_type = get_type_hints(node)
            functions.append({"name": func_name, "args": arg_types, "return": return_type, "docstring": docstring})
        elif isinstance(node, ast.ClassDef):
            class_name = node.name
            methods = []
            for class_node in node.body:
                if isinstance(class_node, ast.FunctionDef):
                    method_name = class_node.name
                    class_method_names.add(method_name)
                    docstring = ast.get_docstring(class_node)
                    arg_types, return_type = get_type_hints(class_node)

                    methods.append(
                        {"name": method_name, "args": arg_types, "return": return_type, "docstring": docstring}
                    )
            classes.append({"name": class_name, "methods": methods, "docstring": ast.get_docstring(node)})

    return functions, classes


def generate_markdown(file_path: str, functions: list, classes: list, delim: str):
    """Generate a Markdown document from the extracted data."""
    # Create path to final md file
    final_path_build = file_path.split(delim)
    file_name = final_path_build.pop()
    final_path_build = ["QuickMDBuild"] + final_path_build
    final_path_build = "/".join(final_path_build)
    os.makedirs(final_path_build, exist_ok=True)
    doc_name = os.path.splitext(file_name)[0] + ".md"

    final_path = final_path_build + "/" + doc_name

    with open(final_path, "w") as md_file:
        md_file.write(f"# `{file_name}`\n\n")

        # Functions
        if functions:
            md_file.write("## Functions\n\n")
            for func in functions:
                md_file.write(f"### {func['name']}()\n\n")
                md_file.write("**Docstring:**\n")
                if func["docstring"]:
                    for line in func['docstring'].split("\n"):
                        md_file.write(f"> {line}<br/>\n")
                    md_file.write("\n")
                else:
                    md_file.write("> None\n\n")

                md_file.write("**Type Hints:**\n")
                for arg, type_hint in func["args"].items():
                    md_file.write(f"- `{arg}`: `{type_hint}`\n")
                md_file.write(f"- `return`: `{func['return']}`\n\n")

        # Classes
        if classes:
            md_file.write("## Classes\n\n")
            for cls in classes:
                md_file.write(f"### {cls['name']}\n\n")
                md_file.write("**Docstring:**\n")
                if cls["docstring"]:
                    md_file.write(f"> {cls['docstring']}\n\n")
                else:
                    md_file.write("> None\n\n")

                # Methods
                if cls["methods"]:
                    md_file.write("**Methods:**\n\n")
                    for method in cls["methods"]:
                        md_file.write(f"#### {cls['name']}.{method['name']}()\n\n")
                        md_file.write("**Docstring:**\n")
                        if method["docstring"]:
                            for line in method['docstring'].split("\n"):
                                md_file.write(f"> {line}<br/>\n")
                            md_file.write("\n")
                        else:
                            md_file.write("> None\n\n")

                        md_file.write("**Type Hints:**\n")
                        for arg, type_hint in method["args"].items():
                            md_file.write(f"- `{arg}`: `{type_hint}`\n")
                        md_file.write(f"- `return`: `{method['return']}`\n\n")
                else:
                    md_file.write("No methods defined.\n\n")

    print(f"Markdown Document Generated: {doc_name}")


def main():
    parser = argparse.ArgumentParser(
        description="Script that generates an MD file for a Python file."
    )
    parser.add_argument(
        "action", choices=["md"], help="Type of file to create (md)"
    )
    parser.add_argument(
        "--path",
        required=True,
        type=str,
        help="Path to the Python file (e.g., 'src/main.py').",
    )
    parser.add_argument(
        "--delim",
        required=False,
        type=str,
        help="Path delimiter (default='/').",
    )
    args = parser.parse_args()

    delim = args.delim if args.delim else "/"
    path = args.path
    functions, classes = parse_python_file(path)
    generate_markdown(path, functions, classes, delim)
    print("Fin.")


if __name__ == "__main__":
    main()
