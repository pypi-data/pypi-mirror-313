"""Building engine to understand and process PDF files."""
import asyncio
import re
from collections import defaultdict

from fastapi import HTTPException
from google.cloud import documentai
from google.cloud.documentai_v1 import Document as docaiv1_document

from src.excel_processing import extract_data_from_excel
from src.io import delete_folder_from_bucket, logger, upload_pdf_to_bucket
from src.postprocessing.postprocess_final_mbl import *
from src.postprocessing.postprocess_customs_assessment import *
from src.postprocessing.postprocess_booking_confirmation import (
    postprocess_booking_confirmation,
)
from src.postprocessing.postprocess_final_mbl import (
    combine_final_mbl_results,
    extract_final_mbl_from_pdf_w_llm,
)
from src.postprocessing.postprocess_pl_ci import post_processing_pl_and_ci
from src.postprocessing.postprocessing_llm import postprocess_llm
from src.prompts.prompt_library import prompt_library
from src.tms_formatting import format_TMS
from src.utils import get_processor_name, run_background_tasks, validate_based_on_schema


async def _process_pdf_w_docai(image_content, client, processor_name):
    """Process the PDF using Document AI.

    Args:
        image_content (bytes): The content of the PDF file as bytes.
        client: The Document AI client.
        processor_name (str): The name of the processor to be used.
                            e.g.: projects/{project_id}/locations/{location}/processor/{processor_id}

    Returns:
        The processed document.
    """
    # Load binary data
    raw_document = documentai.RawDocument(
        content=image_content, mime_type="application/pdf"
    )

    # Configure the process request
    request = documentai.ProcessRequest(
        name=processor_name,
        raw_document=raw_document,  # field_mask=field_mask
    )
    result = await client.process_document(request=request)

    return result.document


async def process_file_w_docai(params, image_content, client, processor_name):
    """
    Process a file using Document AI.

    Args:
        params (dict): The project parameters.
        image_content (bytes): The file to be processed. It can be bytes object.
        client: The Document AI client.
        processor_name (str): The name of the processor to be used.

    Returns:
        The processed document.

    Raises:
        ValueError: If the file is neither a path nor a bytes object.
    """
    result = None

    try:
        logger.info("Processing document...")
        result = await _process_pdf_w_docai(image_content, client, processor_name)
    except Exception as e:
        if e.reason == "PAGE_LIMIT_EXCEEDED":
            logger.warning(
                "Document contains more than 15 pages! Processing in batch method..."
            )
            # Process the document in batch method (offline processing)
            try:
                result = await _batch_process_pdf_w_docai(
                    params, image_content, client, processor_name
                )
            except Exception as batch_e:
                logger.error(f"Error processing document {batch_e}.")

        else:
            logger.error(f"Error processing document {e}.")

    return result


