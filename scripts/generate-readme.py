# /// script
# requires-python = ">=3.14"
# dependencies = [
#     "jinja2>=3.1.6",
#     "pyyaml>=6.0.3",
# ]
# ///
import os
from pathlib import Path
import argparse
import logging

import yaml
from jinja2 import Environment, FileSystemLoader

log = logging.getLogger(__name__)

## Default paths

REPO_ROOT = Path(__file__).parent.parent
DATA_DIR = REPO_ROOT / ".raw"
TEMPLATES_DIR = REPO_ROOT / ".templates"

LOG_LEVEL: str = "INFO"

DATA_FILENAME = DATA_DIR / "data.yml"
TEMPLATE_FILENAME = "README.md.j2"
OUTPUT_FILENAME = "test.README.md"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        "generate-readme",
        description="Render README.md template using data from input file.",
    )

    parser.add_argument(
        "--log-level",
        "--level",
        type=str,
        default=LOG_LEVEL,
        help="Logging level. Options: DEBUG, INFO, WARNING, ERROR, CRITICAL",
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
    log.info("Starting template render")

    data_file: Path = Path(f"{data_file}")
    templates_dir: Path = Path(f"{templates_dir}")
    output_file: Path = Path(f"{output_file}")

    _template_file = templates_dir / template_file

    log.debug(f"""Paths:
    data_file={data_file} (exists: {data_file.exists()})
    templates_dir={templates_dir} (exists: {templates_dir.exists()})
    template_file={_template_file} (exists: {_template_file.exists()})
    output_file={output_file} (exists: {output_file.exists()})
""")

    log.info(f"Reading template data from {data_file}")
    with data_file.open() as file:
        data = yaml.safe_load(file)

    log.info("Preparing render environment")
    ## Set jinja environment
    env = Environment(
        loader=FileSystemLoader(templates_dir),
        trim_blocks=True,
        lstrip_blocks=True,
    )

    log.info(f"Loading template: {_template_file}")
    ## Load the README template
    template = env.get_template(template_file)

    ## Render data from file to README template. Ensure newline at end of file.
    log.info("Rendering template")
    try:
        readme = template.render(data=data).rstrip() + "\n"

        log.debug("Rendered template:\n%s", readme)

        (output_file).write_text(readme)
    except Exception as exc:
        log.error(f"({type(exc).__name__}) Failed rendering template: {exc}")

    log.info(f"Template rendered to: {output_file}")


if __name__ == "__main__":
    ## Path where script was called from
    CWD = Path.cwd()

    args = parse_args()

    ## Configure logging
    logging.basicConfig(
        level=args.log_level.upper(),
        format="%(asctime)s | [%(levelname)s] | %(pathname)s:%(lineno)d :: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    log.debug("DEBUG logging enabled")

    ## cd to repo root
    try:
        log.debug(f"Changing path to: {REPO_ROOT}")
        os.chdir(REPO_ROOT)

        log.debug(f"""Config:
    log_level={args.log_level}
    data_file={args.data_file}
    templates_dir={TEMPLATES_DIR}
    template_file={args.template_file}
    output_file={args.output_file}
""")
        main(
            data_file=args.data_file,
            templates_dir=TEMPLATES_DIR,
            template_file=args.template_file,
            output_file=args.output_file,
        )
    finally:
        os.chdir(CWD)
