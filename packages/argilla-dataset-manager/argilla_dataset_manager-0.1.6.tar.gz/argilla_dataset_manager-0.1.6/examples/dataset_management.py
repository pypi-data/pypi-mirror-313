import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

import argilla as rg

from my_datasets import SettingsManager, create_qa_dataset_settings
from utils import DatasetManager, get_argilla_client


def main():
    # Initialize clients
    client = get_argilla_client()
    dataset_manager = DatasetManager(client)
    settings_manager = SettingsManager()

    # Example 1: Create and save a new dataset configuration
    qa_settings = create_qa_dataset_settings(
        name="enhanced_qa_dataset", include_context=True, include_keywords=True
    )
    settings_manager.save_settings(qa_settings, "enhanced_qa_config")

    # Create initial workspace and dataset if they don't exist
    source_workspace = "qa_workspace"

    try:
        client.get_workspace(source_workspace)
    except:
        try:
            workspace_to_create = rg.Workspace(name=source_workspace)
            workspace_to_create.create()
        except Exception as e:
            # Workspace already exists, we can continue
            pass

    settings = rg.Settings(
        guidelines="Dataset for Q&A pairs with context and keywords",
        fields=[
            rg.TextField(
                name="prompt",
                title="User's Question (Prompt)",
            ),
            rg.TextField(
                name="response",
                title="Agent's Response",
            ),
            rg.TextField(
                name="context",
                title="Context of the Conversation",
            ),
            rg.TextField(
                name="keywords",
                title="Keywords Associated with the Entry",
            ),
        ],
        allow_extra_metadata=True,
        questions=[
            rg.RatingQuestion(
                name="rating",
                title="Rating of the Q&A pair",
                description="Please rate the Q&A pair from 1 to 5",
                values=[1, 2, 3, 4, 5],
                required=True,
            )
        ],
    )

    # Check if dataset exists before creating
    try:
        source_dataset = client.datasets(name="initial_qa_dataset", workspace=source_workspace)[0]
    except:
        source_dataset = rg.Dataset(
            name="initial_qa_dataset", workspace=source_workspace, settings=settings
        )
        source_dataset.create()

        # Add sample records only for new dataset
        sample_records = [
            {
                "prompt": "What is machine learning?",
                "response": "Machine learning is a subset of AI...",
                "context": "AI fundamentals discussion",
                "keywords": "AI,ML,fundamentals",
            },
            {
                "prompt": "Explain neural networks",
                "response": "Neural networks are computing systems...",
                "context": "Deep learning basics",
                "keywords": "neural networks,deep learning",
            },
        ]
        source_dataset.records.log(sample_records)

    # Example 2: Migrate dataset with enhanced settings
    target_workspace = "enhanced_workspace"

    # Create target workspace if it doesn't exist
    try:
        client.get_workspace(target_workspace)
    except:
        try:
            client.create_workspace(target_workspace)
        except Exception as e:
            # Workspace already exists, we can continue
            pass

    # Only migrate if target dataset doesn't exist
    if not client.datasets(name="enhanced_dataset", workspace=target_workspace):
        argilla_settings = settings_manager.create_settings(qa_settings)
        dataset_manager.migrate_dataset(
            source_workspace=source_workspace,
            source_dataset="initial_qa_dataset",
            target_workspace=target_workspace,
            target_dataset="enhanced_dataset",
            new_settings=argilla_settings,
            # Transform records during migration
            transform_record=lambda record: {
                **record.fields,
                "keywords": record.fields.get("keywords", "").split(","),
            },
        )

    # Example 3: Create a new version with updated settings
    updated_settings = create_qa_dataset_settings(
        name="qa_dataset_v2", include_context=True, include_keywords=True
    )
    argilla_settings = settings_manager.create_settings(updated_settings)
    dataset_manager.update_dataset_settings(
        workspace=target_workspace,
        dataset="enhanced_dataset",
        new_settings=argilla_settings,
        create_new_version=True,
    )

    # Example 4: Clone dataset to new workspace
    final_workspace = "production_workspace"

    # Create final workspace if it doesn't exist
    try:
        client.get_workspace(final_workspace)
    except:
        try:
            client.create_workspace(final_workspace)
        except Exception as e:
            # Workspace already exists, we can continue
            pass

    # Only clone if target dataset doesn't exist
    if not client.datasets(name="production_dataset", workspace=final_workspace):
        dataset_manager.clone_dataset(
            workspace=target_workspace,
            dataset="enhanced_dataset",
            new_name="production_dataset",
            new_workspace=final_workspace,
        )


if __name__ == "__main__":
    main()
