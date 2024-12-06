"""Utility functions for data science projects."""
import asyncio
import io
import json
from datetime import datetime

import openpyxl
import pandas as pd
from google.cloud import documentai_v1beta3 as docu_ai_beta

from src.io import get_bq_client, get_storage_client, logger
from src.setup import get_docai_processor_client


def bq_logs(data_to_insert, params):
    """Insert logs into Google BigQuery.

    Args:
        data_to_insert (list): The data to insert into BigQuery.
        params (dict): The parameters dictionary.
    """
    # Get the BigQuery client
    bq_client, config = get_bq_client(params)
    # Get the table string
    table_string = f"{params['g_ai_project_name']}.{params['g_ai_gbq_db_schema']}.{params['g_ai_gbq_db_table_out']}"

    logger.info(f"Log table: {table_string}")
    # Insert the rows into the table
    insert_logs = bq_client.insert_rows_json(table_string, data_to_insert)

    # Check if there were any errors inserting the rows
    if not insert_logs:
        logger.info("New rows have been added.")
    else:
        logger.info("Errors occurred while inserting rows: ", insert_logs)


def get_data_set_schema(
    schema_client, project_id=None, location=None, processor_id=None, name=None
):
    """Get the existing processor schema.

    Args:
        schema_client (documentai_v1beta3.DocumentServiceClient): The schema client.
        project_id (str): The ID of the project.
        location (str): The location of the project.
        processor_id (str): The id of the processor.
        name (str, optional): The name of the dataset schema. Defaults to None.
        The format is "projects/{project_id}/locations/{location}/processors/{processor_id}/dataset/datasetSchema".

    Returns:
        documentai.DatasetSchema: The schema of the dataset.
    """
    # Check if the name is provided as per the format
    if name and not name.endswith("datasetSchema"):
        name = f"{name}/dataset/datasetSchema"

    # Initialize request argument(s)
    if name:
        request = docu_ai_beta.GetDatasetSchemaRequest(
            name=name, visible_fields_only=True
        )
    else:
        request = docu_ai_beta.GetDatasetSchemaRequest(
            name=schema_client.dataset_schema_path(project_id, location, processor_id),
            visible_fields_only=True,
        )

    # Make the request
    response = schema_client.get_dataset_schema(request=request)

    return response


async def get_processor_name(params, input_doc_type, isBetaTest=False):
    """Access models based on the environment and isBetaTest."""
    env = params["environment"]
    g_ai_project_id = params['g_ai_project_id']
    if input_doc_type == "customsAssessment" and env == "sandbox":
        env = "production"
        g_ai_project_id = "738250249861"

    if isBetaTest:
        stages = params["model_config"].get("beta", [])
        model_type = stages[input_doc_type]
        env_models = model_type.get(env, [])
        processor_id = (
            env_models[params["model_selector"]["beta"][input_doc_type]].get("id")
            if env_models
            else None
        )
    else:
        stages = params["model_config"].get("stable", [])
        model_type = stages[input_doc_type]
        env_models = model_type.get(env, [])
        processor_id = (
            env_models[params["model_selector"]["stable"][input_doc_type]].get("id")
            if env_models
            else None
        )

    # Construct the processor path
    # if processor_id not in [
    #     path.split("/")[-1]
    #     for path in params["data_extractor_processor_names"].values()
    # ]:
    #     error_message = "Processor not found."
    #     logger.error(error_message)
    #     raise ValueError(error_message)
    # else:

    processor_name = f"projects/{g_ai_project_id}/locations/eu/processors/{processor_id}"
    logger.info(f"Processor: {processor_name}")

    logger.info(f"Processor ID for {input_doc_type}: {processor_id}")

    return processor_name


async def validate_based_on_schema(extracted_raw_data, processor_name, schema_client):
    """Validate the extracted data based on the schema."""
    # Get the schema of a processor and select only the entity types
    schema_response = await get_data_set_schema(schema_client, name=processor_name)
    # schema_response.document_schema.entity_types contains 2 elements:
    # One for entities at document level
    # One for entities at line item level
    schemas = schema_response.document_schema.entity_types
    schema_header_fields = schemas[0].properties

    result = dict(extracted_raw_data)
    for data_field in schema_header_fields:
        if "once" in data_field.occurrence_type.name.lower():
            if data_field.name in result:
                result[data_field.name] = result[data_field.name][0]
    return result


async def get_data_fields_of_deployed_version(
    params, pros_version_path, remove_child=True
):
    """Get the schema of a specific processor version.

    Args:
        params (dict): parameters dictionary
        pros_version_path (str): The processor version path.
        The Format is 'projects/{project_id}/locations/{location}/processors/{processor_id}/versions/{processor_version_id}'  # noqa: E501

    Returns:
        processor_fields (list): The data fields of a schema from a specific processor version.
    """
    # Get doc AI processor client
    client = get_docai_processor_client(params)

    # Get the schema of a specific processor version
    res = await client.get_processor_version(name=pros_version_path)

    if remove_child:
        # Remove the child fields from the schema
        pros_ver_schema = [
            entity
            for entity in res.document_schema.entity_types
            if entity.base_types == ["document"]
        ][0]

        return [
            prop.name
            for prop in pros_ver_schema.properties
            if prop.value_type != prop.name
        ]
    else:
        return res


