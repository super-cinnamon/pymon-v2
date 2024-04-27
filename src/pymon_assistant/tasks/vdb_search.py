import os
import json
import logging

import dotenv
from qdrant_client import QdrantClient, models
from sentence_transformers import SentenceTransformer

from src.pymon_assistant.utils import check_context_validity

dotenv.load_dotenv()

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_TOKEN = os.getenv("QDRANT_TOKEN")

CONFIG_FOLDER_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config")
with open(os.path.join(CONFIG_FOLDER_PATH, "gemini_config.json"), "r") as f:
    config_dict = json.load(f)

QDRANT_CONFIG = config_dict["qdrant_config"]
QDRANT_CLIENT = QdrantClient(url=QDRANT_URL, api_key=QDRANT_TOKEN)

EMBEDDINGS_MODEL = SentenceTransformer(QDRANT_CONFIG["embeddings_model"])
logging.info("Qdrant client and embeddings model loaded successfully.")


def generate_embeddings(text):
    embeddings = EMBEDDINGS_MODEL.encode(text)
    return embeddings


def search_vdb(query, collection_name=QDRANT_CONFIG["collection_name"]):

    embedded_query = generate_embeddings(query)

    search_results = QDRANT_CLIENT.search(
        collection_name=collection_name,
        search_params=models.SearchParams(hnsw_ef=128, exact=False),
        query_vector=(
            QDRANT_CONFIG["vector_name"],
            [float(num) for num in embedded_query]),
        limit=QDRANT_CONFIG["limit"],
    )

    return search_results


def format_vdb_results(results):
    # make it into a list of strings
    formatted_results = []
    for res in results:
        if res.score > QDRANT_CONFIG["threshold"]:
            formatted_results.append(
                f"{res.payload['class']} page: {res.payload['title']}:\n {res.payload['content']}"
            )
    return formatted_results


def rag_input(context):
    """
    compiles the search results into a single string

    Parameters
    ----------
    search_results: list
        the list of search results from the search engine

    Returns
    -------
    str
        the compiled input for the LLM
    """

    rag_string = "\n\n## Database search results:\n"

    # check context shape validity
    if not check_context_validity(context, search_type="vdb"):
        rag_string += "No search results available.\n"

    else:
        for res in context:
            rag_string += res + "\n\n"

    return rag_string


def get_context(query, collection_name=QDRANT_CONFIG["collection_name"]):
    vdb_res = search_vdb(query, collection_name)
    context = format_vdb_results(vdb_res)

    rag_prompt = rag_input(context)
    return rag_prompt
