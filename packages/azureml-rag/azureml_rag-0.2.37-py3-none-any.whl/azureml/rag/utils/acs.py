# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Functions for interacting with AzureSearch."""

from importlib.util import find_spec, module_from_spec
from packaging import version as pkg_version


def _get_azuresearch_module_instance(langchain_package_version: pkg_version.Version):
    module_spec_name = 'langchain.vectorstores.azuresearch'
    if (langchain_package_version >= pkg_version.parse("0.1.00")):
        module_spec_name = 'langchain_community.vectorstores.azuresearch'
    module_spec = find_spec(module_spec_name)
    if module_spec is None:
        raise ImportError(f"Module {module_spec_name} not found")
    azuresearch = module_from_spec(module_spec)
    module_spec.loader.exec_module(azuresearch)

    azuresearch.AzureSearchVectorStoreRetriever.AzureSearch = azuresearch.AzureSearch
    azuresearch.AzureSearchVectorStoreRetriever.model_rebuild()

    return azuresearch
