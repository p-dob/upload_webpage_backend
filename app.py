import os
import re
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def sanitize_filename(filename):
    # Get the file extension
    name, ext = os.path.splitext(filename)

    # Remove characters that are not allowed in filenames
    name = re.sub(r'[^\w\.-]', '_', name.strip())

    # Combine the sanitized name with the original extension
    sanitized_filename = name + ext
    return sanitized_filename

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part', 400

    base_folder = 'uploaded_files'
    files = request.files.getlist('file')
    folder_list = request.form.getlist('folderName')
    print(folder_list)

    for folder_name, file in zip(folder_list, files):
        # Folder Name will be "undefined" when they are 
        # selected via "Choose Files" button.
        if folder_name=='undefined':
            folder_path = base_folder
        elif folder_name:
            folder_path = f'{base_folder}{folder_name}'
            folder_path = str(folder_path.rsplit('/', 1)[0])
        else:
            folder_path = base_folder
        
        print("Folder Path:", folder_path)
        os.makedirs(folder_path, exist_ok=True)

        # Save the file in the specified folder structure.
        sanitized_filename = sanitize_filename(file.filename)
        file_path = os.path.join(folder_path, sanitized_filename)

        # If a file with the same name exists, append a number to the filename to avoid overwriting
        count = 1
        while os.path.exists(file_path):
            name, ext = os.path.splitext(sanitized_filename)
            file_path = os.path.join(folder_path, f"{name}_{count}{ext}")
            count += 1

        file.save(file_path)

        # Check if the file was saved successfully and its size
        if os.path.exists(file_path):
            file_size = os.path.getsize(file_path)
            print(f"Saved file: {file_path}, Size: {file_size} bytes")
        else:
            print(f"Failed to save file: {file_path}")

    return 'Files uploaded successfully'

if __name__ == '__main__':
    app.run(debug=True, port=5001)
