from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import create_retrieval_chain
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import streamlit as st

from functions.document_loader import DocumentProcessingPipeline 
from functions.app_ui import AppUI

# Load the environment variable set
load_dotenv()

def get_response(query, chat_history, model, temperature):
    """
    Function to get the response from the LLM chain based on the query and chat history.
    Args:
        query (str): The user query.
        chat_history (list): The chat history.
        model (str): The OpenAI LLM model to be used.
        temperature (float): The temperature set to the LLM.
    Returns:
        dict: The response from the LLM chain.
    """

    prompt_template = """
        Answer the question {input} based solely on the provided context. 
        If the answer is not available in the context, respond that you do not know and requires more information.
        \n\n{context}
    """
    # Initializing the template with the chat history for memory
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", prompt_template),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}")
        ]
    )

    # Initializing the LLM used
    llm = ChatOpenAI(
                    model=model,
                    temperature=temperature
                    )

    # Create and invoke the chain that is returned by the function
    combine_docs_chain = create_stuff_documents_chain(llm, prompt)
    retrieval_chain = create_retrieval_chain(retriever, combine_docs_chain)
    response = retrieval_chain.invoke({
        "chat_history": chat_history,
        "input": query
    })
    return response

# Instantiate the application UI and initialize the chat history
model, temperature = AppUI.configure_UI()
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

uploaded_files = AppUI.upload_files()

if uploaded_files:
    # Process Documents
    with st.spinner("Processing documents..."):
        vectorstore = DocumentProcessingPipeline.process_pdfs(uploaded_files)
        retriever = vectorstore.as_retriever()
        if not vectorstore:
            st.error("No documents could be processed.")

    # Conversation
    for message in st.session_state.chat_history:
        if isinstance(message, HumanMessage):
            with st.chat_message("Human"):
                st.markdown(message.content)
        else:
            with st.chat_message("AI"):
                st.markdown(message.content)

    # Input the question of the user and show the response of the chatbot
    user_query = st.chat_input("Ask a question about the documents")
    if user_query is not None and user_query != "":

        with st.chat_message("Human"):
            st.markdown(user_query)

        with st.chat_message("AI"):
            ai_response = get_response(user_query, st.session_state.chat_history, model, temperature)["answer"]
            st.write(ai_response)

        # To show the chat history
        st.session_state.chat_history.append(HumanMessage(user_query))
        st.session_state.chat_history.append(AIMessage(ai_response))