async def _batch_process_pdf_w_docai(
    params, image_content, client, processor_name, timeout=1200
):
    """Process the PDF using Document AI Batch Process API.

    Args:
        image_content (bytes): The content of the PDF file as bytes.
        client: The Document AI client.
        processor_name (str): The name of the processor to be used.
                            e.g.: projects/{project_id}/locations/{location}/processor/{processor_id}
        timeout (int, optional): The timeout in seconds. Defaults to 1200.

    Returns:
        The processed document.
    """
    # Upload the PDF to GCS bucket
    gcs_input_uri, storage_client = upload_pdf_to_bucket(
        params, image_content, "temp.pdf"
    )

    gcs_document = documentai.GcsDocument(
        gcs_uri=gcs_input_uri, mime_type="application/pdf"
    )
    # Load GCS Input URI into a List of document files
    input_config = documentai.BatchDocumentsInputConfig(
        gcs_documents=documentai.GcsDocuments(documents=[gcs_document])
    )

    # Cloud Storage URI for the Output Directory
    # This must end with a trailing forward slash `/`
    destination_uri = f"gs://{params['doc_ai_bucket_batch_output']}/"  # noqa
    gcs_output_config = documentai.DocumentOutputConfig.GcsOutputConfig(
        gcs_uri=destination_uri, field_mask="entities"
    )

    # Where to write results
    output_config = documentai.DocumentOutputConfig(gcs_output_config=gcs_output_config)

    # The full resource name of the processor
    request = documentai.BatchProcessRequest(
        name=processor_name,
        input_documents=input_config,
        document_output_config=output_config,
    )

    # BatchProcess returns a Long Running Operation (LRO)
    logger.info("Processing document in batch mode...")
    operation = await client.batch_process_documents(request)

    try:
        # Wait for the operation to finish
        logger.info(f"Waiting for operation {operation.operation.name} to complete...")
        await operation.result(timeout=timeout)
    # Catch exception when operation doesn't finish before timeout
    except Exception as e:
        logger.error(e)

    # Once the operation is complete,
    # get output document information from operation metadata
    metadata = documentai.BatchProcessMetadata(operation.metadata)

    if metadata.state != documentai.BatchProcessMetadata.State.SUCCEEDED:
        raise ValueError(f"Batch Process Failed: {metadata.state}")

    # One process per Input Document
    for process in metadata.individual_process_statuses:
        # The Cloud Storage API requires the bucket name and URI prefix separately
        matches = re.match(r"gs://(.*?)/(.*)", process.output_gcs_destination)
        if not matches:
            logger.warning(
                "Could not parse output GCS destination:",
                process.output_gcs_destination,
            )
            continue

        output_bucket, output_prefix = matches.groups()

        # Get List of Document Objects from the Output Bucket
        output_blobs = storage_client.list_blobs(output_bucket, prefix=output_prefix)

        # Document AI may output multiple JSON files per source file
        # Selecting only the first output file as of now. No particular reason
        for blob in output_blobs:
            # Document AI should only output JSON files to GCS
            if ".json" not in blob.name:
                logger.warning(
                    f"Skipping non-supported file: {blob.name} - Mimetype: {blob.content_type}"
                )
                continue

            # Download JSON File as bytes object and convert to Document Object
            result_document = documentai.Document.from_json(
                blob.download_as_bytes(), ignore_unknown_fields=True
            )

            # Delete the temporary file and the output file from the bucket
            delete_folder_from_bucket(params["doc_ai_bucket_batch_input"], "temp.pdf")
            delete_folder_from_bucket(output_bucket, output_prefix)
            logger.info("Batch Process Completed!")

            return result_document


async def extract_data_from_pdf(
    params,
    input_doc_type,
    file_content,
    processor_client,
    schema_client,
    embed_manager,
    isBetaTest,
):
    """Extract data from the PDF file."""
    processor_name = await get_processor_name(params, input_doc_type, isBetaTest)

    confidence = {}
    if (
        input_doc_type in params["models"]
        and "confidence" in params["models"][input_doc_type]
    ):
        confidence = params["models"][input_doc_type]["confidence"]

    if not processor_name:
        supported_doc_types = list(params["data_extractor_processor_names"].keys())
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported document type {input_doc_type}. Supported document types are: {supported_doc_types}",  # noqa: E501
        )

    result = await process_file_w_docai(
        params, file_content, processor_client, processor_name
    )

    # Create an entity object to store the result in gcs
    result_for_store = docaiv1_document.to_json(result)

    aggregated_data = defaultdict(list)

    for entity in result.entities:
        child_entities = entity.properties
        if child_entities:
            child_data = defaultdict(dict)
            for child in child_entities:
                if child.confidence >= confidence.get(child.type_, 0):
                    value = format_TMS(child, embed_manager)
                    child_data[child.type_] = value

            aggregated_data[entity.type_].append(dict(child_data))

        elif entity.confidence >= confidence.get(entity.type_, 0):
            # Get the formatted value for the entity in a dictionary format {documentValue: "", formattedValue: ""}
            value = format_TMS(entity, embed_manager)
            # Append the value to the aggregated data
            aggregated_data[entity.type_].append(value)

    aggregated_data = await validate_based_on_schema(
        aggregated_data, processor_name, schema_client
    )

    # Call postprocessing for Multi Leg
    if (
        input_doc_type == "bookingConfirmation"
        or input_doc_type == "bookingConfirmation_test"
    ):
        aggregated_data = postprocess_booking_confirmation(aggregated_data)
        logger.info("Transport Legs assembled successfully")

    response = await processor_client.get_processor(name=processor_name)
    processor_version = response.default_processor_version.split("/")[-1]

    # call postprocessing for packing list and commercial Invoice doc
    if input_doc_type in ("packingList", "commercialInvoice"):
        logger.info("Starting post processing for PL and CI...")
        aggregated_data, processor_version = await post_processing_pl_and_ci(
            params,
            aggregated_data,
            schema_client,
            input_doc_type,
            file_content,
            embed_manager,
            processor_version,
        )

    logger.info("Data Extraction completed successfully")
    logger.info(
        f"Processor & it's version used for current request: {response.display_name} - {processor_version}"
    )

    return aggregated_data, result_for_store, processor_version


