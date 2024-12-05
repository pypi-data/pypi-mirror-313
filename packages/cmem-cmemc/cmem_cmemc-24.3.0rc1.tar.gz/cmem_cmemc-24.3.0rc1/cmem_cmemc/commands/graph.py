"""graph commands for cmem command line interface."""

import gzip
import hashlib
import io
import json
import os
from xml.dom import minidom  # nosec
from xml.etree.ElementTree import (  # nosec
    Element,
    SubElement,
    tostring,
)

import click
from click import Argument
from cmem.cmempy.config import get_cmem_base_uri
from cmem.cmempy.dp.authorization import refresh
from cmem.cmempy.dp.proxy import graph as graph_api
from cmem.cmempy.dp.proxy.graph import get_graph_import_tree, get_graph_imports
from cmem.cmempy.dp.proxy.sparql import get as sparql_api
from jinja2 import Template
from six.moves.urllib.parse import quote
from treelib import Tree

from cmem_cmemc import completion
from cmem_cmemc.command import CmemcCommand
from cmem_cmemc.command_group import CmemcGroup
from cmem_cmemc.commands.validation import validation_group
from cmem_cmemc.context import ApplicationContext
from cmem_cmemc.parameter_types.path import ClickSmartPath
from cmem_cmemc.smart_path import SmartPath as Path
from cmem_cmemc.utils import (
    convert_uri_to_filename,
    get_graphs,
    get_graphs_as_dict,
    iri_to_qname,
    read_rdf_graph_files,
)

UNKNOWN_GRAPH_ERROR = "The graph {} is not accessible or does not exist."


def tuple_to_list(ctx: ApplicationContext, param: Argument, value: tuple) -> list:  # noqa: ARG001
    """Get a list from a tuple

    Used as callback to have mutable values
    """
    return list(value)


def count_graph(graph_iri: str) -> int:
    """Count triples in a graph and return integer."""
    query = "SELECT (COUNT(*) AS ?triples) " + " FROM <" + graph_iri + "> WHERE { ?s ?p ?o }"  # noqa: S608
    result = json.loads(sparql_api(query, owl_imports_resolution=False))
    count = result["results"]["bindings"][0]["triples"]["value"]
    return int(count)


def _get_graph_to_file(  # noqa: PLR0913
    graph_iri: str,
    file_path: str,
    app: ApplicationContext,
    numbers: tuple[int, int] | None = None,
    overwrite: bool = True,
    mime_type: str = "application/n-triples",
) -> None:
    """Request a single graph to a single file (streamed).

    numbers is a tuple of current and count (for output only).
    """
    if Path(file_path).exists():
        if overwrite is True:
            app.echo_warning(f"Output file {file_path} does exist: will overwrite it.")
        else:
            app.echo_warning(f"Output file {file_path} does exist: will append to it.")
    if numbers is not None:
        running_number, count = numbers
        if running_number is not None and count is not None:
            app.echo_info(
                f"Export graph {running_number}/{count}: " f"{graph_iri} to {file_path} ... ",
                nl=False,
            )
    # create and write the .ttl content file
    mode = "wb" if overwrite is True else "ab"

    with (
        gzip.open(file_path, mode)
        if file_path.endswith(".gz")
        else click.open_file(file_path, mode) as triple_file,
        graph_api.get_streamed(graph_iri, accept=mime_type) as response,
    ):
        response.raise_for_status()
        for chunk in response.iter_content(chunk_size=None):
            if chunk:
                triple_file.write(chunk)
        request_headers = response.request.headers
        request_headers.pop("Authorization")
        app.echo_debug(f"cmemc request headers: {request_headers}")
        app.echo_debug(f"server response headers: {response.headers}")
    if numbers is not None:
        app.echo_success("done")


