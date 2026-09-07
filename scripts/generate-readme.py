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

import yaml
from jinja2 import Environment, FileSystemLoader

## Default paths

REPO_ROOT = Path(__file__).parent.parent
DATA_DIR = REPO_ROOT / ".raw"
TEMPLATES_DIR = REPO_ROOT / ".templates"

DATA_FILE = DATA_DIR / "data.yml"





def main():
    with DATA_FILE.open() as file:
        data = yaml.safe_load(file)

    ## Set jinja environment
    env = Environment(
        loader=FileSystemLoader(TEMPLATES_DIR),
        trim_blocks=True,
        lstrip_blocks=True,
    )

    ## Load the README template
    template = env.get_template("README.md.j2")

    ## Render data from file to README template. Ensure newline at end of file.
    readme = template.render(data=data).rstrip() + "\n"

    (REPO_ROOT / "README.test.md").write_text(readme)


if __name__ == "__main__":
    ## Path where script was called from
    CWD = Path.cwd()

    ## cd to repo root
    try:
        os.chdir(REPO_ROOT)
        main()
    finally:
        os.chdir(CWD)
