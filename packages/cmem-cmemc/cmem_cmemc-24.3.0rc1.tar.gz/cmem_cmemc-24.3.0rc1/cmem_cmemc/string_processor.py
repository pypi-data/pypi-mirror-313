"""Helper functions for rich text output"""

from abc import ABC, abstractmethod
from datetime import datetime, timezone
from urllib.parse import quote

import timeago
from cmem.cmempy.config import get_cmem_base_uri

from cmem_cmemc.title_helper import TitleHelper
from cmem_cmemc.utils import get_graphs_as_dict


class StringProcessor(ABC):
    """ABC of a table cell string processor"""

    @abstractmethod
    def process(self, text: str) -> str:
        """Process a single string content and output the processed string."""


class TimeAgo(StringProcessor):
    """Create a string similar to 'x minutes ago' from a timestamp"""

    def process(self, text: str) -> str:
        """Process a single string content and output the processed string."""
        stamp = datetime.fromtimestamp(int(text) / 1000, tz=timezone.utc)
        return str(timeago.format(stamp, datetime.now(tz=timezone.utc)))


class GraphLink(StringProcessor):
    """Create a graph link from an IRI cell

    "Visit my [link=https://www.willmcgugan.com]blog[/link]!"
    """

    def __init__(self) -> None:
        self.cmem_base_uri = get_cmem_base_uri()
        self.base = self.cmem_base_uri + "/explore?graph="
        self.graph_labels: dict[str, str] = {}
        for _ in get_graphs_as_dict().values():
            self.graph_labels[_["iri"]] = _["label"]["title"]

    def process(self, text: str) -> str:
        """Process a single string content and output the processed string."""
        link = self.base + quote(text)
        label = self.graph_labels.get(text, None)
        return f"[link={link}]{label}[/link]" if label else text


class ResourceLink(StringProcessor):
    """Create a resource link from an IRI cell

    "Visit my [link=https://www.willmcgugan.com]blog[/link]!"
    """

    def __init__(self, graph_iri: str, title_helper: TitleHelper | None = None):
        self.graph_iri = graph_iri
        self.base = get_cmem_base_uri() + "/explore?graph=" + quote(graph_iri) + "&resource="
        self.title_helper = title_helper if title_helper else TitleHelper()

    def process(self, text: str) -> str:
        """Process a single string content and output the processed string."""
        link = self.base + quote(text)
        label = self.title_helper.get(text)
        return f"[link={link}]{label}[/link]"


def process_row(row: list[str], hints: dict[int, StringProcessor]) -> list[str]:
    """Process all cells in a row according to the StringProcessors"""
    processed_row = []
    for column_number, cell in enumerate(row):
        if hints.get(column_number):
            processed_row.append(hints[column_number].process(cell))
        else:
            processed_row.append(cell)
    return processed_row
