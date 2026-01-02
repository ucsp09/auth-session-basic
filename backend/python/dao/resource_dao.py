from typing import Any, Tuple, List, Dict, Optional
from core.adapters.db.base_db import BaseDB
from core.logger import Logger

logger = Logger.get_logger(__name__)

class ResourceDao:
    def __init__(self, db: BaseDB):
        self.db = db
        self.collection = "resources"

    async def create_resource(self, resource_data: dict) -> Tuple[Optional[Dict], Any]:
        """Create a resource in the database"""
        try:
            logger.info(f"Creating resource with data: {resource_data}")
            resource = await self.db.create_record(self.collection, resource_data)
            logger.info(f"Resource created successfully with ID: {resource.get('id')}")
            return resource, None
        except Exception as e:
            logger.error(f"Error creating resource: {e}")
            return None, e
        
    async def get_resource(self, resource_id: str) -> Tuple[Optional[Dict], Any]:
        """Retrieve a resource by ID from the database."""
        try:
            logger.info(f"Retrieving resource with ID: {resource_id}")
            resource = await self.db.get_record_by_id(self.collection, resource_id)
            if resource:
                logger.info(f"resource retrieved successfully with ID: {resource_id}")
                return resource, None
            else:
                logger.warning(f"resource not found with ID: {resource_id}")
                return None, None
        except Exception as e:
            logger.error(f"Error retrieving resource with ID: {resource_id}. Error: {e}")
            return None, e

    async def update_resource(self, resource_id: str, update_data: dict) -> Tuple[Optional[Dict], Any]:
        """Update a resource in the database."""
        try:
            logger.info(f"Updating resource with ID: {resource_id} with data: {update_data}")
            updated_resource = await self.db.update_record(self.collection, resource_id, update_data)
            if updated_resource:
                logger.info(f"resource updated successfully with ID: {resource_id}")
                return updated_resource, None
            else:
                logger.warning(f"resource not found with ID: {resource_id}")
                return None, "resource not found"
        except Exception as e:
            logger.error(f"Error updating resource with ID: {resource_id}. Error: {e}")
            return None, e

    async def delete_resource(self, resource_id: str) -> Tuple[bool, Any]:
        """Delete a resource from the database."""
        try:
            logger.info(f"Deleting resource with ID: {resource_id}")
            success = await self.db.delete_record(self.collection, resource_id)
            if success:
                logger.info(f"resource deleted successfully with ID: {resource_id}")
                return True, None
            else:
                logger.warning(f"resource not found with ID: {resource_id}")
                return False, "resource not found"
        except Exception as e:
            logger.error(f"Error deleting resource with ID: {resource_id}. Error: {e}")
            return False, e

    async def get_all_resources(self) -> Tuple[List[Dict], Any]:
        """Retrieve all resources from the database."""
        try:
            logger.info("Retrieving all resources")
            resources = await self.db.get_all_records(self.collection)
            logger.info(f"Successfully retrieved {len(resources)} resources")
            return resources, None
        except Exception as e:
            logger.error(f"Error retrieving all resources. Error: {e}")
            return [], e
        
    async def get_resource_by_name(self, name: str) -> Tuple[Optional[Dict], Any]:
        """Retrieve a resource by name from the database."""
        try:
            logger.info(f"Retrieving resource with name: {name}")
            resources = await self.db.get_all_records(self.collection)
            for resource in resources:
                if resource.get("name") == name:
                    logger.info(f"resource retrieved successfully with name: {name}")
                    return resource, None
            logger.warning(f"resource not found with name: {name}")
            return None, None
        except Exception as e:
            logger.error(f"Error retrieving resource with name: {name}. Error: {e}")
            return None, e
