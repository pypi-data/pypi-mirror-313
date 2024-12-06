"""Config constant params for data science project(s)."""
# This is the sandbox version of the project parameters but different constants
project_parameters_sandbox = {
    # Google Constants
    "g_ai_project_name": "forto-data-science-sandbox",
    "g_ai_project_id": "882852108312",
    # Google Cloud Storage
    "doc_ai_bucket_name": "ds_document_capture",  # Creating a new bucket bcz the prod bucket name is already taken
    "doc_ai_bucket_batch_input": "ds_batch_process_docs",
    "doc_ai_bucket_batch_output": "ds_batch_process_output",
    "excluded_endpoints": ["/healthz", "/", "/metrics", "/healthz/"],
    "model_selector": {
        "stable": {
            "bookingConfirmation": 1,
            "packingList": 0,
            "commercialInvoice": 0,
            "finalMbL": 0,
            "arrivalNotice": 0,
            "shippingInstruction": 0,
            "customsAssessment": 0,
        },
        "beta": {
            "bookingConfirmation": 0,
            "packingList": 0,
            "finalMbL": 0,
            "arrivalNotice": 0,
            "shippingInstruction": 0,
            "customsAssessment": 0,
        },
    },
    # this is the model selector for the model
    # to be used from the model_config.yaml file based on the environment,
    # 0 mean the first model in the list
}
