import streamlit as st
import os
import time

from dotenv import load_dotenv
from streamlit_chat import message
from langchain.chat_models import ChatOpenAI
from langchain.schema import (AIMessage, HumanMessage, SystemMessage)

from utils import extract_text

load_dotenv()

chat = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)


def get_advice(cv_string: str, query: str) -> str:
    response = chat.predict_messages([
        SystemMessage(content="You are AI Career Consultant designed by Arya Adyatma. User give you the CV or Portfolio, then they can ask anything about the CV or Portfolio. IMPORTANT: Don't answer questions that are out of the scope of AI Career Consultant."),
        HumanMessage(content="how to build muscle?"),
        AIMessage(content="Sorry, as AI Career Consultant, I can't answer out of topic questions such as how to build muscle."),
        HumanMessage(content=f"Here is my CV in raw plain text: {cv_string}.\n\nBased on the CV, {query}"),
    ])
    return response.content


def main():
    st.image("assets/aicc-logo.png")
    st.write("# AI Career Consultant")
    st.write("App built by Arya Adyatma - a candidate world class developer 🚀")
    st.write("")
    st.write("**Before you can consult, please upload your portfolio or CV file.**")

    cv_file = st.file_uploader("Upload your CV or Portfolio here", type=["pdf", "docx"])
    
    if cv_file is not None:
        
        file_type = cv_file.name.split(".")[-1]
        path_cv_file = "temp/" + cv_file.name
        
        # Save the file temporarily
        with open(path_cv_file, 'wb') as f:
            f.write(cv_file.getbuffer())
        
        cv_text = extract_text(path_cv_file)[:20000]
        print("CV:", cv_text)
        
        st.write("")
        st.write("**File upload success. Now you're ready to ask the AI Career Consultant.**")
        
        query = st.text_area("Ask to AI Career Consultant based on your CV / Portfolio", placeholder="Consult with AI here...")

        if st.button("Ask Now"):
            
            with st.spinner("The AI is answering..."):
                response = get_advice(cv_text, query)
            
            st.write("")
            st.write(f"**Question: {query}**")
            
            answer_md = st.empty()
            answer_md_state = ""
            
            for char in response:
                time.sleep(0.01)
                answer_md_state += char
                answer_md.write(answer_md_state)


if __name__ == "__main__":
    main()

