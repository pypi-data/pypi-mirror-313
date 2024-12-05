"""Utility functions for CLI interface."""

import json
import os
import pathlib
import re
import sys
import unicodedata
from dataclasses import dataclass
from importlib.metadata import version as cmemc_version
from typing import TYPE_CHECKING
from zipfile import BadZipFile, ZipFile

import requests
from bs4 import BeautifulSoup
from cmem.cmempy.dp.proxy.graph import get_graphs_list
from cmem.cmempy.queries import QueryCatalog
from cmem.cmempy.workspace.projects.project import get_projects
from prometheus_client import Metric

from cmem_cmemc.constants import NAMESPACES

if TYPE_CHECKING:
    from cmem_cmemc.context import ApplicationContext
from cmem_cmemc.smart_path import SmartPath as Path


def get_version() -> str:
    """Get the current version or SNAPSHOT."""
    return cmemc_version("cmem-cmemc")


def check_python_version(ctx: "ApplicationContext") -> None:
    """Check the runtime python version and warn or error."""
    version = sys.version_info
    major_expected = [3]
    minor_expected = [10, 11, 12]
    if version.major not in major_expected:
        ctx.echo_error(f"Error: cmemc can not be executed with Python {version.major}.")
        sys.exit(1)
    if version.minor not in minor_expected and not ctx.is_completing():
        ctx.echo_warning(
            "Warning: You are running cmemc under a non-tested python "
            f"environment ({version.major}.{version.minor})."
        )


def extract_error_message(error: Exception) -> str:
    """Extract a message from an exception."""
    # exceptions with response is HTTPError
    message = type(error).__name__ + ": " + str(error) + "\n"
    try:
        # try to load Problem Details for HTTP API JSON
        details = json.loads(error.response.text)  # type: ignore[attr-defined]
        message += type(error).__name__ + ": "
        if "title" in details:
            message += details["title"] + ": "
        if "detail" in details:
            message += details["detail"]
    except (AttributeError, ValueError):
        # is not json or any other issue, output plain response text
        pass
    return message


def iri_to_qname(iri: str) -> str:
    """Return a qname for an IRI based on well known namespaces.

    In case of no matching namespace, the full IRI is returned.

    Args:
    ----
        iri: the IRI to transform

    Returns: string

    """
    for prefix, namespace in NAMESPACES.items():
        iri = iri.replace(namespace, prefix + ":")
    return iri


def read_rdf_graph_files(directory_path: str) -> list[tuple[str, str]]:
    """Read all files from directory_path and output as tuples.

    The tuple format is (filepath, graph_name),
    for example ("/tmp/rdf.nt", "http://example.com")
    """
    rdf_graphs = []
    for root, _, files in os.walk(directory_path):
        for _file in files:
            if _file.endswith(".graph"):
                continue
            full_file_path = Path(root) / _file
            # Handle compressed files (like .gz)
            if _file.endswith(".gz"):
                graph_file_name = _file.replace(".gz", ".graph")
            else:
                graph_file_name = f"{_file}.graph"
            full_graph_file_name_path = Path(root) / graph_file_name
            if full_graph_file_name_path.exists():
                graph_name = read_file_to_string(str(full_graph_file_name_path)).strip()
                rdf_graphs.append((str(full_file_path.resolve()), graph_name))
    return rdf_graphs


def read_file_to_string(file_path: str) -> str:
    """Read file to string."""
    with Path(file_path).open(mode="rb") as _file:
        return str(_file.read().decode("utf-8"))


def get_graphs(writeable: bool = True, readonly: bool = True) -> list:
    """Retrieve list of accessible graphs from DP endpoint.

    readonly=True|writeable=True outputs all graphs
    readonly=False|writeable=True outputs only writeable graphs
    readonly=True|writeable=False outputs graphs without write access
    (but read access)
    """
    all_graphs = get_graphs_list()
    filtered_graphs = []
    for graph in all_graphs:
        if graph["writeable"] and writeable:
            filtered_graphs.append(graph)
        if not graph["writeable"] and readonly:
            filtered_graphs.append(graph)
    return filtered_graphs


def get_graphs_as_dict(writeable: bool = True, readonly: bool = True) -> dict:
    """Get the graph response as dict with IRI as main key."""
    graph_dict = {}
    for graph in get_graphs(writeable=writeable, readonly=readonly):
        graph_dict[graph["iri"]] = graph
    return graph_dict


