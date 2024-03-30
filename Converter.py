import os
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
import json
import google.generativeai as genai
import uuid

# Set the API key for Google Gemini
api_key = 'AIzaSyDmoTBMoQMsXSQjr8thLYNU5eadgnEYKwI'
genai.configure(api_key=api_key)
model = genai.GenerativeModel('models/gemini-pro')

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
    chunks_with_ids = [{"id": i, "text": chunk} for i, chunk in enumerate(chunks, start=1)]
    return chunks_with_ids

def generate_question_answer(context):
    try:
        question_response = model.generate_content('generate only one good question according to this text :\n'+context)
        question = question_response.text.strip()
        answer_response = model.generate_content('generate only one good answer for this question: '+question+' according to this text :'+ context)
        answer = answer_response.text.strip()
        return {"question": question, "answer": answer, "answer_start": -1}
    except Exception as e:
        print("Error generating question-answer pair:", e)
        return None

def process_text_chunks(text_chunks):
    qa_data = []
    for chunk in text_chunks:
        context = chunk["text"]
        qa_pair = generate_question_answer(context)
        if qa_pair:
            qa_item = {
                "context": context,
                "qas": [
                    {
                        "question": qa_pair["question"],
                        "id": str(uuid.uuid4()),
                        "answers": [{"text": qa_pair["answer"], "answer_start": qa_pair["answer_start"]}]
                    }
                ]
            }
            qa_data.append(qa_item)
    return qa_data

def process_pdf_directory(pdf_dir, output_file):
    all_qa_data = []
    for file in os.listdir(pdf_dir):
        if file.endswith(".pdf"):
            pdf_path = os.path.join(pdf_dir, file)
            raw_text = get_pdf_text(pdf_path)
            text_chunks = get_text_chunks(raw_text)
            qa_data = process_text_chunks(text_chunks)
            all_qa_data.extend(qa_data)  # Append data to the main list

    with open(output_file, "w", encoding="utf-8") as json_file:
        json.dump(all_qa_data, json_file, indent=2)

# Example usage:
pdf_directory = r"C:\Users\Administrator\Desktop\final_project\ppt to json\PDfs"
output_file = "combined_QA_data.json"
process_pdf_directory(pdf_directory, output_file)