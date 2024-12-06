from src.postprocessing.postprocessing_llm import postprocess_llm
from src.prompts.prompt_library import prompt_library


finalMbL_features = [
    "blNumber",
    "bookingNumber",
    "containers",
    "portOfDischarge",
    "portOfLoading",
    "vessel",
    "voyage"
]

def filter_fealtures(final_mbl):
    final_mbl_filtered = {key: final_mbl[key] for key in finalMbL_features if key in final_mbl}
    return final_mbl_filtered


async def process_final_mbl_llm(file_content, input_doc_type, llm_client):
    """Process a document using a language model (gemini) to extract structured data.

    Args:
        document (Union[Part, str]): The document object prepared for processing.
        input_doc_type (str): The type of document, used to select the appropriate prompt from the prompt library.

    Returns:
        result (dict): The structured data extracted from the document, formatted as JSON.
    """
    # TODO: change to a more dynamic struture for multiple LLM types, for now its only compatible with gemini
    # convert file_content to required document
    document = llm_client.prepare_document_for_gemini(file_content)

    # identify carrier for customized prompting
    carrier = "other" # await identify_carrier(document, llm_client)

    # get the related prompt from predefined prompt library
    if input_doc_type in prompt_library.library.keys() \
            and carrier.lower() in prompt_library.library[input_doc_type].keys():
        prompt = prompt_library.create_prompt(prompt_library.library[input_doc_type][carrier.lower()]['prompt'],
                                              prompt_library.library[input_doc_type][carrier.lower()]['placeholders'])

        # generate the result with LLM (gemini)
        result = llm_client.get_unified_json_genai(prompt=prompt, document=document)
        return result
    return {}


async def extract_final_mbl_from_pdf_w_llm(
    input_doc_type,
    file_content,
    embed_manager,
    llm_client
):
    """Extract data from the PDF file."""
    result = await process_final_mbl_llm(file_content, input_doc_type, llm_client)

    aggregated_data = postprocess_llm(result, embed_manager, llm_client)

    return aggregated_data, aggregated_data, "gemini-pro"


def combine_final_mbl_results(doc_ai, llm):
    """
    Combine results from DocAI and LLM extractions.

    Args:
        doc_ai: result from DocAI
        llm: result from LLM

    Returns:
        combined result
    """
    result = filter_fealtures(doc_ai)
    for key in llm.keys():
        if key not in result:
            result[key] = llm[key]
    if "containers" in llm.keys():
        if len(llm["containers"]) < len(result["containers"]):
            result["containers"] = llm["containers"]
        else:
            for i in range(len(llm["containers"])):
                if i == len(result["containers"]):
                    result["containers"].append(llm["containers"][i])
                else:
                    for key in llm["containers"][i].keys():
                        result["containers"][i][key] = llm["containers"][i][key]
    return result