def _get_export_names(
    app: ApplicationContext, iris: list[str], template: str, file_extension: str = "ttl"
) -> dict:
    """Get a dictionary of generated file names based on a template.

    Args:
    ----
        app: the context click application
        iris: list of graph iris
        template (str): the template string to use
        file_extension(str): the file extension to use

    Returns:
    -------
        a dictionary with IRIs as keys and filenames as values

    Raises:
    ------
        ValueError in case the template string produces a naming clash,
            means two IRIs result in the same filename

    """
    template_data = app.get_template_data()
    _names = {}
    for iri in iris:
        template_data.update(
            hash=hashlib.sha256(iri.encode("utf-8")).hexdigest(),
            iriname=convert_uri_to_filename(iri),
        )
        _name_created = f"{Template(template).render(template_data)}.{file_extension}"
        _names[iri] = _name_created
    if len(_names.values()) != len(set(_names.values())):
        raise ValueError(
            "The given template string produces a naming clash. "
            "Please use a different template to produce unique names."
        )
    return _names


def _create_node_label(iri: str, graphs: dict) -> str:
    """Create a label for a node in the tree."""
    if iri not in graphs:
        return "[missing: " + iri + "]"
    title = graphs[iri]["label"]["title"]
    return f"{title} -- {iri}"


def _add_tree_nodes_recursive(tree: Tree, structure: dict, iri: str, graphs: dict) -> Tree:
    """Add all child nodes of iri from structure to tree.

    Call recursively until no child node can be used as parent anymore.

    Args:
    ----
        tree: the graph where to add the nodes
        structure: the result dict of get_graph_import_tree()
        iri: The IRI of the parent
        graphs: the result of get_graphs()

    Returns:
    -------
        the new treelib.Tree object with the additional nodes

    """
    if not tree.contains(iri):
        tree.create_node(tag=_create_node_label(iri, graphs), identifier=iri)
    if iri not in structure:
        return tree
    for child in structure[iri]:
        tree.create_node(tag=_create_node_label(child, graphs), identifier=child, parent=iri)
    for child in structure[iri]:
        if child in structure:
            tree = _add_tree_nodes_recursive(tree, structure, child, graphs)
    return tree


def _add_ignored_nodes(tree: Tree, structure: dict) -> Tree:
    """Add all child nodes as ignored nodes.

    Args:
    ----
        tree: the graph where to add the nodes
        structure: the result dict of get_graph_import_tree()

    Returns:
    -------
        the new treelib.Tree object with the additional nodes

    """
    if len(structure.keys()) > 0:
        for parent in structure:
            for children in structure[parent]:
                tree.create_node(tag="[ignored: " + children + "]", parent=parent)
    return tree


def _get_graphs_filtered(filter_name: str, filter_value: str) -> list[dict]:
    """Get graphs but filtered according to name and value."""
    # not filtered means all graphs
    graphs: list[dict]
    if filter_name is None:
        return get_graphs()
    # check for correct filter names
    possible_filter_names = ("access", "imported-by")
    if filter_name not in possible_filter_names:
        raise ValueError(
            f"{filter_name} is an unknown filter name. " f"Use one of {possible_filter_names}."
        )
    # filter by access condition
    if filter_name == "access":
        if filter_value == "writeable":
            graphs = get_graphs(writeable=True, readonly=False)
        elif filter_value == "readonly":
            graphs = get_graphs(writeable=False, readonly=True)
        else:
            raise ValueError("Filter access is either 'readonly' or 'writeable'.")
    else:
        # default is all graphs
        graphs = get_graphs()
    # filter by imported-by
    if filter_name == "imported-by":
        if filter_value not in get_graphs_as_dict():
            raise ValueError(UNKNOWN_GRAPH_ERROR.format(filter_value))
        imported_graphs = get_graph_imports(filter_value)
        graphs = [_ for _ in graphs if _["iri"] in imported_graphs]
    return graphs


def _add_imported_graphs(iris: list[str], all_graphs: dict) -> list[str]:
    """Get a list of graph IRIs extended with the imported graphs.

    Args:
    ----
        iris: list of graph IRIs
        all_graphs: output of get_graphs_as_dict (dict of all graphs)

    Returns:
    -------
        list of graph IRIs

    """
    extended_list = iris
    for iri in set(iris):
        for _ in get_graph_imports(iri):
            # check if graph exist
            if _ in all_graphs:
                extended_list.append(_)
    return list(set(extended_list))


