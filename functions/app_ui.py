import streamlit as st

class AppUI:
    def configure_UI():
        """
        Model Settings and other configuration placed in the sidebar
        """
        st.set_page_config(
            page_title="Multi-Document Q&A Chatbot", 
            page_icon="📰"
        )
        st.title("Multi-Document Q&A Chatbot")

        st.sidebar.header("⚙️ Configuration")
    
        # Model selection
        model = st.sidebar.selectbox(
            "Select OpenAI Model",
            ["gpt-3.5-turbo", "gpt-3.5-turbo-16k", "gpt-4", "gpt-4-turbo"],
            index=0
        )
        
        # Temperature slider
        temperature = st.sidebar.slider(
            "Temperature (Model Creativity)", 
            min_value=0.0, 
            max_value=1.0, 
            value=0.3, 
            step=0.1
        )

        return model, temperature

    def upload_files():
        """
        Upload PDF files
        """
        uploaded_files = st.sidebar.file_uploader(
            "Upload PDF Documents", 
            type="pdf", 
            accept_multiple_files=True
        )

        return uploaded_files
    