async def identify_carrier(document, llm_client):
    """Identify the carrier from the Booking Confirmation document."""
    prompt = """
            You are a person who works for a freight-forwarder company.
            Identify company that provided this Booking Confirmation document.
            Only answers are: Hapag-Lloyd, MsC, Maersk, YangMing or Other.

            return as JSON: {"carrier": answer}
        """
    result = llm_client.get_unified_json_genai(prompt=prompt, document=document)
    if "carrier" in result and result["carrier"]:
        result = result["carrier"].lower()
    else:
        result = "other"
    return result


async def process_file_w_llm(file_content, input_doc_type, llm_client):
    """Process a document using a language model (gemini) to extract structured data.

    Args:
        document (Union[Part, str]): The document object prepared for processing.
        input_doc_type (str): The type of document, used to select the appropriate prompt from the prompt library.

    Returns:
        result (dict): The structured data extracted from the document, formatted as JSON.
    """
    # TODO: change to a more dynamic struture for multiple LLM types, for now its only compatible with gemini
    # convert file_content to required document
    document = llm_client.prepare_document_for_gemini(file_content)

    # identify carrier for customized prompting
    carrier = await identify_carrier(document, llm_client)

    # get the related prompt from predefined prompt library
    if (
        input_doc_type in prompt_library.library.keys()
        and carrier.lower() in prompt_library.library[input_doc_type].keys()
    ):
        prompt = prompt_library.create_prompt(
            prompt_library.library[input_doc_type][carrier.lower()]["prompt"],
            prompt_library.library[input_doc_type][carrier.lower()]["placeholders"],
        )

        # generate the result with LLM (gemini)
        result = llm_client.get_unified_json_genai(prompt=prompt, document=document)
        return result
    return {}


async def extract_data_from_pdf_w_llm(
    input_doc_type, file_content, embed_manager, llm_client
):
    """Extract data from the PDF file."""
    result = await process_file_w_llm(file_content, input_doc_type, llm_client)

    aggregated_data = postprocess_llm(result, embed_manager, llm_client)

    # Call postprocessing for Multi Leg
    if (
        input_doc_type == "bookingConfirmation"
        or input_doc_type == "bookingConfirmation_test"
    ):
        aggregated_data = postprocess_booking_confirmation(aggregated_data)
        logger.info("Transport Legs assembled successfully")

    return aggregated_data, aggregated_data, "gemini-pro"


def combine_results(doc_ai, llm):
    """
    Combine results from DocAI and LLM extractions.

    Args:
        doc_ai: result from DocAI
        llm: result from LLM

    Returns:
        combined result
    """
    result = doc_ai.copy()
    for key in llm.keys():
        if key not in result:
            result[key] = llm[key]
    if "transportLegs" in llm.keys():
        if len(llm["transportLegs"]) < len(result["transportLegs"]):
            result["transportLegs"] = llm["transportLegs"]
        else:
            for i in range(len(llm["transportLegs"])):
                if i == len(result["transportLegs"]):
                    result["transportLegs"].append(llm["transportLegs"][i])
                else:
                    for key in llm["transportLegs"][i].keys():
                        result["transportLegs"][i][key] = llm["transportLegs"][i][key]
    return result


