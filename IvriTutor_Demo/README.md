# RAG Math Tutor (IvriTutor Demo)

This project implements a Retrieval-Augmented Generation (RAG) chatbot designed to assist students with 8th-grade math exercises. It uses a knowledge base of parsed exercises, Pinecone for vector search, and Google Qwen for natural language understanding.

## Prerequisites

1.  **Python:** Ensure you have Python 3.8 or higher installed.
2.  **API Keys:**
    *   **Pinecone:** Create a Pinecone account and get your API key.
    *   **Google Qwen (Gemini):** Obtain an API key from Google AI Studio or Google Cloud.
3.  **Virtual Environment (Recommended):** It's good practice to use a virtual environment to manage project dependencies.

## Setup

1.  **Clone or Download the Project:**
    Obtain the project files.

2.  **Create a Virtual Environment (Optional but Recommended):**
    ```bash
    python -m venv venv
    # On Windows
    venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```

3.  **Install Dependencies:**
    Navigate to the project's root directory (where `requirements.txt` is located) and run:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Environment Variables:**
    *   Create a file named `.env` in the project's root directory.
    *   Add your API keys to the `.env` file:
        ```
        PINECONE_API_KEY=your_actual_pinecone_api_key_here
        GEMINI_API_KEY=your_actual_gemini_api_key_here
        ```

5.  **Prepare the Knowledge Base:**
    *   Ensure your parsed exercise data (e.g., `8th_grade_lesson_2_parsed.json`) is located in the `IvriTutor_Demo/parsed_outputs/` directory.
    *   **(First Run or After Data Changes):** Generate embeddings for the exercises:
        ```bash
        python IvriTutor_Demo/parsed_outputs/embedding.py
        ```
    *   **(First Run or After Data/Embedding Changes):** Index the embeddings into Pinecone:
        ```bash
        python IvriTutor_Demo/parsed_outputs/index_embedding.py
        ```
        *Note: The `index_embedding.py` script will create (or recreate) the Pinecone index named `mathtutor-e5-large`. Ensure this index name matches the one used in `chatbot.py`.*

## Running the Chatbot

1.  **Ensure Virtual Environment is Active (if used):**
    ```bash
    # On Windows
    venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```

2.  **Start the Chatbot:**
    Run the main chatbot script:
    ```bash
    python chatbot.py
    ```

3.  **Interact:**
    Follow the prompts in the terminal. The chatbot will guide you through small talk, ask for your grade and topic preference, and then present math exercises. You can ask for hints, request solutions, or provide answers for evaluation.

4.  **Exit:**
    Type `exit`, `quit`, or `done` to end the chat session.

## Project Structure (Key Files)

*   `chatbot.py`: The main chatbot application logic using an FSM.
*   `IvriTutor_Demo/parsed_outputs/embedding.py`: Script to generate embeddings for exercises.
*   `IvriTutor_Demo/parsed_outputs/index_embedding.py`: Script to index embeddings into Pinecone.
*   `IvriTutor_Demo/parsed_outputs/8th_grade_lesson_2_parsed.json`: Example parsed exercise data (input).
*   `IvriTutor_Demo/parsed_outputs/8th_grade_lesson_2_embeddings.json`: Generated embeddings (output of `embedding.py`).
*   `requirements.txt`: List of required Python packages.
*   `.env`: File to store your API keys (not included in version control).
*   `svg_outputs/`: Directory where exercise SVG images are saved for display.