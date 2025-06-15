from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma

def create_vectordb():
    """
    This function creates a vector db store for our RAG model to look into while answering user queries
    Returns:
        A vector db that has the information from a known database about the company
    """
    #Loads the data from the known database
    loader = TextLoader("knowledge_db.txt")
    docs = loader.load()
    #Splits the data into chunks
    splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    split_docs = splitter.split_documents(docs)
    #Generates embeddings that are converted to vectors and stored in the vector db
    embeddings = HuggingFaceEmbeddings(model_name = "all-MiniLM-L6-v2")
    db = Chroma.from_documents(split_docs,embeddings,persist_directory="chroma_db")
    return db