import argparse
from jinja2 import Environment
import pandas as pd
from aind_data_schema_models.utils import to_class_name, to_class_name_underscored
from pathlib import Path
import subprocess


def generate_code(data_type: str, root_path: str, isort: bool = True, black: bool = True):
    """Generate code from the template type

    Parameters
    ----------
    data_type : str
        Which template file to use
    isort : bool, optional
        Whether to run isort on the output, by default True
    black : bool, optional
        Whether to run black on the output, by default True
    """
    ROOT_DIR = Path(root_path)
    data_file = ROOT_DIR / "_generators" / "models" / f"{data_type}.csv"
    template_file = ROOT_DIR / "_generators" / "templates" / f"{data_type}.txt"
    output_file = ROOT_DIR / f"{data_type}.py"

    # Load data
    data = pd.read_csv(data_file)

    # Load template
    with open(template_file) as f:
        template = f.read()

    # Set up Jinja2 environment
    env = Environment()
    env.filters["to_class_name"] = to_class_name
    env.filters["to_class_name_underscored"] = to_class_name_underscored
    rendered_template = env.from_string(template)

    # Render template with data
    rendered_code = rendered_template.render(data=data)

    # Write generated code to file
    with open(output_file, "w") as f:
        f.write(rendered_code)

    print(f"Code generated in {output_file}")

    # Optionally, format with isort and black
    if isort:
        subprocess.run(["isort", str(output_file)])

    if black:
        subprocess.run(["black", str(output_file)])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate code from templates.")
    parser.add_argument("--type", required=True, help="The data type to generate code for (e.g., 'platforms').")
    parser.add_argument(
        "--root-path",
        required=False,
        default="./src/aind_data_schema_models/",
        help="Path to the source folder of the project",
    )
    args = parser.parse_args()

    generate_code(args.type, args.root_path)
