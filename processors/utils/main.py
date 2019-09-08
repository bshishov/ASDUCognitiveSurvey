import sys
import json


def default_main(fn: callable):
    args = sys.argv[1:]
    input_filename = args[0]
    output_filename = args[1]
    with open(input_filename, 'r', encoding='utf-8') as input_file:
        input_data = json.loads(input_file)
        output_data = fn(**input_data)
        with open(output_filename, 'w', encoding='utf-8') as output_file:
            json.dump(output_data, output_file)
