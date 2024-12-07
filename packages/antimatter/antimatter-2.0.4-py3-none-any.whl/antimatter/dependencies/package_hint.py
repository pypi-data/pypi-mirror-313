import os
import tomli
from typing import Dict, List, Tuple

from packaging.requirements import InvalidRequirement, Requirement


def _parse_requirements(
    dependencies: Dict,
) -> Dict[str, List[Tuple[List[str], Requirement]]]:
    """
    Builds a mapping of dependencies to the build options requiring them, and the
    associated versions.

    :param dependencies: A dictionary to use for building requirements.
    :return: The dependency mapping
    """
    reqs = {}
    for extras_name, lib_specs in dependencies.items():

        requirements = []
        for spec in lib_specs:
            try:
                requirements.append(Requirement(spec))
            except InvalidRequirement:
                pass

        for r in requirements:
            if r.name not in reqs:
                reqs[r.name] = []
            existing_reqs = reqs[r.name]
            is_present = False
            for t in existing_reqs:
                if str(t[1]) == str(r):
                    t[0].append(extras_name)
                    is_present = True
            if not is_present:
                reqs[r.name].append(([extras_name], r))

    return reqs


def _build_requirements(
    working_dir: str,
) -> Dict[str, List[Tuple[List[str], Requirement]]]:
    """
    Builds a mapping of dependencies to the build options requiring them, and the
    associated versions. If a 'pyproject.toml' file is not found in the working
    directory, this will also check one directory higher.

    :param working_dir: The working directory to use for building requirements.
    :return: The dependency mapping
    """
    # pyproject.toml location will be different for wheel vs source installs
    if "pyproject.toml" not in os.listdir(working_dir):
        working_dir = os.path.join(working_dir, "dependencies", "data")

    if "pyproject.toml" not in os.listdir(working_dir):
        return {}

    with open(os.path.join(working_dir, "pyproject.toml"), "rb") as f:
        pyproject = tomli.load(f)

    return _parse_requirements(pyproject["project"]["optional-dependencies"])


_pkgs = _build_requirements(os.path.dirname(os.path.dirname(__file__)))


def as_install_hint(module_name: str) -> str:
    """
    Get the installation hint from the given module name.

    :param module_name: The module name to find an installation hint for
    :return: A hint for the user as to an action to take for the module
    """
    req_txt = "Recommended action: "
    pip_txt = "'pip install {}'"
    pip_list_txt = "{} for extras {}"

    imports = _pkgs.get(module_name, [])
    imp_txt = "UNKNOWN"
    if len(imports) == 1:
        _, req = imports[0]
        imp_txt = pip_txt.format(str(req))
    elif len(imports) > 1:
        imp_list = []
        for imp in imports:
            extras, req = imp
            imp_list.append(pip_list_txt.format(pip_txt.format(str(req)), str(extras)))
        imp_txt = "; ".join(imp_list)

    return req_txt + imp_txt
