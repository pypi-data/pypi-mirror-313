# Copyright (C) 2024 dssTools Developers
# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)
"""This module enables interaction with our Solr instance."""

from __future__ import annotations

import logging
import os
from functools import singledispatchmethod
from typing import List, Union

import networkx as nx
import pysolr
from requests.auth import HTTPBasicAuth

from .attrs import Code, Category
from .utils import _deprecate


def handle_grafted_terms(fun):
    def wrapper(*args, **kwargs):
        domain, terms = args
        # Flatten list internally
        if all(isinstance(term, list) for term in terms):
            response = fun(domain, [t for te in terms for t in te], **kwargs)
            if response is not None:
                return {
                    term_group[0]: sum([response.get(term) for term in term_group])
                    for term_group in terms
                }
            else:
                return response
        elif any(isinstance(term, list) for term in terms):
            raise ValueError(
                "The passed term list does not exclusively contain either strings or lists."
            )
        else:
            return fun(domain, terms, **kwargs)

    return wrapper

@_deprecate("Use the simpler textsearch module instead.")
class Solr:
    """Class wrapping easy access to the Solr server."""

    def __init__(self, domain, snapshot=-1, insecure=False, timeout=140):
        # Set password through env
        self.password = os.getenv("SOLR_PASSWORD", None)
        if not self.password:
            raise EnvironmentError(
                "Please provide the password for the given Solr user through $SOLR_PASSWORD."
            )
        if not insecure and not domain.startswith("https://"):
            raise UserWarning(
                "Not using HTTPS for your request to the Solr server. Consider using encryption"
            )
        self.domain = domain
        self.username = os.getenv("SOLR_USER", None)
        if not self.username:
            raise EnvironmentError(
                "Please provide the password for the given Solr user through $SOLR_USER."
            )
        self.instance = pysolr.Solr(
            domain, timeout=timeout, auth=HTTPBasicAuth(self.username, self.password)
        )
        self.snapshot = snapshot
        self.chunk_size = 40

    def query_single(
        self, domain: str, terms: List[str], literal_terms=False
    ) -> dict[str, int] | None:
        """Query a single domain for multiple terms.

        Args:
          domain: str: Domain to query.
          terms: list[str]: Terms to query for.
          literal_terms (bool): Toggle for literal matching of search terms. The
            default setup will try to be smart about requested terms like
            escaping spaces. Setting this to True will allow for passing literal
            queries to Solr like regex queries. If you are a starter, leave
            this at default.

        Returns:
          self: Dictionary with the raw response counter keyed by term. If a
                list of list is given, the first value becomes the key.

        """
        # Check if configured correctly
        if self.snapshot < 1:
            raise ValueError("Please set Solr.snapshot to a proper ID value.")

        try:
            # Check if domain exists in database
            if (
                self.instance.search(
                    "*:*",
                    **{"fq": [f"domain_s:{domain}", f"snapshot_id_i:{self.snapshot}"]},
                ).hits
                == 0
            ):
                logging.debug(f"Unable to find {domain} in Solr database. Skipping...")
                return None
        except pysolr.SolrError:
            logging.warning(f"Unable to parse domain '{domain}' in Solr. Skipping...")
            return None

        if not literal_terms:
            terms = [f'"{term}"' for term in terms]

        # Put the query in chunks as long queries lead to empty results (see
        # comment below)
        chunked_query = [
            terms[i : i + self.chunk_size]
            for i in range(0, len(terms), self.chunk_size)
        ]
        values = {}
        for query_chunk in chunked_query:
            # Currently no way to use the full query as apache can't handle
            # super long domains
            results = self.instance.search(
                f"snapshot_id_i:{self.snapshot} && domain_s:{domain}",
                facet="on",
                **{"facet.query": query_chunk},
            )
            if not literal_terms:
                values.update(
                    {
                        key.replace('"', ""): value
                        for key, value in results.facets["facet_queries"].items()
                    }
                )
            else:
                values.update(results.facets["facet_queries"].items())

        return values

    # Note regarding type hinting in the following methods: Using future
    # annotations for tests run in py39 leads to errors as postponed evaluation
    # is incompatible with the singledispatch approach used in this method.
    @singledispatchmethod
    def query_multiple(self, domains, terms, **kwargs):
        """Searches the given keywords across a Graph or iterator.

        Args:
          domains (nx.Graph|list): Set of identifiers to search in.
          terms list[str]: Terms to search for.
          kwargs: Are passed onto the internal query_single function.

        Returns:
          Updated graph or dict containing the responses, Set of all failed
          responses
        """
        raise NotImplementedError("Can only use domain lists and graphs.")

    @query_multiple.register
    def _(
        self, domains: nx.Graph, terms: Union[List[str], List[List[str]]], **kwargs
    ) -> tuple[nx.Graph, set]:
        """Searches the given keywords across a Graph."""
        missing_responses = set()
        if all(isinstance(term, list) for term in terms):
            is_grafted = True
        for domain in domains.nodes:
            response = handle_grafted_terms(self.query_single)(domain, terms, **kwargs)
            node = domains.nodes[domain]
            # Take a note of missing responses
            if response is None:
                missing_responses.add(domain)
                # FIXME Add iteration for None response
            else:
                for key, value in response.items():
                    node[str(Code(key, Category.TEXT))] = value

        return domains, missing_responses

    @query_multiple.register
    def _(
        self, domains: list, terms: Union[List[str], List[List[str]]], **kwargs
    ) -> tuple[dict, set]:
        """Searches the given keywords across a list."""
        missing_responses = set()
        query_results = {}
        for domain in domains:
            response = handle_grafted_terms(self.query_single)(domain, terms, **kwargs)
            # Take a note of missing responses
            if response is None:
                missing_responses.add(domain)
            else:
                query_results[domain] = response

        return query_results, missing_responses
