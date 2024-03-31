import json
import random

def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def save_json(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump({"data": data}, file, indent=2)

def split_data(data, test_size, validation_size):
    total_size = len(data)
    test_count = int(total_size * test_size)
    validation_count = int(total_size * validation_size)

    random.shuffle(data)
    test_data = data[:test_count]
    validation_data = data[test_count:test_count + validation_count]
    training_data = data[test_count + validation_count:]

    return training_data, test_data, validation_data

# Path to your JSON file
input_file = r'C:\Users\Administrator\Desktop\final_project\ppt to json\combined_QA_data.json'  # Replace with your file path

# Load data
original_data = load_json(input_file)

# Check the structure and extract paragraphs if needed
if 'data' in original_data and all('paragraphs' in item for item in original_data['data']):
    # Extract the paragraphs for splitting
    paragraphs = [item['paragraphs'] for item in original_data['data']]
    # Flatten the list of paragraphs
    flat_paragraphs = [para for sublist in paragraphs for para in sublist]
    # Split data
    training, test, validation = split_data(flat_paragraphs, test_size=0.20, validation_size=0.10)
    
    # Wrap them back in the required structure
    training = [{'paragraphs': training}]
    test = [{'paragraphs': test}]
    validation = [{'paragraphs': validation}]

    # Save split data
    save_json(training, 'training_data.json')
    save_json(test, 'test_data.json')
    save_json(validation, 'validation_data.json')
else:
    print("Error: The JSON structure does not match the expected format.")
