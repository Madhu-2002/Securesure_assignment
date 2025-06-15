# securesure_bot/flows/faq.py
from utils import state_manager,vector_db
from langchain.chat_models import ChatOllama
from langchain.chains import RetrievalQA

#Choosing llama3.2 model for answering user and collect information from the known database for answering FAQs from users
llm = ChatOllama(model="llama3.2")
knowledge_base = vector_db.create_vectordb()

async def handle(user_input, state, conversation_id):
    """
    This is the handler function called when user has a FAQ
    Args:
        user_input(str): The user's FAQ
        state: State of answering the FAQ
        conversation_id(str): The id that keeps record of the user's interaction with the assistant
    Returns:
        str: A string giving answer to the user's FAQ
    """
    #Calls the LLM to look into information from the known databse to answer user's query (RAG based architecture)
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever = knowledge_base.as_retriever(search_type="similarity", search_kwargs={"k": 2}),
        chain_type="stuff"
    )
    response = qa_chain.invoke(user_input)
    state_manager.update_state(conversation_id, state)
    return response
