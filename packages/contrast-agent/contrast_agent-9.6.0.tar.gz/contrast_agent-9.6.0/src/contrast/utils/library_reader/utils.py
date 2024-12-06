# Copyright © 2024 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import os
import re
import hashlib

from contrast_vendor.importlib_metadata import packages_distributions
from contrast_vendor.importlib_metadata import files as importlib_get_files

from contrast_vendor import structlog as logging

logger = logging.getLogger("contrast")

CONTRAST_AGENT_DIST = "contrast-agent"

# Both of these metadata files contain a file list of what is installed under the top level dirs
RECORD = "RECORD"
SOURCES = "SOURCES.txt"

NAMESPACE_PACKAGE = "namespace_packages.txt"
TOP_LEVEL_TXT = "top_level.txt"

PY_SUFFIX = ".py"
SO_SUFFIX = ".so"

SITE_PACKAGES_DIR = f"{os.sep}site-packages{os.sep}"
DIST_PACKAGES_DIR = f"{os.sep}dist-packages{os.sep}"

INSTALLED_DISTRIBUTIONS = None
INSTALLED_DISTRIBUTION_TOP_LEVEL_IMPORTS = None


def _load_installed_dist_top_level_imports(cache):
    """
    Returns a dictionary containing a mapping of the package name to each of its top level importable packages by name.
    """
    if cache is None:
        cache = {}

    for top_level_import, dist_names in packages_distributions().items():
        dist_names = set(dist_names)

        for dist in dist_names:
            if cache.get(dist, None) is None:
                cache[dist] = {
                    top_level_import,
                }
            else:
                cache[dist].add(top_level_import)

    return cache


def load_packages_cache():
    global INSTALLED_DISTRIBUTIONS
    global INSTALLED_DISTRIBUTION_TOP_LEVEL_IMPORTS

    INSTALLED_DISTRIBUTIONS = None
    INSTALLED_DISTRIBUTION_TOP_LEVEL_IMPORTS = {}

    _load_installed_dist_top_level_imports(INSTALLED_DISTRIBUTION_TOP_LEVEL_IMPORTS)

    INSTALLED_DISTRIBUTIONS = list(INSTALLED_DISTRIBUTION_TOP_LEVEL_IMPORTS.keys())


def get_installed_dist_top_level_imports():
    return INSTALLED_DISTRIBUTION_TOP_LEVEL_IMPORTS


def get_installed_dist_names():
    return INSTALLED_DISTRIBUTIONS


def is_editable_install(dist, version, all_files):
    editable_install_metadata_fname = f"__editable__{dist.lower()}-{version}.pth"

    return editable_install_metadata_fname in all_files


def normalize_file_name(file_path):
    """
    This function converts a file ending in .pyc to .py. The reason for this
    is due to how screener is configured to verify a file was reported (only supports
    exact match not a regex)
    @param file_path: full path to a python file ending in .pyc or .py
    @return: file_path ending in .py
    """
    file_to_report = file_path.rpartition(SITE_PACKAGES_DIR)

    if not file_to_report[1]:
        file_to_report = file_path.rpartition(DIST_PACKAGES_DIR)
        if not file_to_report[1]:
            return None

    normalized_file_name = file_to_report[2]
    if normalized_file_name.endswith(".pyc"):
        normalized_file_name = normalized_file_name[: len(normalized_file_name) - 1]

    return normalized_file_name


def get_top_level_directories_namespace_pkg(dist: str, namespace: str) -> set:
    """
    @param dist: Distribution name
    @param namespace: The name of the namespace to search
    @return: The top level importable packages/modules under the namespace
    """
    top_level_dirs = set()
    ignore_dirs = ("__pycache__",)
    excluded_files = ("setup.py",)
    all_files = importlib_get_files(dist)

    if not dist:
        return top_level_dirs

    if all_files is None:
        # In the case where the metadata files listing files (RECORD, SOURCES.txt etc..) are missing, importlib_get_files() will return None.
        return top_level_dirs

    # Go through each python file and get the directory name after namespace
    for f in all_files:
        current_file = os.path.realpath(str(f.locate()))
        if current_file:
            current_file = normalize_file_name(current_file)

        if (
            current_file
            and f.name.endswith((PY_SUFFIX, SO_SUFFIX))
            and f.name not in excluded_files
            and current_file.startswith(namespace + os.sep)
        ):
            dirs = current_file.split(os.sep)
            if len(dirs) > 1 and dirs[1] not in ignore_dirs:
                top_level_dirs.add(dirs[1])

    return top_level_dirs


def get_file_from_module(module):
    if hasattr(module, "__file__") and module.__file__:
        return os.path.realpath(module.__file__)

    return None


def normalize_dist_name(name):
    # Normalize the name based on the spec https://packaging.python.org/en/latest/specifications/name-normalization/
    return re.sub(r"[-_.]+", "-", name).lower()


def get_hash(name, version):
    """
    DO NOT ALTER OR REMOVE

    This must match the calculation made by the artifact dependency management database.
    """
    name = normalize_dist_name(name)

    to_hash = name + " " + version

    return hashlib.sha1(to_hash.encode("utf-8")).hexdigest()
