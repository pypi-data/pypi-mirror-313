"""Reboot your system."""
__version__ = "0.0.6"
__version_info__ = tuple((int(num) if num.isdigit() else num for num in __version__.replace("-", ".", 1).split(".")))

from pathlib import Path
import invoke.context
from invoke import task
from jinja2 import Template


def migrate_requirements(c: invoke.context.Context, project_template: str, system: str):
    """Copy requirements from the requirements.txt file to pyproject.toml."""
    lines = Path("requirements.txt").read_text().split("\n")
    current = "package"
    requirements = {current: [], "test": [], "doc": [], "graphical": [], "dev": []}
    for line in lines:
        if line.startswith("#"):
            candidate = line[1:].lower().strip().replace(" ", "_").replace("-", "_")
            if candidate in requirements.keys():
                current = candidate
                continue
        if line.strip() == "" or ("=" in line and "#" in line):
            continue
        versioned_package = line.split("#")[0].split()
        if versioned_package:
            requirements[current].append("".join(versioned_package))
    requirements[system.lower().replace("-", "_")] = requirements.get("package", []) # Support older packages
    import vermin
    config = vermin.Config()
    source_file_paths = list(set(vermin.detect_paths([system, "tests", "docs"], config=config)))
    minimums, *_ = vermin.Processor().process(source_file_paths, config, config.processes())
    minimum_version = vermin.version_strings(list(filter(lambda ver: ver, minimums)))
    Path("pyproject.toml").write_text(
        Template(project_template[1:]).render(requirements=requirements, system=system, minimum_version=minimum_version)
    )


@task
def release(c: invoke.context.Context, version: str, project_template: str, system: str, main_branch: str = "main", dev_branch: str = "dev"):
    """"""
    if version not in ["minor", "major", "patch"]:
        print("Version can be either major, minor or patch.")
        return

    migrate_requirements(c, project_template, system)

    import importlib
    current_module = importlib.import_module(system)
    __version_info__ = current_module.__version_info__
    __version__ = current_module.__version__
    _major, _minor, _patch = __version_info__

    if version == "patch":
        _patch = _patch + 1
    elif version == "minor":
        _minor = _minor + 1
        _patch = 0
    elif version == "major":
        _major = _major + 1
        _minor = 0
        _patch = 0
    c.run(f"git checkout {dev_branch}") # Just to fail early in case the dev branch does not exist
    c.run(f"git checkout -b release-{_major}.{_minor}.{_patch} {dev_branch}")
    c.run(f"sed -i 's/{__version__}/{_major}.{_minor}.{_patch}/g' {system}/__init__.py")
    print(f"Update the readme for version {_major}.{_minor}.{_patch}.")
    input("Press enter when ready.")
    c.run(f"git add -u")
    c.run(f'git commit -m "Update changelog version {_major}.{_minor}.{_patch}"')
    c.run(f"git push --set-upstream origin release-{_major}.{_minor}.{_patch}")
    c.run(f"git checkout {main_branch}")
    c.run(f"git pull")
    c.run(f"git merge --no-ff release-{_major}.{_minor}.{_patch}")
    c.run(f'git tag -a {_major}.{_minor}.{_patch} -m "Release {_major}.{_minor}.{_patch}"')
    c.run(f"git push")
    c.run(f"git checkout {dev_branch}")
    c.run(f"git merge --no-ff release-{_major}.{_minor}.{_patch}")
    c.run(f"git push")
    c.run(f"git branch -d release-{_major}.{_minor}.{_patch}")
    c.run(f"git push origin --tags")
