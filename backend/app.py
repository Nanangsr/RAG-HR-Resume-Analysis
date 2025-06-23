# backend/app.py (FINAL - with Caching Fix)
import os
import json
import logging
import asyncio
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

from core.rag_chain import ResumeRagChain
from utils.resume_parser import parse_resume
from utils.jd_parser import parse_jd

load_dotenv()
app = Flask(__name__)
CORS(app)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- PERBAIKAN KONSISTENSI SKOR ---
# Kita buat cache untuk instance RAG Chain di level aplikasi
# Ini memastikan cache di dalam ResumeStandardizer tidak di-reset setiap request
rag_chains_cache = {}

def get_rag_chain(domain: str) -> ResumeRagChain:
    if domain not in rag_chains_cache:
        logging.info(f"Creating and caching new RAG Chain instance for domain: {domain}")
        rag_chains_cache[domain] = ResumeRagChain(domain=domain)
    return rag_chains_cache[domain]
# ------------------------------------

def process_single_file(file_storage):
    if not file_storage or not file_storage.filename:
        return None, "File tidak valid atau tidak ada nama file."
    text, error = parse_resume(file_storage, file_storage.filename)
    if error:
        logging.warning(f"Tidak dapat memproses {file_storage.filename}: {error}")
        return None, error
    return text, None

@app.route('/')
def index():
    return "<h1>Flask Backend is ALIVE!</h1>"

@app.route('/api/search', methods=['POST'])
def candidate_search():
    jd_file = request.files.get('jd_file')
    if not jd_file:
        return jsonify({"error": "File Job Description tidak ditemukan"}), 400

    domain = request.form.get('domain', 'General')
    jd_text, error = parse_jd(jd_file)
    if error:
        return jsonify({"error": f"Gagal memproses JD: {error}"}), 400

    try:
        rag_chain = get_rag_chain(domain) # Menggunakan cache
        results = asyncio.run(rag_chain.candidate_search(jd_text))
        return jsonify({"results": results})
    except Exception as e:
        logging.error(f"Error di /api/search: {e}", exc_info=True)
        return jsonify({"error": f"Error dalam pencarian kandidat: {str(e)}"}), 500

@app.route('/api/qa', methods=['POST'])
def resume_qa():
    resume_file = request.files.get('resume_file')
    if not resume_file:
        return jsonify({"error": "File resume tidak ditemukan"}), 400

    question = request.form.get('question', '')
    domain = request.form.get('domain', 'General')

    if not question:
        return jsonify({"error": "Pertanyaan tidak boleh kosong"}), 400

    resume_text, error = process_single_file(resume_file)
    if error:
        return jsonify({"error": f"Gagal memproses file resume: {error}"}), 400

    try:
        rag_chain = get_rag_chain(domain) # Menggunakan cache
        results = asyncio.run(rag_chain.resume_qa(resume_text, question, resume_file.filename))
        return jsonify({"answer": results})
    except Exception as e:
        logging.error(f"Error di /api/qa: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500

@app.route('/api/compare', methods=['POST'])
def compare_candidates_endpoint():
    if 'resume_files' not in request.files:
        return jsonify({"error": "File resume tidak ditemukan"}), 400

    resume_files = request.files.getlist('resume_files')
    domain = request.form.get('domain', 'General')
    jd_text_from_form = request.form.get('jd_text', '')

    processed_resumes = [process_single_file(f) for f in resume_files if f and f.filename]
    valid_resumes = [(text, filename) for text, filename in processed_resumes if text]

    if len(valid_resumes) < 2:
        return jsonify({"error": "Membutuhkan minimal 2 resume yang valid untuk dibandingkan"}), 400

    try:
        rag_chain = get_rag_chain(domain) # Menggunakan cache
        results = asyncio.run(rag_chain.compare_candidates(valid_resumes, jd_text_from_form))
        return jsonify({"results": results})
    except Exception as e:
        logging.error(f"Error di /api/compare: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500

@app.route('/api/score', methods=['POST'])
def score_candidates():
    if 'resume_files' not in request.files:
        return jsonify({"error": "File resume tidak ditemukan"}), 400

    resume_files = request.files.getlist('resume_files')
    domain = request.form.get('domain', 'General')
    jd_text_from_form = request.form.get('jd_text', '')
    criteria_str = request.form.get('criteria', '{}')

    try:
        criteria = json.loads(criteria_str)
    except json.JSONDecodeError:
        return jsonify({"error": "Format kriteria JSON tidak valid"}), 400

    processed_resumes = []
    errors = []
    for file in resume_files:
        if file and file.filename:
            text, error = process_single_file(file)
            if text:
                processed_resumes.append((text, file.filename))
            if error:
                errors.append(f"{file.filename}: {error}")

    if not processed_resumes:
        return jsonify({"error": "Gagal memproses semua file resume.", "details": errors}), 400

    try:
        rag_chain = get_rag_chain(domain) # Menggunakan cache
        results = rag_chain.score_and_rank_candidates(
            resume_data=processed_resumes,
            jd_text=jd_text_from_form,
            criteria=criteria if criteria else None
        )
        if errors: results['warnings'] = errors
        return jsonify(results)
    except Exception as e:
        logging.error(f"Error di /api/score: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)