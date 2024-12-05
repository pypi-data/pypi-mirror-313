"""
Argilla client configuration and setup.
"""

import logging
import os
from typing import Optional

import argilla as rg
from dotenv import load_dotenv

logger = logging.getLogger(__name__)


def get_argilla_client() -> rg.Argilla:
    """
    Create and configure an Argilla client using environment variables.

    Required environment variables:
    - ARGILLA_API_URL: The URL of your Argilla instance
    - ARGILLA_API_KEY: Your Argilla API key
    - HF_TOKEN: Optional Hugging Face token for private spaces

    Returns:
        rg.Client: Configured Argilla client

    Raises:
        ValueError: If required environment variables are missing
        ConnectionError: If unable to connect to Argilla
    """
    # Load environment variables
    load_dotenv()

    # Get required environment variables
    api_url = os.getenv("ARGILLA_API_URL")
    api_key = os.getenv("ARGILLA_API_KEY")
    hf_token = os.getenv("HF_TOKEN")

    if not api_url or not api_key:
        raise ValueError(
            "Missing required environment variables. Please ensure ARGILLA_API_URL "
            "and ARGILLA_API_KEY are set in your .env file."
        )

    try:
        # Initialize the client
        client_kwargs = {"api_url": api_url, "api_key": api_key}

        # Add HF token header if provided
        if hf_token:
            client_kwargs["headers"] = {"Authorization": f"Bearer {hf_token}"}

        client = rg.Argilla(**client_kwargs)

        # Test connection
        client.http_client.get("/api/me")
        logger.info("Successfully connected to Argilla")
        return client

    except Exception as e:
        raise ConnectionError(f"Failed to connect to Argilla: {str(e)}")


def get_or_create_workspace(
    client: rg.Argilla, workspace_name: str, create_if_missing: bool = True
) -> Optional[rg.Workspace]:
    """
    Get or create an Argilla workspace.

    Args:
        client: Argilla client
        workspace_name: Name of the workspace
        create_if_missing: Whether to create the workspace if it doesn't exist

    Returns:
        rg.Workspace or None: The workspace object if found/created, None if not found and create_if_missing is False
    """
    try:
        return client.get_workspace(workspace_name)
    except Exception as e:
        if create_if_missing:
            logger.info(f"Creating workspace: {workspace_name}")
            workspace = rg.Workspace(name=workspace_name)
            workspace.create()
            return workspace
        logger.warning(f"Workspace not found: {workspace_name}")
        return None


def get_or_create_dataset(
    client: rg.Argilla,
    workspace: rg.Workspace,
    dataset_name: str,
    settings: dict,
    create_if_missing: bool = True,
) -> Optional[rg.Dataset]:
    """
    Get or create an Argilla dataset.

    Args:
        client: Argilla client
        workspace: Workspace object
        dataset_name: Name of the dataset
        settings: Dataset settings
        create_if_missing: Whether to create the dataset if it doesn't exist

    Returns:
        rg.Dataset or None: The dataset object if found/created, None if not found and create_if_missing is False
    """
    try:
        return client.get_dataset(dataset_name, workspace=workspace.name)
    except Exception as e:
        if create_if_missing:
            logger.info(f"Creating dataset: {dataset_name}")
            dataset = rg.Dataset(name=dataset_name, workspace=workspace.name, settings=settings)
            dataset.create()
            return dataset
        logger.warning(f"Dataset not found: {dataset_name}")
        return None


def log_records_to_dataset(dataset, records):
    """
    Log records to Argilla dataset.

    Args:
        dataset: Argilla dataset instance.
        records (list): List of Argilla records.
    """
    dataset.records.log(records)
