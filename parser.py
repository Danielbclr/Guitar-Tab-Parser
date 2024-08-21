import json
import os
import logging
import random
from collections import OrderedDict

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Define the note mapping for each string and fret number.
note_mapping = {
    'E2': ['E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E'],
    'A2': ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A'],
    'D3': ['D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B', 'C', 'C#', 'D'],
    'G3': ['G', 'G#', 'A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G'],
    'B3': ['B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'],
    'E4': ['E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E']
}

# Initialize the dictionary to count notes.
note_count = {note: 0 for note in set(sum(note_mapping.values(), []))}

# Shift notes and labels
def shift_notes_and_label(notes, label, shift_amount):
    all_notes = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']
    note_index = {note: i for i, note in enumerate(all_notes)}
    
    def shift_index(index, shift):
        return (index + shift) % len(all_notes)
    
    shifted_notes = [0] * len(notes)
    for i, count in enumerate(notes):
        shifted_notes[shift_index(i, shift_amount)] = count
    
    shifted_label = all_notes[shift_index(note_index[label], shift_amount)]
    
    return shifted_notes + [shifted_label]

# Parse the guitar tab.
def parse_tab(file_path):
    local_note_count = {note: 0 for note in note_count}  # Local count for this file
    string = ''
    logging.info(f"Processing file: {file_path}")
    try:
        with open(file_path, 'r') as file:
            for line in file:
                if line.startswith('E|'):
                    string = 'E4'
                elif line.startswith('B|'):
                    string = 'B3'
                elif line.startswith('G|'):
                    string = 'G3'
                elif line.startswith('D|'):
                    string = 'D3'
                elif line.startswith('A|'):
                    string = 'A2'
                elif line.startswith('E|'):
                    string = 'E2'
                else:
                    continue

                # Extract fret numbers and convert them to notes
                frets = ''.join([char if char.isdigit() else ' ' for char in line.strip()])
                for fret in frets.split():
                    try:
                        fret = int(fret)
                        if 0 <= fret < len(note_mapping[string]):
                            note = note_mapping[string][fret]
                            local_note_count[note] += 1
                    except ValueError:
                        logging.warning(f"Error parsing fret number: {fret}")
    except FileNotFoundError:
        logging.error(f"File not found: {file_path}")
    except Exception as e:
        logging.error(f"An unexpected error occurred while processing {file_path}: {e}")
    
    return local_note_count

# Order the note count by musical note order (A to G#)
def order_note_count(note_count):
    ordered_note_count = OrderedDict()
    for note in ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']:
        if note in note_count:
            ordered_note_count[note] = note_count[note]
    return ordered_note_count

# Export the result as a JSON file with each entry on a separate line
def save_as_json(output_filename, data):
    logging.info(f"Saving results to {output_filename}")
    try:
        with open(output_filename, 'w') as json_file:
            json_file.write('[\n')  # Start the JSON array
            for i, entry in enumerate(data):
                if i > 0:
                    json_file.write(',\n')  # Add comma between entries
                json.dump(entry, json_file)
            json_file.write('\n]')  # End the JSON array
    except Exception as e:
        logging.error(f"Failed to save JSON file: {e}")

# Process all files in the folder and its subfolders
def process_folder(target_folder, output_filename):
    all_results = []
    logging.info(f"Processing folder: {target_folder}")
    for foldername, subfolders, filenames in os.walk(target_folder):
        folder_name = os.path.basename(foldername)
        logging.info(f"Processing folder: {folder_name}")
        for filename in filenames:
            if filename.endswith('.txt'):  # Assuming guitar tab files are .txt
                file_path = os.path.join(foldername, filename)
                local_note_count = parse_tab(file_path)
                ordered_note_count = order_note_count(local_note_count)
                result = list(ordered_note_count.values())  # Convert note counts to list
                result.append(folder_name)  # Add folder name as label

                # Add original result
                all_results.append(result)
                logging.info(f"Original result for file {filename}: {result}")
                
                # Generate two random shift amounts and add shifted results
                for _ in range(2):
                    shift_amount = random.randint(1, 11)
                    shifted_result = shift_notes_and_label(result[:-1], result[-1], shift_amount)
                    all_results.append(shifted_result)
                    logging.info(f"Shifted result: {shifted_result}")
    
    save_as_json(output_filename, all_results)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        logging.error("Usage: python script.py <target_folder> <output_file>")
        sys.exit(1)
    target_folder = sys.argv[1]
    output_file = sys.argv[2]
    logging.info(f"Starting processing of folder: {target_folder} with output file: {output_file}")
    process_folder(target_folder, output_file)
    logging.info("Processing complete.")
