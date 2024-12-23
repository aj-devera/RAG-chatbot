## Question and Answering Chatbot
This chatbot uses the documents uploaded by the user and use it as the knowledge base of the Large Language Model (LLM). With this, the response given by the chatbot is contextualize based on the given information. It provides accurate answers to questions that are included in the documents.

In this code, the documents were stored into embeddings inside the FAISS vector database. With Langchain, the process of Retrieval-Augmented Generation (RAG) was implemented wherein the LLM retrieves the context and information from the vector database, augments this information into the LLM, and generates the response with the specific context. 

---
### How to Use the Chatbot
#### This section provides the step-by-step procedure on how to use the chatbot:
1. Run the Terminal and clone the repository.
```
$ git clone https://github.com/aj-devera/TM-MLE-GenAI-Exam.git
```
2. Go to the cloned folder.
```
$ cd <folder-name>
```
(Optional) Create a virtual environment to isolate the Python environment that will be used.
```
$ python -m venv <environment-name>
$ source <environment-name>/bin/activate
```
The location of the `activate` file may vary. For others, it may be located in `<environment-name>/Scripts/activate`. By using this command, it will now use the virtual environment.
3. Install the necessary packages to run the application using this command:
```
$ pip install -r requirements.txt
```
Make sure that the terminal is in the same directory as the `requirements.txt`
4. Create a `.env` file to safely store your OpenAI API Key. The contents of the file should only be:
```
OPENAI_API_KEY="<Your-API-Key>"
```
Make sure to change the value to your API Key.
5. You can now run the Streamlit Application and use the Chatbot.
```
$ streamlit run app.py
```
Make sure that the terminal is in the same directory as the `app.py`
