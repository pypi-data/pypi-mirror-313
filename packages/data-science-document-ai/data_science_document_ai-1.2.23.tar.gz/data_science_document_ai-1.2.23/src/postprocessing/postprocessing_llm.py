from collections import defaultdict
from datetime import timezone
import json
import re

from src.io import logger
from src.prompts.prompt_library import prompt_library
from src.tms_formatting import clean_date_string, extract_date, format_TMS
from src.tms_formatting import extract_number


def remove_none_values(d):
    if isinstance(d, dict):
        # Create a new dictionary to store non-None values
        cleaned_dict = {}
        for key, value in d.items():
            cleaned_value = remove_none_values(value)
            if cleaned_value is not None:  # Only add non-None values
                cleaned_dict[key] = cleaned_value
        return cleaned_dict
    
    elif isinstance(d, list):
        # Create a new list to store non-None values
        cleaned_list = []
        for item in d:
            cleaned_item = remove_none_values(item)
            if cleaned_item is not None:  # Only add non-None values
                cleaned_list.append(cleaned_item)
        return cleaned_list
    
    else:
        # Return the value if it's not a dictionary or list
        return d if d is not None else None


def format_label(entity_key, entity_value, embed_manager, llm_client):
    entity_key = entity_key.lower()
    if entity_key.startswith("port"):
        formatted_value = get_port_code_ai(entity_value, llm_client)
    elif "terminal" in entity_key:
        formatted_value = format_TMS(
            {"type": entity_key,
             "mentionText": entity_value},
            embed_manager)["formattedValue"]
    elif entity_key.startswith(("eta", "etd")):
        try:
            cleaned_data_field_value = clean_date_string(entity_value)
            dt_obj = extract_date(cleaned_data_field_value)
            formatted_value = str(dt_obj.date())
        except ValueError as e:
            logger.info(f"ParserError: {e}")
            formatted_value = None
    elif "cutoff" in entity_key:
        try:
            cleaned_data_field_value = clean_date_string(entity_value)
            dt_obj = extract_date(cleaned_data_field_value)
            if dt_obj.tzinfo is None:
                dt_obj = dt_obj.replace(tzinfo=timezone.utc)
            else:
                dt_obj = dt_obj.astimezone(timezone.utc)
            formatted_value = dt_obj.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
        except ValueError as e:
            logger.info(f"ParserError: {e}")
            formatted_value = None
    elif any(numeric_indicator in entity_key.lower() for numeric_indicator in [
                "weight", "quantity", "measurements", "value"
            ]):
        formatted_value = extract_number(entity_value)
    else:
        formatted_value = None

    result = {
        "documentValue": entity_value,
        "formattedValue": formatted_value,
    }
    return result


def get_port_code_ai(port: str, llm_client):
    if "postprocessing" in prompt_library.library.keys() \
            and "port_code" in prompt_library.library["postprocessing"].keys():
        placeholders = {"PORT_INFO": port}
        prompt = prompt_library.create_prompt(prompt_library.library["postprocessing"]["port_code"]['prompt'],
                                              placeholders)
        response = llm_client.ask_chatgpt(prompt)
        cleaned_response = llm_client.clean_llm_response(response)
        try:
            cleaned_response = json.loads(cleaned_response)
        except json.JSONDecodeError:
            return None
        return cleaned_response['port']
    return None


def postprocess_llm(result, embed_manager, llm_client):

    # remove None values from dict
    result = remove_none_values(result)
    aggregated_data = defaultdict(list)
    # apply TMS formatting, convert LLM result to similar structure with Doc Ai
    for entity_key, entity_value in result.items():
        if isinstance(entity_value, list):
            for child_entity in entity_value:
                child_data = {}
                for child_entity_key, child_entity_value in child_entity.items():
                    child_data[child_entity_key] = format_label(child_entity_key,
                                                                child_entity_value,
                                                                embed_manager,
                                                                llm_client)
                aggregated_data[entity_key].append(child_data)
        else:
            aggregated_data[entity_key] = format_label(entity_key, entity_value, embed_manager, llm_client)

    logger.info("Data Extraction completed successfully")

    return aggregated_data