def _check_and_extend_exported_graphs(
    iris: list[str], all_flag: bool, imported_flag: bool, all_graphs: dict
) -> list[str]:
    """Get a list of IRIs checked and extended.

    Args:
    ----
        iris: List or tuple of given user IRIs
        all_flag: user wants all graphs
        imported_flag: user wants imported graphs as well
        all_graphs: dict of all graphs (get_graph_as_dict())

    Returns:
    -------
        checked and extended list of IRIs

    Raises:
    ------
         ValueError

    """
    # transform given IRI-tuple to a distinct IRI-list
    iris = list(set(iris))
    if len(iris) == 0 and not all_flag:
        raise ValueError(
            "Either provide at least one graph IRI or use the --all option "
            "in order to work with all graphs."
        )
    for iri in iris:
        if iri not in all_graphs:
            raise ValueError(UNKNOWN_GRAPH_ERROR.format(iri))
    if all_flag:
        # in case --all is given,
        # list of graphs is filled with all available graph IRIs
        iris = [str(_) for _ in all_graphs]
    elif imported_flag:
        # does not need be executed in case of --all
        iris = _add_imported_graphs(iris, all_graphs)
    return iris


def _create_xml_catalog_file(app: ApplicationContext, names: dict, output_dir: str) -> None:
    """Create a Protégé suitable XML catalog file.

    Args:
    ----
        app: the cmemc context object
        names: output of _get_export_names()
        output_dir: path where to create the XML file

    """
    file_name = Path(output_dir) / "catalog-v001.xml"
    catalog = Element("catalog")
    catalog.set("prefer", "public")
    catalog.set("xmlns", "urn:oasis:names:tc:entity:xmlns:xml:catalog")
    for name in names:
        uri = SubElement(catalog, "uri")
        uri.set("id", "Auto-Generated Import Resolution by cmemc")
        uri.set("name", name)
        uri.set("uri", names[name])
    parsed_string = minidom.parseString(  # nosec - since source is trusted  # noqa: S318
        tostring(catalog, "utf-8")
    ).toprettyxml(indent="  ")
    file = click.open_file(str(file_name), "w")
    file.truncate(0)
    file.write(parsed_string)
    app.echo_success(f"XML catalog file created as {file_name}.")


def _prepare_tree_output_id_only(iris: list[str], graphs: dict) -> str:
    """Prepare a sorted, de-duplicated IRI list of graph imports."""
    output_iris = []
    for iri in iris:
        # get response for one requested graph
        api_response = get_graph_import_tree(iri)

        # add all imported IRIs to the IRI list
        # add the requested graph as well
        output_iris.append(iri)
        for top_graph in api_response["tree"]:
            output_iris.append(top_graph)
            for sub_graph in api_response["tree"][top_graph]:
                output_iris.append(sub_graph)  # noqa: PERF402

    # prepare a sorted, de-duplicated IRI list of existing graphs
    # and create a line-by-line output of it
    output_iris = sorted(set(output_iris), key=lambda x: x.lower())
    filtered_iris = [iri for iri in output_iris if iri in graphs]
    return "\n".join(filtered_iris[0:]) + "\n"


@click.command(cls=CmemcCommand, name="tree")
@click.option("-a", "--all", "all_", is_flag=True, help="Show tree of all (readable) graphs.")
@click.option("--raw", is_flag=True, help="Outputs raw JSON of the graph importTree API response.")
@click.option(
    "--id-only",
    is_flag=True,
    help="Lists only graph identifier (IRIs) and no labels or other "
    "metadata. This is useful for piping the IRIs into other commands. "
    "The output with this option is a sorted, flat, de-duplicated list "
    "of existing graphs.",
)
@click.argument(
    "iris",
    nargs=-1,
    type=click.STRING,
    shell_complete=completion.graph_uris,
    callback=tuple_to_list,
)
@click.pass_obj
def tree_command(
    app: ApplicationContext, all_: bool, raw: bool, id_only: bool, iris: list[str]
) -> None:
    """Show graph tree(s) of the owl:imports hierarchy.

    You can output one or more trees of the import hierarchy.

    Imported graphs which do not exist are shown as `[missing: IRI]`.
    Imported graphs which will result in an import cycle are shown as
    `[ignored: IRI]`.
    Each graph is shown with label and IRI.
    """
    graphs = get_graphs_as_dict()
    if not iris and not all_:
        raise ValueError(
            "Either specify at least one graph IRI or use the "
            "--all option to show the owl:imports tree of all graphs."
        )
    if all_:
        iris = [str(_) for _ in graphs]

    for iri in iris:
        if iri not in graphs:
            raise ValueError(UNKNOWN_GRAPH_ERROR.format(iri))

    iris = sorted(iris, key=lambda x: graphs[x]["label"]["title"].lower())

    if raw:
        for iri in iris:
            # direct output of the response for one requested graph
            app.echo_info_json(get_graph_import_tree(iri))
        return

    if id_only:
        app.echo_result(_prepare_tree_output_id_only(iris, graphs), nl=False)
        return

    # normal execution
    output = ""
    for iri in iris:
        # get response for on requested graph
        api_response = get_graph_import_tree(iri)

        tree = _add_tree_nodes_recursive(Tree(), api_response["tree"], iri, graphs)
        tree = _add_ignored_nodes(tree, api_response["ignored"])

        # strip empty lines from the tree.show output
        output += os.linesep.join(
            [
                line
                for line in tree.show(key=lambda x: x.tag.lower(), stdout=False).splitlines()
                if line.strip()
            ]
        )
        output += "\n"
    # result output
    app.echo_result(output, nl=False)


