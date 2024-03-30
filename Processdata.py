from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
import json

def get_pdf_text(pdf_docs):
    text = ""
    
    pdf_reader = PdfReader(pdf_docs)
    for page in pdf_reader.pages:
        text += page.extract_text()     
    return text        

def get_text_chunks(raw_text):
    text_splitter = CharacterTextSplitter(
            separator=". ",
            chunk_size=250,
            chunk_overlap=250,
            length_function=len
    )
    chunks = text_splitter.split_text(raw_text)
    # Create a list to store dictionaries with unique IDs for each chunk
    chunks_with_ids = []
    for i, chunk in enumerate(chunks, start=1):
        chunk_dict = {"id": i, "text": chunk}
        chunks_with_ids.append(chunk_dict)
    return chunks_with_ids

# Add PDF path here then run and the output file 
# pdf_docs = "C:\Users\Administrator\Desktop\final_project\ppt to json\PDfs\ethics_in_information_technology2c_5th_ed._0_.pdf"            
raw_text = get_pdf_text(r"C:\Users\Administrator\Desktop\final_project\ppt to json\PDfs\ethics_in_information_technology2c_5th_ed._0_.pdf")
text_chunks = get_text_chunks(raw_text) 

with open("output.json", 'w', encoding='utf-8') as json_file:
    json.dump(text_chunks, json_file, indent=2)
