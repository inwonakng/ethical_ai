from Generator import Generator
import yaml
import json
from pathlib import Path

import argparse

parser = argparse.ArgumentParser(description='Generate scene from rule')
parser.add_argument('file', metavar='FILE', type=str, nargs=1,
                    help='Rule file, in yaml')

args = parser.parse_args()
file_path = Path(args.file[0])
yaml_path = str(file_path.resolve())
yaml_filename = file_path.name
rule = {}
with open(args.file[0], 'r') as stream:
    try:
        rule = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

# feed to generator

generator = Generator(rule=rule)
data = generator.extended_options

with open('{}.json'.format(yaml_filename.split('.')[0]), 'w') as f:
    json.dump(data, f)
