# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List
from typing_extensions import TypeAlias

from .source_metadata import SourceMetadata

__all__ = ["MetadataRetrieveResponse"]

MetadataRetrieveResponse: TypeAlias = List[SourceMetadata]
