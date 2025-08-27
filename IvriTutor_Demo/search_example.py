# search_example_updated.py
import os
from pathlib import Path
from pinecone import Pinecone # Use Pinecone client from pinecone package
from sentence_transformers import SentenceTransformer # Use SentenceTransformer
import logging

# Load environment variables (if using .env)
# from dotenv import load_dotenv
# load_dotenv() # Make sure PINECONE_API_KEY is in your .env

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- CONFIGURATION ---
INDEX_NAME = "mathtutor-e5-large" # Your updated index name
EMBEDDING_MODEL_NAME = "intfloat/multilingual-e5-large" # Your embedding model

def main():
    # --- 1. INITIALIZE PINECONE ---
    pinecone_api_key = os.getenv("PINECONE_API_KEY")
    if not pinecone_api_key:
        raise ValueError("PINECONE_API_KEY environment variable is not set")
    pc = Pinecone(api_key=pinecone_api_key)

    # --- 2. INITIALIZE SENTENCE TRANSFORMER MODEL ---
    try:
        embedding_model = SentenceTransformer(EMBEDDING_MODEL_NAME)
        logger.info(f"Loaded SentenceTransformer model: {EMBEDDING_MODEL_NAME}")
    except Exception as e:
        logger.error(f"Error loading SentenceTransformer model: {e}")
        return

    # --- 3. GET PINECONE INDEX ---
    try:
        index = pc.Index(INDEX_NAME)
        logger.info(f"Connected to Pinecone index: {INDEX_NAME}")
    except Exception as e:
        logger.error(f"Error connecting to Pinecone index {INDEX_NAME}: {e}")
        return

    # --- 4. DEFINE QUERY AND FILTERS ---
    # Example query in Hebrew
    query_text = "נקודות על מערכת צירים עם משולש" # "Points on a coordinate system with a triangle"
    # Example filter (adjust as needed)
    flt = {
        "grade": {"$eq": "ח"}, # Filter for grade ח (8th)
        # "topic": {"$eq": "ישר במערכת צירים"}, # Example: filter by topic
        # "svg_exists": {"$eq": True} # Example: only exercises with SVG
    }

    # --- 5. GENERATE EMBEDDING ---
    try:
        # SentenceTransformer.encode returns a numpy array, convert to list for Pinecone
        query_vector = embedding_model.encode([query_text], show_progress_bar=False)[0].tolist()
        logger.info("Generated query embedding.")
    except Exception as e:
        logger.error(f"Error generating embedding: {e}")
        return

    # --- 6. QUERY PINECONE ---
    try:
        # Query Pinecone index
        top_k = 5
        res = index.query(
            vector=query_vector,
            top_k=top_k,
            include_metadata=True,
            filter=flt # Include the filter
        )
        logger.info(f"Queried Pinecone index '{INDEX_NAME}' with top_k={top_k}")
    except Exception as e:
        logger.error(f"Error querying Pinecone: {e}")
        return

    # --- 7. DISPLAY RESULTS ---
    print(f"\n--- Search Results for Query: '{query_text}' ---")
    if res and "matches" in res and res["matches"]:
        for i, match in enumerate(res["matches"], 1):
            score = round(match.get("score", 0), 4)
            id = match.get("id", "N/A")
            metadata = match.get("metadata", {})
            exercise_id = metadata.get("exercise_id", "N/A")
            chunk_type = metadata.get("chunk_type", "N/A")
            topic = metadata.get("topic", "N/A")
            grade = metadata.get("grade", "N/A")
            text_snippet = metadata.get("text", "")[:100] + "..." if metadata.get("text") else "N/A"

            print(f"{i}. Score: {score}")
            print(f"   ID: {id}")
            print(f"   Exercise ID: {exercise_id}")
            print(f"   Chunk Type: {chunk_type}")
            print(f"   Topic: {topic}")
            print(f"   Grade: {grade}")
            print(f"   Text Snippet: {text_snippet}")
            print("-" * 20)
    else:
        print("No matches found.")

if __name__ == "__main__":
    main()