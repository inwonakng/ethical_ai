from Generator import Generator
import yaml
import json
from pathlib import Path
from django.conf import settings
import argparse

# parser = argparse.ArgumentParser(description='Generate scene from rule')
# parser.add_argument('file', metavar='FILE', type=str, nargs=1,
#                     help='Rule file, in yaml')

# args = parser.parse_args()
# file_path = Path(args.file[0])
fp = 'ethicssite/survey/generation/rule/rule.json'
file_path = Path(fp)
yaml_path = str(file_path.resolve())
yaml_filename = file_path.name
rule = {}
with open(fp, 'r') as stream:
    try:
        rule = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

# feed to generator
# print(rule)
# quit()

generator = Generator(rule=rule)
data = generator.get_scenario(3)

with open('{}.json'.format(yaml_filename.split('.')[0]), 'w') as f:
    json.dump(data, f)
