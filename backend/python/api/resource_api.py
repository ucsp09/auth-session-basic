from fastapi import APIRouter, Response, status, Depends
from schema.resource_schema import CreateResourceRequestSchema, CreateResourceResponseSchema, GetResourceResponseSchema, GetAllResourcesResponseSchema, UpdateResourceRequestSchema
from schema.common_schema import ErrorResponseSchema, SuccessResponseSchema
from utils import uuid_utils
from dao.resource_dao import ResourceDao
from core.bootstrap import get_resource_dao
from core.logger import Logger


resource_api_router = APIRouter()
logger = Logger.get_logger(__name__)


@resource_api_router.post("/resources")
async def create_resource(input_data: CreateResourceRequestSchema, response: Response, resource_dao: ResourceDao = Depends(get_resource_dao)):
    logger.info(f"Received request to create a new resource with name: {input_data.name}")

    resource_data, err = await resource_dao.get_resource_by_name(name=input_data.name)
    if err:
        logger.error(f"Error occurred while checking existing resource with name: {input_data.name}. Error: {err}")
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return ErrorResponseSchema(error="Failed to create resource.")
    if resource_data:
        logger.warning(f"Resource with name: {input_data.name} already exists.")
        response.status_code = status.HTTP_409_CONFLICT
        return ErrorResponseSchema(error="Resource already exists.")
    
    logger.info(f"Creating resource with name: {input_data.name}")
    resource_data = input_data.dict()
    resource_data['id'] = uuid_utils.generate_uuid()

    _, err = await resource_dao.create_resource(resource_data=resource_data)
    if err:
        logger.error(f"Failed to create resource with name: {input_data.name}. Error: {err}")
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return ErrorResponseSchema(error="Failed to create resource.")

    logger.info(f"Resource created successfully with name: {input_data.name}")
    response.status_code = status.HTTP_201_CREATED
    return CreateResourceResponseSchema(resourceId=resource_data['id'], name=input_data.name, properties=input_data.properties)

@resource_api_router.get("/resources")
async def get_all_resources(response: Response, resource_dao: ResourceDao = Depends(get_resource_dao)):
    logger.info("Received request to fetch all resources")

    resources, err = await resource_dao.get_all_resources()
    if err:
        logger.error(f"Error while fetching all resources. Error: {err}")
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return ErrorResponseSchema(error="Failed to fetch all resources.")
    
    logger.info(f"Successfully retrieved {len(resources)} resources")
    response.status_code = status.HTTP_200_OK
    return GetAllResourcesResponseSchema(items=[GetResourceResponseSchema(resourceId=resource['id'], name=resource['name'], properties=resource['properties']) for resource in resources], total=len(resources))

@resource_api_router.get("/resources/{resource_id}")
async def get_resource(resource_id: str, response: Response, resource_dao: ResourceDao = Depends(get_resource_dao)):
    logger.info(f"Received request to get resource with resource_id: {resource_id}")

    if not resource_id:
        logger.warning("Resource ID is missing in the request.")
        response.status_code = status.HTTP_400_BAD_REQUEST
        return ErrorResponseSchema(error="Resource ID is required.")

    logger.info(f"Fetching resource data for resource_id: {resource_id}")
    resource_data, err = await resource_dao.get_resource(resource_id=resource_id)
    if err:
        logger.error(f"Error occurred while fetching resource data for resource_id: {resource_id}. Error: {err}")
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return ErrorResponseSchema(error="Failed to retrieve resource.")
    if not resource_data:
        logger.warning(f"Resource with resource_id: {resource_id} does not exist.")
        response.status_code = status.HTTP_404_NOT_FOUND
        return ErrorResponseSchema(error="Resource not found.")

    logger.info(f"Successfully retrieved resource data for resource_id: {resource_id}")
    response.status_code = status.HTTP_200_OK
    return GetResourceResponseSchema(resourceId=resource_data["id"], name=resource_data["name"], properties=resource_data["properties"])

@resource_api_router.put("/resources/{resource_id}")
async def update_resource(resource_id: str, input_data: UpdateResourceRequestSchema, response: Response, resource_dao: ResourceDao = Depends(get_resource_dao)):
    logger.info(f"Received request to update resource with resource_id: {resource_id}")

    if not resource_id:
        logger.warning("Resource ID is missing in the request.")
        response.status_code = status.HTTP_400_BAD_REQUEST
        return ErrorResponseSchema(error="Resource ID is required.")

    resource_data, err = await resource_dao.get_resource(resource_id)
    if err:
        logger.error(f"Error occurred while fetching resource data for resource_id: {resource_id}. Error: {err}")
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return ErrorResponseSchema(error="Failed to update resource.")
    if not resource_data:
        logger.warning(f"Resource with resource_id: {resource_id} does not exist.")
        response.status_code = status.HTTP_404_NOT_FOUND
        return ErrorResponseSchema(error="Resource not found.")

    update_data = input_data.dict(exclude_unset=True)

    logger.info(f"Updating resource with resource_id: {resource_id}")
    updated_resource_data, err = await resource_dao.update_resource(resource_id, update_data)
    if err:
        logger.error(f"Failed to update resource with resource_id: {resource_id}. Error: {err}")
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return ErrorResponseSchema(error="Failed to update resource.")

    logger.info(f"Resource updated successfully with resource_id: {resource_id}")
    response.status_code = status.HTTP_200_OK
    return GetResourceResponseSchema(resourceId=updated_resource_data["id"], name=updated_resource_data["name"], properties=updated_resource_data["properties"])


@resource_api_router.delete("/resources/{resource_id}")
async def delete_resource(resource_id: str, response: Response, resource_dao: ResourceDao = Depends(get_resource_dao)):
    logger.info(f"Received request to delete resource with resource_id: {resource_id}")

    if not resource_id:
        logger.warning("Resource ID is missing in the request.")
        response.status_code = status.HTTP_400_BAD_REQUEST
        return ErrorResponseSchema(error="Resource ID is required.")

    resource_data, err = await resource_dao.get_resource(resource_id)
    if err:
        logger.error(f"Error occurred while fetching resource data for resource_id: {resource_id}. Error: {err}")
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return ErrorResponseSchema(error="Failed to delete resource.")
    if not resource_data:
        logger.warning(f"Resource with resource_id: {resource_id} does not exist.")
        response.status_code = status.HTTP_404_NOT_FOUND
        return ErrorResponseSchema(error="Resource not found.")

    logger.info(f"Deleting resource with resource_id: {resource_id}")
    success, err = await resource_dao.delete_resource(resource_id)
    if err or not success:
        logger.error(f"Failed to delete resource with resource_id: {resource_id}. Error: {err}")
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return ErrorResponseSchema(error="Failed to delete resource.")

    logger.info(f"Resource deleted successfully with resource_id: {resource_id}")
    response.status_code = status.HTTP_200_OK
    return SuccessResponseSchema(message="Resource deleted successfully.")
