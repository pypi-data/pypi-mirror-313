"""
Settings management for Argilla datasets.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

import argilla as rg


@dataclass
class DatasetTemplate:
    """Base template for dataset settings."""

    name: str
    guidelines: str = ""
    allow_extra_metadata: bool = True
    metadata_properties: List[Dict[str, Any]] = field(default_factory=list)


class SettingsManager:
    """
    Manages dataset settings and provides templates for common dataset types.
    """

    @staticmethod
    def create_metadata_properties(
        metadata_fields: List[str]
    ) -> List[Dict[str, Any]]:
        """Convert metadata field names to property configurations."""
        return [{"name": field} for field in metadata_fields]

    @staticmethod
    def create_text_classification(
        labels: List[str],
        guidelines: str = "",
        include_metadata: bool = True,
        metadata_fields: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Create settings for a text classification dataset.

        Args:
            labels: List of classification labels
            guidelines: Dataset guidelines
            include_metadata: Whether to include default metadata fields
            metadata_fields: Additional metadata fields to include
        """
        settings = {"guidelines": guidelines, "task": "TextClassification", "labels": labels}

        if include_metadata:
            default_metadata = ["source", "date", "confidence"]
            if metadata_fields:
                default_metadata.extend(metadata_fields)
            settings["metadata_properties"] = SettingsManager.create_metadata_properties(default_metadata)

        return settings

    @staticmethod
    def create_qa_dataset(
        include_context: bool = True,
        include_keywords: bool = True,
        include_references: bool = False,
        guidelines: str = "Dataset for question-answer pairs",
    ) -> Dict[str, Any]:
        """
        Create settings for a Q&A dataset.

        Args:
            include_context: Whether to include context field
            include_keywords: Whether to include keywords field
            include_references: Whether to include references field
            guidelines: Dataset guidelines
        """
        fields = [
            rg.TextField(name="question", required=True),
            rg.TextField(name="answer", required=True),
        ]

        if include_context:
            fields.append(rg.TextField(name="context", required=False))

        if include_keywords:
            fields.append(rg.TextField(name="keywords", required=False))

        if include_references:
            fields.append(rg.TextField(name="references", required=False))

        return {
            "guidelines": guidelines,
            "fields": fields,
            "metadata_properties": [{"name": "source"}, {"name": "date"}, {"name": "confidence"}],
        }

    @staticmethod
    def create_text_generation(
        include_prompt_template: bool = True,
        include_context: bool = True,
        guidelines: str = "Dataset for text generation",
    ) -> Dict[str, Any]:
        """
        Create settings for a text generation dataset.

        Args:
            include_prompt_template: Whether to include prompt template field
            include_context: Whether to include context field
            guidelines: Dataset guidelines
        """
        fields = [
            rg.TextField(name="prompt", required=True),
            rg.TextField(name="response", required=True),
        ]

        if include_prompt_template:
            fields.append(rg.TextField(name="template", required=False))

        if include_context:
            fields.append(rg.TextField(name="context", required=False))

        return {
            "guidelines": guidelines,
            "fields": fields,
            "metadata_properties": [
                {"name": "model"},
                {"name": "date"},
                {"name": "temperature"},
                {"name": "max_tokens"},
            ],
        }

    @staticmethod
    def create_text_summarization(
        include_metadata: bool = True,
        include_keywords: bool = True,
        guidelines: str = "Dataset for text summarization",
    ) -> Dict[str, Any]:
        """
        Create settings for a text summarization dataset.

        Args:
            include_metadata: Whether to include metadata fields
            include_keywords: Whether to include keywords field
            guidelines: Dataset guidelines
        """
        fields = [
            rg.TextField(name="text", required=True),
            rg.TextField(name="summary", required=True),
        ]

        if include_keywords:
            fields.append(rg.TextField(name="keywords", required=False))

        metadata = []
        if include_metadata:
            metadata = [
                {"name": "source"},
                {"name": "date"},
                {"name": "length_ratio"},
                {"name": "compression_ratio"},
            ]

        return {"guidelines": guidelines, "fields": fields, "metadata_properties": metadata}

    @staticmethod
    def create_custom_dataset(
        fields: List[Dict[str, Any]],
        guidelines: str = "",
        metadata_properties: Optional[List[Dict[str, Any]]] = None,
    ) -> Dict[str, Any]:
        """
        Create settings for a custom dataset.

        Args:
            fields: List of field configurations
            guidelines: Dataset guidelines
            metadata_properties: List of metadata field configurations
        """
        return {
            "guidelines": guidelines,
            "fields": [rg.TextField(**field) for field in fields],
            "metadata_properties": metadata_properties or [],
        } 