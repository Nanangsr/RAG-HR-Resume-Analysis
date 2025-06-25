import asyncio
import os
import json
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from core.retriever import get_retriever
from typing import List, Optional, Dict, Tuple
from core.scoring import ResumeScorer
from utils.resume_standardizer import ResumeStandardizer
from utils.name_extractor import NameExtractor
import logging
import hashlib
import re
from PyPDF2 import PdfReader

load_dotenv()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class ResumeRagChain:
    def __init__(self, domain: str = "general"):
        self.domain = domain.lower()
        self.llm = ChatGroq(
            temperature=0,
            model_name="llama3-8b-8192",
            api_key=os.getenv("GROQ_API_KEY"),
            request_timeout=120,
            model_kwargs={"seed": 42}
        )
        self.name_extractor = NameExtractor()
        self.standardizer = ResumeStandardizer(domain=domain)
        self.narrative_cache = {}
        self._init_prompts()

    def _init_prompts(self):
        # prompt dan definisi tidak diubah sesuai permintaan Anda
        domain_context = self._get_domain_context()
        self.qa_prompt = ChatPromptTemplate.from_template(f"Jawab pertanyaan tentang resume {{name}}:\nPertanyaan: {{question}}\nKonten Resume:\n{{resume_text}}\n\nKonteks Domain {self.domain.upper()}: {domain_context}\n\nAturan: Jawab spesifik dalam Bahasa Indonesia. Jika tidak tahu, katakan 'Informasi tidak ditemukan di resume'.")
        self.search_prompt = ChatPromptTemplate.from_template(f"Dari Deskripsi Pekerjaan ini:\n{{jd_text}}\n\nBerikut adalah kandidat yang relevan:\n{{candidates}}\n\nBerdasarkan konteks domain {self.domain.upper()} ({domain_context}), berikan analisis dalam Bahasa Indonesia:\n1. 3 kandidat teratas  yang paling cocok beserta alasannya, sebutkan nama dari kadidat.\n2. Rekomendasi singkat untuk proses rekrutmen selanjutnya.")
        self.compare_prompt = ChatPromptTemplate.from_template(f"Bandingkan {{count}} kandidat berikut untuk konteks domain {self.domain.upper()} ({domain_context}). {{jd_context}}:\n\n{{candidates}}\n\nBerikan analisis komparatif dalam Bahasa Indonesia yang mencakup perbandingan skill, potensi, dan rekomendasi kandidat terkuat.")
        self.narrative_prompt = ChatPromptTemplate.from_template(f"Anda adalah seorang manajer HR. Berikut adalah data hasil skoring untuk beberapa kandidat:\n\n{{candidates_info}}\n\nDengan konteks deskripsi pekerjaan:\n{{jd_context}}\n\nDan konteks domain {self.domain.upper()} ({domain_context}), tuliskan analisis naratif dalam Bahasa Indonesia dengan struktur:\n1. **Ringkasan Eksekutif**: Kesimpulan singkat (2-3 kalimat).\n2. **Analisis Komparatif**: Perbandingan kekuatan utama antar kandidat top.\n3. **Rekomendasi**: Siapa kandidat yang paling direkomendasikan dan kenapa.")

    def _get_domain_context(self) -> str:
        # Definisi domain tidak diubah
        contexts = {"it": "Keterampilan teknis, pengalaman proyek teknologi, sertifikasi.", "hr": "Manajemen SDM, komunikasi, talent management.", "finance": "Analisis keuangan, kepatuhan, pelaporan, sertifikasi (CPA, CFA)."}
        return contexts.get(self.domain, "Keterampilan profesional, pengalaman kerja, dan potensi kepemimpinan.")

    def _clean_output(self, text: str) -> str:
        return re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL | re.IGNORECASE).strip()

    def get_candidate_name(self, resume_text: str, filename: str = "") -> str:
        return self.name_extractor.extract_name_from_resume(resume_text, filename) or "Kandidat Anonim"

    async def resume_qa(self, resume_text: str, question: str, filename: str = "") -> str:
        std_resume = self.standardizer.standardize_resume(resume_text)
        candidate_name = self.get_candidate_name(resume_text, filename)
        chain = self.qa_prompt | self.llm
        result = await chain.ainvoke({"question": question, "resume_text": std_resume, "name": candidate_name})
        return self._clean_output(result.content)

    async def candidate_search(self, jd_text: str) -> str:
        # Ambil semua resume dari folder data/resumes (path sudah diperbaiki)
        resumes_dir = r"C:\Users\ASUS\Downloads\MBKM DataIns\RAG CV baru\backend\data\resumes"
        resume_files = [f for f in os.listdir(resumes_dir) if f.lower().endswith(('.txt', '.pdf'))]

        resume_data = []
        for filename in resume_files:
            file_path = os.path.join(resumes_dir, filename)
            if filename.lower().endswith('.txt'):
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
            elif filename.lower().endswith('.pdf'):
                try:
                    reader = PdfReader(file_path)
                    content = "\n".join(page.extract_text() or "" for page in reader.pages)
                except Exception:
                    content = ""
            else:
                content = ""
            if content.strip():
                resume_data.append((content, filename))

        if not resume_data:
            return "Tidak ditemukan resume pada folder data/resumes."

        standardized_resumes = [self.standardizer.standardize_resume(text) for text, fn in resume_data]
        names = [self.get_candidate_name(text, fn) for text, fn in resume_data]
        candidates_formatted = "\n\n---\n\n".join(
            f"**Kandidat: {names[i]}**\n{std_text[:1500]}..." for i, std_text in enumerate(standardized_resumes)
        )
        chain = self.search_prompt | self.llm
        result = await chain.ainvoke({"jd_text": jd_text, "candidates": candidates_formatted})
        return self._clean_output(result.content)

    async def compare_candidates(self, resume_data: List[Tuple[str, str]], jd_text: Optional[str] = None) -> str:
        standardized_resumes = [self.standardizer.standardize_resume(text) for text, fn in resume_data]
        names = [self.get_candidate_name(text, fn) for text, fn in resume_data]
        candidates_formatted = "\n\n---\n\n".join(
            f"**Kandidat: {names[i]}**\n{std_text[:1500]}..." for i, std_text in enumerate(standardized_resumes)
        )
        chain = self.compare_prompt | self.llm
        jd_context = f"Konteks Deskripsi Pekerjaan: {jd_text}" if jd_text else ""
        result = await chain.ainvoke({"count": len(resume_data), "jd_context": jd_context, "candidates": candidates_formatted})
        return self._clean_output(result.content)

    async def generate_llm_narrative_analysis(self, scoring_results: Dict, jd_text: Optional[str] = None) -> str:
        try:
            key_data = {"ranking": [{"id": r["candidate_id"], "score": r.get("ai_score", 0)} for r in scoring_results.get("ranking", [])], "jd": jd_text}
            cache_key = hashlib.md5(json.dumps(key_data, sort_keys=True).encode()).hexdigest()
            if cache_key in self.narrative_cache:
                logging.info(f"Mengambil analisis naratif dari cache untuk key: {cache_key}")
                return self.narrative_cache[cache_key]
        except Exception: cache_key = None

        if not scoring_results.get("ranking"): return "Tidak ada data ranking untuk dianalisis."

        candidates_info = "\n".join([
            f"Kandidat: {c.get('name', 'N/A')}, Skor AI: {c.get('ai_score', 0):.1f}, Level: {c.get('level', 'N/A')}"
            for c in scoring_results["ranking"]
        ])

        chain = self.narrative_prompt | self.llm
        result = await chain.ainvoke({"candidates_info": candidates_info, "jd_context": jd_text or "Tidak ada"})
        cleaned_result = self._clean_output(result.content)
        if cache_key: self.narrative_cache[cache_key] = cleaned_result
        return cleaned_result

    def score_and_rank_candidates(self, resume_data: List[Tuple[str, str]], jd_text: Optional[str] = None, criteria: Optional[Dict[str, int]] = None) -> Dict:
        try:
            if not resume_data: return {"error": "No resume data provided"}

            logging.info(f"Standardizing {len(resume_data)} resumes...")
            standardized_resumes = [self.standardizer.standardize_resume(raw_text) for raw_text, filename in resume_data]
            logging.info("Standardization complete.")

            scorer = ResumeScorer(domain=self.domain, criteria=criteria)

            logging.info("Scoring standardized resumes...")
            scoring_results = scorer.compare_resumes(standardized_resumes, jd_text)
            logging.info("Scoring complete.")

            for i, candidate in enumerate(scoring_results.get("ranking", [])):
                raw_text, filename = resume_data[i]
                candidate["name"] = self.get_candidate_name(raw_text, filename)

            logging.info("Generating narrative analysis...")
            narrative = asyncio.run(self.generate_llm_narrative_analysis(scoring_results, jd_text))
            scoring_results["narrative_analysis"] = narrative
            logging.info("Narrative analysis complete.")

            return scoring_results
        except Exception as e:
            logger.error(f"Error in score_and_rank_candidates: {e}", exc_info=True)
            return {"error": f"Terjadi kesalahan internal saat skoring: {str(e)}"}