async def data_extraction_manual_flow(
    params,
    file_content,
    mime_type,
    meta,
    processor_client,
    schema_client,
    embed_manager,
):
    """
    Process a PDF file and extract data from it.

    Args:
        params (dict): Parameters for the data extraction process.
        file_content (bytes): The content of the PDF file to process.
        mime_type (str): The MIME type of the document.
        meta (DocumentMeta): Metadata associated with the document.
        processor_client (DocumentProcessorClient): Client for the Document AI processor.
        schema_client (DocumentSchemaClient): Client for the Document AI schema.
        embed_manager (EmbeddingsManager): Manager for embeddings.

    Returns:
        dict: A dictionary containing the processed document information.

    Raises:
        Refer to reasons in 400 error response examples.
    """
    # Validate the file type
    if mime_type == "application/pdf":
        # Extract data from the PDF file
        if meta.documentTypeCode == "bookingConfirmation":
            (
                extracted_data_doc_ai,
                store_data,
                processor_version_doc_ai,
            ) = await extract_data_from_pdf(
                params,
                input_doc_type=meta.documentTypeCode,
                file_content=file_content,
                processor_client=processor_client,
                schema_client=schema_client,
                embed_manager=embed_manager,
                isBetaTest=meta.isBetaTest,
            )
            # Extract data from PDF using LLM
            (
                extracted_data_llm,
                store_data_llm,
                processor_version_llm,
            ) = await extract_data_from_pdf_w_llm(
                input_doc_type=meta.documentTypeCode,
                file_content=file_content,
                embed_manager=embed_manager,
                llm_client=params["LlmClient"],
            )
            extracted_data = combine_results(extracted_data_doc_ai, extracted_data_llm)
            processor_version = processor_version_doc_ai + "/" + processor_version_llm
        elif meta.documentTypeCode == "finalMbL":
            (
                extracted_data_doc_ai,
                store_data,
                processor_version_doc_ai,
            ) = await extract_data_from_pdf(
                params,
                input_doc_type=meta.documentTypeCode,
                file_content=file_content,
                processor_client=processor_client,
                schema_client=schema_client,
                embed_manager=embed_manager,
                isBetaTest=meta.isBetaTest,
            )
            # Extract data from PDF using LLM
            (
                extracted_data_llm,
                store_data_llm,
                processor_version_llm,
            ) = await extract_final_mbl_from_pdf_w_llm(
                input_doc_type=meta.documentTypeCode,
                file_content=file_content,
                embed_manager=embed_manager,
                llm_client=params["LlmClient"],
            )
            extracted_data = combine_final_mbl_results(
                extracted_data_doc_ai, extracted_data_llm
            )
            processor_version = processor_version_doc_ai + "/" + processor_version_llm
        elif meta.documentTypeCode == "customsAssessment":
            extracted_data_doc_ai, store_data, processor_version_doc_ai = await extract_data_from_pdf(
                params,
                input_doc_type=meta.documentTypeCode,
                file_content=file_content,
                processor_client=processor_client,
                schema_client=schema_client,
                embed_manager=embed_manager,
                isBetaTest=meta.isBetaTest,
            )
            # Extract data from PDF using LLM
            extracted_data_llm, store_data_llm, processor_version_llm = await extract_customs_assessment_from_pdf_w_llm(
                input_doc_type=meta.documentTypeCode,
                file_content=file_content,
                embed_manager=embed_manager,
                llm_client=params["LlmClient"]
            )
            extracted_data = combine_customs_assessment_results(extracted_data_doc_ai, extracted_data_llm)
            processor_version = processor_version_doc_ai + "/" + processor_version_llm
        else:
            extracted_data, store_data, processor_version = await extract_data_from_pdf(
                params,
                input_doc_type=meta.documentTypeCode,
                file_content=file_content,
                processor_client=processor_client,
                schema_client=schema_client,
                embed_manager=embed_manager,
                isBetaTest=meta.isBetaTest,
            )

    elif "excel" in mime_type or "spreadsheet" in mime_type:
        # Extract data from the Excel file
        extracted_data, store_data, processor_version = await extract_data_from_excel(
            params=params,
            input_doc_type=meta.documentTypeCode,
            file_content=file_content,
            schema_client=schema_client,
            embed_manager=embed_manager,
            isBetaTest=meta.isBetaTest,
            mime_type=mime_type,
        )

    else:
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Please upload a PDF or Excel file.",
        )
    # Create the result dictionary with the extracted data
    result = {
        "id": meta.id,
        "documentTypeCode": meta.documentTypeCode,
        "data": extracted_data,
        "processor_version": processor_version,
    }

    # Schedule background tasks without using FastAPI's BackgroundTasks
    asyncio.create_task(
        run_background_tasks(
            params,
            meta.id,
            meta.documentTypeCode,
            extracted_data,
            store_data,
            processor_version,
            mime_type,
        )
    )

    return result