def convert_uri_to_filename(value: str, allow_unicode: bool = False) -> str:
    """Convert URI to unix friendly filename.

    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert / to underscore. Convert to lowercase.
    Also strip leading and trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize("NFKC", value)
    else:
        value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    value = re.sub(r"\.", "_", value.lower())
    value = re.sub(r"/", "_", value.lower())
    value = re.sub(r"[^\w\s-]", "", value.lower())
    return re.sub(r"[-\s]+", "-", value).strip("-_")


def struct_to_table(
    source: str | bool | float | list | dict, table: list | None = None, prefix: str = ""
) -> list:
    """Prepare flat key/value table from a deep structure.

    This function takes structure and creates a flat table out of it,
    key by key, value by value. For each level deeper it prefixes the
    father keys.

    Example input:  {'k1': '1', 'k2': {'k3': '3', 'k4': '4'}}
    Example output: [['k1', '1'], ['k2:k3', '3'], ['k2:k4', '4']]

    Args:
    ----
        source (any): The structure which is transformed into a flat table.
        table (list): The table where the key/value rows will be appended.
        prefix (str): A prefix which is used to indicate the level.

    Returns:
    -------
        The input table extended with rows from the input source.

    """
    if table is None:
        table = []
    if type(source) in (str, bool, int, float):
        table.append([prefix, source])
        return table
    if isinstance(source, dict):
        if len(prefix) != 0:
            prefix = prefix + "."
        for key in source:
            table = struct_to_table(source[key], table, prefix + key)
        return table
    if isinstance(source, list):
        for value in source:
            table = struct_to_table(value, table, prefix)
        return table
    return table


def split_task_id(task_id: str) -> tuple[str, str]:
    """Validate and split cmemc task ID.

    Args:
    ----
        task_id (str): The task ID in the workspace.

    Raises:
    ------
        ValueError: in case the task ID is not splittable

    """
    try:
        project_part = task_id.split(":")[0]
        task_part = task_id.split(":")[1]
    except IndexError as error:
        raise ValueError(f"{task_id} is not a valid task ID.") from error
    return project_part, task_part


def metric_get_labels(family: Metric, clean: bool = True) -> dict[str, list[str]]:
    """Get the labels of a metric family.

    clean: remove keys with only one dimension
    family: the metric family

    Returns: labels as dict
    """
    labels: dict[str, list[str]] = {}
    # build tree structure
    for sample in family.samples:
        for label in sample.labels:
            value = sample.labels[label]
            if label not in labels:
                labels[label] = []
            if value not in labels[label]:
                labels[label].append(value)
    if clean:
        labels = dict(filter(lambda elem: len(elem[1]) > 1, labels.items()))
    return labels


def check_or_select_project(app: "ApplicationContext", project_id: str | None = None) -> str:
    """Check for given project, select the first one if there is only one.

    Args:
    ----
        app (ApplicationContext): the click cli app context.
        project_id (str): The project ID.

    Raises:
    ------
        ValueError: if no projects available.
        ValueError: if more than one project is.

    Returns:
    -------
        Maybe project_id if there was no project_id before.

    """
    if project_id is not None:
        return project_id

    projects = get_projects()
    if len(projects) == 1:
        project_name = str(projects[0]["name"])
        app.echo_warning(
            "Missing project (--project) - since there is only one project, "
            f"this is selected: {project_name}"
        )
        return project_name

    if len(projects) == 0:
        raise ValueError(
            "There are no projects available. "
            "Please create a project with 'cmemc project create'."
        )

    # more than one project
    raise ValueError(
        "There is more than one project available so you need to "
        "specify the project with '--project'."
    )


@dataclass
class PublishedPackage:
    """Represents a published package from pypi.org."""

    name: str
    description: str
    published: str


def get_published_packages() -> list[PublishedPackage]:
    """Get a scraped list of plugin packages scraped from pypi.org."""
    url_pattern = "https://pypi.org/search/?q=%22cmem-plugin-%22&page={}"
    packages = []
    package_names = []
    page = 0
    while True:
        page += 1
        url = url_pattern.format(page)
        soup = BeautifulSoup(requests.get(url, timeout=5).content, "html.parser")
        snippets = soup.find_all("a", class_="package-snippet")
        if len(snippets) == 0:
            break
        for _ in snippets:
            name = _.findChildren(class_="package-snippet__name")[0].getText()
            if name == "cmem-plugin-base":
                continue
            if not name.startswith("cmem-plugin-"):
                continue
            try:
                description = _.findChildren(class_="package-snippet__description")[0].getText()
            except IndexError:
                description = "no description"
            published = _.findChildren(name="time")[0].attrs["datetime"]
            if name not in package_names:
                package_names.append(name)
                packages.append(
                    PublishedPackage(
                        name=name,
                        description=description,
                        published=published,
                    )
                )
    return packages


def convert_iri_to_qname(iri: str, default_ns: str) -> str:
    """Convert IRI to a QName based on the default namespace.

    If the IRI does not match the default namespace, the method returns the full IRI.
    """
    if iri.startswith(default_ns):
        return iri.replace(default_ns, ":")
    return iri


def convert_qname_to_iri(qname: str, default_ns: str) -> str:
    """Convert a QName to an IRI based on the default namespace.

    If the QName does not match the default namespace, the method returns the full IRI.
    """
    if qname.startswith(":"):
        return default_ns + qname[1:]

    return qname


def get_query_text(file_or_uri: str, required_projections: set) -> str:
    """Get query text for a file or graph catalog URI.

    Args:
    ----
        file_or_uri (str): The file path or URI to fetch the query from.
        required_projections (set): A set of required projections.

    Returns:
    -------
        str: The query text.

    Raises:
    ------
        ValueError: If the input is not a readable file or a query URI,
                    or if the query contains placeholders,
                    or if the query does not include the required projections.

    """
    sparql_query = QueryCatalog().get_query(file_or_uri)
    if sparql_query is None:
        raise ValueError(f"{file_or_uri} is neither a readable file nor a query URI.")

    if sparql_query.get_placeholder_keys():
        raise ValueError("Placeholder queries are not supported.")

    result = sparql_query.get_json_results()
    projected_vars = set(result["head"]["vars"])

    missing_projections = required_projections - projected_vars
    if missing_projections:
        missing = ", ".join(missing_projections)
        raise ValueError(f"Select query must include projections for: {missing}")
    txt: str = sparql_query.text
    return txt


def validate_zipfile(zipfile: str | pathlib.Path) -> bool:
    """Validate a zipfile."""
    zipfile = pathlib.Path(zipfile)
    try:
        ZipFile(zipfile).testzip()
    except BadZipFile:
        return False
    return True
