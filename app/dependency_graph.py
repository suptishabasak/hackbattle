import ast


def parse_file(file_path):
    """Read and parse a Python file."""
    
    with open(file_path, "r") as file:
        code = file.read()

    tree = ast.parse(code)

    return tree


def find_imports(tree):
    """Find all imports in the AST."""
    
    dependencies = []

    for node in ast.walk(tree):

        if isinstance(node, ast.Import):
            for alias in node.names:
                dependencies.append(alias.name)

        elif isinstance(node, ast.ImportFrom):
            if node.module:
                dependencies.append(node.module)

    return dependencies

from pathlib import Path


def find_python_files(folder):
    """Find all Python files in a folder."""
    
    python_files = list(Path(folder).rglob("*.py"))
    
    return python_files

def import_to_file(import_name):
    """Convert a Python import name into a possible file path."""

    return import_name.replace(".", "/") + ".py"

def find_dependency_file(import_name, folder):
    """Find the actual Python file for an import."""

    possible_file = Path(folder) / import_to_file(import_name)

    if possible_file.exists():
        return str(possible_file)

    # Try without the first module name
    parts = import_name.split(".")

    if len(parts) > 1:
        possible_file = Path(folder) / import_to_file(".".join(parts[1:]))

        if possible_file.exists():
            return str(possible_file)

    return None

def build_dependency_graph(folder):
    """Build a graph showing which files depend on which files."""

    graph = {}

    files = find_python_files(folder)

    for file in files:
        tree = parse_file(file)
        imports = find_imports(tree)

        dependencies = []

        for import_name in imports:
            dependency_file = find_dependency_file(import_name, folder)

            if dependency_file:
                dependencies.append(dependency_file)

        graph[str(file)] = dependencies

    return graph


if __name__ == "__main__":
    graph = build_dependency_graph(".")

    print("Dependency Graph:")

    for file, dependencies in graph.items():
        print(f"\n{file} depends on:")

        for dependency in dependencies:
            print(f"  -> {dependency}")

def get_affected_files(graph, changed_file):
    """Find all files that depend on the changed file."""

    affected = []

    for file, dependencies in graph.items():
        if changed_file in dependencies:
            affected.append(file)

            # Find files affected by this file too
            affected += get_affected_files(graph, file)

    return list(set(affected))


def get_affected_tests(graph, changed_file):
    """Find tests that may be affected by a changed file."""

    affected_files = get_affected_files(graph, changed_file)

    affected_tests = []

    for file in affected_files:
        if file.startswith("tests/"):
            affected_tests.append(file)

    return affected_tests

print("\nAffected files:")
print(get_affected_files(graph, "github_client.py"))

print("\nAffected tests:")
print(get_affected_tests(graph, "app/sample_code.py"))