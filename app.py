import streamlit as st
from dotenv import load_dotenv
import pickle
from PyPDF2 import PdfReader
from streamlit_extras.add_vertical_space import add_vertical_space
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain


import os


#sidebar contents

with st.sidebar:
    st.title('😎 LLM Chat App')
    
    st.markdown(
    '''
    **About**\n
    This app is an LLM powere chatbot using:-\n
     - [Streamlit](https://streamlit.io/)\n
     - [LangChain](https://python.langchain.com/)\n
     
    
    ''')
    add_vertical_space(5)
    st.write('Made with love♥ by Rajat Goyal')




def main():
    st.header("Chat with PDF💭")

    load_dotenv()

    #upload pdf file
    pdf = st.file_uploader("Upload your PDF", type = "pdf")
    
     
    #Read pdf file
    if pdf is not None:
        pdf_reader = PdfReader(pdf)
        st.write(pdf_reader)

        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()

            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size = 1000,
                chunk_overlap = 200,
                length_function = len
            )

        chunks = text_splitter.split_text(text=text)
        #st.write(chunks)

            
            # # Embeddings

        store_name = pdf.name[:-4]
            
        if os.path.exists(f"{store_name}.pkl"):
            with open(f"{store_name}.pkl","rb") as f:
                VectorStore = pickle.load(f)
            #st.write("Embeddings loaded from disk.")
            
        else:

            embeddings = OpenAIEmbeddings()
            VectorStore = FAISS.from_texts(chunks , embedding=embeddings)
                
                
            with open(f"{store_name}.pkl" , "wb") as f:
                
                pickle.dump(VectorStore, f)
                
            #st.write("Embeddings computed sucsessfully")

        #Accepting user query.
        query = st.text_input("Ask questions about your PDF file")
        #st.write(query)

        if query:

            docs = VectorStore.similarity_search(query=query , k =3)

            llm = OpenAI(temperature=0)
            chain = load_qa_chain(llm=llm ,chain_type="stuff")
            response = chain.run(input_documents = docs ,question = query)
            st.write(response)







            #st.write(text)

    


if __name__ == '__main__':
    main()
         