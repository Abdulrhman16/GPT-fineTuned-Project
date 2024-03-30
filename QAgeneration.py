import json
import google.generativeai as genai
import os
import uuid

# Set the API key directly
api_key = 'AIzaSyDmoTBMoQMsXSQjr8thLYNU5eadgnEYKwI'
import json
import google.generativeai as genai

# Set the API key directly


# Configure GenAI with the API key
genai.configure(api_key=api_key)
model = genai.GenerativeModel('models/gemini-pro')

def generate_question_answer(context):
    try:
        # Generate question from the provided context
        question_response = model.generate_content('generate only one good question according to this text :\n'+context)
        question = question_response.text.strip()  # Extract the text from the response
        
        # Generate answer for the plain context
        answer_response = model.generate_content('generate only one good answer for this question: '+question+' according to this text :'+ context)
        answer = answer_response.text.strip()  # Extract the text from the response
        
        return {
            "question": question,
            "answer": answer,
            "answer_start": -1  # We'll leave this as -1 for now
        }
    except Exception as e:
        print("Error generating question-answer pair:", e)
        return None

def process_text_chunks(text_chunks):
    qa_data = []
    for chunk in text_chunks:
        try:
            context = chunk["text"]
            qa_pair = generate_question_answer(context)
            if qa_pair:
                # Create a dictionary in the desired structure
                qa_item = {
                    "context": context,
                    "qas": [
                        {
                            "question": qa_pair["question"],
                            "id": str(uuid.uuid4()),  # Generate a unique ID for each QA pair
                            "answers": [
                                {
                                    "text": qa_pair["answer"],
                                    "answer_start": qa_pair["answer_start"]
                                }
                            ]
                        }
                    ]
                }
                qa_data.append(qa_item)
        except KeyError as e:
            print("Error processing text chunk:", e)
    return qa_data

# Load JSON file containing text chunks
with open("output.json", "r", encoding="utf-8") as file:
    text_chunks = json.load(file)

# Generate QA data for each text chunk
qa_data = process_text_chunks(text_chunks)

# Dump the generated QA data to a JSON file
with open("QA.json", "w", encoding="utf-8") as json_file:
    json.dump(qa_data, json_file, indent=2)
