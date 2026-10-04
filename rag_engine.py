import os
os.environ['ANONYMIZED_TELEMETRY'] = 'False'
# --- IMPORT LIBRARY (LANGCHAIN 0.2.x) ---
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_chroma import Chroma

from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

# --- KONFIGURASI ---
DB_PATH = "./chroma_db"
DATA_PATH = "./data"

# --- MODEL ---
embedding_function = OllamaEmbeddings(model="nomic-embed-text")
llm = ChatOllama(model="llama3.2", temperature=0.3, streaming=True)

# ================= FILE HANDLING =================

def save_uploaded_file(uploaded_file):
    if not os.path.exists(DATA_PATH):
        os.makedirs(DATA_PATH)

    file_path = os.path.join(DATA_PATH, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    return file_path

def get_list_of_files():
    if not os.path.exists(DATA_PATH):
        return []
    return os.listdir(DATA_PATH)

def delete_file(filename):
    file_path = os.path.join(DATA_PATH, filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        return True
    return False

# ================= INGEST =================

def ingest_document(file_path):
    """Membaca PDF dan menyimpannya ke Database Vector"""
    # 1. Baca PDF
    loader = PyPDFLoader(file_path)
    docs = loader.load()
    
    # 2. Pecah Teks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    splits = text_splitter.split_documents(docs)
    
    # 3. Simpan ke ChromaDB (AUTO PERSIST)
    Chroma.from_documents(
        documents=splits,
        embedding=embedding_function,
        persist_directory=DB_PATH
    )


# ================= RAG QA =================

def answer_question(user_question):
    db = Chroma(
        persist_directory=DB_PATH,
        embedding_function=embedding_function
    )

    retriever = db.as_retriever(search_kwargs={"k": 3})

    system_prompt = (
        "Kamu adalah asisten AI profesional untuk Bank Mandiri. "
        "Tugasmu adalah menjawab pertanyaan berdasarkan dokumen regulasi yang diberikan. "
        "\n\n"
        "ATURAN JAWABAN:\n"
        "1. Gunakan format Markdown yang rapi (Gunakan Bold untuk poin penting).\n"
        "2. Jika jawaban mengandung poin-poin, gunakan daftar list (1, 2, 3 atau peluru).\n"
        "3. Sebutkan nama Peraturan atau Pasal di awal jawaban sebagai referensi.\n"
        "4. Jawab dengan gaya bahasa formal namun mudah dipahami.\n"
        "5. Jika tidak ada di dokumen, katakan: 'Maaf, informasi tidak ditemukan dalam basis data regulasi kami.'\n"
        "\n\n"
        "KONTEKS DOKUMEN:\n"
        "{context}"
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}")
    ])

    qa_chain = create_stuff_documents_chain(llm, prompt)
    rag_chain = create_retrieval_chain(retriever, qa_chain)

    result = rag_chain.invoke({"input": user_question})

    return result.get("answer", ""), result.get("context", [])
