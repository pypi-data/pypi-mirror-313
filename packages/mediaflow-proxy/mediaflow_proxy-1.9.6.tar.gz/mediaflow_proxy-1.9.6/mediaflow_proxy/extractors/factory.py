from typing import Dict, Type

from mediaflow_proxy.extractors.base import BaseExtractor, ExtractorError
from mediaflow_proxy.extractors.doodstream import DoodStreamExtractor
from mediaflow_proxy.extractors.livetv import LiveTVExtractor
from mediaflow_proxy.extractors.mixdrop import MixdropExtractor
from mediaflow_proxy.extractors.uqload import UqloadExtractor


class ExtractorFactory:
    """Factory for creating URL extractors."""

    _extractors: Dict[str, Type[BaseExtractor]] = {
        "Doodstream": DoodStreamExtractor,
        "Uqload": UqloadExtractor,
        "Mixdrop": MixdropExtractor,
        "LiveTV": LiveTVExtractor,
    }

    @classmethod
    def get_extractor(cls, host: str, request_headers: dict) -> BaseExtractor:
        """Get appropriate extractor instance for the given host."""
        extractor_class = cls._extractors.get(host)
        if not extractor_class:
            raise ExtractorError(f"Unsupported host: {host}")
        return extractor_class(request_headers)
