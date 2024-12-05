"""
Advanced dataset management functionality for Argilla.
"""

import logging
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional

import argilla as rg
from tqdm import tqdm

logger = logging.getLogger(__name__)


class DatasetError(Exception):
    """Base exception for dataset operations."""

    pass


class DatasetManager:
    def __init__(self, client: rg.Argilla):
        """
        Initialize the dataset manager.

        Args:
            client: Configured Argilla client
        """
        self.client = client
        self._validate_client()

    def _validate_client(self) -> None:
        """Validate that the client is properly configured."""
        try:
            self.client.http_client.get("/api/me")
        except Exception as e:
            raise DatasetError(f"Invalid Argilla client configuration: {str(e)}")

    def list_workspaces(self) -> List[rg.Workspace]:
        """
        List all available workspaces.

        Returns:
            List[rg.Workspace]: List of workspace objects

        Raises:
            DatasetError: If workspace listing fails
        """
        try:
            workspaces = self.client.workspaces()
            logger.info(f"Found {len(workspaces)} workspaces")
            for ws in workspaces:
                logger.info(f"Workspace: {ws.name}")
            return workspaces
        except Exception as e:
            raise DatasetError(f"Failed to list workspaces: {str(e)}")

    def list_datasets(self, workspace: str) -> List[rg.Dataset]:
        """
        List all datasets in a workspace.

        Args:
            workspace: Workspace name

        Returns:
            List[rg.Dataset]: List of dataset objects

        Raises:
            DatasetError: If dataset listing fails
        """
        try:
            ws = self._get_workspace(workspace, create=False)
            datasets = ws.datasets
            logger.info(f"Found {len(datasets)} datasets in workspace '{workspace}'")
            for ds in datasets:
                logger.info(
                    f"Dataset: {ds.name}\n"
                    f"  - Records: {len(ds.records)}\n"
                    f"  - Created: {ds.created_at}\n"
                    f"  - Last updated: {ds.last_updated}"
                )
            return datasets
        except Exception as e:
            if not isinstance(e, DatasetError):
                e = DatasetError(f"Failed to list datasets in workspace '{workspace}': {str(e)}")
            raise e

    def _get_workspace(self, workspace: str, create: bool = True) -> rg.Workspace:
        """
        Get or create a workspace.

        Args:
            workspace: Workspace name
            create: Whether to create the workspace if it doesn't exist

        Returns:
            rg.Workspace: The workspace object

        Raises:
            DatasetError: If workspace cannot be accessed or created
        """
        try:
            # First try to get the workspace
            workspace_obj = self.client.workspaces(workspace)
            if workspace_obj is not None:
                logger.info(f"Found existing workspace: {workspace}")
                return workspace_obj

            # If not found and create is True, create it
            if create:
                logger.info(f"Creating new workspace: {workspace}")
                workspace_obj = rg.Workspace(name=workspace, client=self.client)
                return workspace_obj.create()

            raise DatasetError(f"Workspace '{workspace}' not found")

        except Exception as e:
            if not isinstance(e, DatasetError):
                e = DatasetError(f"Error accessing workspace '{workspace}': {str(e)}")
            raise e

    def create_dataset(self, workspace: str, dataset: str, settings: Dict[str, Any]) -> rg.Dataset:
        """
        Create a new dataset.

        Args:
            workspace: Workspace name
            dataset: Dataset name
            settings: Dataset settings dictionary

        Returns:
            rg.Dataset: The created dataset

        Raises:
            DatasetError: If dataset creation fails
        """
        try:
            # Get or create workspace
            ws = self._get_workspace(workspace, create=True)

            # Create the dataset
            logger.info(f"Creating dataset '{dataset}' in workspace '{workspace}'")

            # Create Argilla settings object
            argilla_settings = rg.Settings(
                guidelines=settings.get("guidelines", ""),
                fields=[rg.TextField(name="text")],
                questions=[
                    rg.LabelQuestion(
                        name="label", labels=settings.get("labels", ["positive", "negative"])
                    )
                ],
            )

            # Create and return the dataset
            dataset_obj = rg.Dataset(
                name=dataset, workspace=ws.name, settings=argilla_settings, client=self.client
            )
            return dataset_obj.create()

        except Exception as e:
            if not isinstance(e, DatasetError):
                e = DatasetError(f"Failed to create dataset '{dataset}': {str(e)}")
            raise e

    def migrate_dataset(
        self,
        source_workspace: str,
        source_dataset: str,
        target_workspace: str,
        target_dataset: str,
        new_settings: Dict[str, Any],
        transform_record: Optional[Callable] = None,
        batch_size: int = 100
    ) -> Dataset:
        """
        Migrate records from one dataset to another with new settings.
        """
        logger.info(
            f"Starting dataset migration from {source_workspace}/{source_dataset} "
            f"to {target_workspace}/{target_dataset}"
        )
        
        try:
            # Get source dataset
            source = self.client.datasets(name=source_dataset, workspace=source_workspace)
            if source is None:
                raise DatasetError(f"Source dataset '{source_dataset}' not found")
            
            # Create target dataset
            target = self.create_dataset(
                workspace=target_workspace,
                dataset=target_dataset,
                settings=new_settings
            )
            
            # Get records from source
            records = source.records.list()
            total_records = len(records)
            logger.info(f"Found {total_records} records to migrate")
            
            # Process records in batches
            for i in range(0, total_records, batch_size):
                batch = records[i:i + batch_size]
                
                # Transform records if needed
                if transform_record:
                    try:
                        batch = [transform_record(record) for record in batch]
                    except Exception as e:
                        raise DatasetError(
                            f"Record transformation failed at offset {i}: {str(e)}"
                        )
                
                # Log records to new dataset
                try:
                    target.add_records(batch)
                except Exception as e:
                    raise DatasetError(
                        f"Failed to add records at offset {i}: {str(e)}"
                    )
                
                logger.info(f"Migrated {i + len(batch)} of {total_records} records")
            
            logger.info("Migration completed successfully")
            return target
            
        except Exception as e:
            if not isinstance(e, DatasetError):
                e = DatasetError(f"Migration failed: {str(e)}")
            logger.error(str(e))
            raise e

    def update_dataset_settings(
        self,
        workspace: str,
        dataset: str,
        new_settings: Dict[str, Any],
        create_new_version: bool = True,
    ) -> rg.Dataset:
        """
        Update dataset settings, optionally creating a new version.

        Args:
            workspace: Workspace name
            dataset: Dataset name
            new_settings: New settings to apply
            create_new_version: If True, creates a new version

        Returns:
            rg.Dataset: The updated or new dataset

        Raises:
            DatasetError: If update fails
        """
        try:
            if create_new_version:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                new_name = f"{dataset}_v{timestamp}"
                logger.info(f"Creating new version: {new_name}")

                return self.migrate_dataset(
                    source_workspace=workspace,
                    source_dataset=dataset,
                    target_workspace=workspace,
                    target_dataset=new_name,
                    new_settings=new_settings,
                )
            else:
                ws = self._get_workspace(workspace, create=False)
                dataset_obj = self.client.datasets(name=dataset, workspace=ws)
                # Update settings that can be modified after creation
                for key, value in new_settings.items():
                    if hasattr(dataset_obj, key):
                        setattr(dataset_obj, key, value)
                return dataset_obj

        except Exception as e:
            if not isinstance(e, DatasetError):
                e = DatasetError(f"Settings update failed: {str(e)}")
            logger.error(str(e))
            raise e

    def clone_dataset(
        self, workspace: str, dataset: str, new_name: str, new_workspace: Optional[str] = None
    ) -> rg.Dataset:
        """
        Create an exact copy of a dataset.

        Args:
            workspace: Source workspace name
            dataset: Source dataset name
            new_name: Name for the cloned dataset
            new_workspace: Optional new workspace for the clone

        Returns:
            rg.Dataset: The cloned dataset

        Raises:
            DatasetError: If cloning fails
        """
        try:
            ws = self._get_workspace(workspace, create=False)
            source = self.client.datasets(name=dataset, workspace=ws)
            settings = source.settings

            return self.migrate_dataset(
                source_workspace=workspace,
                source_dataset=dataset,
                target_workspace=new_workspace or workspace,
                target_dataset=new_name,
                new_settings=settings,
            )

        except Exception as e:
            if not isinstance(e, DatasetError):
                e = DatasetError(f"Dataset cloning failed: {str(e)}")
            logger.error(str(e))
            raise e

    def delete_dataset(self, workspace: str, dataset: str) -> None:
        """
        Safely delete a dataset.

        Args:
            workspace: Workspace name
            dataset: Dataset name

        Raises:
            DatasetError: If deletion fails
        """
        try:
            ws = self._get_workspace(workspace, create=False)
            dataset_obj = self.client.datasets(name=dataset, workspace=ws)
            logger.warning(f"Deleting dataset {dataset} from workspace {workspace}")
            dataset_obj.delete()
            logger.info("Dataset deleted successfully")

        except Exception as e:
            if not isinstance(e, DatasetError):
                e = DatasetError(f"Dataset deletion failed: {str(e)}")
            logger.error(str(e))
            raise e
