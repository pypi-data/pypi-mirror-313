"""
Argilla Dataset Management Tutorial
=================================

This script demonstrates how to use the advanced dataset management features for Argilla.
Each section is clearly marked and includes instructions for when to check the Argilla UI
for results.

Before running this script:
1. Make sure you have your .env file configured with:
   ARGILLA_API_URL=your_argilla_api_url
   ARGILLA_API_KEY=your_api_key
2. Replace the workspace and dataset names with your actual values
"""

import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from my_datasets import SettingsManager, create_qa_dataset_settings
from utils import DatasetManager, get_argilla_client


def tutorial():
    """
    Run through the dataset management tutorial step by step.
    """
    print("Step 1: Initialize Clients")
    print("-------------------------")
    # Initialize our management clients
    client = get_argilla_client()
    dataset_manager = DatasetManager(client)
    settings_manager = SettingsManager()
    print("✓ Clients initialized successfully")
    print()

    print("Step 2: Create and Save Dataset Configuration")
    print("-----------------------------------------")
    # Create a new dataset configuration with context and keywords
    qa_settings = create_qa_dataset_settings(
        name="enhanced_qa_dataset", include_context=True, include_keywords=True
    )

    # Save the configuration for later use
    config_path = settings_manager.save_settings(qa_settings, "enhanced_qa_config")
    print(f"✓ Configuration saved to: {config_path}")
    print("→ Check your project directory for the new YAML configuration file")
    print()

    print("Step 3: Migrate Dataset with New Settings")
    print("-------------------------------------")
    print("This step will migrate an existing dataset to a new one with enhanced settings")

    # Convert our settings to Argilla format
    argilla_settings = settings_manager.create_settings(qa_settings)

    # Migrate the dataset
    source_workspace = "qa_workspace"  # Replace with your source workspace
    source_dataset = "initial_qa_dataset"  # Replace with your source dataset
    target_workspace = "keboola-slack-ft-model-comparison"  # Replace with your target workspace
    target_dataset = "enhanced_dataset"  # Replace with your desired target name

    print(f"Migrating dataset from {source_workspace}/{source_dataset}")
    print(f"to {target_workspace}/{target_dataset}")

    new_dataset = dataset_manager.migrate_dataset(
        source_workspace=source_workspace,
        source_dataset=source_dataset,
        target_workspace=target_workspace,
        target_dataset=target_dataset,
        new_settings=argilla_settings,
        # Optional: Transform records during migration
        transform_record=lambda record: {
            **record.fields,
            "keywords": record.fields.get("keywords", "").split(","),
        },
    )
    print("✓ Migration completed")
    print("→ Check Argilla UI now to see:")
    print("  1. New dataset in your target workspace")
    print("  2. Migrated records with new field configuration")
    print("  3. Keywords split into arrays")
    print()

    print("Step 4: Create a New Dataset Version")
    print("--------------------------------")
    print("This step will create a new version of a dataset with updated settings")

    # Create updated settings
    updated_settings = create_qa_dataset_settings(
        name="qa_dataset_v2", include_context=True, include_keywords=True
    )
    argilla_settings = settings_manager.create_settings(updated_settings)

    workspace = "keboola-slack-ft-model-comparison"  # Replace with your workspace
    dataset = "qa_dataset"  # Replace with your dataset

    print(f"Creating new version of {workspace}/{dataset}")

    new_version = dataset_manager.update_dataset_settings(
        workspace=workspace, dataset=dataset, new_settings=argilla_settings, create_new_version=True
    )
    print("✓ New version created")
    print("→ Check Argilla UI now to see:")
    print("  1. New dataset with timestamp suffix")
    print("  2. All records from original dataset")
    print("  3. Updated field configuration")
    print()

    print("Step 5: Clone Dataset to New Workspace")
    print("----------------------------------")
    print("This step will clone a dataset to a different workspace")

    source_workspace = "qa_workspace"  # Replace with source workspace
    source_dataset = "qa_dataset"  # Replace with source dataset
    target_workspace = "target_workspace"  # Replace with target workspace

    print(f"Cloning {source_workspace}/{source_dataset}")
    print(f"to {target_workspace}/cloned_dataset")

    cloned_dataset = dataset_manager.clone_dataset(
        workspace=source_workspace,
        dataset=source_dataset,
        new_name="cloned_dataset",
        new_workspace=target_workspace,
    )
    print("✓ Dataset cloned successfully")
    print("→ Check Argilla UI now to see:")
    print("  1. Exact copy of dataset in target workspace")
    print("  2. All records and settings preserved")
    print()

    print("Tutorial Complete!")
    print("----------------")
    print("Next steps:")
    print("1. Create custom dataset configurations for your needs")
    print("2. Set up automated dataset versioning workflows")
    print("3. Implement data transformation during migrations")
    print("4. Manage multiple dataset versions across workspaces")


if __name__ == "__main__":
    tutorial()
