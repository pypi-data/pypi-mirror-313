import os
import shutil
import sys
from enum import Enum
from typing import Dict

import click
from jinja2 import Environment, PackageLoader

from deeploy._version import __version__
from deeploy.cli.utils import validate_project_name

ALLOWED_TYPES = ["model", "explainer", "transformer"]

env = Environment(loader=PackageLoader("deeploy", "cli/templates"), autoescape=True)


class Instances(Enum):
    model = "model"
    explainer = "explainer"
    transformer = "transformer"

    def __str__(self):
        return self.value


@click.group()
@click.version_option(__version__)
def cli():
    pass


@cli.command()
@click.option(
    "--name",
    "-n",
    prompt="Name of Project",
    help="Provide name of the project to be initialized.",
    callback=validate_project_name,
)
@click.option(
    "--initialization",
    "-i",
    default=["model"],
    help="State for which components the templates should be generated.\n\
        Three options: -i model -i transformer -i explainer.\n\
        Select one or more.",
    multiple=True,
)
def generate_template(name, initialization):
    """Generates Sample Docker Image Template for Custom Docker Image"""
    # catch unknown type
    if not set(initialization).issubset(set(ALLOWED_TYPES)):
        raise RuntimeError("Initialization types can only be model, explainer or transformer.")

    projectname = name

    click.echo(f"Creating Project '{projectname}'.")
    os.makedirs(projectname, exist_ok=True)

    template_vars = {
        "projectname": projectname,
        "model": True if Instances.model.value in initialization else False,
        "explainer": True if Instances.explainer.value in initialization else False,
        "transformer": True if Instances.transformer.value in initialization else False,
        "version": __version__,
    }
    generate_readme(projectname, template_vars)
    click.echo("Generated README.")

    generate_metadata(projectname)
    click.echo("Generated metadata.")

    generate_script(projectname, template_vars)
    click.echo("Generated build script.")

    if Instances.explainer.value in initialization:
        response = generate_instance(projectname, template_vars, Instances.explainer.value)
        if response:
            click.echo("Docker Image Template for explainer is generated.")
        else:
            click.echo(f"Skipping {Instances.explainer.value} since the files already exists")

    if Instances.model.value in initialization:
        response = generate_instance(projectname, template_vars, Instances.model.value)
        if response:
            click.echo(f"Docker Image Template for {Instances.model.value} is generated.")
        else:
            click.echo(f"Skipping {Instances.model.value} since the files already exists")

    if Instances.transformer.value in initialization:
        response = generate_instance(projectname, template_vars, Instances.transformer.value)
        if response:
            click.echo(f"Docker Image Template for {Instances.transformer.value} is generated.")
        else:
            click.echo(f"Skipping {Instances.transformer.value} since the files already exists")

    click.echo(f"All templates for project '{projectname}' have been created!")


def generate_metadata(projectname: str):
    """Generates metadata.json file"""
    templates_metadata = env.get_template("metadata.json.j2")
    content_metadata = templates_metadata.render({})
    with open(os.path.join(projectname, "metadata.json"), "w+") as metadata_file:
        metadata_file.write(content_metadata)


def generate_readme(projectname: str, template_vars: Dict):
    """Generates Primary Readme file"""
    templates_readme = env.get_template("README.md.j2")
    content_readme = templates_readme.render(template_vars)
    with open(os.path.join(projectname, "README.md"), "w+") as readme_file:
        readme_file.write(content_readme)


def generate_script(projectname: str, template_vars: Dict):
    """Generates Script file"""
    templates_script = env.get_template("build.sh.j2")
    content_script = templates_script.render(template_vars)
    with open(os.path.join(projectname, "build.sh"), "w+") as script_file:
        script_file.write(content_script)


def generate_instance(projectname: str, template_vars: Dict, instance_type: str):
    """Generates subdirectories and files of provided instance type"""
    template_vars["instance"] = instance_type
    generate_folder = projectname + "_" + instance_type
    if not os.path.exists(os.path.join(projectname, generate_folder)):
        os.mkdir(os.path.join(projectname, generate_folder))
    else:
        return False

    # generate sample files
    templates_dockerfile = env.get_template(f"{instance_type}/Dockerfile.j2")
    templates_main = env.get_template(f"{instance_type}/__main__.py.j2")
    templates_sample_wrapper = env.get_template(f"{instance_type}/sample_{instance_type}.py.j2")
    templates_requirements = env.get_template(f"{instance_type}/requirements.txt.j2")

    content_dockerfile = templates_dockerfile.render(template_vars)
    with open(os.path.join(projectname, generate_folder, "Dockerfile"), "w+") as file:
        file.write(content_dockerfile)

    content_requirements = templates_requirements.render(template_vars)
    with open(
        os.path.join(
            projectname,
            generate_folder,
            "requirements.txt",
        ),
        "w+",
    ) as file:
        file.write(content_requirements)

    content_main = templates_main.render(template_vars)
    with open(
        os.path.join(
            projectname,
            generate_folder,
            "__main__.py",
        ),
        "w+",
    ) as file:
        file.write(content_main)

    content_sample_wrapper = templates_sample_wrapper.render(template_vars)
    with open(
        os.path.join(
            projectname,
            generate_folder,
            f"sample_{instance_type}.py",
        ),
        "w+",
    ) as file:
        file.write(content_sample_wrapper)

    # copy model and explainer objects
    pkgdir = sys.modules[str(sys.modules[__name__].__name__).split(".")[0]].__path__[0]
    if instance_type == Instances.explainer.value:
        shutil.copy(
            pkgdir + f"/cli/templates/{instance_type}/{instance_type}.dill",
            os.path.join(
                projectname,
                generate_folder,
                f"{instance_type}.dill",
            ),
        )
    if instance_type == Instances.model.value:
        shutil.copy(
            pkgdir + f"/cli/templates/{instance_type}/{instance_type}.bst",
            os.path.join(
                projectname,
                generate_folder,
                f"{instance_type}.bst",
            ),
        )

    # generate reference
    if not os.path.exists(os.path.join(projectname, instance_type)):
        os.mkdir(os.path.join(projectname, instance_type))
    templates_reference = env.get_template("reference.json.j2")
    content_reference = templates_reference.render(template_vars)
    with open(os.path.join(projectname, instance_type, "reference.json"), "w+") as file:
        file.write(content_reference)

    return True


def main():
    cli()
