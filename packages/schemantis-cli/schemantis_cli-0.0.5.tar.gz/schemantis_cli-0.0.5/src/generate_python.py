from click import echo
import string
import random
import os

JSON_PYTHON_TYPE_MAP = {
    "string": "str",
    "number": "float",
    "boolean": "bool",
    "object": "dict",
    "array": "list",
}


def get_subSchema_by_path(schema, path):
    if len(path) == 0:
        return schema
    if len(path) == 1:
        return schema.properties[path[0]]
    return get_subSchema_by_path(schema.properties[path[0]], path[1:])


def generate_random_string():
    return "".join(
        random.choice(string.ascii_uppercase + string.digits) for _ in range(10)
    )


def generate_random_float():
    return random.uniform(1, 100)


def generate_random_bool():
    return bool(random.getrandbits(1))


def generate_random_data(py_type_str):
    if py_type_str == "str":
        return generate_random_string()
    if py_type_str == "float":
        return generate_random_float()
    if py_type_str == "bool":
        return generate_random_bool()
    if py_type_str == "list":
        return [generate_random_string() for _ in range(10)]
    if py_type_str == "dict":
        return {generate_random_string(): generate_random_string() for _ in range(10)}


def set_by_path(object, path, value):
    if len(path) == 0:
        return value
    if len(path) == 1:
        return {**(object or {}), path[0]: value}
    return {
        **(object or {}),
        path[0]: set_by_path(object.get(path[0], {}), path[1:], value),
    }


def build_map_dict(schemantis_map):
    result = {}
    for intermediate_edge in schemantis_map.intermediate.edges:
        if intermediate_edge.target[0] == "intermediate":
            continue

        result = set_by_path(result, intermediate_edge.target, intermediate_edge.source)
    return result


def format_path(path):
    return f"{path[0]}['{"']['".join(path[1:])}']"


def format_leaf(path, intermediate_node_incoming_edges):
    if path[0] == "intermediate":
        args = [
            format_path(e.source) for e in intermediate_node_incoming_edges[path[1]]
        ]
        return f"{path[1]}({','.join(args)})"
    return format_path(path)


def stringify_dict(d, intermediate_node_incoming_edges):
    result = "{"
    for k, v in d.items():
        result += f"'{k}':"

        if isinstance(v, dict):
            result += stringify_dict(v, intermediate_node_incoming_edges)
        else:
            result += format_leaf(v, intermediate_node_incoming_edges)

        result += ","
    result += "}"
    return result


def generate_python(schemantis_map, output_directory):
    echo(f"Generating Python translator based on map '{schemantis_map.name}'...")

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    lower_map_name = schemantis_map.name.lower()

    intermediate_functions_file = os.path.join(
        output_directory, f"{lower_map_name}_intermediate_functions.py"
    )
    intermediate_tests_file = os.path.join(
        output_directory, f"{lower_map_name}_intermediate_function_tests.py"
    )
    main_file = os.path.join(output_directory, f"{lower_map_name}.py")

    if os.path.exists(intermediate_functions_file):
        echo(
            f"Intermediate functions file '{intermediate_functions_file}' already exists."
        )
    else:
        with open(intermediate_functions_file, "w") as f:
            f.write(f"""""")

    if os.path.exists(intermediate_tests_file):
        echo(
            f"Intermediate function tests file '{intermediate_tests_file}' already exists."
        )
    else:
        with open(intermediate_tests_file, "w") as f:
            f.write(
                f"""
from unittest import TestCase, main
from {lower_map_name}_intermediate_functions import *
                           
class TestIntermediateFunctions(TestCase):
"""
            )

    intermediate_nodes = schemantis_map.intermediate.nodes
    intermediate_edges = schemantis_map.intermediate.edges

    source_schema = schemantis_map.source.var_schema
    target_schema = schemantis_map.target.var_schema

    intermediate_node_incoming_edges = {}

    for intermediate_node in intermediate_nodes:
        intermediate_node_name = intermediate_node.name

        input_arg_names_and_types = {}
        output_types = set()
        incoming_edges = []

        for intermediate_edge in intermediate_edges:
            if (
                intermediate_edge.source[0] == "intermediate"
                and intermediate_edge.source[1] == intermediate_node_name
            ):
                output_schema = get_subSchema_by_path(
                    target_schema, intermediate_edge.target[1:]
                )
                output_json_type = output_schema.type
                output_python_type = JSON_PYTHON_TYPE_MAP[output_json_type]
                output_types.add(output_python_type)
            elif (
                intermediate_edge.target[0] == "intermediate"
                and intermediate_edge.target[1] == intermediate_node_name
            ):
                input_schema = get_subSchema_by_path(
                    source_schema, intermediate_edge.source[1:]
                )
                input_json_type = input_schema.type
                input_python_type = JSON_PYTHON_TYPE_MAP[input_json_type]
                arg_name = intermediate_edge.source[-1]
                input_arg_names_and_types[arg_name] = input_python_type
                incoming_edges.append(intermediate_edge)

        if len(output_types) > 1:
            raise Exception("MULTIPLE OUTPUT TYPES")

        output_type = list(output_types)[0]

        new_intermediate_function = f"""
def {intermediate_node_name}({', '.join([f'{arg_name}: {arg_type}' for arg_name, arg_type in input_arg_names_and_types.items()])}) -> {output_type}:
    #TODO
    raise NotImplemented
"""
        new_intermediate_function_test = f"""
\tdef test_{intermediate_node_name}(self):
{'\n'.join([
    f'\t\t{arg_name} = "{generate_random_data(arg_type)}"' for arg_name, arg_type in input_arg_names_and_types.items()
])}
\t\tresponse = {intermediate_node_name}({', '.join([arg_name for arg_name in input_arg_names_and_types])})
\t\tassert isinstance(response, {output_type})
"""

        # Check if intermediate node name is in intermediate function file
        if (
            f"def {intermediate_node_name}("
            not in open(intermediate_functions_file).read()
        ):
            with open(intermediate_functions_file, "a") as f:
                f.write(new_intermediate_function)

        # Check if intermediate node name is in intermediate function test file
        if (
            f"def test_{intermediate_node_name}("
            not in open(intermediate_tests_file).read()
        ):
            with open(intermediate_tests_file, "a") as f:
                f.write(new_intermediate_function_test)

        intermediate_node_incoming_edges[intermediate_node_name] = incoming_edges

    map_dict = build_map_dict(schemantis_map)
    string_dict = stringify_dict(
        map_dict[schemantis_map.target.name], intermediate_node_incoming_edges
    )

    if os.path.exists(main_file):
        echo("Main file already exists.")
    else:
        with open(main_file, "w") as f:
            f.write(
                f"""
from {lower_map_name}_intermediate_functions import *

def {lower_map_name}({schemantis_map.source.name}: dict):
    return {string_dict}
"""
            )
