# /// script
# requires-python = ">=3.14"
# dependencies = [
#     "jinja2>=3.1.6",
#     "pyyaml>=6.0.3",
# ]
# ///
import os
from pathlib import Path
from contextlib import chdir
import argparse

import yaml
from jinja2 import Environment, FileSystemLoader

## Default paths

REPO_ROOT = Path(__file__).parent.parent
DATA_DIR = REPO_ROOT / ".raw"
TEMPLATES_DIR = REPO_ROOT / ".templates"

DATA_FILENAME = DATA_DIR / "data.yml"
TEMPLATE_FILENAME = "README.md.j2"
OUTPUT_FILENAME = "test.README.md"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        "generate-readme",
        description="Render README.md template using data from input file.",
    )

    parser.add_argument(
        "-f",
        "--data-file",
        type=str,
        default=DATA_FILENAME,
        help="Path to read data from. Loads from dir. Default: .raw/data.yml",
    )
    parser.add_argument(
        "-t",
        "--template-file",
        type=str,
        default=TEMPLATE_FILENAME,
        help="Template file to generate output file from. Loads from .templates/ dir. Default: README.md.j2",
    )
    parser.add_argument(
        "-o",
        "--output-file",
        type=str,
        default=OUTPUT_FILENAME,
        help="Generated file output. Default: README.md",
    )

    args = parser.parse_args()

    return args


def main(
    data_file: str | Path,
    templates_dir: str | Path,
    template_file: str,
    output_file: str | Path,
):
    data_file: Path = Path(f"{data_file}")
    templates_dir: Path = Path(f"{templates_dir}")
    output_file: Path = Path(f"{output_file}")

    with data_file.open() as file:
        data = yaml.safe_load(file)

    ## Set jinja environment
    env = Environment(
        loader=FileSystemLoader(templates_dir),
        trim_blocks=True,
        lstrip_blocks=True,
    )

    ## Load the README template
    template = env.get_template(template_file)

    ## Render data from file to README template. Ensure newline at end of file.
    readme = template.render(data=data).rstrip() + "\n"

    (output_file).write_text(readme)


if __name__ == "__main__":
    ## Path where script was called from
    CWD = Path.cwd()

    ## cd to repo root
    try:
        args = parse_args()
        os.chdir(REPO_ROOT)

        main(
            data_file=args.data_file,
            templates_dir=TEMPLATES_DIR,
            template_file=args.template_file,
            output_file=args.output_file,
        )
    finally:
        os.chdir(CWD)
