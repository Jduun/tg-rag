import os
import json
import logging
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

from models import model_list, model_alias
from litellm import Router

router = Router(
    model_list=model_list, cache_responses=True, allowed_fails=1, cooldown_time=100
)
system_prompt = "You're an intelligent assistant. Answer to the user using context."

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
db = FAISS.load_local(
    "db_embeddings",
    embeddings,
    allow_dangerous_deserialization=True,
)

folder_with_chat_histories = os.getenv("CHAT_HISTORIES_FOLDER")
basic_chat_history = [
    {"role": "system", "content": system_prompt},
]
max_chat_history_len = 10


def get_chat_history(history_filename: str) -> list:
    with open(history_filename, "r", encoding="utf-8") as story_file:
        chat_history = json.load(story_file)
    return chat_history


def delete_user_chat_history(user_id: int):
    user_chat_history_file_path = f"./{folder_with_chat_histories}/{user_id}.json"
    if os.path.exists(user_chat_history_file_path):
        os.remove(user_chat_history_file_path)
        logging.getLogger(__name__).info(f"{user_chat_history_file_path} deleted")


def chat_history_exist(user_id: int) -> bool:
    user_chat_history_file_path = f"./{folder_with_chat_histories}/{user_id}.json"
    return os.path.exists(user_chat_history_file_path)


async def get_llm_answer(user_id: int, message: str = None) -> str:
    docs = db.similarity_search_with_score(message)[:1]
    similar_chunk = docs[0]
    similar_chunk_content = similar_chunk[0].page_content
    message = f"""
    Answer to the message using following context:
    
    {similar_chunk_content}

    Message: {message}
    """
    logging.getLogger(__name__).info(f"Chunk: {similar_chunk_content}")
    logging.getLogger(__name__).info(f"Message: {message}")
    user_chat_history_file_path = f"./{folder_with_chat_histories}/{user_id}.json"
    chat_history = []
    if not os.path.exists(user_chat_history_file_path):
        logging.getLogger(__name__).info(f"{user_chat_history_file_path} doesn't exist")
        if not os.path.exists(folder_with_chat_histories):
            os.makedirs(folder_with_chat_histories)
        with open(
            user_chat_history_file_path, "w", encoding="utf-8"
        ) as user_chat_history_file:
            chat_history = basic_chat_history.copy()
            chat_history.append({"role": "user", "content": message})
            json.dump(
                basic_chat_history, user_chat_history_file, ensure_ascii=False, indent=4
            )
        logging.getLogger(__name__).info(f"{user_chat_history_file_path} created")
    else:
        chat_history = get_chat_history(user_chat_history_file_path)
        logging.getLogger(__name__).info(f"{user_chat_history_file_path} exist")
        chat_history.append({"role": "user", "content": message})
        with open(
            user_chat_history_file_path, "w", encoding="utf-8"
        ) as user_chat_history_file:
            json.dump(
                chat_history, user_chat_history_file, ensure_ascii=False, indent=4
            )
    response = await router.acompletion(
        model=model_alias,
        messages=chat_history,
        temperature=0.2,
    )
    llm_response = response.choices[0].message.content
    chat_history.append({"role": "assistant", "content": llm_response})
    if len(chat_history) > max_chat_history_len:
        del chat_history[1:3]
    with open(
        user_chat_history_file_path, "w", encoding="utf-8"
    ) as user_chat_history_file:
        json.dump(chat_history, user_chat_history_file, ensure_ascii=False, indent=4)
    return llm_response