@click.command(cls=CmemcCommand, name="list")
@click.option("--raw", is_flag=True, help="Outputs raw JSON of the graphs list API response.")
@click.option(
    "--id-only",
    is_flag=True,
    help="Lists only graph identifier (IRIs) and no labels or other "
    "metadata. This is useful for piping the IRIs into other commands.",
)
@click.option(
    "--filter",
    "filter_",
    type=click.Tuple([click.Choice(["access", "imported-by"]), str]),
    shell_complete=completion.graph_list_filter,
    default=[None] * 2,
    help="Filter graphs based on effective access conditions or import "
    "closure. "
    "First parameter CHOICE can be 'access' or 'imported-by'. "
    "The second parameter can be 'readonly' or 'writeable' in case "
    "of 'access' or any readable graph in case of 'imported-by'.",
)
@click.pass_obj
def list_command(
    app: ApplicationContext, raw: bool, id_only: bool, filter_: tuple[str, str]
) -> None:
    """List accessible graphs."""
    filter_name, filter_value = filter_
    graphs = _get_graphs_filtered(filter_name, filter_value)

    if raw:
        app.echo_info_json(graphs)
        return
    if id_only:
        # output a sorted list of graph IRIs
        for graph_desc in sorted(graphs, key=lambda k: k["iri"].lower()):
            app.echo_result(graph_desc["iri"])
        return
    # output a user table
    table = []
    for _ in graphs:
        if len(_["assignedClasses"]) > 0:
            graph_class = iri_to_qname(sorted(_["assignedClasses"])[0])
        else:
            graph_class = ""
        row = [
            _["iri"],
            graph_class,
            _["label"]["title"],
        ]
        table.append(row)
    app.echo_info_table(
        table,
        headers=["Graph IRI", "Type", "Label"],
        sort_column=2,
        empty_table_message="No graphs found. "
        "Use the `graph import` command to import a graph from a file, or "
        "use the `admin store bootstrap` command to import the default graphs.",
    )


def _validate_export_command_input_parameters(
    output_dir: str, output_file: str, compress: str, create_catalog: bool
) -> None:
    """Validate export command input parameters combinations"""
    if output_dir and create_catalog and compress:
        raise click.UsageError(
            "Cannot create a catalog file when using a compressed graph file."
            " Please remove either the --create-catalog or --compress option."
        )
    if output_file == "- " and compress:
        raise click.UsageError("Cannot output a binary file to terminal. Use --output-file option.")


