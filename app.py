from flask import Flask, request

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part', 400

    uploaded_file = request.files['file']
    if uploaded_file.filename == '':
        return 'No selected file', 400

    if uploaded_file:
        uploaded_file.save('uploaded_file.txt')
        return 'File uploaded successfully'

if __name__ == '__main__':
    app.run(debug=True)
