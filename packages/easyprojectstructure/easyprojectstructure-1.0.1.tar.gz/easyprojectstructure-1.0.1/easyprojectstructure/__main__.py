import os
import fnmatch
import sys
import argparse

# Exclusion patterns similar to .gitignore
exclusion_patterns = [
    "__pycache__/",
    "*.py[cod]",
    "*$py.class",
    "*.so",
    ".Python",
    "build/",
    "develop-eggs/",
    "dist/",
    "downloads/",
    "eggs/",
    ".eggs/",
    "lib/",
    "lib64/",
    "parts/",
    "sdist/",
    "var/",
    "wheels/",
    "share/python-wheels/",
    "*.egg-info/",
    ".installed.cfg",
    "*.egg",
    "MANIFEST",
    "*.manifest",
    "*.spec",
    "pip-log.txt",
    "pip-delete-this-directory.txt",
    "htmlcov/",
    ".tox/",
    ".nox/",
    ".coverage",
    ".coverage.*",
    ".cache",
    "nosetests.xml",
    "coverage.xml",
    "*.cover",
    "*.py,cover",
    ".hypothesis/",
    ".pytest_cache/",
    "cover/",
    "*.mo",
    "*.pot",
    "*.log",
    "local_settings.py",
    "db.sqlite3",
    "db.sqlite3-journal",
    "instance/",
    ".webassets-cache",
    ".scrapy",
    "docs/_build/",
    ".pybuilder/",
    "target/",
    ".ipynb_checkpoints",
    "profile_default/",
    "ipython_config.py",
    "pdm.lock",
    ".pdm.toml",
    ".pdm-python",
    ".pdm-build/",
    "__pypackages__/",
    "celerybeat-schedule",
    "celerybeat.pid",
    "*.sage.py",
    ".env",
    ".venv",
    "env/",
    "venv/",
    "ENV/",
    "env.bak/",
    "venv.bak/",
    ".spyderproject",
    ".spyproject",
    ".ropeproject",
    "site/",
    ".mypy_cache/",
    ".dmypy.json",
    "dmypy.json",
    ".pyre/",
    ".pytype/",
    "cython_debug/",
    ".idea/",
    ".git/"
]


def is_excluded(relative_path, root_path, root_input):
    # Always include the root input path
    if os.path.abspath(relative_path) == os.path.abspath(root_input):
        return False
    for pattern in exclusion_patterns:
        pattern = pattern.rstrip("/")
        if fnmatch.fnmatch(relative_path, pattern) or fnmatch.fnmatch(
            os.path.basename(relative_path), pattern
        ):
            return True
    return False


def get_project_structure(path, root_path, indent=0, root=True, root_input=None):
    if root_input is None:
        root_input = root_path
    relative_path = os.path.relpath(path, root_path)
    if not root and is_excluded(path, root_path, root_input):
        return

    # Print the directory or file name
    if os.path.isdir(path):
        print("    " * indent + os.path.basename(path) + "/")
    else:
        print("    " * indent + os.path.basename(path))

    if os.path.isdir(path):
        try:
            entries = os.listdir(path)
        except PermissionError:
            return

        for entry in sorted(entries):
            full_path = os.path.join(path, entry)
            get_project_structure(
                full_path, root_path, indent + 1, root=False, root_input=root_input
            )


def main():
    parser = argparse.ArgumentParser(
        description="Outputs the directory structure of the given path."
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Relative path to the project root. Defaults to current directory.",
    )
    args = parser.parse_args()
    path = args.path
    if not os.path.exists(path):
        print(f"Error: Path '{path}' does not exist.")
        sys.exit(1)
    path = os.path.abspath(path)
    get_project_structure(path, os.path.dirname(path), root_input=path)


if __name__ == "__main__":
    main()
