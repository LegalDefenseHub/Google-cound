"""
Cloud function to generate embedding of given file.
"""


import os

from dotenv import load_dotenv

import functions_framework
from typing import Any
import json
from vertexai.preview.language_models import TextEmbeddingModel


load_dotenv()


PROJECT_ID = os.getenv("PROJECT_ID")
LOCATION = os.getenv("LOCATION")


embedding_model = TextEmbeddingModel.from_pretrained("textembedding-gecko@003")


def get_embeddings(instances: list[str]) -> list[Any]:
    """
    Generates embeddings for given text.

    Args:
        instance (list[str]):
            Text to convert to embeddings.

    Returns:
        embeddings (list):
            values of embeddings.
    """
    try:
        embeddings = embedding_model.get_embeddings(instances)
        return [embedding.values for embedding in embeddings]
    except Exception as e:
        print("NOT PROCESSED")
        print(e)
        return []


def generate_embeddings(pdf_data: dict) -> dict:
    """
    Extracts content from pdf_data for creating embeddings.

    Args:
        pdf_data (dict): file data to be processed.
    """
    pdf_data=json.loads(pdf_data)
    instances=[]
    values=[]

    batch_size = 10
    iterate = 0

    for content in pdf_data.values():
        instances.append(content)
        iterate += 1

        if iterate % batch_size == 0 or iterate == len(pdf_data):
            embeddings = get_embeddings(instances)
            values.append(embeddings)

            instances = []


    response_json = json.dumps({'embedding_column': values})
    response = json.loads(response_json)
    return response


@functions_framework.http
def hello_http(request):
    request_json = request.get_json(silent=True)
    if not request_json or "pdf_data" not in request_json:
        return {"error": "Request body must contain 'pdf_data' field."}, 400
    pdf_data = request_json["pdf_data"]
    return  generate_embeddings(pdf_data)