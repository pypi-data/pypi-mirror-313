import typer
import yaml
import json

from typing import Optional, Annotated
from jinja2 import Template

app = typer.Typer()


@app.command()
def generate(template: str, output: str, variable_file_path: Annotated[Optional[str], typer.Argument()] = None):
    with open(template) as template_file:
        template = Template(template_file.read())
        variables = {}
        if variable_file_path:
            with open(variable_file_path) as variable_file:
                if variable_file_path.endswith(".json"):
                    variables = json.load(variable_file)
                elif variable_file_path.endswith(".yaml") or variable_file_path.endswith(".yml"):
                    variables = yaml.safe_load(variable_file)
        with open(output, "w") as output_file:
            output_file.write(template.render(variables))
