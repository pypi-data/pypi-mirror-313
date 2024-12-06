# Copyright © 2024 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import os
import time
import threading

from contrast_vendor import importlib_metadata
from contrast_vendor.importlib_metadata import files as importlib_get_files


from contrast.utils.library_reader.utils import get_installed_dist_names
from contrast.utils.library_reader.utils import (
    get_hash,
    CONTRAST_AGENT_DIST,
    PY_SUFFIX,
    SO_SUFFIX,
    is_editable_install,
    normalize_file_name,
)

from contrast.agent import scope
from contrast.api import Library
from contrast.utils.patch_utils import get_loaded_modules
from contrast_vendor import structlog as logging

logger = logging.getLogger("contrast")


class LibraryReader:
    def __init__(self, settings, send_ts_message_func):
        self.settings = settings
        self.send_ts_message_func = send_ts_message_func
        self.analysis_thread = None
        self.installed_distribution_keys = []

        # All packages installed in the site-packages/ directory
        self.installed_dists = get_installed_dist_names()

    def start_library_analysis_thread(self, daemon=True):
        self.analysis_thread = threading.Thread(target=self._read_libraries)
        self.analysis_thread.daemon = daemon

        self.analysis_thread.start()

    def join_library_analysis_thread(self):
        if self.analysis_thread:
            self.analysis_thread.join()

    def _read_libraries(self):
        """
        Looks at every library installed in self.installed_dists, then calls search_dist
        on each dist that has metadata associated with the list of files/modules that can be loaded
        :return: None
        """
        with scope.contrast_scope():
            logger.debug("Analyzing libraries...")

            all_dists = read_dists(self.installed_dists)
            reportable_dists = [
                dist
                for dist in all_dists
                if dist.get("file_path", "")
                and dist.get("file_path", "") != CONTRAST_AGENT_DIST
            ]

            self._send_analysis_results_appstart(reportable_dists)
            self._send_analysis_results_files_loaded(reportable_dists)

    def _send_analysis_results_appstart(self, reportable_dists):
        """
        Send library discovery in ApplicationUpdate message.
        :param reportable_dists: A list of dictionaries containing information about
            each distribution.
        """
        if not reportable_dists:
            return

        libraries = [Library(dist) for dist in reportable_dists]

        logger.debug(
            "Discovered libraries: %s",
            [f"{lib.file_path} - {lib.version}" for lib in libraries],
        )

        logger.debug("Sending ApplicationUpdate message with library analysis results")

        # Import here to prevent circular import
        from contrast.reporting import teamserver_messages

        app_update_msg = teamserver_messages.ApplicationUpdate(libraries)
        self.send_ts_message_func(app_update_msg)

    def _send_analysis_results_files_loaded(self, reportable_dists):
        if not reportable_dists:
            return

        from contrast.reporting import teamserver_messages

        msg = teamserver_messages.LibraryUsage(reportable_dists)

        logger.debug("Sending list of modules loaded to Contrast")

        self.send_ts_message_func(msg)


def read_dists(installed_dists):
    results = []

    for dist in installed_dists:
        analysis_result = search_dist(dist)

        if analysis_result:
            results.append(analysis_result)

    return results


def search_dist(dist):
    """
    Searches directories related to dist, gathering relevant statistics and metadata.
    Then, assuming library was loaded, appends that metadata to the self.libraries.

    Created package is added to the output for the process

    :param dist: Name of the python distribution we are analyzing
    :return: A dictionary containing contrast-relevant information about the current distribution
    """
    excluded_files = ("setup.py",)
    metadata = importlib_metadata.metadata(dist)
    version = metadata.get("Version", "")
    url = metadata.get("Home-page", "")
    all_files = importlib_get_files(dist)
    path = None

    if all_files is None:
        # In the case where the metadata files listing files (RECORD, SOURCES.txt etc..) are missing, importlib_get_files() will return None.
        return None

    if is_editable_install(dist, version, all_files):
        # We decided to omit this case since whatever the package is, its probably under active development
        # and still not a library at that point in time
        return None

    # Omit metadata files from total module count
    all_modules = {
        path
        for f in all_files
        if f.name.endswith((PY_SUFFIX, SO_SUFFIX))
        and f.name not in excluded_files
        and (path := os.path.realpath(str(f.locate())))
    }

    file_count = len(all_modules)
    library_hash = get_hash(dist, version)

    used_files = search_modules(all_modules)

    result = create_package(version, file_count, dist, url, library_hash)
    result["used_files"] = used_files

    return result


def create_package(version, class_count, name, url, sha):
    """
    Generate a json-serializable representation of a package for teamserver

    :param version: version of package
    :param class_count: count of files
    :param name: name of the library
    :param url: homepage of package
    :param sha: sha1 hash of the name(space)version
    :return: dict of package
    """
    current_time = int(time.time() * 1000)

    return {
        "version": version,
        "class_count": class_count,
        "file_path": name,
        "url": url,
        "hash_code": sha,
        "external_ms": current_time,
        "internal_ms": current_time,
    }


def search_modules(all_modules):
    """
    Searches every module in a distribution to see if it is loaded in the python interpreter.

    :param all_modules: modules in a specific package
    :return: The set of modules for a specific dist loaded in the python interpreter
    """
    # __file__ (Path to the loaded file) __file__ is optional. The import system may opt to leave
    # __file__ unset if it has no semantic meaning (e.g. a module loaded from a database).
    # Using os.path.realpath because in some environments there is a symlink to the directory containg 3rd party packages
    loaded_modules = {
        normalize_file_name(os.path.realpath(mod.__file__))
        for mod in get_loaded_modules().values()
        if hasattr(mod, "__file__")
        and mod.__file__
        and mod.__file__ in all_modules
        and normalize_file_name(os.path.realpath(mod.__file__)) is not None
    }

    return loaded_modules
