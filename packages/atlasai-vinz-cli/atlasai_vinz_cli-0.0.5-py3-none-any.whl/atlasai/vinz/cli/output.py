import csv
import io
import json

from rich.console import Console
from rich.table import Table
from rich.syntax import Syntax

import yaml

console = Console()

def output_result(ctx, result, no_wrap_columns=None):
    if no_wrap_columns is None:
        no_wrap_columns = []
    output = ctx.obj['config'].get('output', 'yaml')
    if output.lower() == 'json':
        data = json.dumps(result, indent=4)
        console.print_json(data)
    elif output.lower() == 'table':
        data = json_to_table(result, no_wrap_columns)
        console.print(data)
    elif output.lower() == 'csv':
        data = json_to_csv(result)
        console.print(data)
    else:
        data = yaml.dump(result, default_flow_style=False)
        console.print(Syntax(data, 'yaml'))


def json_to_table(data, no_wrap_columns=None):
    if no_wrap_columns is None:
        no_wrap_columns = []
    if not data:
        return ''
    if not isinstance(data, list):
        data = [data]
    table = Table(title='')
    for key in sorted(data[0].keys()):
        if key in no_wrap_columns:
            table.add_column(key.title(), justify='right', no_wrap=True)
        else:
            table.add_column(key.title(), justify='right')
    for record in data:
        d = []
        for key in sorted(record.keys()):
            value = record[key]
            if not isinstance(value, str):
                d.append(json.dumps(value))
            else:
                d.append(value)
        table.add_row(*d)
    return table

def json_to_csv(data):
    if not data:
        return ''
    if not isinstance(data, list):
        data = [data]
    output = io.StringIO()

    csv_writer = csv.DictWriter(output, fieldnames=sorted(data[0].keys()))
    csv_writer.writeheader()
    csv_writer.writerows(data)

    content = output.getvalue()
    output.close()
    return content

def output_message(output, style=None, newline=False):
    console.print(output, style=style)
    if newline:
        console.print("\n")