async def get_data_fields_of_processor(schema_client, name, remove_child=True):
    """Get the schema of a processor.

    Args:
        schema_client (documentai_v1beta3.DocumentServiceClient): The schema client.
        name (str): The processor name. The format is
        either 'projects/{project_id}/locations/{location}/processors/{processor_id}' or
        'projects/{project_id}/locations/{location}/processors/{processor_id}/dataset/datasetSchema'

    Returns:
        processor_fields (list): The data fields of the latest schema of a processor.
    """
    _pros_schema = await get_data_set_schema(schema_client, name=name)

    # Remove the child fields from the schema
    if remove_child:

        processor_schema = [
            entity
            for entity in _pros_schema.document_schema.entity_types
            if entity.base_types == ["document"]
        ][0]

        return [
            prop.name
            for prop in processor_schema.properties
            if prop.value_type != prop.name
        ]
    else:
        return _pros_schema


async def find_new_data_fields(params, processor_name, processor_client, schema_client):
    """Check if the schema is updated.

    Args:
        params (dict): The parameters for the processor.
        processor_name: str, The name of the processor to be used.
        The format of processor_name is "projects/{project_id}/locations/{location}/processors/{processor_id}"

    Returns:
        tuple: The zero-shot processor version and the new data fields.
    """
    # Get the processor details
    response = await processor_client.get_processor(name=processor_name)

    # Get the processor deployed version details
    deployed_version = response.default_processor_version

    # Get the zero-shot model
    zero_shot_model = response.processor_version_aliases[0].processor_version

    # Skip if the deployed version is the same as the zero-shot version
    if deployed_version != zero_shot_model:

        # Get the schema of a specific processor version and the latest schema of a processor
        deployed_version_fields, processor_latest_fields = await asyncio.gather(
            get_data_fields_of_deployed_version(params, deployed_version),
            get_data_fields_of_processor(schema_client, name=response.name),
        )

        # Check if the schema of a processor is updated
        if deployed_version_fields != processor_latest_fields:
            # Identify the new fields in the updated schema
            new_data_fields = [
                field
                for field in processor_latest_fields
                if field not in deployed_version_fields
            ]

            return new_data_fields, zero_shot_model
        return None, None
    return None, None


def store_json_in_gcs(
    params, document_id, json_data, folder_path="docai_entity_storage/"
):
    """Store a JSON object in a Google Cloud Storage bucket.

    Args:
        bucket_name (str): The name of the GCS bucket.
        object_name (str): The desired name for the stored JSON object.
        json_data (dict): The JSON data to be stored.
        folder_path (str): The folder path in the GCS bucket. Default is "docai_entity_storage/".
    """
    try:
        storage_client = get_storage_client(params)
        bucket = storage_client.bucket(params.get("doc_ai_bucket_name"))
        full_object_name = folder_path + document_id
        blob = bucket.blob(full_object_name)
        blob.upload_from_string(json_data, content_type="application/json")

        print(
            f"JSON object stored successfully in gs://{params.get('doc_ai_bucket_name')}/{full_object_name}"  # noqa
        )

    except Exception as e:
        print(f"An error occurred: {e}")


# Execute synchronous functions in the background
async def run_background_tasks(
    params, doc_id, docType, extracted_data, store_data, processor_version, mime_type
):
    """
    Run background tasks asynchronously.

    Args:
        params (dict): The parameters dictionary.
        doc_id (str): The document ID.
        docType (str): The document type code.
        extracted_data (dict): The extracted data from the document.
        store_data: The data to store in GCS.
        processor_version: The processor version used to extract the data.
        mime_type: The MIME type of the document.

    Returns:
        None
    """
    loop = asyncio.get_running_loop()

    await loop.run_in_executor(None, store_json_in_gcs, params, doc_id, store_data)

    # Keep the page count as 1 for Excel files.
    page_count = 1
    # calculate the number of pages processed for PDFs
    try:
        if mime_type == "application/pdf":
            page_count = len(json.loads(store_data.encode("utf-8"))["pages"])
    except AttributeError:
        page_count = 0

    # Log the request in BigQuery
    await loop.run_in_executor(
        None,
        bq_logs,
        [
            {
                "session_id": params["session_id"],
                "upload_date": datetime.utcnow().isoformat(),
                "doc_id": doc_id,
                "documentTypeCode": docType,
                "status": "processed",
                "response": json.dumps(extracted_data),
                "processor_version": processor_version,
                "page_count": page_count,
                "mime_type": mime_type,
            }
        ],
        params,
    )


def get_excel_sheets(file_content, mime_type):
    """Get the sheet names from the Excel file.

    Args:
        file_content (bytes): The content of the Excel file.
        mime_type (str): The MIME type of the file.

    Returns:
        sheets (list): The list of sheet names.
        openpyxl.Workbook: The workbook
    """
    file_stream = io.BytesIO(file_content)
    if "spreadsheet" in mime_type:
        workbook = openpyxl.load_workbook(file_stream, data_only=True)
        sheets = [
            sheet_name
            for sheet_name in workbook.sheetnames
            if workbook[sheet_name].sheet_state == "visible"
        ]
    else:
        workbook = pd.read_excel(file_stream, sheet_name=None)
        # Select only the sheets that are not empty
        sheets = [sheet for sheet in workbook.keys() if not workbook[sheet].empty]

    return sheets, workbook
