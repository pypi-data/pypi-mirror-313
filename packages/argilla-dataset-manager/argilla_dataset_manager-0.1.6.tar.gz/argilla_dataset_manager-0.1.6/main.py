import argilla as rg

from config import Config
from my_datasets.dataset_settings import get_dataset_settings
from utils.argilla_client import (
    get_argilla_client,
    get_or_create_dataset,
    get_or_create_workspace,
    log_records_to_dataset,
)
from utils.data_loader import load_csv_files
from utils.data_processor import process_dataframe
from utils.logger import setup_logger


def main():
    logger = setup_logger()

    # Load Data
    logger.info("Loading data...")
    file_paths = {
        "confluence_qa_v2_df": "path/to/confluence_qa_v2.csv",
        # Add other files as needed
    }
    dataframes = load_csv_files(file_paths)

    # Process Data
    logger.info("Processing data...")
    processed_df = process_dataframe(dataframes["confluence_qa_v2_df"])

    # Initialize Argilla client
    logger.info("Initializing Argilla client...")
    client = get_argilla_client()

    # Get or create workspace and dataset
    workspace_name = "keboola-slack-confluence"
    dataset_name = "keboola-slack-confluence-v2"
    settings = get_dataset_settings()
    workspace = get_or_create_workspace(client, workspace_name)
    dataset = get_or_create_dataset(client, workspace, dataset_name, settings)

    # Prepare Argilla records
    logger.info("Preparing records...")
    records = []
    for _, row in processed_df.iterrows():
        record = rg.Record(
            fields={
                "prompt": row.get("prompt", "").strip(),
                "response": row.get("response", "").strip(),
                "context": row.get("context", "").strip(),
                "keywords": row.get("keywords", "").strip(),
                "category": row.get("category", "").strip(),
                "references": row.get("references", "").strip(),
            },
            metadata={
                "conversation_date": row.get("conversation_date", "").strip(),
                "source_platform": row.get("source_platform", "").strip(),
            },
        )
        records.append(record)

    # Log records to Argilla dataset
    logger.info(f"Logging {len(records)} records to the dataset...")
    log_records_to_dataset(dataset, records)
    logger.info("Data upload completed successfully.")


if __name__ == "__main__":
    main()
