from pathlib import Path
from langchain_community.document_loaders import PDFMinerLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings


directory_path = Path("./documents")
all_texts = []

for file_path in directory_path.rglob("*.pdf"):
    loader = PDFMinerLoader(str(file_path))
    data = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1700, 
        chunk_overlap=200,
        length_function=len
    )
    texts = text_splitter.split_documents(data)
    all_texts.extend(texts)

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
db = FAISS.from_documents(all_texts, embeddings)
db.save_local("db_embeddings")
