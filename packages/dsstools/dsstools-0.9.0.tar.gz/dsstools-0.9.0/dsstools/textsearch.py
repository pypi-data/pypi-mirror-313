# Copyright (C) 2024 dssTools Developers
# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)
"""This module allows for text search in graph nodes. """

from __future__ import annotations

import logging
import os
from functools import singledispatchmethod
from typing import List, Union
import warnings

import networkx as nx
import pysolr
from requests.auth import HTTPBasicAuth
import requests

from .attrs import Code, Category

logger = logging.getLogger("dsstools")

class TextSearch:
    """Class allowing easy access to the WDC server."""

    def __init__(
        self,
        snapshot: str | None,
        token: str,
        api_endpoint: str = "https://dss-wdc.wiso.uni-hamburg.de/api",
        insecure: bool = False,
        timeout: int = 60,
    ):
        errors = []
        self.token = token
        # Set password through env
        if not insecure and not api_endpoint.startswith("https://"):
            warnings.warn(
                "Not using HTTPS for your request to the Solr server. Consider using encryption."
            )
        self.endpoint = (
            api_endpoint[:-1] if api_endpoint.endswith("/") else api_endpoint
        )
        self.snapshot = snapshot
        self.session = requests.Session()
        headers = {"Token": f"{self.token}"}
        self.session.headers.update(headers)

    @staticmethod
    def _handle_grafted_terms(fun):
        def wrapper(*args, **kwargs):
            domain, terms = args
            # Flatten list internally
            if all(isinstance(term, list) for term in terms):
                response = fun(domain, [t for te in terms for t in te], **kwargs)
                if response is not None:
                    return {
                        term_group[0]: sum(response.get(term) for term in term_group)
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

    def construct_url(self) -> str:
        if self.snapshot:
            return f"{self.endpoint}/snapshot/{self.snapshot}/"
        else:
            raise ValueError("Please set a snapshot id to the TextSearch object first.")

    def get_pages(self, url, params={}):
        response = None
        response = self.session.get(url, params=params)
        try:
            response.raise_for_status()
        except requests.HTTPError as exc:
            invalid_request_reason = response.json()["responseHeader"]["msg"]
            print(f"Your request has failed because: {invalid_request_reason}")
            raise

        first_page = response.json()
        yield first_page
        num_pages = first_page["page"]["totalPages"]

        for page in range(1, num_pages):
            response = self.session.get(url, params={"page": page})
            response.raise_for_status()
            yield response.json()

    def get_missing(self, domains):
        domain_hits = set()
        for page in self.get_pages(self.construct_url() + "domains"):
            for data in page["content"]:
                domain_hits.add(data["domainName"])
        return set(domains) - domain_hits

    def __query_domains(self, domains, query_term, missing_domains=None, key=None) -> dict:
        if key is None:
            key = query_term

        domain_hits = {}
        params = {"query": query_term}
        for page in self.get_pages(self.construct_url() + "searchDomains", params):
            for data in page["content"]:
                domain_hits[data["domainName"]] = data["hits"]
        single_term_hits = {}
        for domain in domains:
            if domain in missing_domains:
                # Make missing domains a None for visualization purposes.
                single_term_hits[domain] = None
            else:
                # Make zero hits an actual zero (and not None).
                single_term_hits[domain] = domain_hits.get(domain, 0)
        return single_term_hits

    @singledispatchmethod
    def search(self, domains, terms, **kwargs):
        """Searches the given keywords across a Graph or iterator.

        Args:
          domains (nx.Graph|list): Set of identifiers to search in.
          terms list[str]: Terms to search for.
          **kwargs: Are passed onto the internal dispatch function.

        Returns:
          Updated graph or dict containing the responses, Set of all failed
          responses
        """
        raise NotImplementedError("Can only search on domain lists or graphs.")

    # TODO How to handle literal terms?
    @search.register
    def _(
        self,
        domains: list,
        terms: Union[List[str], List[List[str]]],
        summarize=False,
        exact=True,
    ) -> dict:
        def traverse_lists(lst):
            if isinstance(lst, list):
                for value in lst:
                    for inner_value in traverse_lists(lst):
                        yield inner_value
            else:
                yield lst


        if not exact:
            raise NotImplementedError()

        term_hits = {}
        missing_domains = self.get_missing(domains)
        logger.info(f"The following terms are set for the query: {terms}")
        keys = {}
        # if smart_query:
        #     for term in terms:
        #     keys = {}

        for term in terms:
            # This only works for list in lists and not for higher level ones. But
            # it would not make much sense tbh.
            if isinstance(term, list) and not summarize:
                logger.info(f"Querying API for {term}...")
                term_hits.update(
                    {t: self.__query_domains(domains, t, missing_domains) for t in term}
                )
            else:
                # Grafted list are handled the same if `concat=True` is selected as one
                # single query is constructed. Only the key handling differs.
                logger.info(f"Querying API for {term}...")
                if isinstance(term, list):
                    query_term = " OR ".join(term)
                    key = term[0]
                    # TODO literal_terms
                else:
                    query_term = term
                    key = term
                term_hits[key] = self.__query_domains(
                    domains, query_term, missing_domains, key=key
                )

        # Transpose dict of dict (nested dict). We first get the keys from the first
        # entry and then construct the resulting new dictionary. See for an explanation
        # here:
        # https://stackoverflow.com/questions/33425871/rearranging-levels-of-a-nested-dictionary-in-python
        # This could also be done by converting to a Pandas DataFrame as a dict of dict
        # is equivalent to a 2D matrix:
        # df = pd.DataFrame.from_dict(term_hits).T
        keys = term_hits[next(iter(term_hits.keys()))].keys()
        return {key:{k:term_hits[k][key] for k in term_hits if key in term_hits[k]} for key in keys}


    @search.register
    def _(
        self,
        domains: nx.Graph,
        terms: Union[List[str], List[List[str]]],
        summarize=False,
        exact=True,
    ) -> nx.Graph:
        domain_hits = self.search(
            list(domains.nodes), terms, summarize=summarize
        )
        for node_id, values in domain_hits.items():
            node = domains.nodes[node_id]
            for key,value in values.items():
                if value is not None:
                    node[str(Code(key, Category.TEXT))] = value
        return domains
