import os
import re
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def sanitize_filename(filename):
    # Remove characters that are not allowed in filenames
    return re.sub(r'[^\w\.-]', '_', filename)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part', 400

    base_folder = 'uploaded_files'
    files = request.files.getlist('file')

    for file in files:
        folder_name = request.form.get('folderName')
        if folder_name:
            folder_path = f'{base_folder}/{sanitize_filename(folder_name)}'
        else:
            folder_path = base_folder

        os.makedirs(folder_path, exist_ok=True)

        # Save the file in the specified folder structure.
        sanitized_filename = sanitize_filename(file.filename)
        file_path = os.path.join(folder_path, sanitized_filename)
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
