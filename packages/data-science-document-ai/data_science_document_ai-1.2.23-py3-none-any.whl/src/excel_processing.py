"""This module contains the functions to extract data from an Excel file."""
import re
from collections import defaultdict

import numpy as np
import pandas as pd

from src.io import logger
from src.llm import prompt_excel_extraction
from src.tms_formatting import format_tms_excel_data
from src.utils import (
    get_data_set_schema,
    get_excel_sheets,
    get_processor_name,
    validate_based_on_schema,
)


async def extract_data_from_excel(
    params,
    input_doc_type,
    file_content,
    schema_client,
    embed_manager,
    isBetaTest,
    mime_type,
):
    """Extract data from the Excel file.

    Args:
        params (dict): Parameters for the data extraction process.
        input_doc_type (str): The type of the document.
        file_content (bytes): The content of the Excel file to process.
        schema_client (DocumentSchemaClient): Client for the Document AI schema.
        embed_manager (EmbeddingsManager): Manager for embeddings.
        isBetaTest (bool): A flag indicating if the request is for beta testing.
        mime_type (str): The MIME type of the file.

    Returns:
        formatted_data (list): A list of dictionaries containing the extracted data.
        result (list): The extracted data from the document.
        model_id (str): The ID of the model used for extraction.

    """
    # Get the processor name
    processor_name = await get_processor_name(params, input_doc_type, isBetaTest)

    # Get the schema of a processor and select only the entity types
    schema = await get_data_set_schema(schema_client, name=processor_name)
    # Remove "custom_extraction_document_type" from the schema. bcz the model sometimes thinks it's a document name :(
    schema = re.sub(
        r'name: "custom_extraction_document_type"',
        "",
        str(schema.document_schema.entity_types),
    )

    # Load the Excel file and get ONLY the "visible" sheet names
    sheets, workbook = get_excel_sheets(file_content, mime_type)

    # Store the extracted data from multiple worksheets
    extracted_data = defaultdict(dict)
    stored_data = defaultdict(dict)

    # Excel files may contain multiple sheets. Extract data from each sheet
    for sheet in sheets:
        logger.info(f"Processing sheet: {sheet}")
        excel_content = pd.DataFrame(workbook[sheet].values)
        # Convert to Markdown format for the LLM model
        worksheet = (
            "This is from a excel. Pay attention to the cell position:\n"
            + excel_content.replace(np.nan, "").to_markdown(index=False, headers=[])
        )

        # Prompt for the LLM JSON
        prompt_docai = prompt_excel_extraction(worksheet, schema)

        # Extract the data from the Excel file
        # parameters = params["gemini_params"] if "gemini_params" in params else None
        try:
            result = params["LlmClient"].get_unified_json_genai(prompt_docai)
        except Exception as e:
            logger.error(f"Error extracting data from LLM: {e}")
            continue
        # Postprocess the extracted data with the embedded model
        formatted_data = format_tms_excel_data(result, embed_manager)

        # Return the extracted data as per the required format
        formatted_data = await validate_based_on_schema(
            formatted_data, processor_name, schema_client
        )

        # Append the extracted data to the dictionary. Couldn't use defaultdict(list) due to the logs storage d_type
        extracted_data[sheet] = formatted_data
        stored_data[sheet] = result

    return dict(extracted_data), dict(stored_data), params["gemini_params"]["model_id"]
