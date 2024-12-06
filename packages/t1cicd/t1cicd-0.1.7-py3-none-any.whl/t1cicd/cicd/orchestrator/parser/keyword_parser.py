"""
This module contains the KeywordParser and related classes for parsing keyword-related data.
"""

from abc import ABC, abstractmethod

from t1cicd.cicd.orchestrator.parser.artifact import Artifact


class KeywordParser(ABC):
    """
    Abstract base class for keyword parsers.
    """

    @abstractmethod
    def parse(self, value):
        """
        Parse the given value.

        Args:
            value: The value to be parsed.

        Returns:
            The parsed value.
        """


class KeywordParserFactory(ABC):
    """
    Factory class for creating keyword parsers.
    """

    @staticmethod
    def get_parser(keyword: str) -> KeywordParser:
        """
        Get the parser for the given keyword.

        Args:
            keyword (str): The keyword to get the parser for.

        Returns:
            KeywordParser: The parser for the given keyword.

        Raises:
            ValueError: If the keyword is unknown.
        """
        if keyword == "stage":
            return StageParser()
        if keyword == "needs":
            return NeedParser()
        if keyword == "script":
            return ScriptParser()
        if keyword == "artifacts":
            return ArtifactsParser()
        if keyword == "image":
            return ImageParser()
        if keyword == "allow_failure":
            return AllowFailureParser()

        raise ValueError(f"Unknown keyword: {keyword}")


class StageParser(KeywordParser):
    """
    Parser for the 'stage' keyword.
    """

    def parse(self, value):
        if not isinstance(value, str):
            raise ValueError(f"Expected a string, got {type(value)}")
        return value


class NeedParser(KeywordParser):
    """
    Parser for the 'needs' keyword.
    """

    def parse(self, value):
        if not isinstance(value, list):
            raise ValueError(f"Expected a list, got {type(value)}")
        return value


class ScriptParser(KeywordParser):
    """
    Parser for the 'script' keyword.
    """

    def parse(self, value):
        if not isinstance(value, list) and not isinstance(value, str):
            raise ValueError(f"Expected a list or string, got {type(value)}")
        return value


class ArtifactsParser(KeywordParser):
    """
    Parser for the 'artifacts' keyword.
    """

    def parse(self, value):
        if not isinstance(value, object):
            raise ValueError(f"Expected a Object, got {type(value)}")
        return Artifact(paths=value["paths"])


class ImageParser(KeywordParser):
    """
    Parser for the 'image' keyword.
    """

    def parse(self, value):
        if not isinstance(value, str):
            raise ValueError(f"Expected a string, got {type(value)}")
        return value


class AllowFailureParser(KeywordParser):
    """
    Parser for the 'allow_failure' keyword.
    """

    def parse(self, value):
        if not isinstance(value, bool):
            raise ValueError(f"Expected a boolean, got {type(value)}")
        return value
