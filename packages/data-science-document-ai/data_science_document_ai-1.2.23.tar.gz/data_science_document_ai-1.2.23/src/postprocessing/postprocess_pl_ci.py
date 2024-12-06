"""This module contains the post-processing work for the packingList and commercialInvoice document."""
from src.llm import LlmClient
from src.tms_formatting import get_formatted_value
from src.utils import get_data_set_schema, get_processor_name


async def get_sku_doc_ai_schema(params, schema_client, input_doc_type):
    """Get the SKU schema of the document from the Document AI processor.

    Args:
        params (dict): The project parameters.
        schema_client (object): The schema client object.
        input_doc_type (str): The document type.

    Returns:
        entity (object): The entity type of the document.
        str: The name of the entity
    """
    processor_name = await get_processor_name(params, input_doc_type)
    # Get the schema of a processor and select only the entity types
    schema = await get_data_set_schema(schema_client, name=processor_name)

    # Find the entity type with the name "skuData" or "skus" and return it
    for entity in schema.document_schema.entity_types:
        if entity.name == "skuData" or entity.name == "skus":
            return entity, entity.name

    return None, None


async def process_file_w_llm(params, schema_sku, file_content):
    """Process a document using a large language model to extract structured data.

    Args:
        params (dict): The project parameters.
        schema_sku (object): The schema of the SKU data.
        file_content (str): The content of the file to be processed.

    Returns:
        result (dict): The structured data extracted from the document, formatted as JSON.
    """
    # Initialize the LLM model with the PL params
    parameters = params["gemini_params"] if "gemini_params" in params else None
    llm_model = LlmClient(parameters=parameters)

    # convert file_content to required document
    document = llm_model.prepare_document_for_gemini(file_content)

    # Create a prompt for the task along with the schema
    prompt = await prompt_sku_extraction(schema_sku)

    # Extract data using the LLM
    response = llm_model.get_unified_json_genai(prompt, document=document)

    return response, parameters["model_id"]


# flake8: noqa
# pylint: disable=all
async def prompt_sku_extraction(schema):
    """Write a prompt to extract data from PL and CI documents.

    Args:
        schema (str): The schema of the data to extract

    Returns:
        prompt str: The prompt for common json.
    """
    pl = """
    - If containerNumber, sealNumber, poNumber, or poPosition are not found within an skuData entity, look for these fields elsewhere in the document. Once found, insert these fields to all relevant skuData entities by populating their respective fields.
    - Do not create additional skuData entries separately for these shared attributes; instead, insert them to existing skuData entries by populating their respective fields.
    - Do not extract or associate the total Gross Weight, total Net Weight, or quantityShipped.
    """
    ci = """
    - If the containerNumber, hsCode, or poNumber are not found in the sku data, search in other location of the document and map it to all the sku entities. But do not map the total Gross Weight, Net Weight, or Quantity to all the sku entities."""  # noqa

    footnote = """
                [{"skuData"},
                {"skuData"},
                {"..."}]
                """

    prompt = f"""
    Task: Fill in the following dictionary from the information in the given pdf document.

    Each data point is part of a master field called skuData. There may be multiple skuData entries in a document.
    Your goal is to extract all instances.

    Instructions:
    - Do not change the keys of the following dictionary.
    - The values should be filled in as per the schema provided below.
    - The entity can be extracted multiple times. Please pay attention to the occurrence_type.
    - Use the data field description to understand the context of the data.
    {pl if schema.name == 'skuData' else ci}

    The schema is as follows:
    {schema}

    The output format should be as follows:
    {footnote}
    return only the extracted data in the above format excluding all other information.
    And return the output in a valid json format.

    """.replace(
        "skuData", schema.name
    )  # Replace "skuData" with the "skus" for the CI document

    return prompt


# pylint: enable=all


async def post_processing_pl_and_ci(
    params,
    aggregated_data,
    schema_client,
    input_doc_type,
    file_content,
    embed_manager,
    processor_version,
):
    """Extract the SKU data using the LLMs from the PL and CI documents.

    Args:
        params (dict): Constants stored in a dictionary
        aggregated_data (dict): The aggregated data from the document
        schema_client (object): The schema client object
        input_doc_type (str): The document type
        file_content (str): The content of the file to be processed
        embed_manager (object): An object to manage embeddings for formatted values

    Returns:
        dict: The aggregated data with the SKU data extracted
        str: The processor
    """
    # Get the schema from the Doc AI processor and the sku_name (i.e., "skuData" from PL & "skus" from CI)
    schema_sku, sku_name = await get_sku_doc_ai_schema(
        params, schema_client, input_doc_type
    )

    # Remove the "skuData" or "skus" key from the aggregated data if it exists
    if sku_name in aggregated_data and aggregated_data[sku_name]:
        del aggregated_data[sku_name]

    # Extract the sku data using the LLMs
    result, model_id = await extract_sku_data(
        params, schema_sku, sku_name, file_content, embed_manager
    )

    # Add the SKU result to the Doc AI aggregated data
    aggregated_data[sku_name] = result

    # Join the LLM model id to the Doc Ai processor version
    processor_version = processor_version + "/" + model_id

    return aggregated_data, processor_version


async def extract_sku_data(params, sku_schema, sku_name, file_content, embed_manager):
    """
    Process file content using an LLM and formats SKU data.

    Args:
        params (dict): The project parameters.
        sku_schema (object): The schema of the SKU data.
        file_content (str): The content of the file to be processed.
        embed_manager (object): An object to manage embeddings for formatted values.
        sku_name (st): Name of the sku field as per the schema (i.e., "skuData" for PL and "skus" for CI).

    Returns:
        dict: A dictionary containing the aggregated SKU data.
    """
    # Process the file content with the LLM
    llm_response, model_id = await process_file_w_llm(params, sku_schema, file_content)

    # Initialize a list to store SKU data
    sku_data_list = []

    # Apply the TMS formatting
    for sku in llm_response:
        # Determine if it's nested under 'skuData' or direct
        if sku_name in sku:  # sku_key is "skuData" or "skus" depends on the doc type
            sku_values = sku[sku_name]  # Extract the inner dictionary
        else:
            sku_values = sku  # Treat as a flat dictionary

        sku_dict = {}  # Create a formatted SKU dictionary
        # Get TMS formatted value for the applicable fields
        for key, value in sku_values.items():
            if value is None:
                sku_dict.update({key: {"documentValue": value, "formattedValue": None}})
            else:
                # Get the TMS formatted value
                formatted_value = get_formatted_value(key, value, embed_manager)
                sku_dict.update(
                    {key: {"documentValue": value, "formattedValue": formatted_value}}
                )
        # Append each SKU to the list
        sku_data_list.append(sku_dict)

    return sku_data_list, model_id
