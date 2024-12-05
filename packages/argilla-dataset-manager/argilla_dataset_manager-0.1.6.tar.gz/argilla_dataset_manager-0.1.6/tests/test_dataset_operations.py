"""
Test script for dataset management operations.
"""

import logging
import sys
from datetime import datetime
from pathlib import Path

import argilla as rg

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

from argilla_dataset_manager.datasets.settings_manager import DatasetTemplate, SettingsManager
from argilla_dataset_manager.utils.argilla_client import get_argilla_client
from argilla_dataset_manager.utils.dataset_manager import DatasetManager

# Use an existing workspace for testing
TEST_WORKSPACE = "qa_workspace"  # This workspace exists in your Argilla instance

def test_connection() -> rg.Argilla:
    """Test Argilla connection."""
    try:
        client = get_argilla_client()
        logger.info("✓ Successfully connected to Argilla")
        return client
    except Exception as e:
        logger.error(f"✗ Failed to connect to Argilla: {str(e)}")
        raise

def test_dataset_creation(client: rg.Argilla) -> rg.Dataset:
    """Test dataset creation with settings."""
    try:
        # Initialize managers
        dataset_manager = DatasetManager(client)
        settings_manager = SettingsManager()
        
        # Create test settings
        test_name = f"test_dataset_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Create dataset settings using SettingsManager
        settings = settings_manager.create_text_classification(
            labels=["question", "answer", "other"],
            guidelines="Test dataset for QA classification"
        )
        
        # Create dataset
        dataset = dataset_manager.create_dataset(
            workspace=TEST_WORKSPACE,
            dataset=test_name,
            settings=settings
        )
        
        logger.info(f"✓ Successfully created test dataset: {test_name}")
        return dataset
        
    except Exception as e:
        logger.error(f"✗ Failed to create dataset: {str(e)}")
        raise

def test_record_creation(dataset: rg.Dataset) -> None:
    """Test adding records to a dataset."""
    try:
        # Create a test record
        record = rg.Record(
            fields={"text": "What is Argilla?"}
        )
        
        # Add record to dataset
        dataset.records.log([record])
        logger.info("✓ Successfully added test record")
        
    except Exception as e:
        logger.error(f"✗ Failed to add record: {str(e)}")
        raise

def main() -> None:
    """Run all tests."""
    try:
        logger.info("Starting dataset operation tests...")
        
        # Test 1: Connection
        client = test_connection()
        
        # Test 2: Dataset Creation
        dataset = test_dataset_creation(client)
        
        # Test 3: Record Creation
        test_record_creation(dataset)
        
        logger.info("All tests completed successfully!")
        
    except Exception as e:
        logger.error(f"Tests failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