# pylint: disable=too-many-arguments,too-many-locals
@click.command(cls=CmemcCommand, name="export")
@click.option("-a", "--all", "all_", is_flag=True, help="Export all readable graphs.")
@click.option(
    "--include-imports",
    is_flag=True,
    help="Export selected graph(s) and all graphs which are imported from "
    "these selected graph(s).",
)
@click.option(
    "--create-catalog",
    is_flag=True,
    help="In addition to the .ttl and .graph files, cmemc will create an "
    "XML catalog file (catalog-v001.xml) which can be used by "
    "applications such as Protégé.",
)
@click.option(
    "--output-dir",
    type=ClickSmartPath(writable=True, file_okay=False),
    help="Export to this directory.",
)
@click.option(
    "--output-file",
    type=ClickSmartPath(writable=True, allow_dash=True, dir_okay=False),
    default="-",
    show_default=True,
    shell_complete=completion.triple_files,
    help="Export to this file.",
)
@click.option(
    "--filename-template",
    "-t",
    "template",
    default="{{hash}}",
    show_default=True,
    type=click.STRING,
    shell_complete=completion.graph_export_templates,
    help="Template for the export file name(s). "
    "Used together with --output-dir. "
    "Possible placeholders are (Jinja2): "
    "{{hash}} - sha256 hash of the graph IRI, "
    "{{iriname}} - graph IRI converted to filename, "
    "{{connection}} - from the --connection option and "
    "{{date}} - the current date as YYYY-MM-DD. "
    "The file suffix will be appended. "
    "Needed directories will be created.",
)
@click.option(
    "--mime-type",
    default="application/n-triples",
    show_default=True,
    type=click.Choice(["application/n-triples", "text/turtle"]),
    help="Define the requested mime type",
)
@click.option(
    "--compress",
    type=click.Choice(["gzip"]),
    help="Compress the exported graph files.",
)
@click.argument(
    "iris",
    nargs=-1,
    type=click.STRING,
    shell_complete=completion.graph_uris,
    callback=tuple_to_list,
)
@click.pass_obj
def export_command(  # noqa: PLR0913
    app: ApplicationContext,
    all_: bool,
    include_imports: bool,
    create_catalog: bool,
    output_dir: str,
    output_file: str,
    template: str,
    mime_type: str,
    iris: list[str],
    compress: str,
) -> None:
    """Export graph(s) as NTriples to stdout (-), file or directory.

    In case of file export, data from all selected graphs will be concatenated
    in one file.
    In case of directory export, .graph and .ttl files will be created
    for each graph.
    """
    _validate_export_command_input_parameters(output_dir, output_file, compress, create_catalog)
    iris = _check_and_extend_exported_graphs(iris, all_, include_imports, get_graphs_as_dict())

    count: int = len(iris)
    app.echo_debug("graph count is " + str(count))
    if output_dir:
        # output directory set
        app.echo_debug("output is directory")
        # pre-calculate all filenames with the template,
        # in order to output errors on naming clashes as early as possible
        _names = _get_export_names(app, iris, template, "ttl.gz" if compress else "ttl")
        _graph_file_names = _get_export_names(app, iris, template, "ttl.graph")
        # create directory
        if not Path(output_dir).exists():
            app.echo_warning("Output directory does not exist: " + "will create it.")
            Path(output_dir).mkdir(parents=True)
        # one .graph, one .ttl file per named graph
        for current, iri in enumerate(iris, start=1):
            # join with given output directory and normalize full path
            triple_file_name = os.path.normpath(Path(output_dir) / _names[iri])
            graph_file_name = os.path.normpath(Path(output_dir) / _graph_file_names[iri])
            # output directory is created lazy
            Path(triple_file_name).parent.mkdir(parents=True, exist_ok=True)
            # create and write the .ttl.graph metadata file
            graph_file = click.open_file(graph_file_name, "w")
            graph_file.write(iri + "\n")
            _get_graph_to_file(
                iri, triple_file_name, app, numbers=(current, count), mime_type=mime_type
            )
        if create_catalog:
            _create_xml_catalog_file(app, _names, output_dir)
        return
    # no output directory set -> file export
    if output_file == "-":
        if compress:
            raise click.UsageError(
                "Cannot output a binary file to terminal. Use --output-file option."
            )
        # in case a file is stdout,
        # all triples from all graphs go in and other output is suppressed
        app.echo_debug("output is stdout")
        for iri in iris:
            _get_graph_to_file(iri, output_file, app, mime_type=mime_type)
    else:
        # in case a file is given, all triples from all graphs go in
        if compress and not output_file.endswith(".gz"):
            output_file = output_file + ".gz"

        app.echo_debug("output is file")
        for current, iri in enumerate(iris, start=1):
            _get_graph_to_file(
                iri,
                output_file,
                app,
                numbers=(current, count),
                overwrite=False,
                mime_type=mime_type,
            )


