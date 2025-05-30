import os
from flask import Flask, render_template, request, redirect
from werkzeug.utils import secure_filename
from config import UPLOAD_FOLDER, INDEX_FOLDER
from utils.pdf_reader import extract_text_from_pdf
from utils.faiss_utils import build_faiss_index, search_faiss
from utils.log_config import logger

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(INDEX_FOLDER, exist_ok=True)

texts = []
faiss_index = None

@app.route('/', methods=['GET', 'POST'])
def index():
    global texts, faiss_index
    if request.method == 'POST':
        file = request.files['file']
        if file.filename.endswith('.pdf'):
            filename = secure_filename(file.filename)
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(path)
            logger.info(f"PDF uploaded: {filename}")
            texts = extract_text_from_pdf(path)
            faiss_index, _ = build_faiss_index(texts)
            return redirect('/')
        else:
            return "Please upload a PDF file."
    return render_template('index.html', uploaded=bool(texts))

@app.route('/search', methods=['POST'])
def search():
    global texts, faiss_index
    query = request.form.get('query')
    if not faiss_index:
        return redirect('/')
    results = search_faiss(faiss_index, texts, query)
    return render_template('results.html', query=query, results=results)

if __name__ == "__main__":
    app.run(debug=True)
