# 📄 RAG HR Resume Analisis AI

Platform cerdas berbasis web yang dirancang untuk merevolusi proses rekrutmen. Aplikasi ini membantu tim Human Resources (HR) untuk menyederhanakan proses seleksi, memahami kualifikasi kandidat secara mendalam, dan mengambil keputusan berbasis data dengan cepat dan objektif.

<img width="385" alt="image" src="https://github.com/user-attachments/assets/85101dd1-8149-438c-b343-77c2d414f798" />


## 🎯 Tentang Proyek

Proses seleksi kandidat secara manual, terutama dengan ratusan CV, adalah pekerjaan yang memakan waktu, subjektif, dan melelahkan. Tim rekrutmen seringkali kesulitan untuk mengidentifikasi talenta terbaik secara efisien di tengah tumpukan dokumen yang tidak terstruktur.

**Resume Analisis AI** hadir sebagai solusi modern. Aplikasi ini menggunakan kekuatan Large Language Models (LLM) dengan arsitektur Retrieval-Augmented Generation (RAG) untuk mengubah CV menjadi data yang *insightful* dan terukur.

Platform ini memungkinkan tim HR untuk:
-   **Menghemat waktu drastis** dalam proses penyaringan awal.
-   **Mendapatkan skor relevansi** kandidat terhadap deskripsi pekerjaan.
-   **Membandingkan beberapa kandidat** secara berdampingan dengan analisis naratif.
-   **Memahami kandidat lebih dalam** dengan mengajukan pertanyaan spesifik ke CV mereka.
-   **Mengurangi bias** dalam pengambilan keputusan dan fokus pada kualifikasi objektif.

📂 Struktur Proyek
Berikut adalah struktur direktori lengkap proyek ini, sesuai dengan lingkungan pengembangan Anda.
```bash
/RAG-HR-Resume-Analisis/
├── backend/
│   ├── .venv/
│   ├── __pycache__/
│   ├── core/
│   │   ├── __pycache__/
│   │   ├── comparator.py
│   │   ├── embedding.py
│   │   ├── rag_chain.py
│   │   ├── retriever.py
│   │   └── scoring.py
│   ├── data/
│   │   ├── jobs/
│   │   └── resumes/
│   ├── models/
│   │   ├── __pycache__/
│   │   ├── __init__.py
│   │   └── best_resume_scorer.pkl
│   ├── utils/
│   │   ├── __pycache__/
│   │   ├── jd_parser.py
│   │   ├── name_extractor.py
│   │   ├── resume_parser.py
│   │   └── resume_standardizer.py
│   ├── vector_store/
│   │   └── chroma/
│   ├── .env
│   ├── app.py
│   ├── initialize_db.py
│   └── requirements.txt
│
└── frontend/
    ├── node_modules/
    ├── public/
    │   ├── hero-image.svg
    │   └── logo.svg
    ├── src/
    │   ├── assets/
    │   │   ├── datains-logo.png
    │   │   └── hr-image.jpg
    │   ├── components/
    │   │   ├── AnalysisForm.css
    │   │   ├── AnalysisForm.jsx
    │   │   ├── DataVisualization.jsx
    │   │   ├── FeatureCard.css
    │   │   ├── FeatureCard.jsx
    │   │   ├── Footer.css
    │   │   ├── Footer.jsx
    │   │   ├── Navbar.css
    │   │   ├── Navbar.jsx
    │   │   ├── ResultsDisplay.css
    │   │   └── ResultsDisplay.jsx
    │   ├── pages/
    │   │   ├── AnalysisPage.jsx
    │   │   ├── HomePage.css
    │   │   └── HomePage.jsx
    │   ├── utils/
    │   │   └── export.js
    │   ├── App.css
    │   ├── App.jsx
    │   ├── index.css
    │   └── main.jsx
    ├── .gitignore
    ├── index.html
    ├── package-lock.json
    ├── package.json
    └── vite.config.js
```

## ✨ Fitur Utama

Aplikasi ini dilengkapi dengan empat fitur analisis yang kuat:

* **📊 Skoring & Peringkat Otomatis**: Unggah beberapa CV sekaligus untuk mendapatkan skor relevansi dan peringkat otomatis berdasarkan kriteria yang bisa Anda sesuaikan.
* **🔄 Analisis Perbandingan Kandidat**: Dapatkan analisis naratif komparatif yang mendalam untuk memahami kekuatan dan kelemahan relatif dari para kandidat top.
* **❓ Tanya Jawab (QA) Interaktif**: Punya pertanyaan spesifik? "Wawancarai" sebuah CV secara langsung dan dapatkan jawaban instan dari AI yang berbasis data dari dokumen tersebut.
* **🔍 Pencarian Berbasis Deskripsi**: Temukan kandidat paling relevan dari database vektor Anda hanya dengan mengunggah Deskripsi Pekerjaan (Job Description).

