# tg-rag

`tg-rag` is a Telegram bot that uses Retrieval-Augmented Generation (RAG). The bot can analyze text documents, extract information, and respond to user queries using LLM within context from documents.


## Technologies

- **[Aiogram](https://docs.aiogram.dev/)** — for working with the Telegram API.
- **[LangChain](https://langchain.com/)** — for text processing and LLM integration.
- **[FAISS](https://github.com/facebookresearch/faiss)** — for working with a vector store.
- **[LiteLLM](https://github.com/BerriAI/litellm)** — for interacting with different LLMs using one interface.


## Installation and Setup

1. Clone the repository:
    ```
    https://github.com/Jduun/tg-rag.git
    ```

2. Navigate to the project folder:
    ```
    cd tg-rag
    ```

3. Create file with environment variables:
    ```
    cp .env.example .env
    ```

    Change the values of the environment variables to your own.
    
4. Build project:
    ```
    docker compose up --build
    ```

## Usage

1. Upload PDF documents to the `documents` folder so the bot can use them to generate responses.
2. Index the files with the command:
    ```
    python3 src/index.py
    ```
3. Restart the bot.
4. Send a message to the bot in Telegram to receive a response.