def validate_input_path(input_path: str) -> None:
    """Validate input path

    This function checks the provided folder for any .ttl or .nt files
    that have corresponding .gz files. If such files are found, it raises a ValueError.
    """
    files = os.listdir(input_path)

    # Check for files with the given extensions (.ttl and .nt)
    rdf_files = [f for f in files if f.endswith((".ttl", ".nt"))]

    # Check for corresponding .gz files
    gz_files = [f"{f}.gz" for f in rdf_files]
    conflicting_files = [f for f in gz_files if f in files]

    if conflicting_files:
        raise ValueError(
            f"The following RDF files (.ttl/.nt) have corresponding '.gz' files,"
            f" which is not allowed: {', '.join(conflicting_files)}"
        )


@click.command(cls=CmemcCommand, name="import")
@click.option(
    "--replace",
    is_flag=True,
    help="Replace / overwrite the graph(s), instead of just adding the triples to the graph.",
)
@click.option(
    "--skip-existing",
    is_flag=True,
    help="Skip importing a file if the target graph already exists in "
    "the store. Note that the graph list is fetched once at the "
    "beginning of the process, so that you can still add multiple "
    "files to one single graph (if it does not exist).",
)
@click.argument(
    "input_path",
    required=True,
    shell_complete=completion.triple_files,
    type=ClickSmartPath(allow_dash=False, readable=True, remote_okay=True),
)
@click.argument("iri", type=click.STRING, required=False, shell_complete=completion.graph_uris)
@click.pass_obj
def import_command(
    app: ApplicationContext,
    input_path: str,
    replace: bool,
    skip_existing: bool,
    iri: tuple[str, ...],
) -> None:
    """Import graph(s) to the store.

    If input is a file, content will be uploaded to the graph identified with the IRI.

    If input is a directory and NO IRI is given, it scans for file-pairs such as
    `xyz.ttl` and `xyz.ttl.graph`, where `xyz.ttl` is the actual triples file and
    `xyz.ttl.graph` contains the graph IRI in the first line: `https://mygraph.de/xyz/`.

    If input is a directory AND a graph IRI is given, it scans for all `*.ttl` files
    in the directory and imports all content to the graph, ignoring the `*.ttl.graph`
    files.

    If the `--replace` flag is set, the data in the graphs will be overwritten,
    if not, it will be added.

    Note: Directories are scanned on the first level only (not recursively).
    """
    # is an array of tuples like this [('path/to/triple.file', 'graph IRI')]
    if replace and skip_existing:
        raise ValueError(
            "The options --replace and --skip-existing are mutually "
            "exclusive, so please remove one of them."
        )
    graphs: list
    if Path(input_path).is_dir():
        validate_input_path(input_path)
        if iri is None:
            # in case a directory is the source (and no IRI is given),
            # the graph/nt file structure is crawled
            graphs = read_rdf_graph_files(input_path)
        else:
            # in case a directory is the source AND IRI is given
            graphs = [(file, iri) for file in Path(input_path).glob("*.ttl")]
            graphs += [(file, iri) for file in Path(input_path).glob("*.ttl.gz")]
    elif Path(input_path).is_file():
        if iri is None:
            raise ValueError(
                "Either specify an input file AND a graph IRI or an input directory ONLY."
            )
        graphs = [(input_path, iri)]
    else:
        raise NotImplementedError(
            "Input from special files (socket, FIFO, device file) is not supported."
        )

    existing_graphs = get_graphs_as_dict()
    processed_graphs: set = set()
    count: int = len(graphs)
    current: int = 1
    for triple_file, graph_iri in graphs:
        app.echo_info(
            f"Import file {current}/{count}: " f"{graph_iri} from {triple_file} ... ", nl=False
        )
        if graph_iri in existing_graphs and skip_existing:
            app.echo_warning("skipped")
            continue
        # prevents re-replacing of graphs in a single run
        _replace = False if graph_iri in processed_graphs else replace
        _buffer = io.BytesIO()
        transport_prams = {}
        if Path(str(triple_file)).schema in ["http", "https"]:
            transport_prams["headers"] = {
                "Accept": "text/turtle; q=1.0, application/x-turtle; q=0.9, text/n3;"
                " q=0.8, application/rdf+xml; q=0.5, text/plain; q=0.1"
            }
        with ClickSmartPath.open(triple_file, transport_params=transport_prams) as _:
            _buffer.write(_.read())
        _buffer.seek(0)
        response = graph_api.post_streamed(graph_iri, _buffer, replace=_replace)
        request_headers = response.request.headers
        request_headers.pop("Authorization")
        app.echo_debug(f"cmemc request headers: {request_headers}")
        app.echo_debug(f"server response headers: {response.headers}")
        app.echo_success("replaced" if _replace else "added")
        # refresh access conditions in case of dropped AC graph
        if graph_iri == refresh.AUTHORIZATION_GRAPH_URI:
            refresh.get()
            app.echo_debug("Access conditions refreshed.")
        processed_graphs.add(graph_iri)
        current += 1