<img width="379" alt="image" src="https://github.com/user-attachments/assets/6509e976-1c3e-4891-b0b9-70b007084528" />



## 🛠️ Dibangun Dengan

Arsitektur aplikasi ini memisahkan antara logika backend dan tampilan frontend untuk skalabilitas dan kemudahan pengembangan.

**Backend:**
* **Python 3.10**
* **Flask**: Sebagai micro-framework untuk membangun REST API.
* **LangChain**: Sebagai framework utama untuk membangun alur kerja RAG.
* **Groq**: Sebagai penyedia inferensi LLM yang sangat cepat.
* **Sentence-Transformers**: Untuk membuat embedding dari teks CV.
* **ChromaDB**: Sebagai database vektor untuk menyimpan dan mencari CV.
* **Gunicorn**: Sebagai WSGI server untuk production.

**Frontend:**
* **React.js (with Vite)**: Sebagai library untuk membangun antarmuka pengguna yang interaktif dan modern.
* **React Router**: Untuk menangani navigasi multi-halaman.
* **Axios**: Untuk melakukan panggilan API ke backend.
* **Chart.js**: Untuk menampilkan visualisasi data.
* **Lucide Icons**: Untuk ikonografi yang bersih dan modern.

## 🚀 Memulai

Untuk menjalankan proyek ini di lingkungan lokal Anda, ikuti langkah-langkah berikut.

### Prasyarat

* Git
* Python 3.10 atau lebih baru
* Node.js & npm (versi LTS direkomendasikan)

### Instruksi Instalasi

1.  **Clone Repository :**
    ```bash
    git clone https://github.com/Nanangsr/RAG-HR-Resume-Analysis.git
    cd RAG-HR-Resume-Analysis
    ```

2.  **Setup Backend (di Terminal 1):**
    * Masuk ke direktori `backend`:
        ```bash
        cd backend
        ```
    * Buat dan aktifkan *virtual environment*:
        ```bash
        # Buat venv
        python -m venv venv
        # Aktifkan venv (untuk Windows PowerShell)
        .\venv\Scripts\activate
        ```
    * Instal semua library Python yang dibutuhkan:
        ```bash
        pip install -r requirements.txt
        ```
    * Atur API Key di .env
        ```bash
        GROQ_API_KEY="gsk_xxxxxx" (Dapatkan GROQ API KEY di laman berikut https://console.groq.com/keys)
        EMBEDDING_MODEL="all-MiniLM-L6-v2"
        ```

    * Siapkan data CV. Buat folder `data/resumes` dan letakkan semua file CV (PDF/DOCX) Anda di dalamnya.

    * **Inisialisasi Database Vektor (Hanya dilakukan sekali di awal):**
        ```bash
        # Jalankan skrip untuk mengisi database dari folder data/resumes
        .\venv\Scripts\python.exe initialize_db.py
        ```
    * **Jalankan Server Backend:**
        ```bash
        # Gunakan perintah ini untuk menjalankan server Flask
        .\venv\Scripts\python.exe app.py
        ```
    * Biarkan terminal ini tetap berjalan. Server backend Anda kini aktif di `http://127.0.0.1:5000`.

3.  **Setup Frontend (di Terminal 2):**
    * Buka jendela terminal **baru**.
    * Masuk ke direktori `frontend`:
        ```bash
        cd frontend
        ```
    * Instal semua library JavaScript yang dibutuhkan:
        ```bash
        npm install
        ```
    * Jalankan server pengembangan frontend:
        ```bash
        npm run dev
        ```
    * Biarkan terminal ini juga tetap berjalan.

4.  **Akses Aplikasi:**
    * Buka browser Anda dan kunjungi alamat yang diberikan oleh server Vite, biasanya **`http://localhost:5173`**.

##  Penggunaan

1.  **Halaman Home**: Memberikan gambaran umum tentang kemampuan aplikasi. Klik "Mulai Analisis Sekarang" untuk menuju ke alat utama.
2.  **Halaman Mulai Analisis**:
    * Pilih salah satu dari empat "Use Case" yang tersedia di form.
    * Pilih "Domain Industri" untuk menyesuaikan konteks analisis.
    * Unggah file yang diperlukan (CV atau Deskripsi Pekerjaan).
    * Klik tombol "Mulai Analisis" dan tunggu hasilnya muncul di sisi kanan layar.
    * Hasil dapat dieksplorasi melalui tab Ranking, Visualisasi, atau Analisis Naratif.
<img width="385" alt="image" src="https://github.com/user-attachments/assets/b7093e4e-8831-49d1-80e7-36e1e7d8bcd3" />

---
© 2024 Nanang Safiu Ridho - Data Scientist Intern at Global Data Inspirasi
