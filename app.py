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

    # Check if the request contains the 'webkitRelativePath' field.
    if 'webkitRelativePath' in request.files['file']:
        base_folder = 'uploaded_files'
        file = request.files['file']
        for filename in request.files.getlist('file'):
            # Get the relative path of the file from the folder structure.
            folder_structure = filename.webkit_relative_path.split('/')
            # Sanitize folder names
            sanitized_folder_structure = [sanitize_filename(folder_name) for folder_name in folder_structure]
            # Get the folder name where the file should be saved.
            folder_name = os.path.join(base_folder, *sanitized_folder_structure[:-1])
            os.makedirs(folder_name, exist_ok=True)

            # Save the file in the specified folder structure.
            sanitized_filename = sanitize_filename(filename.filename)
            file.save(os.path.join(folder_name, sanitized_filename))
    else:
        # Handle single file upload as before.
        uploaded_file = request.files['file']
        folder_name = request.form.get('folderName')
        if folder_name:
            # Save the file in the specified folder structure.
            folder_path = f'uploaded_files/{sanitize_filename(folder_name)}'
            os.makedirs(folder_path, exist_ok=True)
            sanitized_filename = sanitize_filename(uploaded_file.filename)
            uploaded_file.save(os.path.join(folder_path, sanitized_filename))
        else:
            # Save the file in the root folder.
            sanitized_filename = sanitize_filename(uploaded_file.filename)
            uploaded_file.save(f'uploaded_files/{sanitized_filename}')

    return 'Files uploaded successfully'

if __name__ == '__main__':
    app.run(debug=True, port=5001)