@click.command(cls=CmemcCommand, name="delete")
@click.option("-a", "--all", "all_", is_flag=True, help="Delete all writeable graphs.")
@click.option(
    "--include-imports",
    is_flag=True,
    help="Delete selected graph(s) and all writeable graphs which are "
    "imported from these selected graph(s).",
)
@click.argument(
    "iris",
    nargs=-1,
    type=click.STRING,
    shell_complete=completion.writable_graph_uris,
    callback=tuple_to_list,
)
@click.pass_obj
def delete_command(
    app: ApplicationContext, all_: bool, include_imports: bool, iris: list[str]
) -> None:
    """Delete graph(s) from the store."""
    graphs = get_graphs_as_dict(writeable=True, readonly=False)
    iris = _check_and_extend_exported_graphs(iris, all_, include_imports, graphs)

    count: int = len(iris)
    for current, iri in enumerate(iris, start=1):
        app.echo_info(f"Drop graph {current}/{count}: {iri} ... ", nl=False)
        graph_api.delete(iri)
        app.echo_success("done")
        # refresh access conditions in case of dropped AC graph
        if iri == refresh.AUTHORIZATION_GRAPH_URI:
            refresh.get()
            app.echo_debug("Access conditions refreshed.")


@click.command(cls=CmemcCommand, name="open")
@click.argument("iri", type=click.STRING, shell_complete=completion.graph_uris)
@click.pass_obj
def open_command(app: ApplicationContext, iri: str) -> None:
    """Open / explore a graph in the browser."""
    explore_uri = get_cmem_base_uri() + "/explore?graph=" + quote(iri)
    click.launch(explore_uri)
    app.echo_debug(explore_uri)


@click.command(cls=CmemcCommand, name="count")
@click.option("-a", "--all", "all_", is_flag=True, help="Count all graphs")
@click.option(
    "-s", "--summarize", is_flag=True, help="Display only a sum of all counted graphs together"
)
@click.argument("iris", nargs=-1, type=click.STRING, shell_complete=completion.graph_uris)
@click.pass_obj
def count_command(
    app: ApplicationContext, all_: bool, summarize: bool, iris: tuple[str, ...]
) -> None:
    """Count triples in graph(s).

    This command lists graphs with their triple count.
    Counts do not include imported graphs.
    """
    if not iris and not all_:
        raise ValueError(
            "Either specify at least one graph IRI " "or use the --all option to count all graphs."
        )
    if all_:
        # in case --all is given,
        # list of graphs is filled with all available graph IRIs
        iris = tuple(iri["iri"] for iri in get_graphs())

    count: int
    overall_sum: int = 0
    for iri in iris:
        count = count_graph(iri)
        overall_sum = overall_sum + count
        if not summarize:
            app.echo_result(f"{count!s} {iri}")
    if summarize:
        app.echo_result(str(overall_sum))


@click.group(cls=CmemcGroup)
def graph() -> CmemcGroup:  # type: ignore[empty-body]
    """List, import, export, delete, count, tree or open graphs.

    Graphs are identified by an IRI.

    Note: The get a list of existing graphs,
    execute the `graph list` command or use tab-completion.
    """


graph.add_command(count_command)
graph.add_command(tree_command)
graph.add_command(list_command)
graph.add_command(export_command)
graph.add_command(delete_command)
graph.add_command(import_command)
graph.add_command(open_command)
graph.add_command(validation_group)
