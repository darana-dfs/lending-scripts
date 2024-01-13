import argparse
import json
import boto3
import os
import sys
from string import Template
from dynamodb_helper import create_table, put_item

base_path = os.path.split(os.path.abspath(sys.argv[0]))[0]

TEMPLATES_PATH = os.path.join(base_path, "resources/templates")

def replace_dict_values(base_string, value_dict):
    for key, value in value_dict.items():
        base_string = base_string.replace(key, value)
    return base_string

def get_template_map():
    template_map = {}
    for filename in os.listdir(TEMPLATES_PATH):
        template_path = os.path.join(TEMPLATES_PATH, filename)
        template_map[filename] = {
            'path': template_path
        }
    return template_map
   
template_map = get_template_map()

def get_template_context(template_path, context_id):
    context_path = os.path.join(template_path, "context", context_id + ".json")
    if not os.path.isfile(context_path):
        raise argparse.ArgumentTypeError('Invalid context id')
    with open(context_path, 'r') as f:
        json_data = json.load(f)
    return json_data
     
def get_custom_context(attributes):
    custom_context = {}
    if attributes is not None:
        for attribute in attributes:
            key, value = attribute.split("=")
            custom_context[key] = value
    return custom_context
    
def template_type(argument):
    if argument not in template_map:
        raise argparse.ArgumentTypeError('Invalid template type')
    return template_map[argument]

def custom_context_type(argument):
    try:
        return json.loads(argument)
    except ValueError:
        raise argparse.ArgumentTypeError('Invalid JSON string')
    
def template_context(argument):
    try:
        return json.loads(argument)
    except ValueError:
        raise argparse.ArgumentTypeError('Invalid JSON string')

def clean_raw_json(raw_json):
    return ''.join(raw_json.splitlines())
    
def get_clean_context(context):
    clean_context = {}
    for key, value in context.items():
        clean_context[key] = "null" if value is None else value
    return clean_context

def process_dynamo_attribute(item):
    for key, value in item.items():
        if(value is None):
            return {
                'NULL': True
            }
    return item

def clean_parsed_item(item):
    clean_item = {}
    for key, value in item.items():
        clean_item[key] = process_dynamo_attribute(value)
    return clean_item

def parse_item(item_path, context):
    clean_context = get_clean_context(context)
    with open(item_path) as item_file:
        item_template = clean_raw_json(item_file.read())
        print("Raw Item \n" + item_template)
        item = Template(item_template).substitute(clean_context)
        item = replace_dict_values(item, {"\"null\"": "null"})
        print("Parsed Item \n" + item)
        return clean_parsed_item(json.loads(item))
    
def parse_table(table_path):
    with open(table_path) as table_file:
        return json.loads(table_file.read())

# Create the parser and add arguments
parser = argparse.ArgumentParser()
parser.add_argument(
    '-t', '--template', 
    dest='template', required=True, 
    type=template_type  ,help="Template to use"
)
parser.add_argument(
    '-c', '--context', 
    dest='context_id', default="default" ,type=str,
    help="JSON context to populate template with"
)

parser.add_argument(
    '-cc', '--custom-context', 
    dest='custom_context', default="{}" ,type=custom_context_type,
    help="JSON context to populate template with"
)

parser.add_argument(
    '-l', '--localhost', 
    dest='is_localhost', action='store_true', 
    help='Enable localhost mode, script will use http://localhost:8000 as endpoint url'
)
parser.add_argument(
    '-a', '--attribute', 
    dest='attribute', nargs='+', 
    help='List of context attributes to process'
)
parser.add_argument(
    '-cf', '--context-file', 
    dest='context_file', type=argparse.FileType('r'), 
    help='JSON context file to populate template with'
)

# Parse and print the results
args = parser.parse_args()

template = args.template
template_path = template['path']
is_localhost = args.is_localhost
endpoint_url = "http://localhost:8000" if is_localhost else None
dynamodb_client = boto3.client("dynamodb", endpoint_url=endpoint_url)

context = get_template_context(template_path, args.context_id)
if args.custom_context is not None:
    context.update(args.custom_context)

print("Template Context \n" + json.dumps(context, indent=4))

items_path = os.path.join(template_path, "items")

tables = {}
tables_path = os.path.join(template_path, "tables")
for filename in os.listdir(tables_path):
    template_id = os.path.splitext(filename)[0]
    tables[template_id] = {
        "filename": filename,
        "parsed_table": parse_table(os.path.join(tables_path, filename))
    }

for table_id, table in tables.items():
    create_table(table['parsed_table'], dynamodb_client)
    
items = {}
for table_name in os.listdir(items_path):
    for item_filename in os.listdir(os.path.join(items_path, table_name)):
        template_id = os.path.splitext(item_filename)[0]
        items[template_id] = {
            "table_name": table_name,
            "filename": item_filename,
            "parsed_item": parse_item(os.path.join(items_path, table_name, item_filename), context)
        }

for item_id, item in items.items():
    put_item(item['table_name'], item['parsed_item'], dynamodb_client)